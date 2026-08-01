#!/usr/bin/perl -w
use strict;
use Test::More;
use IO::Select;
use IO::Socket::INET;

my $script = 'wakeonlan';
plan skip_all => "script $script not found" unless -f $script;

# Receive the magic packets on the loopback interface instead of
# broadcasting them over the network.
my $listener = IO::Socket::INET->new(
    LocalAddr => '127.0.0.1',
    Proto     => 'udp',
) or plan skip_all => "cannot listen on the loopback interface: $!";

my $port = $listener->sockport;

# The magic sequence: 6 times 0xFF followed by 16 times the hardware
# address of the NIC.
my $hwaddr_bytes = "\x01\x02\x03\x04\x05\x06";
my $expected     = chr(0xFF) x 6 . $hwaddr_bytes x 16;

# Every supported representation of the very same hardware address
my @formats = (
    [ 'canonical'                 => '01:02:03:04:05:06' ],
    [ 'Windows'                   => '01-02-03-04-05-06' ],
    [ 'Hewlett-Packard switches'  => '010203-040506'     ],
    [ 'Intel Landesk'             => '010203040506'      ],
    [ 'abbreviated bytes'         => '1:2:3:4:5:6'       ],
    [ 'abbreviated bytes, dashes' => '1-2-3-4-5-6'       ],
);

plan tests => 3 * scalar @formats;

foreach my $format (@formats) {
    my ($name, $hwaddr) = @{$format};

    my $rc = system($^X, $script,
        '-q', '-i', '127.0.0.1', '-p', $port, $hwaddr);
    is($rc, 0, "$name ($hwaddr): exits successfully");

    my $packet = '';
    if (IO::Select->new($listener)->can_read(5)) {
        $listener->recv($packet, 1024);
    }

    is(length($packet), length($expected),
        "$name ($hwaddr): magic packet is " . length($expected) . " bytes");
    is(unpack('H*', $packet), unpack('H*', $expected),
        "$name ($hwaddr): magic packet carries the hardware address");
}

# vim:set ai ts=4 sw=4 sts=4 et syntax=perl:
