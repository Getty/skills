<?php
declare(strict_types=1);
// Pure domain layer: no Gearman extension needed. Duplicate JSON keys are not rejected.
function parse_request(string $raw): stdClass {
    if (PHP_INT_SIZE < 8 || strlen($raw) > 65536) {
        throw new InvalidArgumentException('64-bit PHP and bounded input required');
    }
    $o = json_decode($raw, false, 32, JSON_THROW_ON_ERROR);
    if (!$o instanceof stdClass) { throw new InvalidArgumentException('expected envelope'); }
    $required = ['schema_version','request_id','operation','payload'];
    $keys = array_keys(get_object_vars($o));
    if (array_diff($required, $keys) || array_diff($keys, [...$required, 'deadline_unix_ms'])) {
        throw new InvalidArgumentException('incorrect fields');
    }
    if (!is_int($o->schema_version) || $o->schema_version !== 1) {
        throw new InvalidArgumentException('unsupported schema');
    }
    if (!is_string($o->request_id) || !preg_match('/\A[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\z/', $o->request_id)) {
        throw new InvalidArgumentException('invalid request id');
    }
    if ($o->operation !== 'sum.v1' || !$o->payload instanceof stdClass
        || array_keys(get_object_vars($o->payload)) !== ['numbers']) {
        throw new InvalidArgumentException('invalid operation/payload');
    }
    $numbers = $o->payload->numbers;
    if (!is_array($numbers) || count($numbers) < 1 || count($numbers) > 1000) {
        throw new InvalidArgumentException('invalid numbers');
    }
    foreach ($numbers as $v) {
        if (!is_int($v) || $v < -1000000000 || $v > 1000000000) {
            throw new InvalidArgumentException('invalid integer');
        }
    }
    if (property_exists($o, 'deadline_unix_ms') && (!is_int($o->deadline_unix_ms)
        || $o->deadline_unix_ms < 0 || $o->deadline_unix_ms > 9007199254740991)) {
        throw new InvalidArgumentException('invalid deadline');
    }
    return $o;
}
function execute_request(stdClass $o): array {
    if (property_exists($o, 'deadline_unix_ms') && $o->deadline_unix_ms <= (int)(microtime(true)*1000)) {
        throw new InvalidArgumentException('deadline expired');
    }
    return ['schema_version'=>1, 'request_id'=>$o->request_id, 'ok'=>true,
            'result'=>['sum'=>array_sum($o->payload->numbers)]];
}
function request_stdin(): string {
    $raw = stream_get_contents(STDIN, 65537);
    if ($raw === false || strlen($raw) > 65536) { throw new InvalidArgumentException('input failed or oversized'); }
    return $raw;
}
