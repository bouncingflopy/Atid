from scapy.all import *
from scapy.layers.dns import DNS, DNSQR
from scapy.layers.inet import UDP, IP


def load_data():
    with open("database.txt", 'r+') as f:
        lines = f.readlines()
    return lines


def dns_filter(p):
    return DNS in p and p[DNS].opcode == 0 and (p[DNSQR].qtype == 1 or p[DNSQR].qtype == 12)


def main():
    d = [line.split(' ') for line in load_data()]

    while True:
        r = sniff(count=1, lfilter=dns_filter)[0]

        if r[DNSQR].qtype == 1:
            dnames = [d[i][1] for i in range(len(d)) if d[i][0] == "1"]
            if r[DNSQR].qname.decode() in dnames:
                p = IP(dst=r[IP].src, ttl=64)/UDP()/DNS(id=r[DNS].id, qr=1, ra=1)
                print("need to answer " + r[DNSQR].qname.decode())


if __name__ == "__main__":
    main()
