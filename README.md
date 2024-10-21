# Silkmoth - Network Scanner and Deauth Tool

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

2. **Install dependencies** (if required):
    Ensure you have Python 3.x installed on your system. The `scapy` library is required for deauthentication.
    You can install it using pip:
    ```bash
    pip install scapy
    ```

## Usage

### Network Scanner

The network scanner scans the specified subnet to find active devices. It listens for ICMP replies and identifies hosts that are up.

**Running the Scanner**:
```bash
python scanner.py <your_ip_address>
