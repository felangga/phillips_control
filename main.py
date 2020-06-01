from scapy.all import ARP, Ether, srp
import socket

def scan_host(host, port, r_code = 1) :
    try :
        s = socket(AF_INET, SOCK_DGRAM)
        code = s.connect_ex((host, port))
        if code == 0 :
            r_code = code
        s.close()
    except Exception, e :
        pass
    return r_code

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
print("######################################");
print("# Phillips Smart LED Override        #");
print("# BGL. 2020                          #");
print("######################################");
print("");
print("IP ADDRESS ANDA : " + ip_address)
target_ip = ip_address + "/24"

arp = ARP(pdst=target_ip)
ether = Ether(dst="ff:ff:ff:ff:ff:ff")
packet = ether/arp

result = srp(packet, timeout=3, verbose=0)[0]

clients = []
targets = []

for sent, received in result:
    clients.append({'ip': received.psrc, 'mac': received.hwsrc})

# print clients
print("Daftar Phillips Smart LED terhubung : ")
for client in clients:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto("HELLO", (client['ip'], 38899))
    sock.settimeout(1.0)
    try:
        data, server = sock.recvfrom(1024)
        print("{:16}    {}".format(client['ip'], client['mac']))
        targets.append(client['ip']);
    except socket.timeout:
        # do nothing
        continue

if (len(targets)>0):
    print("[1] Matikan Semua");
    print("[2] Nyalakan Semua");

    g = raw_input("Apa yang akan anda lakukan? ")
    if (g=="1"):
        print("Mematikan semua ...")
        for target in targets:
            print(" - Matikan " + target);
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto('{"params":{"state":false},"id":6,"method":"setPilot"}', (target, 38899))
            sock.settimeout(2.0);

    if (g=="2"):
        print("Menyalakan semua ...")
        for target in targets:
            print(" - Nyalakan " + target);
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto('{"params":{"state":true},"method":"setPilot"}', (target, 38899))
            sock.settimeout(2.0);




else:
    print("Tidak menemukan perangkat");
