#!/usr/bin/env python3
"""netcli.py — run commands on a network device CLI over SSH, driven by pexpect.

Solves what a plain `ssh host cmd` cannot: legacy SSH algorithms, devices that
ignore the exec channel (Cisco IOS, Cisco Small Business), in-band
"User Name:/Password:" logins, enable mode and pager prompts.

Usage:
  netcli.py --profile sx300    --host 172.16.0.99 --user ops --password-file ~/router.txt "show vlan" "show lldp neighbors"
  netcli.py --profile ios      --host 172.16.0.5  --user admin  --password-file ~/.secrets/rtr-b --enable "show ip int brief"
  netcli.py --profile routeros --host 172.16.0.8  --user ops --password-file ~/router.txt "/ip/route/print terse"
  netcli.py --profile ios … --json "show version"

Environment fallbacks: NETCLI_HOST, NETCLI_USER, NETCLI_PASSWORD_FILE, NETCLI_PROFILE.
Passwords are read from the first line of the password file; never pass them as arguments.
Exit codes: 0 ok, 2 login failure, 3 command timeout, 1 other error.
"""
import argparse
import json
import os
import pathlib
import re
import shlex
import sys

try:
    import pexpect
except ImportError:  # pragma: no cover
    sys.stderr.write("netcli.py needs python3-pexpect (pip install pexpect / apt install python3-pexpect)\n")
    sys.exit(1)

PROFILES = {
    # prompt regexes are anchored at a line break (devices send \r\n\r before prompts) and the end of the buffer
    "ios": dict(
        prompt=r"[\r\n][\w.\-]+(?:\([\w\-]+\))?[#>] ?$",
        paging="terminal length 0",
        enable="enable",
        legacy=True,
        mode="interactive",
        errors=(r"% Invalid input", r"% Incomplete command", r"% Ambiguous command", r"% Unrecognized command"),
    ),
    "sx300": dict(
        prompt=r"[\r\n][\w.\-]+(?:\([\w\-]+\))?[#>] ?$",
        paging="terminal datadump",
        enable="enable",
        legacy=True,
        mode="interactive",
        errors=(r"% Unrecognized command", r"% Wrong number of parameters", r"% Bad parameter value", r"Insufficient privilege"),
    ),
    "routeros": dict(
        prompt=r"[\r\n]\[[^\]\r\n]+\] (?:/[^ >]*)?> ?$",
        paging=None,
        enable=None,
        legacy=False,
        mode="exec",            # RouterOS honours `ssh host cmd`; no pager, no echo games
        user_suffix="+ct",      # no colors, no terminal capability detection
        errors=(r"bad command name", r"syntax error", r"input does not match any value", r"no such item"),
    ),
    "generic": dict(
        prompt=r"[\r\n][^\r\n]{1,80}[#>$%] ?$",
        paging=None,
        enable=None,
        legacy=False,
        mode="interactive",
        errors=(),
    ),
}

LEGACY_OPTS = (
    "-o KexAlgorithms=+diffie-hellman-group-exchange-sha1,diffie-hellman-group14-sha1,diffie-hellman-group1-sha1 "
    "-o HostKeyAlgorithms=+ssh-rsa,ssh-dss -o PubkeyAcceptedAlgorithms=+ssh-rsa "
    "-o Ciphers=+aes128-cbc,aes256-cbc,3des-cbc -o MACs=+hmac-sha1"
)
BASE_OPTS = "-o StrictHostKeyChecking=accept-new -o ConnectTimeout=15 -o ServerAliveInterval=15"
PW_OPTS = "-o PubkeyAuthentication=no -o PreferredAuthentications=password,keyboard-interactive"
PAGER = [r"--More--", r"More: <space>", r"More:.*q to quit", r"-- \[Q quit\|D dump\|down\]"]


def read_password(path):
    if not path:
        return None
    p = pathlib.Path(path).expanduser()
    if not p.exists():
        sys.stderr.write(f"password file not found: {p}\n")
        sys.exit(1)
    return p.read_text().splitlines()[0].strip()


def build_ssh(args, prof, command=None):
    user = args.user + prof.get("user_suffix", "") if args.user else None
    opts = [BASE_OPTS]
    if args.legacy if args.legacy is not None else prof["legacy"]:
        opts.append(LEGACY_OPTS)
    if args.password_file and not args.keys:
        opts.append(PW_OPTS)
    if args.port:
        opts.append(f"-p {args.port}")
    if args.ssh_opt:
        opts.extend(args.ssh_opt)
    target = f"{user}@{args.host}" if user else args.host
    cmd = f"ssh {' '.join(opts)} {target}"
    if command is not None:
        cmd += " " + shlex.quote(command)
    return cmd


def spawn(cmd, timeout):
    return pexpect.spawn(cmd, timeout=timeout, encoding="utf-8", codec_errors="replace",
                         dimensions=(1000, 400), env={**os.environ, "TERM": "vt100", "LANG": "C"})


