import socket
import requests
from bs4 import BeautifulSoup

# ------------------------------
# 1. Port Scanner
# ------------------------------
def port_scanner(target, ports=[21, 22, 23, 80, 443, 8080]):
    print(f"\n[+] Scanning ports on {target}")
    for port in ports:
        try:
            with socket.socket() as s:
                s.settimeout(1)
                s.connect((target, port))
                print(f"[OPEN] Port {port}")
        except:
            pass

# ------------------------------
# 2. Banner Grabber
# ------------------------------
def banner_grabber(target, port):
    try:
        with socket.socket() as s:
            s.settimeout(2)
            s.connect((target, port))
            banner = s.recv(1024).decode().strip()
            print(f"[+] Banner on port {port}: {banner}")
    except Exception as e:
        print(f"[-] Could not grab banner on port {port}: {e}")

# ------------------------------
# 3. Web Login Brute Forcer
# ------------------------------
def brute_force_login(url, username_field, password_field, user_list, pass_list):
    print(f"\n[+] Starting brute-force on {url}")
    for user in user_list:
        for password in pass_list:
            data = {username_field: user, password_field: password}
            response = requests.post(url, data=data)
            if "invalid" not in response.text.lower():
                print(f"[!] Valid credentials found → {user}:{password}")
                return
    print("[-] Brute-force complete. No valid credentials found.")

# ------------------------------
# 4. Directory Fuzzer
# ------------------------------
def dir_fuzz(base_url, wordlist):
    print(f"\n[+] Starting directory fuzz on {base_url}")
    for word in wordlist:
        url = f"{base_url.rstrip('/')}/{word.strip()}"
        response = requests.get(url)
        if response.status_code == 200:
            print(f"[FOUND] {url}")

# ------------------------------
# MAIN INTERFACE
# ------------------------------
def main():
    print("\n=== Penetration Testing Toolkit ===")
    print("1. Port Scanner")
    print("2. Banner Grabbing")
    print("3. Brute-Force Login")
    print("4. Directory Fuzzer")
    print("0. Exit")
    choice = input("Select an option: ")

    if choice == '1':
        target = input("Target IP/Host: ")
        port_scanner(target)

    elif choice == '2':
        target = input("Target IP/Host: ")
        port = int(input("Port: "))
        banner_grabber(target, port)

    elif choice == '3':
        url = input("Login URL: ")
        user_field = input("Username field name: ")
        pass_field = input("Password field name: ")
        users = input("Comma-separated usernames: ").split(',')
        passwords = input("Comma-separated passwords: ").split(',')
        brute_force_login(url, user_field, pass_field, users, passwords)

    elif choice == '4':
        url = input("Base URL (e.g., http://example.com): ")
        words = input("Comma-separated directory names to try: ").split(',')
        dir_fuzz(url, words)

    else:
        print("Exiting...")

if __name__ == "__main__":
    main(