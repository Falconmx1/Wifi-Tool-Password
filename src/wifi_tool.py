#!/usr/bin/env python3
"""
Wifi Tool Password - Tool to recover saved WiFi credentials
For Linux and Windows systems
Educational purpose only - Use only on your own networks
"""

import os
import sys
import subprocess
import platform
import argparse

class WifiTool:
    def __init__(self):
        self.system = platform.system()
        
    def run_as_admin_windows(self):
        """Elevate privileges on Windows"""
        if self.system == "Windows":
            try:
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin()
            except:
                return False
        return True
    
    def get_windows_passwords(self):
        """Extract saved WiFi passwords on Windows"""
        try:
            # Get all profiles
            profiles = subprocess.check_output(
                "netsh wlan show profiles", 
                shell=True, 
                text=True
            )
            
            # Parse profile names
            wifi_profiles = []
            for line in profiles.split('\n'):
                if "All User Profile" in line:
                    profile_name = line.split(":")[1].strip()
                    wifi_profiles.append(profile_name)
            
            # Get passwords
            results = []
            for profile in wifi_profiles:
                try:
                    info = subprocess.check_output(
                        f'netsh wlan show profile "{profile}" key=clear',
                        shell=True,
                        text=True
                    )
                    
                    password = None
                    for line in info.split('\n'):
                        if "Key Content" in line:
                            password = line.split(":")[1].strip()
                            break
                    
                    results.append({
                        "ssid": profile,
                        "password": password if password else "Not found"
                    })
                except:
                    results.append({
                        "ssid": profile,
                        "password": "Error retrieving"
                    })
            
            return results
            
        except Exception as e:
            return f"Error: {e}"
    
    def get_linux_passwords(self):
        """Extract saved WiFi passwords on Linux (NetworkManager)"""
        connections_path = "/etc/NetworkManager/system-connections/"
        
        if not os.path.exists(connections_path):
            return "NetworkManager connections not found"
        
        try:
            results = []
            # Need sudo for this
            if os.geteuid() != 0:
                return "Run with sudo on Linux"
            
            for file in os.listdir(connections_path):
                if os.path.isfile(os.path.join(connections_path, file)):
                    with open(os.path.join(connections_path, file), 'r') as f:
                        content = f.read()
                        
                        ssid = None
                        password = None
                        
                        for line in content.split('\n'):
                            if 'ssid=' in line:
                                ssid = line.split('=')[1].strip()
                            if 'psk=' in line:
                                password = line.split('=')[1].strip()
                        
                        if ssid:
                            results.append({
                                "ssid": ssid,
                                "password": password if password else "Not found (open network)"
                            })
            
            return results
            
        except Exception as e:
            return f"Error: {e}"
    
    def run(self):
        """Main execution"""
        parser = argparse.ArgumentParser(
            description="Recover saved WiFi passwords (own networks only)"
        )
        parser.add_argument(
            "--output", "-o", 
            choices=["text", "json"], 
            default="text",
            help="Output format"
        )
        
        args = parser.parse_args()
        
        print("\n" + "="*50)
        print("🔐 WiFi Tool Password - Security Tool")
        print("⚠️  Use only on your own networks")
        print("="*50 + "\n")
        
        if self.system == "Windows":
            if not self.run_as_admin_windows():
                print("❌ Please run as Administrator on Windows")
                print("   Right-click -> Run as Administrator")
                return
            
            print("📡 Scanning Windows saved WiFi profiles...\n")
            results = self.get_windows_passwords()
            
        elif self.system == "Linux":
            if os.geteuid() != 0:
                print("❌ Please run with sudo: sudo python3 wifi_tool.py")
                return
            
            print("📡 Scanning Linux (NetworkManager) saved WiFi profiles...\n")
            results = self.get_linux_passwords()
            
        else:
            print(f"❌ Unsupported OS: {self.system}")
            return
        
        # Display results
        if isinstance(results, str):
            print(results)
            return
        
        if args.output == "json":
            import json
            print(json.dumps(results, indent=2))
        else:
            for i, wifi in enumerate(results, 1):
                print(f"{i}. SSID: {wifi['ssid']}")
                print(f"   Password: {wifi['password']}")
                print("-"*40)
        
        print(f"\n✅ Found {len(results)} saved WiFi networks")

if __name__ == "__main__":
    tool = WifiTool()
    tool.run()
