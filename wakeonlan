#!/usr/bin/perl -w
#
# $Id: wakeonlan,v 1.4.2.3 2005/01/27 16:03:54 jpo Exp $
#
######################################################################

use strict;
use Socket;
use Getopt::Long;
use Pod::Usage;

our $VERSION = '0.41_90';

use constant {
	PORT_MIN           => 0,
	PORT_MAX           => 65535,
};

#
# Hardware address formats
#
our @hwaddr_regexs = (
	# xx:xx:xx:xx:xx:xx (canonical)
	'^(?:[\da-f]{1,2}:){5}[\da-f]{1,2}$',

	# xx-xx-xx-xx-xx-xx (Windows)
	'^(?:[\da-f]{1,2}-){5}[\da-f]{1,2}$',

	# xxxxxx-xxxxxx (Hewlett-Packard switches)
	'^[\da-f]{6}-[\da-f]{6}$',

	# xxxxxxxxxxxx (Intel Landesk)
	'^[\da-f]{12}$',
);

my $DEFAULT_IP         = '255.255.255.255';
my $DEFAULT_PORT       = getservbyname('discard', 'udp');

my $verbose            = 1;
my $dryrun             = 0;
my $filename           = '';

my @queue              = ();

my %stats = (
	total              => 0,
	valid              => 0,
	invalid            => 0,
	sent               => 0,
);

######################################################################

sub isValidPort {
	my $port = shift;

	return ($port >= PORT_MIN and $port <= PORT_MAX) ? 1 : 0;
}


sub isValidIPAddress {
	my $ipaddress = shift;
	my $t = 0;

	$t += $_ for map { ($_ <= 255)?1:0 }
			$ipaddress =~ m/^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/;

	return ($t == 4) ? 1 : 0;
}


sub isValidHardwareAddress {
	my $hwaddr = shift;

	foreach my $re (@hwaddr_regexs) {
		return 1 if ($hwaddr =~ m/$re/i);
	}

	return 0;
}

######################################################################

sub loadFromCommandLine {

	for my $arg (@_) {
		$stats{total}++;

		if (! isValidHardwareAddress($arg) ) {
			warn "Invalid hardware address: $arg\n";
			$stats{invalid}++;
			next;
		}

		$stats{valid}++;
		push @queue, [ $arg, $DEFAULT_IP, $DEFAULT_PORT ];
	}
}


sub loadFromFile {
	my $filename = shift;
	my ($hwaddr, $ipaddr, $port);

	open (my $FILE, '<', $filename) or die "open : $!";
	while(<$FILE>) {
		next if /^\s*#/;		# ignore comment lines
		next if /^\s*$/;		# ignore empty lines

		$stats{total}++;

		chomp;
		($hwaddr, $ipaddr, $port) = split;

		if (! isValidHardwareAddress($hwaddr) ) {
			warn "Invalid hardware address: $hwaddr\n";
			$stats{invalid}++;
			next;
		}

		$ipaddr = $DEFAULT_IP unless defined($ipaddr);
		if (! isValidIPAddress($ipaddr) ) {
			warn "Invalid IP address: $ipaddr\n";
			$stats{invalid}++;
			next;
		}

		$port = $DEFAULT_PORT unless defined($port);
		if (! isValidPort($port) ) {
			warn "Invalid port number: $port\n";
			$stats{invalid}++;
			next;
		}

		$stats{valid}++;
		push @queue, [ $hwaddr, $ipaddr, $port ];
	}
	close $FILE;
}


######################################################################

#
# wake
#
# The 'magic packet' consists of 6 times 0xFF followed by 16 times
# the hardware address of the NIC. This sequence can be encapsulated
# in any kind of packet, in this case an UDP packet targeted at the
# discard port (9).
#

sub wake {
	my ($sock, $hwaddr, $ipaddr, $port) = @_;
	my ($raddr, $them, $pkt);
	#
	# Expects hardware address in canonical form (xx:xx:xx:xx:xx:xx)
	#

	#
	# Generate the magic sequence
	#
	foreach (split /:/, $hwaddr) {
		$pkt .= chr(hex($_));
	}
	$pkt = chr(0xFF) x 6 . $pkt x 16;

	#
	# Send packet
	#

	# Patch by Eugenio Jarosiewicz <ej0 at mac.com>
	# $raddr = inet_aton($ipaddr);
	#
	$raddr = gethostbyname($ipaddr);
	$them = pack_sockaddr_in($port, $raddr);

	print "Sending magic packet to $ipaddr:$port with payload $hwaddr\n"
		if $verbose;

	#send($sock, $pkt, 0, $them) or die "send : $!";
	send($sock, $pkt, 0, $them) unless $dryrun;

}


