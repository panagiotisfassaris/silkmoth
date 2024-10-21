import os
import sys
import socket
import struct
import ipaddress
import threading
import time

subnet = "192.168.1.0/24"
message = "testing"


class IP:
    def __init__(self, buff=None):
        header = struct.unpack("<BBHHHBBH4s4s", buff)
        self.version = header[0] >> 4
        self.hdrlen = header[0] & 0xF
        self.tos = header[1]
        self.length = header[2]
        self.id = header[3]
        self.foffset = header[4]
        self.ttl = header[5]
        self.proto_num = header[6]
        self.csum = header[7]
        self.src = header[8]
        self.dst = header[9]

        self.src_addr = ipaddress.ip_address(self.src)
        self.dst_addr = ipaddress.ip_address(self.dst)

        self.proto_map = {1: "ICMP", 6: "TCP", 17: "UDP"}

        try:
            self.protocol = self.proto_map[self.proto_num]
        except KeyError:
            self.protocol = str(self.proto_num)


class ICMP:
    def __init__(self, buff=None):
        header = struct.unpack("<BBHHH", buff)
        self.type = header[0]
        self.code = header[1]
        self.sum = header[2]
        self.id = header[3]
        self.seq = header[4]


class UDP:
    pass


class TCP:
    pass


class Scanner:
    def __init__(self, host):
        self.host = host

        #-------------------PROTOCOL-------------------
        if os.name == "nt":
            sock_proto = socket.IPPROTO_IP  #Windows: IPv4
        else:
            sock_proto = socket.IPPROTO_ICMP  #Other: ICMP
        #----------------------------------------------

        #-------------------SNIFFER-------------------
        #Raw sockets
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, sock_proto)
        #Bind raw socket to our PC/Host
        self.socket.bind((host, 0))
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        # ---------------------------------------------

        # -------------------PROMISCUOUS MODE = ON-------------------
        if os.name == "nt":
            #Turn on promiscuous mode on Windows (Sniffs packets from the entire network)
            self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
        # -----------------------------------------------------------

        print("Starting to sniff packets...")

    def sniff(self):
        hosts = set([f"{str(self.host)} *"])
        try:
            while True:
                raw_buff = self.socket.recvfrom(65565)[0]
                ip_head = IP(raw_buff[0:20])
                #If ICMP, process it further
                if ip_head.protocol == "ICMP":
                    offset = ip_head.hdrlen * 4
                    buf = raw_buff[offset : offset + 8]
                    icmp_head = ICMP(buf)
                    if (
                        icmp_head.type == 3 and icmp_head.code == 3
                    ):  #3 = error
                        print(f"ICMP -> Type: {icmp_head.type} Code: {icmp_head.code}")
                        if ipaddress.ip_address(
                            ip_head.src_addr
                        ) in ipaddress.IPv4Network(subnet):
                            if raw_buff[len(raw_buff) - len(message) :] == bytes(
                                message, "utf8"
                            ):
                                tgt = str(ip_head.src_addr)
                                if tgt != self.host and tgt not in hosts:
                                    hosts.add(str(ip_head.src_addr))
                                    print(f"Host up: {tgt}")

                elif ip_head.protocol == "TCP":
                    icmp_head = TCP(buf)

        except KeyboardInterrupt:
            if os.name == "nt":
                self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
                print("\nUser interrupted")
                if hosts:
                    print(f"\nSummary: Hosts up on {subnet}")
                    for _host in sorted(hosts):
                        print(_host)
                input("Press any key to exit: ")
                sys.exit()

        except Exception as e:
            print(f"An error occurred: {e}")


def udp_sender():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sender:
        for ip in ipaddress.ip_network(subnet).hosts():
            sender.sendto(bytes(message, "utf8"), (str(ip), 65212))


if __name__ == "__main__":
    if len(sys.argv) == 2:
        host = sys.argv[1]
    else:
        host = "192.168.1.95"

    s = Scanner(host)
    time.sleep(5)
    t = threading.Thread(target=udp_sender)
    t.start()
    s.sniff()
