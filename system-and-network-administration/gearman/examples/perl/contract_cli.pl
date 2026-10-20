#!/usr/bin/env perl
use strict;
use warnings;
use FindBin;
use lib "$FindBin::Bin/lib";
use GearmanSkill::Contract qw(parse_request execute_request encode_json read_request);
binmode STDOUT;
my $result = eval { encode_json(execute_request(parse_request(read_request(\*STDIN)))) };
if ($@) { print STDERR "contract rejected input\n"; exit 1; }
print $result, "\n";
