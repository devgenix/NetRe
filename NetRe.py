import subprocess
import platform
import json
import csv
import argparse
import sys
import os

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
        print(f"Error on Windows: {e}")
    return networks

def get_macos_wifi():
    networks = []
    try:
        # Get preferred networks
        output = subprocess.check_output(['networksetup', '-listpreferredwirelessnetworks', 'en0']).decode('utf-8').split('\n')
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
        print(f"Error on macOS: {e}")
    return networks

def get_linux_wifi():
    networks = []
    try:
        # Using nmcli (NetworkManager)
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
        print(f"Error on Linux: {e}")
    return networks

def export_data(data, format, filename):
    if format == 'json':
        with open(f"{filename}.json", 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Exported to {filename}.json")
    elif format == 'csv':
        keys = data[0].keys() if data else []
        with open(f"{filename}.csv", 'w', newline='') as f:
            dict_writer = csv.DictWriter(f, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)
        print(f"Exported to {filename}.csv")

def main():
    parser = argparse.ArgumentParser(description="NetRe: Cross-platform Wi-Fi Password Retriever")
    parser.add_argument("-m", "--mask", action="store_true", help="Mask passwords in terminal output")
    parser.add_argument("-e", "--export", choices=['json', 'csv'], help="Export format")
    parser.add_argument("-o", "--output", default="wifi_passwords", help="Output filename (without extension)")
    
    args = parser.parse_args()
    
    os_type = platform.system()
    print(f"--- NetRe Wi-Fi Retriever ---")
    print(f"Detected OS: {os_type}\n")
    
    if os_type == "Windows":
        wifi_data = get_windows_wifi()
    elif os_type == "Darwin":
        wifi_data = get_macos_wifi()
    elif os_type == "Linux":
        wifi_data = get_linux_wifi()
    else:
        print(f"OS {os_type} not supported.")
        return

    # Terminal Output
    print(f"{'SSID':<30} | {'Password'}")
    print("-" * 50)
    for entry in wifi_data:
        display_pass = "********" if args.mask else entry['password']
        print(f"{entry['ssid']:<30} | {display_pass}")

    # Export
    if args.export:
        export_data(wifi_data, args.export, args.output)

if __name__ == "__main__":
    main()
