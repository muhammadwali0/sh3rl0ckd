import os
import platform
import concurrent.futures

def ping_sweep():
    GREEN = "\033[38;5;46m"
    RESET = "\033[0m"

    network = input("\nEnter the network (e.g., 192.168.1.0/24): ").strip()

    if not network:
        print("[-] Error: Network cannot be empty.")
        return

    try:
        base_ip = network.split('/')[0]
        base_parts = base_ip.split('.')
        if len(base_parts) != 4:
            raise ValueError
        
        # Only supports /24 networks for now (can expand later)
        ip_base = '.'.join(base_parts[:3])
    except:
        print("[-] Invalid network format.")
        return

    print(f"\n{GREEN}Starting Ping Sweep on {ip_base}.0/24 ...{RESET}\n")

    alive_hosts = []

    def ping_host(ip):
        # Cross-platform ping command
        param = "-n" if platform.system().lower() == "windows" else "-c"
        command = f"ping {param} 1 -W 1 {ip} > /dev/null 2>&1"

        if os.system(command) == 0:
            print(f"[+] Host Alive: {ip}")
            alive_hosts.append(ip)

    ip_range = [f"{ip_base}.{i}" for i in range(1, 255)]

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(ping_host, ip_range)

    print(f"\n{GREEN}Total live hosts found: {len(alive_hosts)}{RESET}\n")

    if alive_hosts:
        print("\nLive hosts list:")
        for host in alive_hosts:
            print(f" -> {host}")
    else:
        print("\nNo live hosts detected.")

    print(f"\n{GREEN}Ping sweep completed!{RESET}\n")
