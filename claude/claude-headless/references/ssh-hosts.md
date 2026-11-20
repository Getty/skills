# Driving Claude Code over ssh

Read when driving an agent on another host over ssh — one whose Claude is somebody
else's login, or one that runs Windows.

The stream-json channel ([stream-json.md](stream-json.md)) is a pipe, so it survives
ssh — and that is how you drive an agent on a host whose Claude is somebody else's
login:

```bash
ssh -T host 'export PATH=$HOME/.local/bin:$PATH; cd /srv/project; exec claude -p \
  --input-format stream-json --output-format stream-json --verbose'
```

Write the same JSON lines into ssh's stdin. Use `-T` (no tty) and `exec` so the remote
claude owns the connection's stdio and its signals. Verified across hosts: turn two
still knew what turn one had been told. Nothing is shared but the ssh session — no
account, no Remote Control.

## When the ssh host is Windows

Windows' built-in OpenSSH server works for all of the above, with a few
traps. Verified on Windows 11 with OpenSSH from the optional feature and
claude 2.1.319:

- **Make Git Bash the ssh shell.** The default is `cmd.exe`, which breaks every
  `export …; cd … && exec claude …` line. Set
  `HKLM:\SOFTWARE\OpenSSH` → `DefaultShell` =
  `C:\Program Files\Git\bin\bash.exe`. After that the POSIX command lines in
  this skill run unchanged, and Claude Code needs Git for Windows anyway.
- **Keys of an admin account go elsewhere.** For members of Administrators,
  sshd reads only `C:\ProgramData\ssh\administrators_authorized_keys`, never
  `~/.ssh/authorized_keys`. The file must be owned by SYSTEM/Administrators
  only (`icacls … /inheritance:r /grant *S-1-5-32-544:F /grant *S-1-5-18:F`),
  or sshd silently ignores it.
- **Password logins come in by a second door.** `PasswordAuthentication no` alone
  still leaves `keyboard-interactive` open, and on Windows that asks for the
  account password. Set `KbdInteractiveAuthentication no` too.
- **Put claude on PATH yourself.** The native installer puts
  `claude.exe` in `%USERPROFILE%\.local\bin` and does not add it to PATH, so
  keep the `export PATH=$HOME/.local/bin:$PATH` prefix. In Git Bash, `$HOME` is
  `/c/Users/<name>`.
- **Session files speak Windows.** `~/.claude/sessions/*.json` stores `cwd` as
  `C:\Users\…` and `pid` as a Windows PID. Normalise the path before you compare
  it with a Git Bash path (`\` → `/`, `C:` → `/c`, compare case-insensitively).
  msys Perl's `kill 0` cannot see Windows PIDs, so take them from the WINPID
  column of `ps -W` (the fourth column).
- **msys rewrites slash arguments.** An argument that starts with `/`, passed to
  a native `.exe`, is turned into a path (`tasklist /FI` becomes
  `C:/Program Files/Git/FI`). Write `//FI`, or set `MSYS_NO_PATHCONV=1`.
- **The command line itself gets mangled.** Windows sshd hands the remote
  command to the shell through a Windows command line, and double quotes and
  backslashes inside it arrive broken: `perl -e '<script>'` fails to compile,
  and an `--append-system-prompt` with quotes in it comes out wrong. Send
  anything non-trivial base64-wrapped and unpack it with process
  substitution, which keeps stdin free for the prompt:

  ```bash
  b=$(printf %s "$cmd" | base64 -w0)
  printf %s "$prompt" | ssh -T host "bash <(echo $b | base64 -d)"
  ```

  The same line works unchanged against a Linux host.
- **PowerShell through ssh is a quoting trap.** Nesting `powershell -Command "…"`
  inside bash inside ssh breaks on `$`, quotes and backslashes. For anything
  longer than one line, `scp` a `.ps1` file over and run
  `powershell -NoProfile -ExecutionPolicy Bypass -File x.ps1`. Write JSON or
  other backslash-heavy files locally and copy them, rather than building them
  with `printf` on the far side.
