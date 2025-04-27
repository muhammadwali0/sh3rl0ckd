import subprocess
import ipaddress
import concurrent.futures
from scapy.all import ARP, Ether, srp  # Required for ARP scanning

# Function to ping a host and check if it's alive
def ping_host(ip, param):
    try:
        output = subprocess.check_output(
            ["ping", param, "1", "-W", "1", str(ip)],
            stderr=subprocess.DEVNULL
        )
        return ip
    except subprocess.CalledProcessError:
        return None


# Function to perform Ping Sweep
def ping_sweep():
    network = input("Enter the target subnet (e.g., 192.168.0.0/24): ").strip()

    try:
        ip_network = ipaddress.IPv4Network(network, strict=False)
    except ValueError:
        print("[-] Invalid subnet. Please enter a valid subnet.")
        return

    print(f"\nStarting Ping Sweep on {network}...\n")

    alive_hosts = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(lambda ip: ping_host(ip, "-c"), ip_network.hosts())

    # Collect live hosts
    for result in results:
        if result:
            alive_hosts.append(result)
            print(f"Host alive: {result}")

    print(f"\nLive hosts found:")
    for host in alive_hosts:
        print(f"  {host}")

    # Call ARP Scan after Ping Sweep
    arp_scan(alive_hosts)

# Function to perform ARP Scan
def arp_scan(alive_hosts):
    print("\nStarting ARP Scan...\n")

    # Prepare the ARP request
    arp_request = ARP(pdst="192.168.0.0/24")  # You can replace with the subnet discovered from the ping sweep
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")

    # Combine the ARP request and broadcast frame
    arp_request_broadcast = broadcast/arp_request

    # Send the packet and capture the response
    result = srp(arp_request_broadcast, timeout=3, verbose=False)[0]

    # Collect and display the ARP scan results
    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})

    if devices:
        print("\nARP Scan Results:")
        for device in devices:
            print(f"{device['ip']}   {device['mac']}")
    else:
        print("[-] No devices found in ARP Scan.")

