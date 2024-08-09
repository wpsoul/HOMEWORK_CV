import subprocess

def connect_to_wifi(ssid, password):
    command = f'networksetup -setairportnetwork en0 "{ssid}" "{password}"'
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    if result.returncode == 0:
        print(f"Connected to {ssid}")
    else:
        print(f"Failed to connect to {ssid}")

if __name__ == "__main__":
    ssid = "ASUS"
    password = "12345678admin"  # Tello drones typically don't require a password
    connect_to_wifi(ssid, password)