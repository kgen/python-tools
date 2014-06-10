#encoding: UTF-8
import sys
import time
import random
from socket import inet_aton
from ctypes import *

from winpcapy import *
from dpkt.ip import IP, IP_PROTO_TCP
from dpkt.tcp import TCP
from dpkt.ethernet import Ethernet


MESSAGES = (
    "~\(O_o)/~",
    "(T_T)",
    "(=^_^=)",
    "(x_x)",
    "\(^(oo)^)/",
    "(@_@)..",
    "(>_<)",
    "(=_= #)"
)


def print_all_devs():
    """Print a list of all interfaces on local host.
    """
    errbuf = create_string_buffer(PCAP_ERRBUF_SIZE)
    alldevs = POINTER(pcap_if_t)()
    if (pcap_findalldevs_ex(PCAP_SRC_IF_STRING, None,
                            byref(alldevs), errbuf) != 0):
        print("Error in pcap_findalldevs(): %s" % errbuf.value)

    dev = alldevs.contents
    while dev:
        print("  %s:\n  >> %s\n" % (dev.description, dev.name))
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


def send_packet(fp, msg):
    http = u"HTTP/1.1 %s\r\n\r\njust for fun" % msg

    tcp = TCP(sport=80,
              dport=random.uniform(0, 65535), data=http)

    ip = IP(src=inet_aton('19.89.6.4'), dst=inet_aton('20.13.9.27'),
            p=IP_PROTO_TCP, data=tcp, len=20 + len(str(tcp)))

    eth = Ethernet(src='\xac\xf7\xf3\x00\x00\x00',
                   dst='\x00\x00\x00\x00\x00\x00',
                   data=ip)

    packet = str(eth)
    if (pcap_sendpacket(fp, build_packet(packet), len(packet)) != 0):
        print("Error sending the packet:\n  %s" % pcap_geterr(fp))


def main():
    if len(sys.argv) == 2:
        msg = None
        repeat = 1
    elif len(sys.argv) == 3:
        repeat = int(sys.argv[2])
        msg = None
    elif len(sys.argv) == 4:
        repeat = int(sys.argv[2])
        msg = sys.argv[3]
    else:
        print(r"Usage: net_test.py <interface> [repeat_times [message]]")
        print("  <interface>:\trpcap://\Device\NPF_{x-x-x-x-x}")
        print("\n  List of interfaces:")
        print_all_devs()
        sys.exit(1)
    dev = sys.argv[1]

    errbuf = create_string_buffer(PCAP_ERRBUF_SIZE)
    fp = pcap_open_live(dev, 65536, PCAP_OPENFLAG_PROMISCUOUS, 1000, errbuf)
    if not bool(fp):
        print("Unable to open the adapter (%s)." % dev)
        sys.exit(2)

    for i in range(repeat):
        if msg is None:
            sendmsg = random.choice(MESSAGES)
        else:
            sendmsg = msg
        send_packet(fp, sendmsg)
        time.sleep(0.1)

    pcap_close(fp)


if __name__ == '__main__':
    main()
