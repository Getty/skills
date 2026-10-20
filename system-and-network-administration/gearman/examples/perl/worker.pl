#!/usr/bin/env perl
# One execution slot; use an external supervisor. No external side effects in this demo.
use strict;
use warnings;
use FindBin;
use lib "$FindBin::Bin/lib";
use GearmanSkill::Contract qw(parse_request execute_request encode_json);
require Gearman::Worker;
my $stop = 0;
$SIG{TERM} = $SIG{INT} = sub { $stop = 1 };
my $worker = Gearman::Worker->new;
$worker->job_servers($ENV{GEARMAN_SERVER} // '127.0.0.1:4730');
$worker->register_function('gearman_skill.sum.v1', sub {
    my ($job) = @_;
    my $result = eval { encode_json(execute_request(parse_request($job->arg))) };
    if ($@) {
        warn "contract rejected job; returning WORK_FAIL\n";
        return undef; # Catch here: do not depend on the binding's uncaught-exception sequence.
    }
    return $result;
});
$worker->work(stop_if => sub { return $stop });
