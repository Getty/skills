<?php
declare(strict_types=1);
require __DIR__ . '/contract.php';
try {
    echo json_encode(execute_request(parse_request(request_stdin())), JSON_THROW_ON_ERROR), "\n";
} catch (Throwable $e) {
    fwrite(STDERR, "contract rejected input\n");
    exit(1);
}
