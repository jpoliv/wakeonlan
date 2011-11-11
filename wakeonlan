#!/usr/bin/perl -w
#
# $Id: wakeonlan,v 1.4.2.3 2005/01/27 16:03:54 jpo Exp $
#
#########################################################################       

use strict;
use Socket;
use Getopt::Std;
use vars qw($VERSION $opt_v $opt_h $opt_i $opt_p $opt_f);
$VERSION = '0.41';

my $DEFAULT_IP      = '255.255.255.255';
my $DEFAULT_PORT    = getservbyname('discard', 'udp');

#
# Process the command line
#

getopts("hvp:i:f:");

if ($opt_h) { usage(); exit(0); }
if ($opt_v) { print "wakeonlan version $VERSION\n"; exit(0); }
if (!$opt_f and !@ARGV) { usage(); exit(0); }
if ($opt_i) { $DEFAULT_IP = $opt_i; }		# override default value
if ($opt_p) { $DEFAULT_PORT = $opt_p; }		# override default value

if ($opt_f) { process_file($opt_f); }

# The rest of the command line is a list of hardware addresses 

foreach (@ARGV) {
	wake($_, $opt_i, $opt_p);
} 

#
# wake
#
# The 'magic packet' consists of 6 times 0xFF followed by 16 times
# the hardware address of the NIC. This sequence can be encapsulated
# in any kind of packet, in this case an UDP packet targeted at the
# discard port (9).
#                                                                               

sub wake
{
	my $hwaddr  = shift;
	my $ipaddr  = shift || $DEFAULT_IP;
	my $port    = shift || $DEFAULT_PORT;

	my ($raddr, $them, $proto);
	my ($hwaddr_re, $pkt);
	
	# Validate hardware address (ethernet address)

	$hwaddr_re = join(':', ('[0-9A-Fa-f]{1,2}') x 6);
	if ($hwaddr !~ m/^$hwaddr_re$/) {
		warn "Invalid hardware address: $hwaddr\n";
		return undef;
	}

	# Generate magic sequence

	foreach (split /:/, $hwaddr) {
		$pkt .= chr(hex($_));
	}
	$pkt = chr(0xFF) x 6 . $pkt x 16;

	# Allocate socket and send packet

	$raddr = gethostbyname($ipaddr);
	$them = pack_sockaddr_in($port, $raddr);
	$proto = getprotobyname('udp');

	socket(S, AF_INET, SOCK_DGRAM, $proto) or die "socket : $!";
	setsockopt(S, SOL_SOCKET, SO_BROADCAST, 1) or die "setsockopt : $!";

	print "Sending magic packet to $ipaddr:$port with $hwaddr\n";

	send(S, $pkt, 0, $them) or die "send : $!";
	close S;
}

#
# process_file
#

sub process_file {
	my $filename = shift;
	my ($hwaddr, $ipaddr, $port);

	open (F, "<$filename") or die "open : $!";
	while(<F>) {
		next if /^\s*#/;		# ignore comments
		next if /^\s*$/;		# ignore empty lines

		chomp;
		($hwaddr, $ipaddr, $port) = split;

		wake($hwaddr, $ipaddr, $port);
	}
	close F;
}


#
# Usage
#

sub usage {
print <<__USAGE__;
Usage
    wakeonlan [-h] [-v] [-i IP_address] [-p port] [-f file] [[hardware_address] ...]

Options
    -h
        this information
    -v
        displays the script version
    -i ip_address
        set the destination IP address
        default: 255.255.255.255 (the limited broadcast address)
    -p port
        set the destination port
        default: 9 (the discard port)
    -f file 
        uses file as a source of hardware addresses

See also
    wakeonlan(1)    

__USAGE__
}


__END__

# Script documentation

=head1 NAME

wakeonlan - Perl script to wake up computers

=head1 SYNOPSIS

wakeonlan [-h] [-v] [-i IP_address] [-p port] [-f file] [[hardware_address] ...]

=head1 DESCRIPTION

This script sends 'magic packets' to wake-on-lan enabled ethernet adapters and motherboards, in order to switch on the called PC. Be sure to connect the NIC with the motherboard if neccesary, and enable the WOL function in the BIOS.

The 'magic packet' consists of 6 times 0xFF followed by 16 times the hardware address of the NIC. This sequence can be encapsulated in any kind of packet. This script uses UDP packets.

=head1 OPTIONS

=over

=item B<-h>

Displays the help information.

=item B<-v>

Displays the script version.

=item B<-i ip_address>

Destination IP address. Unless you have static ARP tables you should
use some kind of broadcast address (the broadcast address of the network where the computer resides or the limited broadcast address). Default: 255.255.255.255 (the limited broadcast address).

=item B<-p port>

Destination port. Default: 9 (the discard port).

=item B<-f file>

File with hardware addresses of wakeable computers. For an example check
the file lab001.wol in the examples subdirectory.

=back

=head1 EXAMPLES

Using the limited broadcast address (255.255.255.255):

    $ wakeonlan 01:02:03:04:05:06
    $ wakeonlan 01:02:03:04:05:06 01:02:03:04:05:07

Using a subnet broadcast address:

    $ wakeonlan -i 192.168.1.255 01:02:03:04:05:06

Using another destination port:

    $ wakeonlan -i 192.168.1.255 -p 1234 01:02:03:04:05:06

Using a file as source of hardware and IP addresses:

    $ wakeonlan -f examples/lab001.wol
    $ wakeonlan -f examples/lab001.wol 01:02:03:04:05:06

=head1 AUTHOR

José Pedro Oliveira <jpo@di.uminho.pt> maintaining and expanding original work done by Ico Doornekamp <ico@edd.dhs.org>.

=head1 COPYRIGHT

Copyright (c) 2000-2005 José Pedro Oliveira.

This is free software.  You may modify it and distribute it under Perl's Artistic Licence.  Modified versions must be clearly indicated.                                                    

=head1 SEE ALSO

For more information regarding this script and Wakeonlan technology just check the following address http://gsd.di.uminho.pt/jpo/software/wakeonlan/.

=cut
