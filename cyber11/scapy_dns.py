from scapy.all import *
from scapy.layers.dns import DNS, DNSQR
import socket

s = socket.socket()
s.bind('0.0.0.0', 53)

def dns_filter(packet):
    return DNS in packet and packet[DNS].opcode == 0 and (packet[DNSQR].qtype == 1 or packet[DNSQR].qtype == 12)


def main():
    while True:
        p = sniff(count=1, lfilter=dns_filter)[0]
        print(p[DNSQR].qname)


if __name__ == "__main__":
    main()
