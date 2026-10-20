/* Binary-safe foreground echo demo; no TLS, failover or intermediate-event support.
 * Compile only with matching installed libgearman headers/library; see README. */
#include <libgearman/gearman.h>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#define LIMIT 65536u
int main(int argc, char **argv) {
    if (argc != 4) { fprintf(stderr, "usage: client HOST PORT UNIQUE < payload\n"); return 2; }
    char *end = NULL;
    errno = 0;
    long port = strtol(argv[2], &end, 10);
    if (errno || !end || end == argv[2] || *end || port < 1 || port > 65535) return 2;
    size_t unique_size = strlen(argv[3]);
    if (unique_size == 0 || unique_size > 64) return 2;
    for (size_t i = 0; i < unique_size; i++) {
        unsigned char ch = (unsigned char)argv[3][i];
        if (ch < 33 || ch > 126) return 2;
    }
    unsigned char *input = malloc(LIMIT + 1u);
    if (!input) return 1;
    size_t len = fread(input, 1, LIMIT + 1u, stdin);
    if (ferror(stdin) || len > LIMIT) { free(input); return 2; }
    gearman_client_st *client = gearman_client_create(NULL);
    if (!client) { free(input); return 1; }
    gearman_return_t rc = gearman_client_add_server(client, argv[1], (in_port_t)port);
    if (rc != GEARMAN_SUCCESS) { free(input); gearman_client_free(client); return 1; }
    gearman_client_set_timeout(client, 5000);
    size_t result_size = 0;
    void *result = gearman_client_do(client, "gearman_skill.bytes.v1", argv[3], input, len, &result_size, &rc);
    int exit_code = 0;
    if (rc != GEARMAN_SUCCESS) {
        fprintf(stderr, "No final success (code %d); reconcile before resubmitting\n", (int)rc);
        exit_code = 3;
    } else if (result_size > LIMIT || (result_size && !result)) {
        exit_code = 1;
    } else if (result_size && fwrite(result, 1, result_size, stdout) != result_size) {
        exit_code = 1;
    }
    if (fflush(stdout) == EOF) exit_code = 1;
    free(result); free(input); gearman_client_free(client);
    return exit_code;
}
