#!/usr/bin/env python3

# Script created by s3B-a
# =======================
#  TORmap Console v1.0.0
# =======================

import cmd
import logging
import os
import shlex
import subprocess
import sys

logging.basicConfig(
	level=logging.INFO,
	format='\033[1;36m[TORmap]\033[0m %(message)s',
)
logger = logging.getLogger('TORmap')

# Checks for root perms
def checkRoot():
	if os.geteuid() != 0:
		print("Script must be run as root!")
		sys.exit(1)

# Class that contains the console
class TORmapConsole(cmd.Cmd):
	prompt = "TORmap > "

	# variables
	def __init__(self):
		super().__init__()
		self.target = ""
		self.flags = []
		self.allowed_flags = {
			"-sS", "-sV", "-p-", "-Pn", "-O", "-n", "-f"
		}
		self.valuesFlag = {
			"-p", "--spoof-mac", "--data-length", "--max-retries"
		}

	# on input "set target" or "set flags"
	def do_set(self, args):
		parts = shlex.split(args)
		if len(parts) < 2:
			logger.warning("Usage: set [target|flags] <value>")
			return

		key, value = parts[0], " ".join(parts[1:])
		if key == "target":
			self.target = value
			logger.info(f"Target set to: {self.target}")

		elif key == "flags":
			rawFlags = shlex.split(value)
			validFlags = []
			i = 0
			while i < len(rawFlags):
				flag = rawFlags[i]

				if flag in self.valuesFlag:
					if i + 1 < len(rawFlags):
						param = rawFlags[i + 1]

						if flag == "-p-" or param == "-":
							validFlags.append("-p-")
						else:
							validFlags.extend([flag, param])
						i += 2
						continue
					else:
						logger.warning(f"Missing value for {flag}")
						break

				elif flag in self.allowed_flags:
					validFlags.append(flag)
					i += 1
					continue

				else:
					logger.warning(f"Ignoring unrecognized flag: {flag}")
					i += 1

			self.flags = validFlags
			logger.info(f"Flags set to: {' '.join(self.flags)}")
		else:
			logger.warning("Unknown key. Use 'target' or 'flags'")

	# on input "show"
	def do_show(self, args):
		logger.info("Current settings:")
		logger.info(f"Target: {self.target}")
		logger.info(f"Flags: {' '.join(self.flags)}")

	# on input "run"
	def do_run(self, args):
		if not self.target:
			logger.error("Target not set. Use: set target <IP/host>")
			return
		command = ["proxychains", "nmap"] + self.flags + ["-D 185.228.168.9,23.67.253.113,8.26.56.26,ME,138.197.0.0", "-vvv"] + [self.target]
		logger.info(f"Running: {' '.join(command)}")
		try:
			subprocess.run(command)
		except Exception as e:
			logger.error(f"Execution failed: {e}")

	# on input "exit"
	def do_exit(self, args):
		logger.info("Exiting...")
		return True

	# on input "help" or "?"
	def do_help(self, args):
		helpTxt = """
[console help]
Available Commands:

	set target <ip>		Set the target IP or Host
	set flags <options>	Set the Nmap flags
	show			Show the current settings
	run			Run Nmap through proxychains
	exit			Exit the console
	help			Show this message


Flags Available (Use with: set flags <flags>):

	Scan Tags:
	  -sS			TCP/SYN (Stealth) scan
	  -sV			Service Version Detection
	  -p			Specified Ports to scan

	Host Discovery:
	  -Pn			Treat hosts as online (skip ping)

	Agressiveness:
	  -O			Enable OS detection
	  -n			skip DNS resolution
	  --max-retries <n>	Number of times nmap will retry sending a probe

	Bypass:
	  -f			Fragment Packets
	  --spoof-mac		Spoofs mac address (Cisco, Apple, Dell, etc.)
	  --data-length <n>	Append random data to packets

	Note: you can combine flags by typing 'set flags -sS -Pn -n'

"""
		logger.info(helpTxt.strip())


# Confirms Launch of terminal
def launch():
	logger.info("Welcome to the TORmap console!")
	logger.info("Map a network like Anon")
	shell = TORmapConsole()
	shell.cmdloop()

if __name__ == "__main__":
	if len(sys.argv) > 1 and sys.argv[1] == "launch":
		launch()
	else:
		logger.info("Usage: ./console.py launch")

