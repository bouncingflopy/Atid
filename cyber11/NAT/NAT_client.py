from scapy.all import *
from scapy.layers.inet import IP, UDP

SERVER_IP, SERVER_PORT = ('77.137.77.109', 1337)
MY_IP = '77.137.77.109'
name = input()
port = int(input())


def server_filter(p):
    return Raw in p and UDP in p and IP in p and p[IP].src == SERVER_IP and p[UDP].sport == SERVER_PORT and p[UDP].dport == port


def peer_filter(p):
    return Raw in p and UDP in p and IP in p and p[IP].src == peer_ip and p[UDP].sport == peer_port and p[UDP].dport == port


r = []
p = IP(src=MY_IP, dst=SERVER_IP) / UDP(sport=port, dport=SERVER_PORT) / Raw(load=f'Hello my name is {name}')
while len(r) == 0:
    send(p, verbose=False)
    r = sniff(count=1, lfilter=server_filter, timeout=0.25)
    r = r[0] if len(r) > 0 else r

peer_ip, peer_port = str(r[Raw].load)[2:-1].split(' ')
peer_port = int(peer_port)

r = []
p = IP(src=MY_IP, dst=peer_ip) / UDP(sport=port, dport=peer_port) / Raw(load=f'Hello my name is {name}')
while True:
    send(p, verbose=False)
    r = sniff(count=1, lfilter=peer_filter, timeout=0.1)
    r = r[0] if len(r) > 0 else r
    if len(r) > 0:
        print(str(r[Raw].load)[2:-1])
