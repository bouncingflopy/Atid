from scapy.all import *
from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.inet import UDP, IP


def load_data():
    with open("C://Networks//work//dns//database.txt", 'r+') as f:
        lines = f.readlines()
    return lines


def dns_filter(p):
    return DNS in p and DNSQR in p and p[DNS].opcode == 0 and p[DNS].qr == 0 and (p[DNSQR].qtype == 1 or p[DNSQR].qtype == 12)


def generate(d, r):
    data = None
    for line in d:
        if r[DNSQR].qname.decode() == line[0] or r[DNSQR].qname.decode() == line[1]:
            data = line
    if data is None:
        p = IP(dst=r[IP].src) / UDP(dport=53) / DNS(id=r[DNS].id, qr=1, ra=1, rcode=3, qd=r[DNSQR])
        return p

    p = IP(dst=r[IP].src, ttl=int(data[2])) / UDP(dport=53) / DNS(id=r[DNS].id, qr=1, ra=1, ancount=1)

    p.qd = r[DNSQR]
    p.an = DNSRR(rrname=r[DNSQR].qname, type=r[DNSQR].qtype, ttl=int(data[2]), rdlen=4 if r[DNSQR].qtype == 1 else len(data[0]) + 1, rdata=data[1] if r[DNSQR].qtype == 1 else data[0])

    return p


def main():
    database = [line.split(' ') for line in load_data()]

    while True:
        request = sniff(count=1, lfilter=dns_filter)[0]
        p = generate(database, request)
        send(p, )


if __name__ == "__main__":
    main()
