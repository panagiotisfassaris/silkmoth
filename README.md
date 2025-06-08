# Silkmoth - Deauth Tool & Network Scanner

![Silkmoth Sniffer's Logo](logo.jpg)

**Silkmoth** is a lightweight Wi-Fi deauthentication tool built for system administrators and cybersecurity enthusiasts. It allows you to execute controlled deauth attacks to test the resilience of wireless networks. This is ideal for Wi-Fi security assessments, penetration testing, or educational purposes.

## Table of Contents

- [About](#about)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Notes](#notes)
- [License](#license)

---

## About

**Silkmoth** provides one main capability:

- **Deauthentication Attack**: Sends 802.11 deauthentication frames to forcibly disconnect a specific device (client) from a Wi-Fi access point. Useful for testing client reconnection behavior or simulating DoS in security labs.

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

> ⚠️ Requires root privileges and a Wi-Fi adapter that supports monitor mode.

```bash
sudo python3 deauth.py <target_mac> <router_mac> [-i interface] [-p packet_count] [--auto-monitor]
```

### Arguments
- **<target_mac>**: MAC address of the victim device to disconnect.
- **<router_mac>**: MAC address of the access point.
- **-i, --interface**: Network interface to use (default: wlan0).
- **-p, --packets**: Number of deauth packets to send (default: 1000).
- **--auto-monitor**: Automatically switch the interface to monitor mode using native Linux commands (ip and iw).

## Features

- **Deauthentication Attack**: Includes functionality for conducting controlled deauthentication attacks in Wi-Fi environments, allowing security professionals to test the robustness of wireless networks. The tool crafts and sends deauth packets, targeting specific devices (clients) and routers to simulate disconnections and assess how vulnerable a network might be to such an attack.
- **Active Host Discovery**: Efficiently scans a specified IP range (subnet) to identify live hosts by sending ICMP packets and processing their responses.
- **Raw Socket Support**: Utilizes raw sockets to capture and analyze network packets, allowing for low-level access to network protocols.
- **Protocol Analysis**: Supports analysis of multiple protocols, including ICMP, TCP, and potentially UDP, enabling comprehensive monitoring of network activity.
- **Multithreading**: Implements multithreading to send UDP packets concurrently, improving efficiency and speed during the scanning process.
- **User-Friendly Output**: Provides real-time output of detected hosts, including the IP address of active devices within the subnet, enhancing visibility into network status.

## Notes

- For the deauth tool to work, your network interface must support monitor mode and it should be enabled (usually set to `wlan0mon`). You can use tools like `airmon-ng` to set your interface to monitor mode. 

### Enabling Monitor Mode

To enable monitor mode using `airmon-ng`, follow these steps:

1. Open a terminal.
2. Start `airmon-ng` to check your wireless interfaces:

    ```bash
    airmon-ng
    ```

3. Identify the wireless interface you want to set to monitor mode (e.g., `wlan0`).
4. Enable monitor mode on that interface:

    ```bash
    sudo airmon-ng start wlan0
    ```

5. Your interface will typically be renamed to `wlan0mon`. You can verify this by running:

    ```bash
    airmon-ng
    ```

Once your interface is in monitor mode, you can use the deauthentication tool in Silkmoth.

- On Windows, ensure that you are running the scripts with administrator privileges to access raw sockets.
