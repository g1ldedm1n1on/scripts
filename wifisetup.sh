!#/bin/bash
ifconfig wlan0 down
ifconfig wlan1 down
macchanger -r wlan0
macchanger -r wlan1
ifconfig wlan0 up
ifconfig wlan1 up
airmon-ng start wlan1
