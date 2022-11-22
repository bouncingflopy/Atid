from scapy.all import *
from scapy.layers.inet import UDP, IP

PORT = 1337
MY_IP = '77.137.77.109'
connections = []


def client_filter(p):
    return Raw in p and UDP in p and IP in p and p[UDP].dport == PORT


while True:
    while len(connections) < 2:
        r = sniff(count=4, lfilter=client_filter, timeout=0.5)

        if len(r) > 0:
            for c in r:
                name = (c[IP].src, c[UDP].sport)
                if name not in connections:
                    connections.append(name)

    p1 = IP(src=MY_IP, dst=connections[0][0]) / UDP(sport=PORT, dport=connections[0][1]) / Raw(load=f'{connections[1][0]} {connections[1][1]}')
    p2 = IP(src=MY_IP, dst=connections[1][0]) / UDP(sport=PORT, dport=connections[1][1]) / Raw(load=f'{connections[0][0]} {connections[0][1]}')
    send(p1, verbose=False)
    send(p2, verbose=False)

    connections = []