def run_exec_mode(args, prof, password, commands):
    """One ssh process per command (devices with a working exec channel)."""
    results = {}
    for c in commands:
        child = spawn(build_ssh(args, prof, c), args.timeout)
        while True:
            i = child.expect([r"(?i)password:", r"continue connecting", pexpect.EOF, pexpect.TIMEOUT])
            if i == 0:
                if password is None:
                    sys.stderr.write("device asks for a password but none given\n")
                    sys.exit(2)
                child.sendline(password)
            elif i == 1:
                child.sendline("yes")
            elif i == 2:
                break
            else:
                sys.stderr.write(f"timeout running {c!r}\n")
                sys.exit(3)
        out = (child.before or "").replace("\r", "")
        child.close()
        if child.exitstatus not in (0, None):
            sys.stderr.write(f"ssh exited {child.exitstatus} for {c!r}\n")
        results[c] = out.strip("\n")
    return results


def run_interactive(args, prof, password, commands):
    prompt = re.compile(args.prompt or prof["prompt"], re.S)
    child = spawn(build_ssh(args, prof), args.timeout)
    login_pw_sent = False
    while True:
        i = child.expect([r"User Name:", r"(?i)password:", r"continue connecting", r"(?i)permission denied",
                          prompt, pexpect.EOF, pexpect.TIMEOUT])
        if i == 0:
            child.sendline(args.user or "")
        elif i == 1:
            if password is None or login_pw_sent:
                sys.stderr.write("login failed (password prompt repeated or no password)\n")
                sys.exit(2)
            child.sendline(password)
            login_pw_sent = True
        elif i == 2:
            child.sendline("yes")
        elif i == 3:
            sys.stderr.write("permission denied\n")
            sys.exit(2)
        elif i == 4:
            break
        else:
            sys.stderr.write("no prompt after login (EOF/timeout). Output so far:\n" + (child.before or "") + "\n")
            sys.exit(2)

    def at_prompt():
        m = prompt.search(child.after or "")
        return (m.group(0) if m else child.after or "").strip()

    # enable mode if requested and we are at a ">" prompt
    if args.enable and at_prompt().endswith(">") and prof.get("enable"):
        child.sendline(prof["enable"])
        j = child.expect([r"(?i)password:", prompt, pexpect.TIMEOUT])
        if j == 0:
            child.sendline(args.enable_password or password or "")
            k = child.expect([prompt, r"(?i)password:", pexpect.TIMEOUT])
            if k != 0:
                sys.stderr.write("enable failed\n")
                sys.exit(2)
        elif j == 2:
            sys.stderr.write("enable: no response\n")
            sys.exit(2)

    def run(cmd, t):
        child.sendline(cmd)
        try:
            child.expect_exact(cmd, timeout=10)  # swallow the echo
        except pexpect.TIMEOUT:
            pass
        while True:
            k = child.expect([prompt] + PAGER + [pexpect.TIMEOUT], timeout=t)
            if k == 0:
                out = (child.before or "").replace("\r", "")
                return out.strip("\n")
            if k == len(PAGER) + 1:
                sys.stderr.write(f"timeout waiting for prompt after {cmd!r}\n")
                sys.exit(3)
            child.send(" ")

    paging = args.paging if args.paging is not None else prof["paging"]
    if paging:
        run(paging, 10)
    results = {c: run(c, args.timeout) for c in commands}
    child.sendline("exit")
    child.close()
    return results


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("commands", nargs="*", help="commands to run in order")
    ap.add_argument("--profile", default=os.environ.get("NETCLI_PROFILE", "generic"), choices=PROFILES)
    ap.add_argument("--host", default=os.environ.get("NETCLI_HOST"))
    ap.add_argument("--user", default=os.environ.get("NETCLI_USER"))
    ap.add_argument("--port", type=int)
    ap.add_argument("--password-file", default=os.environ.get("NETCLI_PASSWORD_FILE"))
    ap.add_argument("--keys", action="store_true", help="use SSH keys even if a password file is given (password then only for enable)")
    ap.add_argument("--enable", action="store_true", help="enter privileged mode after login (ios/sx300)")
    ap.add_argument("--enable-password-file")
    ap.add_argument("--legacy", dest="legacy", action="store_true", default=None, help="force legacy SSH algorithms on")
    ap.add_argument("--no-legacy", dest="legacy", action="store_false", help="force legacy SSH algorithms off")
    ap.add_argument("--prompt", help="override prompt regex")
    ap.add_argument("--paging", help="override paging-off command ('' to skip)")
    ap.add_argument("--mode", choices=["interactive", "exec"], help="override profile mode")
    ap.add_argument("--timeout", type=int, default=60, help="seconds per command")
    ap.add_argument("--ssh-opt", action="append", help="extra raw ssh option, e.g. --ssh-opt='-o ProxyJump=bastion'")
    ap.add_argument("--json", action="store_true", help="emit {command: output} JSON")
    args = ap.parse_args()

    if not args.host:
        ap.error("--host (or NETCLI_HOST) required")
    prof = PROFILES[args.profile]
    password = read_password(args.password_file)
    args.enable_password = read_password(args.enable_password_file) if args.enable_password_file else None
    commands = args.commands or ["show version"]
    mode = args.mode or prof["mode"]

    results = run_exec_mode(args, prof, password, commands) if mode == "exec" else run_interactive(args, prof, password, commands)

    for c, out in results.items():
        for pat in prof.get("errors", ()):
            if re.search(pat, out):
                sys.stderr.write(f"warning: device reported an error for {c!r}: {pat}\n")
                break
    if args.json:
        json.dump(results, sys.stdout, indent=2, ensure_ascii=False)
        print()
    else:
        for c, out in results.items():
            print(f"\n########## {c} ##########")
            print(out)


if __name__ == "__main__":
    main()
