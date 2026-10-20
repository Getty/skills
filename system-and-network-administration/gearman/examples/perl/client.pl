#!/usr/bin/env perl
# Classic binding demo; private/plaintext endpoint only. See references/perl-classic.md.
use strict;
use warnings;
use FindBin;
use lib "$FindBin::Bin/lib";
use GearmanSkill::Contract qw(parse_request encode_json read_request);
my $background = @ARGV && $ARGV[0] eq '--background';
die "usage: client.pl [--background]\n" if @ARGV > 1 || (@ARGV && !$background);
my $raw = read_request(\*STDIN);
my $request = parse_request($raw);
require Gearman::Client; # Runtime require permits syntax checks without the binding installed.
my $client = Gearman::Client->new;
my $endpoint = $ENV{GEARMAN_SERVER} // '127.0.0.1:4730';
$client->job_servers($endpoint);
my $function = 'gearman_skill.sum.v1';
my $result;
my $ok = eval {
    local $SIG{ALRM} = sub { die "submission budget exceeded\n" };
    alarm 10; # Process-level lab guard; an interrupted submission has an uncertain outcome.
    $result = $background
        ? $client->dispatch_background($function, $raw, {uniq => $request->{request_id}})
        : $client->do_task($function, $raw, {uniq => $request->{request_id}});
    alarm 0;
    1;
};
alarm 0;
if (!$ok || !defined $result) {
    print STDERR "no successful completion evidence; reconcile request_id before retry\n";
    exit 3;
}
binmode STDOUT;
if ($background) {
    print encode_json({accepted => JSON::PP::true, completed => JSON::PP::false,
        handle => $result, request_id => $request->{request_id}, server => $endpoint}), "\n";
} else {
    die "unexpected classic client return type\n" unless ref($result) eq 'SCALAR';
    print $$result, "\n";
}
