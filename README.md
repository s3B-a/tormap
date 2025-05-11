# tormap
## Description
Less noisy Nmap using ProxyChains and Tor
"Map a network like Anon"

### What does it do?
- Automatically sets up the tor service, configures proxychains to work with tor, as well as allows the use to access Nmap with specific restrictions for available flags
- In short, a more anonymous Nmap

## How to Use
### Download and Running
- Download the repo ```git clone https://github.com/s3B-a/tormap.git```
- Once downloaded, enter the directory
- Enter ```chmod +x tormap.sh``` if ```tormap.sh``` is not executable
- Run the program ```./tormap.sh```

### How to use the Console
- Once ```tormap.sh``` loads, you will be greated with a welcome message, from there you may type ```help``` or ```?``` to access the manual
- use ```set target``` to specify you attacker IP
- use ```set flags``` to specify your desired Nmap flags (note that only specific flags are permitted, other flags that are available in Nmap may result in leaks, hence the restrictions)
- use ```show``` to see the current configuration
- use ```run``` to run Nmap through ProxyChains
