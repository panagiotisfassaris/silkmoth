# Silkmoth - Deauth Tool & Network Scanner

![Silkmoth Sniffer's Logo](logo.jpg)

**Silkmoth** is a lightweight Wi-Fi deauthentication and scanning tool built for system administrators and cybersecurity enthusiasts. It allows you to perform controlled deauth attacks and discover nearby clients and routers. This is ideal for Wi-Fi security assessments, penetration testing, or educational purposes.

## Table of Contents

- [About](#about)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Notes](#notes)
- [License](#license)

---

## About

**Silkmoth** provides two primary capabilities:

- **Deauthentication Attack**: Sends 802.11 deauthentication frames to forcibly disconnect a specific device (client) from a Wi-Fi access point.
- **Wireless Scanner**: Discovers nearby clients and access points using passive sniffing.

---

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/panagiotisfassaris/silkmoth.git
    cd silkmoth
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

    > Make sure `scapy` is installed. Run `pip install scapy` if needed.

---

## Usage

> ⚠️ Requires root privileges and a Wi-Fi adapter that supports monitor mode (Linux only).

```bash
sudo python3 deauth.py <target_mac> <router_mac> [-i interface] [-p packet_count] [--auto-monitor] [--scan] [--interactive]
```

### Arguments
- **<target_mac>**: MAC address of the victim device to disconnect.
- **<router_mac>**: MAC address of the access point.
- **-i, --interface**: Network interface to use (default: wlan0).
- **-p, --packets**: Number of deauth packets to send (default: 1000).
- **--auto-monitor**: Automatically switch the interface to monitor mode using native Linux commands (ip and iw).
- **--scan**: Passive scan for clients and access points in range.
- **--interactive**: Scan and let you choose target and AP from the list.

### Usage Examples

```bash
# Deauth a device
sudo python3 deauth.py AA:BB:CC:DD:EE:FF 11:22:33:44:55:66 -i wlan0 --auto-monitor -p 500

# Scan for APs and clients
sudo python3 deauth.py --scan -i wlan0 --auto-monitor

# Interactive selection of target and AP
sudo python3 deauth.py --interactive -i wlan0 --auto-monitor
```

## Features

- **Deauthentication Attack**: Conducts controlled deauth attacks to test client reconnection and simulate wireless DoS.
- **Passive Scanner**: Detects active APs and clients via passive sniffing using Scapy.
- **Interactive Mode**: Guides the user through selecting targets from scanned results.
- **Auto Monitor Mode**: Enables monitor mode automatically (Linux-only).
- **Cross-platform Compatibility**: Windows support for scanning; Linux required for full features.
- **Lightweight & CLI-based**: Minimal dependencies, clean CLI interface.
- **Multithreaded Architecture** (planned): Improve performance during scanning.

## Notes

- The deauth tool only works on systems with Wi-Fi interfaces that support monitor mode and packet injection.
- Use `--scan` to list nearby clients and APs. Use `--interactive` to pick from results without manually inputting MACs.
- On Linux, use `--auto-monitor` to set your interface to monitor mode. Manual mode setup instructions are no longer required.

### On Windows

Monitor mode and packet injection are not supported natively in Windows. As a result, the deauth functionality **does not work on Windows**. However, scanning and discovery features may work with limited functionality. Use a Linux environment for full capabilities.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.
