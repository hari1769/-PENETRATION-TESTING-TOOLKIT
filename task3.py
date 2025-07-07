import socket
import requests
from bs4 import BeautifulSoup


def port_scanner(target, ports=[21, 22, 23, 80, 443, 8080]):
    print(f"\n[+] Scanning ports on {target}")
    for port in ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.connect((target, port))
                print(f"[OPEN] Port {port}")
        except:
            pass


def banner_grabber(target, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            s.connect((target, port))
            banner = s.recv(1024).decode(errors='ignore').strip()
            print(f"[+] Banner on port {port}: {banner}")
    except Exception as e:
        print(f"[-] Could not grab banner on port {port}: {e}")


def brute_force_login(url, username_field, password_field, user_list, pass_list):
    print(f"\n[+] Starting brute-force on {url}")
    headers = {'User-Agent': 'Mozilla/5.0'}
    for user in user_list:
        for password in pass_list:
            data = {
                username_field: user.strip(),
                password_field: password.strip()
            }
            try:
                response = requests.post(url, data=data, headers=headers, timeout=5)
                if "invalid" not in response.text.lower():
                    print(f"[!] Valid credentials found → {user}:{password}")
                    return
            except requests.exceptions.RequestException as e:
                print(f"[-] Request failed for {user}:{password} → {e}")
    print("[-] Brute-force complete. No valid credentials found.")


def dir_fuzz(base_url, wordlist):
    print(f"\n[+] Starting directory fuzz on {base_url}")
    headers = {'User-Agent': 'Mozilla/5.0'}
    for word in wordlist:
        url = f"{base_url.rstrip('/')}/{word.strip()}"
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                print(f"[FOUND] {url}")
        except requests.exceptions.RequestException as e:
            print(f"[-] Error accessing {url} → {e}")


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
        try:
            port = int(input("Port: "))
            banner_grabber(target, port)
        except ValueError:
            print("[-] Invalid port number.")

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

    elif choice == '0':
        print("Exiting...")

    else:
        print("[-] Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()
