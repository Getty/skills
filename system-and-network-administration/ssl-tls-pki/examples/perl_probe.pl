#!/usr/bin/env perl
use strict;
use warnings;
use IO::Socket::SSL qw(SSL_VERIFY_PEER);
my ($host, $port, $name, $ca) = @ARGV;
die "usage: perl_probe.pl host port expected-name ca.pem\n" unless @ARGV == 4;
die "invalid port/name\n" unless $port =~ /^\d+$/ && $port > 0 && $port < 65536 && $name !~ /[\r\n \/\\]/;
$SIG{ALRM} = sub { die "timeout\n" };
alarm 8;
my $s = IO::Socket::SSL->new(
    PeerHost=>$host, PeerPort=>$port, Timeout=>5,
    SSL_verify_mode=>SSL_VERIFY_PEER, SSL_ca_file=>$ca,
    SSL_hostname=>$name, SSL_verifycn_name=>$name, SSL_verifycn_scheme=>'http',
) or die IO::Socket::SSL::errstr()."\n";
print {$s} "GET / HTTP/1.1\r\nHost: $name\r\nConnection: close\r\n\r\n" or die "write failed: $!\n";
my $status = <$s>;
die "application rejected or response missing\n" unless defined($status) && $status =~ m{^HTTP/1\.1 200 };
print $status;
close $s;
alarm 0;
