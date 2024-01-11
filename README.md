# wakeonlan

This is some premature documentation for this project. Feel free to contact
with comments or additions (good or bad).

Authors:

* José Pedro Oliveira ~~<jpo[at]di.uminho.pt>~~ <jose.p.oliveira.oss[at]gmail.com>
* Ico Doornekamp <ico[at]edd.dhs.org>

Table of contents:

1. [What is wakeonlan](#1-what-is-wakeonlan)
2. [How does WOL work?](#2-how-does-wol-work)
3. [How is it implemented here?](#3-how-is-it-implemented-here)
4. [Known to work hardware](#4-known-to-work-hardware)
5. [References](#5-references)

## 1. What is wakeonlan

This script sends 'magic packets' to wake-on-lan enabled ethernet
adapters, in order to switch on the called PC.

## 2. How does WOL work?

WOL is based on the following principle :

When the PC shuts down, the NIC still gets power, and keeps listening on
the network for a 'magic' packet to arrive. This packet must contain a
certain byte-sequence, but can be encapsulated in any kind of packet
(IPX, IP, anything). Take a look at the code for the magic sequence.

This program uses UDP for sending the packet. The complete UDP packet, sent
over an ethernet interface, looks something like this

```text
[Ethernet header][IP header][UDP header][Magic sequence][CRCS]
```

The only goal of the script is to send this packet over the network. It
expects no returning data, since the NIC only listens, and does not reply
anything.

For a more detailed description of the Magic Packet technology, check the
AMD resources listed in the [references](#5-references) section.

## 3. How is it implemented here?

The scripts takes 2 arguments, the MAC-address of the NIC, and an IP
address. The IP-address is tricky :

For a NIC on your local subnet, use the broadcast-address of this subnet.
(e.g. subnet 192.168.10.0 with netmask 255.255.255.0, use 192.168.10.255)

For waking up a PC on a network behind one or more routers, some tricks must
be used. When the routers forward directed subnet broadcasts, it is possible
to use the broadcast address of the destination network. The problem is that
many routers don't forward broadcast packets, so the packet will never arrive
at the network.

It is possible to send the packet to the remote net however, by sending it
to the IP address of another host on that network that's alive at that
moment. The remote hosts will probably ignore the packet, but it has been
seen by the listening NIC that's also on the same subnet, and it will turn
on the computer... Feel free to experiment on this.

## 4. Known-to-work hardware

* 3Com 3c905B Cyclone 100baseTx on an Abit BP6 Motherboard;
  (Ico Doornekamp)

* Intel EtherExpress Pro (i82557) with management chip built onto an IBM
  IntelliStation motherboard;
  (Sean-Paul Rees)

* Intel EtherExpress PRO/100+ (chipset 82559) with a PXE boot agent on
  an ASUS P2B motherboard;
  (José Pedro Oliveira)

* Motherboard: ASUS TUSL2-C;
  BIOS: Award BIOS / Power / Power Up Control / Wake On LAN or PCI Modem [Enable];
  Network card: Intel Pro/100 S Desktop Adapter (chipset 82550)
  with PXE boot agent v4.0.22;
  (José Pedro Oliveira)

* Motherboard: ASUS TUSL2-C;
  BIOS: Award BIOS / Power / Power Up Control / Wake On LAN or PCI Modem [Enable]
  Network card: 3Com Fast Etherlink TX 10/100 PCI (3C905C-TXM)
  with Managed PC Boot Agent (MBA) v4.30 (build 3)
  Pre-boot eXecution Environment (PXE) v2.20;
  (José Pedro Oliveira)

* nVidia Corporation nForce2 Ethernet Controller on ASUS and EPOX motherboards;
  (Antoniu-George)

* Macs: All Powerbooks;
  Energy Prefs: Wake on ethernet network Administrator access;
  (Denis Ahrens)

## 5. References

* [AMD - Magic Packet Technology](https://web.archive.org/web/20000414213425/http://www.amd.com/products/npd/overview/20212.html) - Internet Archive link
* [AMD - Magic Packet Technology - White paper](https://www.amd.com/content/dam/amd/en/documents/archived-tech-docs/white-papers/20213.pdf)
* [Wireshark wiki - WakeOnLan](https://gitlab.com/wireshark/wireshark/-/wikis/WakeOnLan)
* [Wikipedia - Wake-On-LAN](https://en.wikipedia.org/wiki/Wake-on-LAN)
* [Old wakeonlan project page](https://web.archive.org/web/20140120212300/http://gsd.di.uminho.pt:80/jpo/software/wakeonlan/) - Internet Archive link
* [Old Wake on LAN mini HOWTO](https://web.archive.org/web/20080321144028/http://gsd.di.uminho.pt/jpo/software/wakeonlan/mini-howto/wol-mini-howto.html) - Internet Archive link

<!-- vim:set ai ts=4 sw=4 sts=4 et: -->
