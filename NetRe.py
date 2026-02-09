import subprocess
import platform
import json
import csv
import argparse
import sys
import os

# ANSI Color Codes for UX enhancement (Zero-dependency)
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_banner():
    banner = f"""{Colors.OKBLUE}{Colors.BOLD}
    ========================================
       _   _      _   ____
      | \\ | | ___| |_|  _ \\ ___
      |  \\| |/ _ \\ __| |_) / _ \\
      | |\\  |  __/ |_|  _ <  __/
      |_| \\_|\\___|\\__|_| \\_\\___|
    
      Cross-Platform Wi-Fi Retriever
    ========================================{Colors.ENDC}
    """
    print(banner)

def get_windows_wifi():
    networks = []
    try:
        data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors='ignore').split('\n')
        profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
        for i in profiles:
            try:
                results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8', errors='ignore').split('\n')
                password = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
                networks.append({"ssid": i, "password": password[0] if password else ""})
            except subprocess.CalledProcessError:
                networks.append({"ssid": i, "password": "Error retrieving"})
    except Exception as e:
        print(f"{Colors.FAIL}Error on Windows: {e}{Colors.ENDC}")
    return networks

def get_macos_wifi(interface='en0'):
    networks = []
    try:
        output = subprocess.check_output(['networksetup', '-listpreferredwirelessnetworks', interface]).decode('utf-8').split('\n')
        profiles = [line.strip() for line in output[1:] if line.strip()]
        for ssid in profiles:
            try:
                # Triggers keychain prompt
                cmd = f'security find-generic-password -D "AirPort network password" -a "{ssid}" -gw'
                password = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
                networks.append({"ssid": ssid, "password": password})
            except subprocess.CalledProcessError:
                networks.append({"ssid": ssid, "password": "Permission denied/Not found"})
    except Exception as e:
        print(f"{Colors.FAIL}Error on macOS: {e}{Colors.ENDC}")
    return networks

def get_linux_wifi():
    networks = []
    try:
        output = subprocess.check_output(['nmcli', '-t', '-f', 'name', 'connection', 'show']).decode('utf-8').split('\n')
        profiles = [line.strip() for line in output if line.strip()]
        for ssid in profiles:
            try:
                cmd = f'nmcli -s -g 802-11-wireless-security.psk connection show "{ssid}"'
                password = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
                networks.append({"ssid": ssid, "password": password})
            except subprocess.CalledProcessError:
                networks.append({"ssid": ssid, "password": "Requires sudo/Not found"})
    except Exception as e:
        print(f"{Colors.FAIL}Error on Linux: {e}{Colors.ENDC}")
    return networks

def export_data(data, format, filename):
    try:
        if format == 'json':
            full_path = f"{filename}.json"
            with open(full_path, 'w') as f:
                json.dump(data, f, indent=4)
        elif format == 'csv':
            full_path = f"{filename}.csv"
            keys = data[0].keys() if data else []
            with open(full_path, 'w', newline='') as f:
                dict_writer = csv.DictWriter(f, fieldnames=keys)
                dict_writer.writeheader()
                dict_writer.writerows(data)
        print(f"\n{Colors.OKGREEN}[+] Successfully exported to {full_path}{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.FAIL}[!] Export failed: {e}{Colors.ENDC}")

def main():
    parser = argparse.ArgumentParser(description="NetRe: Secure and Stylish Wi-Fi Password Retriever")
    parser.add_argument("-m", "--mask", action="store_true", help="Hide passwords in the terminal output")
    parser.add_argument("-e", "--export", choices=['json', 'csv'], help="Export results to a file (JSON or CSV)")
    parser.add_argument("-o", "--output", default="wifi_passwords", help="Custom name for the output file")
    parser.add_argument("-i", "--interface", default="en0", help="Network interface (macOS only, default: en0)")
    parser.add_argument("-s", "--silent", action="store_true", help="Skip the welcome banner")
    
    args = parser.parse_args()
    
    if not args.silent:
        print_banner()
    
    os_type = platform.system()
    print(f"{Colors.BOLD}System detected:{Colors.ENDC} {Colors.OKBLUE}{os_type}{Colors.ENDC}")
    print(f"{Colors.BOLD}Action:{Colors.ENDC} Retrieving stored Wi-Fi profiles...\n")
    
    if os_type == "Windows":
        wifi_data = get_windows_wifi()
    elif os_type == "Darwin":
        wifi_data = get_macos_wifi(args.interface)
    elif os_type == "Linux":
        wifi_data = get_linux_wifi()
    else:
        print(f"{Colors.FAIL}[!] OS {os_type} is not supported.{Colors.ENDC}")
        return

    # Results Table
    header = f"{'SSID':<30} | {'Password'}"
    print(f"{Colors.BOLD}{header}{Colors.ENDC}")
    print("-" * 50)
    
    for entry in wifi_data:
        ssid = entry['ssid']
        raw_pass = entry['password']
        
        # Color coding passwords for readability
        if "Error" in raw_pass or "Denied" in raw_pass or "Requires" in raw_pass:
            pass_colored = f"{Colors.FAIL}{raw_pass}{Colors.ENDC}"
        elif not raw_pass:
            pass_colored = f"{Colors.WARNING}None{Colors.ENDC}"
        else:
            pass_colored = f"{Colors.OKGREEN}{'********' if args.mask else raw_pass}{Colors.ENDC}"
            
        print(f"{ssid:<30} | {pass_colored}")

    if args.export:
        export_data(wifi_data, args.export, args.output)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}[!] Operation cancelled by user.{Colors.ENDC}")
        sys.exit(0)
