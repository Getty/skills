<?php
declare(strict_types=1);
require __DIR__ . '/contract.php';
if (!extension_loaded('gearman')) { fwrite(STDERR, "Gearman extension required\n"); exit(2); }
try {
    $background = ($argv[1] ?? '') === '--background';
    if ($argc > 2 || ($argc === 2 && !$background)) { throw new InvalidArgumentException('usage: client.php [--background]'); }
    $raw = request_stdin();
    $request = parse_request($raw);
    $port = filter_var(getenv('GEARMAN_PORT') ?: '4730', FILTER_VALIDATE_INT,
        ['options'=>['min_range'=>1, 'max_range'=>65535]]);
    if ($port === false) { throw new InvalidArgumentException('invalid port'); }
    $client = new GearmanClient();
    if (!$client->addServer(getenv('GEARMAN_HOST') ?: '127.0.0.1', $port)) { throw new RuntimeException('server configuration failed'); }
    $deadline = hrtime(true) + 10_000_000_000;
    do {
        $remainingMs = (int)(($deadline - hrtime(true)) / 1_000_000);
        if ($remainingMs <= 0) { throw new RuntimeException('deadline; reconcile outcome'); }
        $client->setTimeout(min(5000, $remainingMs));
        $value = $background
            ? $client->doBackground('gearman_skill.sum.v1', $raw, $request->request_id)
            : $client->doNormal('gearman_skill.sum.v1', $raw, $request->request_id);
        $code = $client->returnCode();
        if ($code === GEARMAN_SUCCESS) {
            echo $background ? json_encode(['accepted'=>true,'completed'=>false,'handle'=>$value,
                'request_id'=>$request->request_id], JSON_THROW_ON_ERROR) : $value;
            echo "\n";
            exit(0);
        }
        // These codes resume the current operation; transport errors never cause a resend here.
        if ($background || !in_array($code, [GEARMAN_WORK_DATA, GEARMAN_WORK_STATUS, GEARMAN_WORK_WARNING], true)) {
            throw new RuntimeException('no successful completion; reconcile request id');
        }
    } while (true);
} catch (Throwable $e) {
    fwrite(STDERR, "request rejected or outcome uncertain; do not retry blindly\n");
    exit(3);
}
