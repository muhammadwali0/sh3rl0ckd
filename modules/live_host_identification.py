import subprocess
import ipaddress
import concurrent.futures
import time
from scapy.config import conf
from scapy.all import ARP, Ether, srp, IP, ICMP, sr1, TCP, UDP

# Ping host function (ICMP ping via system command)
def ping_host(ip, param):
    try:
        process = subprocess.Popen(
            ["ping", param, "1", "-W", "1", str(ip)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            if "1 packets transmitted, 1 received" in stdout.decode("utf-8"):
                return ip
    except Exception as e:
        print(f"Error occurred while pinging {ip}: {e}")
    return None

# ICMP Probe function
def icmp_probe(ip):
    try:
        packet = IP(dst=str(ip))/ICMP()
        start_time = time.time()
        response = sr1(packet, timeout=2, verbose=False)
        end_time = time.time()

        if response:
            latency_ms = (end_time - start_time) * 1000
            return {
                "ip": ip,
                "method": "ICMP",
                "latency": round(latency_ms, 2),
                "ttl": response.ttl,
                "ip_id": response.id
            }
    except Exception:
        pass
    return None

# TCP Probe fallback
def tcp_probe(ip):
    try:
        packet = IP(dst=str(ip))/TCP(dport=80, flags="S")  # SYN packet to port 80
        start_time = time.time()
        response = sr1(packet, timeout=2, verbose=False)
        end_time = time.time()

        if response and response.haslayer(TCP):
            latency_ms = (end_time - start_time) * 1000
            return {
                "ip": ip,
                "method": "TCP",
                "latency": round(latency_ms, 2),
                "ttl": response.ttl,
                "ip_id": response.id
            }
    except Exception:
        pass
    return None

# UDP Probe fallback
def udp_probe(ip):
    try:
        packet = IP(dst=str(ip))/UDP(dport=53)  # UDP packet to port 53 (DNS)
        start_time = time.time()
        response = sr1(packet, timeout=2, verbose=False)
        end_time = time.time()

        if response:
            latency_ms = (end_time - start_time) * 1000
            return {
                "ip": ip,
                "method": "UDP",
                "latency": round(latency_ms, 2),
                "ttl": response.ttl,
                "ip_id": response.id
            }
    except Exception:
        pass
    return None

# Combined probing function
def advanced_probe(ip):
    result = icmp_probe(ip)
    if not result:
        result = tcp_probe(ip)
    if not result:
        result = udp_probe(ip)
    return result

# ARP scan function
def arp_scan(target_ips, interface="eth0"):
    live_hosts = []
    conf.iface = interface
    
    for target_ip in target_ips:
        try:
            arp_request = ARP(pdst=str(target_ip))
            ether_frame = Ether(dst="ff:ff:ff:ff:ff:ff")
            packet = ether_frame/arp_request

            result = srp(packet, timeout=3, iface=interface, verbose=False)[0]

            for sent, received in result:
                live_hosts.append(received.psrc)
        except Exception as e:
            print(f"Error occurred during ARP scan on {target_ip}: {e}")
    
    return live_hosts

# Main Ping Sweep function
def ping_sweep():
    network = input("Enter the network to scan (e.g., 192.168.0.0/24): ")
    
    try:
        ip_network = ipaddress.IPv4Network(network)
    except ValueError:
        print("[-] Invalid network format.")
        return

    print(f"\nStarting Ping Sweep on {network}...\n")

    live_hosts = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(lambda ip: ping_host(ip, "-c"), ip_network.hosts())
        for result in results:
            if result:
                live_hosts.append(result)
                print(f"[+] Host alive: {result}")

    print(f"\nTotal Live Hosts found: {len(live_hosts)}")

    if live_hosts:
        print("\nStarting ARP scan on live hosts...")
        arp_hosts = arp_scan(live_hosts)

        for host in arp_hosts:
            print(f"[+] ARP response from: {host}")

        print("\nStarting Advanced Probe (ICMP -> TCP -> UDP)...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            results = executor.map(advanced_probe, live_hosts)
            for result in results:
                if result:
                    print(f"[+] {result['method']} reply from {result['ip']} | Latency: {result['latency']}ms | TTL: {result['ttl']} | IP ID: {result['ip_id']}")
                else:
                    print("[-] No response from host (even after fallback probes)")
