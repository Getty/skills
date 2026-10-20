package GearmanSkill::Contract;
use strict;
use warnings;
use Exporter 'import';
use JSON::PP ();
use B ();
use Config ();
our @EXPORT_OK = qw(parse_request execute_request encode_json read_request);
my $json = JSON::PP->new->utf8->canonical->allow_nonref(0)->max_depth(32);
sub integer {
    my ($v) = @_;
    return 0 if !defined($v) || ref($v);
    return (B::svref_2object(\$v)->FLAGS & B::SVp_IOK()) ? 1 : 0;
}
sub read_request {
    my ($fh) = @_;
    binmode($fh);
    my $raw = '';
    while (length($raw) <= 65536) {
        my $n = read($fh, my $chunk, 65537 - length($raw));
        die "input read failed\n" unless defined $n;
        last if !$n;
        $raw .= $chunk;
    }
    die "request too large\n" if length($raw) > 65536;
    return $raw;
}
sub parse_request {
    my ($raw) = @_;
    die "64-bit Perl required\n" if $Config::Config{ivsize} < 8;
    die "request too large\n" if length($raw) > 65536;
    # JSON::PP does not reject duplicate keys; require stricter ingress for hostile JSON.
    my $obj = eval { $json->decode($raw) };
    die "invalid JSON\n" if $@ || ref($obj) ne 'HASH';
    my %allowed = map { $_ => 1 } qw(schema_version request_id operation payload deadline_unix_ms);
    die "unknown envelope fields\n" if grep { !$allowed{$_} } keys %$obj;
    die "missing envelope fields\n" if grep { !exists $obj->{$_} } qw(schema_version request_id operation payload);
    die "unsupported schema\n" unless integer($obj->{schema_version}) && $obj->{schema_version} == 1;
    die "invalid request_id\n" if ref($obj->{request_id}) || !defined($obj->{request_id})
        || $obj->{request_id} !~ /\A[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\z/;
    die "unsupported operation\n" if ref($obj->{operation}) || !defined($obj->{operation}) || $obj->{operation} ne 'sum.v1';
    my $p = $obj->{payload};
    die "invalid payload\n" unless ref($p) eq 'HASH' && keys(%$p) == 1 && exists $p->{numbers};
    my $n = $p->{numbers};
    die "invalid numbers\n" unless ref($n) eq 'ARRAY' && @$n >= 1 && @$n <= 1000;
    for my $v (@$n) {
        die "invalid integer\n" unless integer($v) && abs($v) <= 1000000000;
    }
    if (exists $obj->{deadline_unix_ms}) {
        my $d = $obj->{deadline_unix_ms};
        die "invalid deadline\n" unless integer($d) && $d >= 0 && $d <= 9007199254740991;
    }
    return $obj;
}
sub execute_request {
    my ($obj) = @_;
    die "deadline expired\n" if exists($obj->{deadline_unix_ms}) && $obj->{deadline_unix_ms} <= int(time() * 1000);
    my $sum = 0;
    $sum += $_ for @{$obj->{payload}{numbers}};
    return {schema_version => 1, request_id => $obj->{request_id}, ok => JSON::PP::true,
            result => {sum => $sum}};
}
sub encode_json { return $json->encode($_[0]); }
1;
