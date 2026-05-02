
# 🔐 WiFi Tool Password

Tool to recover saved WiFi passwords on Linux and Windows systems.

## ⚠️ Legal Disclaimer
**Use only on your own networks or with explicit permission. Unauthorized access to WiFi networks is illegal.**

## 📋 Requirements

### Windows
- Run as **Administrator**
- Windows 7/8/10/11

### Linux
- Run with **sudo**
- NetworkManager (default on Ubuntu, Debian, Fedora)

## 🚀 Installation

```bash
git clone https://github.com/Falconmx1/Wifi-Tool-Password.git
cd Wifi-Tool-Password

💻 Usage
Windows (as Administrator)
cmd

python src/wifi_tool.py

Linux (with sudo)
bash

sudo python3 src/wifi_tool.py

JSON output
bash

python src/wifi_tool.py --output json

📝 Example Output
text

==================================================
🔐 WiFi Tool Password - Security Tool
⚠️  Use only on your own networks
==================================================

1. SSID: MyHomeNetwork
   Password: MySecurePass123
----------------------------------------
2. SSID: GuestWiFi
   Password: GuestPassword456

🔧 How it works

    Windows: Uses netsh wlan show profiles (built-in Windows command)

    Linux: Reads from /etc/NetworkManager/system-connections/

🛡️ Privacy

This tool only accesses files and commands that store YOUR saved passwords. No data is sent anywhere.
