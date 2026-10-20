/* Callback-return ownership example: libgearman sends the terminal response. */
#include <libgearman/gearman.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <errno.h>
#define LIMIT 65536u
static volatile sig_atomic_t stopping = 0;
static void stop_handler(int sig) { (void)sig; stopping = 1; }
static void *echo_job(gearman_job_st *job, void *context, size_t *result_size, gearman_return_t *ret) {
    (void)context;
    *result_size = 0;
    size_t n = gearman_job_workload_size(job);
    if (n > LIMIT) { *ret = GEARMAN_WORK_FAIL; return NULL; }
    void *out = malloc(n ? n : 1u);
    if (!out) { *ret = GEARMAN_WORK_FAIL; return NULL; }
    if (n) memcpy(out, gearman_job_workload(job), n);
    *result_size = n;
    *ret = GEARMAN_SUCCESS;
    return out;
}
int main(int argc, char **argv) {
    if (argc != 3) { fprintf(stderr, "usage: worker HOST PORT\n"); return 2; }
    char *end = NULL;
    errno = 0;
    long port = strtol(argv[2], &end, 10);
    if (errno || end == argv[2] || !end || *end || port < 1 || port > 65535) return 2;
    signal(SIGTERM, stop_handler); signal(SIGINT, stop_handler);
    gearman_worker_st *worker = gearman_worker_create(NULL);
    if (!worker) return 1;
    gearman_return_t rc = gearman_worker_add_server(worker, argv[1], (in_port_t)port);
    if (rc == GEARMAN_SUCCESS) rc = gearman_worker_add_function(worker, "gearman_skill.bytes.v1", 0, echo_job, NULL);
    if (rc != GEARMAN_SUCCESS) { gearman_worker_free(worker); return 1; }
    gearman_worker_set_timeout(worker, 1000);
    int code = 0;
    while (!stopping) {
        rc = gearman_worker_work(worker);
        if (rc != GEARMAN_SUCCESS && rc != GEARMAN_TIMEOUT) {
            fprintf(stderr, "worker stopped (code %d)\n", (int)rc);
            code = 1; break;
        }
    }
    gearman_worker_free(worker);
    return code;
}