sub sendMagicPackets {

	if (! @queue) {
		warn "Nothing to do!\n";
		return;
	}

	my $sock;
	my $proto = getprotobyname('udp');

	socket($sock, AF_INET, SOCK_DGRAM, $proto) or die "socket : $!";
	setsockopt($sock, SOL_SOCKET, SO_BROADCAST, 1) or die "setsockopt : $!";

	for my $ref (@queue) {

		wake($sock, $ref->[0], $ref->[1], $ref->[2]);

		$stats{sent}++;
	}

	close $sock;
}

######################################################################
# main
######################################################################

#
# Process the command line
#

GetOptions(
	"h|help"       => sub { pod2usage( -exitval => 0, -verbose => 1); },
	"v|version"    => sub { print "wakeonlan $VERSION\n"; exit(0); },
	"q|quiet"      => sub { $verbose = 0; },
	"i|ip=s"       => \$DEFAULT_IP,
	"p|port=i"     => \$DEFAULT_PORT,
	"f|file=s"     => \$filename,
	"n|dry-run"    => sub { $dryrun = 1; },
) or pod2usage( -exitval => 1, -verbose => 1);


#
# Validate information
#
#
if (! isValidPort($DEFAULT_PORT)) {
	warn "Invalid default port number: $DEFAULT_PORT\n";
	exit(2);
}

if (! isValidIPAddress($DEFAULT_IP)) {
	warn "Invalid default IP address: $DEFAULT_IP\n";
	exit(3);
}

if ($filename and ! -f $filename) {
	warn "Invalid filename: $filename\n";
	exit(4);
}

#
# Nothing to do ?
#
if (!$filename and !@ARGV) { pod2usage( -exitval => 0, -verbose => 1); };


#
# Load hardware addresses
#

loadFromCommandLine(@ARGV);
loadFromFile($filename) if $filename;

# print Dumper(@queue);

sendMagicPackets();

#
# Print statistics
#
if ($verbose) {
	printf "Hardware addresses: <total=%d, valid=%d, invalid=%d>\n",
		$stats{total}, $stats{valid}, $stats{invalid};
	printf "Magic packets: <sent=%d>\n", $stats{sent};
}

exit 0;

##########


__END__


# Script documentation
=encoding utf8

=head1 NAME

wakeonlan - Perl script to wake up computers

=head1 SYNOPSIS

wakeonlan [-h|--help] [-v|--version] [-q|--quiet] [-n|--dry-run] [-i|--ip IP_address] [-p|--port port] [-f|--file file_name] [[hardware_address] ...]

=head1 DESCRIPTION

This script sends 'magic packets' to wake-on-lan enabled ethernet adapters and motherboards, in order to switch on the called PC. Be sure to connect the NIC with the motherboard if necessary, and to enable the WOL function in the BIOS.

The 'magic packet' consists of 6 times 0xFF followed by 16 times the hardware address of the NIC. This sequence can be encapsulated in any kind of packet. This script uses UDP packets.

=head1 OPTIONS

=over

=item B<-h, --help>

Displays the help information.

=item B<-v, --version>

Displays the script version.

=item B<-i, --ip=IP_address>

Destination IP address. Unless you have static ARP tables you should
use some kind of broadcast address (the broadcast address of the network where the computer resides or the limited broadcast address). Default: 255.255.255.255 (the limited broadcast address).

=item B<-p, --port=port>

Destination port. Default: 9 (the discard port).

=item B<-f, --file=file_name>

File with hardware addresses of wakeable computers. For an example check
the file lab001.wol in the examples subdirectory.

=item B<-q, --quiet>

Quiet mode.

=item B<-n, --dry-run>

Print the commands that would be executed, but do not execute them.

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

Copyright (c) 2000-2009 José Pedro Oliveira.

This is free software.  You may modify it and distribute it under Perl's Artistic License.  Modified versions must be clearly indicated.

=head1 SEE ALSO

For more information regarding this script and Wakeonlan technology just check the following address http://gsd.di.uminho.pt/jpo/software/wakeonlan/.

=cut

# vim:set ai ts=4 sw=4 sts=4 syntax=perl:
