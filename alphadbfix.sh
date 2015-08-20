#!/bin/bash
ifconfig wlan1 down
iw reg set BO
ifconfig wlan1 up
