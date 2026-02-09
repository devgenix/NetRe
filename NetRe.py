import subprocess
import platform

def process_windows():
    try:
        data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')
        profiles = [i.split(":") [1][1:-1] for i in data if "All User Profile" in i]
        for i in profiles:
            results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8').split('\n')
            results = [b.split(":") [1][1:-1] for b in results if "Key Content" in b]
            try:
                print ("{:<30}|  {:<}".format(i, results[0]))
            except IndexError:
                print("{:<30}|  {:<}".format(i, "No password found"))
    except Exception as e:
        print(f"Error on Windows: {e}")

def process_macos():
    try:
        # Get list of Wi-Fi services
        networks = subprocess.check_output(['networksetup', '-listpreferredwirelessnetworks', 'en0']).decode('utf-8').split('\n')
        # Skip the first line header
        profiles = [line.strip() for line in networks[1:] if line.strip()]
        
        print("{:<30}|  {:<}".format("SSID", "Password"))
        print("-" * 45)
        
        for ssid in profiles:
            try:
                # Note: This will trigger a keychain prompt on macOS
                cmd = f'security find-generic-password -D "AirPort network password" -a "{ssid}" -gw'
                password = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
                print("{:<30}|  {:<}".format(ssid, password))
            except subprocess.CalledProcessError:
                print("{:<30}|  {:<}".format(ssid, "Permission denied or Not found"))
    except Exception as e:
        print(f"Error on macOS: {e}")

def main():
    os_type = platform.system()
    print(f"Detected OS: {os_type}")
    
    if os_type == "Windows":
        process_windows()
    elif os_type == "Darwin":
        process_macos()
    else:
        print(f"OS {os_type} is not supported yet.")

if __name__ == "__main__":
    input("Press Enter to start retrieving passwords...")
    main()
