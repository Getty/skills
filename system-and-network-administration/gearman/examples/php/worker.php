<?php
declare(strict_types=1);
require __DIR__ . '/contract.php';
if (!extension_loaded('gearman')) { fwrite(STDERR, "Gearman extension required\n"); exit(2); }
$stop = false;
if (function_exists('pcntl_async_signals')) {
    pcntl_async_signals(true);
    pcntl_signal(SIGTERM, function () use (&$stop): void { $stop = true; });
    pcntl_signal(SIGINT, function () use (&$stop): void { $stop = true; });
}
try {
    $port = filter_var(getenv('GEARMAN_PORT') ?: '4730', FILTER_VALIDATE_INT,
        ['options'=>['min_range'=>1,'max_range'=>65535]]);
    if ($port === false) { throw new InvalidArgumentException('invalid port'); }
    $worker = new GearmanWorker();
    if (!$worker->addServer(getenv('GEARMAN_HOST') ?: '127.0.0.1', $port)) { throw new RuntimeException('configuration failed'); }
    $worker->setTimeout(1000); // Bounded idle I/O wait, not a business runtime limit.
    if (!$worker->addFunction('gearman_skill.sum.v1', function (GearmanJob $job): string {
        try {
            $out = execute_request(parse_request($job->workload()));
        } catch (InvalidArgumentException | JsonException $e) {
            // Intentional domain-error result. Transport completes; callers inspect ok.
            $out = ['schema_version'=>1,'ok'=>false,'error'=>['code'=>'invalid_request']];
        }
        return json_encode($out, JSON_THROW_ON_ERROR);
    })) { throw new RuntimeException('registration failed'); }
    while (!$stop) {
        $worker->work();
        if (!in_array($worker->returnCode(), [GEARMAN_SUCCESS, GEARMAN_TIMEOUT], true)) {
            throw new RuntimeException('worker connection stopped');
        }
    }
} catch (Throwable $e) {
    fwrite(STDERR, "worker stopped; supervisor/reconciliation required\n");
    exit(1);
}
