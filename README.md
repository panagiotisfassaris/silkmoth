# Silkmoth - Deauth Tool & Network Scanner

**Silkmoth** is a lightweight network scanning and deauthentication tool designed for system administrators and security enthusiasts. This tool allows for the identification of active hosts on a network and facilitates the execution of Wi-Fi deauthentication attacks. It is ideal for performing network assessments, troubleshooting, and security auditing.

## Table of Contents

- [About](#about)
- [Installation](#installation)
- [Usage](#usage)
  - [Network Scanner](#network-scanner)
  - [Deauthentication Attack](#deauthentication-attack)
- [Features](#features)
- [Notes](#notes)
- [Disclaimer](#disclaimer)

## About

**Silkmoth** offers two primary functionalities:
1. **Network Scanner**: Silkmoth scans the specified subnet to identify active devices by sending ICMP packets and analyzing their responses.
2. **Deauthentication Attack**: Sends deauthentication packets to a target Wi-Fi device, effectively disconnecting it from the network.

## Installation

To install and run **Silkmoth**, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/silkmoth.git
    cd silkmoth
    ```

2. **Install dependencies**:
    Ensure you have Python 3.x installed on your system. The `scapy` library is required for deauthentication.
    ```bash
    pip install -requirements
    ```

## Usage

### Network Scanner

The network scanner scans the specified subnet to find active devices. It listens for ICMP replies and identifies hosts that are up.

**Running the Scanner**:
```bash
python scanner.py <your_ip_address>
```

Replace <your_ip_address> with the IP address of the machine running the scanner. 

Example:

```bash
python scanner.py 192.168.1.95
```

By default, the scanner will scan the 192.168.1.0/24 subnet for active hosts. You can modify the subnet variable in the script to scan a different range.

### Deauthentication Attack

Silkmoth also includes the capability to perform deauthentication attacks, which can disconnect a target from the Wi-Fi network.

**Running the Deauth Tool**:
To execute the deauthentication attack, use the following command:
```bash
python deauth.py <target_mac> <router_mac> [-i interface] [-p packet_count]
```

- **<target_mac>**: The MAC address of the device you want to disconnect (victim).
- **<router_mac>**: The MAC address of the router (Wi-Fi access point).
- **-i**: Network interface (default is wlan0mon).
- **-p**: Number of deauth packets to send (default: 1000).

Example:

```bash
python deauth.py AA:BB:CC:DD:EE:FF 11:22:33:44:55:66 -i wlan0mon -p 500
```

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
