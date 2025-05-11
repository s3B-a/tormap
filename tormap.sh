#!/bin/bash

#Script created by s3B-a
# =======================
#      TORmap v1.0.0
# =======================


#Color codes

GREEN="\e[32m"
CYAN="\e[36m"
ORANGE="\e[38;2;255;140;0m"
YELLOW="\e[33m"
RED="\e[31m"
RES="\e[0m"
BOLD="\e[1m"

printAsciiLogo() {
	echo -e "${ORANGE} +-----------------------------------------------------+"
	echo -e "${ORANGE} |████████╗ ██████╗ ██████╗ ███╗   ███╗ █████╗ ██████╗ |"
	echo -e "${ORANGE} |╚══██╔══╝██╔═══██╗██╔══██╗████╗ ████║██╔══██╗██╔══██╗|"
	echo -e "${ORANGE} |   ██║   ██║   ██║██████╔╝██╔████╔██║███████║██████╔╝|"
	echo -e "${ORANGE} |   ██║   ██║   ██║██╔══██╗██║╚██╔╝██║██╔══██║██╔═══╝ |"
	echo -e "${ORANGE} |   ██║   ╚██████╔╝██║  ██║██║ ╚═╝ ██║██║  ██║██║     |"
	echo -e "${ORANGE} |   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝     |"
	echo -e "${ORANGE} +----------------------(v1.0.0)-----------------------+${RES}"
}

log() {
	local color=$1
	local message=$2
	echo -e "${color}${message}${RES}"
}

#Asks for root perms
if [ "$EUID" -ne 0 ]; then
	echo "Run as root"
	exec sudo "$0" "$@"
	exit
fi

#Installs Dependancies
log "${YELLOW}" "Checking if tor, privoxy and proxychains are installed..."
apt install tor
apt install privoxy
apt install proxychains

#Checks if the last line of proxychains.conf contains necessary parameters
lastLineChains=$(tail -n 1 "/etc/proxychains.conf")
if [[ $lastLineChains != *'socks5 127.0.0.1 9050'* ]]; then
	echo "socks5 127.0.0.1 9050" >> /etc/proxychains.conf
fi

#Quickly deactivates tor if it was previously running
if systemctl is-active --quiet tor@default; then
	log "${YELLOW}" "Exiting tor to reset connection..."
	systemctl stop --quiet tor@default
fi

#Checks if required services are running
log "${YELLOW}" "Checking tor status"
if ! systemctl is-active --quiet tor@default; then
	log "${YELLOW}" "tor isn't running, launching..."
	systemctl start --quiet tor@default
else
	log "${GREEN}" "Tor is running!"
fi

printAsciiLogo

#Lauches TORmap console
log "${GREEN}" "Launching console..."
if [ -f "./console.py" ]; then
	chmod +x console.py
	./console.py launch
fi
