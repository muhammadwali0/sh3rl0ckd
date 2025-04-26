import socket
import dns.resolver
import dns.exception
import os

def domain_to_ip():
    domain = input("\nEnter the domain name (e.g., example.com): ").strip()

    try:
        ip_address = socket.gethostbyname(domain)
        print(f"\n[+] {domain} resolved to IP: {ip_address}\n")
    except socket.gaierror:
        print("\n[-] Error: Unable to resolve domain's main IP.\n")
        return

    record_types = ['A', 'AAAA', 'MX', 'TXT', 'CNAME', 'NS', 'SOA']

    resolver = dns.resolver.Resolver()
    resolver.lifetime = 3.0
    resolver.timeout = 2.0

    for record in record_types:
        print(f"\n=== {record} Records ===")

        try:
            answers = resolver.resolve(domain, record)
            for rdata in answers:
                print(f"-> {rdata}")

                if record in ['NS', 'MX']:
                    target = str(rdata.exchange) if record == 'MX' else str(rdata.target)
                    try:
                        target_ip = socket.gethostbyname(target.rstrip('.'))
                        print(f"   [IP] {target.rstrip('.')}: {target_ip}")
                    except socket.gaierror:
                        print(f"   [IP] {target.rstrip('.')}: Unable to resolve IP")
        except dns.resolver.NoAnswer:
            print(f"-> No {record} records found.")
        except dns.resolver.NXDOMAIN:
            print("-> Domain does not exist.")
            return
        except dns.exception.Timeout:
            print(f"-> Timeout while resolving {record} records.")
        except dns.resolver.NoNameservers:
            print(f"-> No nameservers could be reached.")

    # -------- Subdomain Brute Forcing Start --------
    print("\n\n=== Subdomain Bruteforce ===\n")

    wordlist_path = os.path.join("sh3rl0ckd", "subdomains.txt")

    if not os.path.isfile(wordlist_path):
        print(f"[-] Wordlist file not found: {wordlist_path}")
        return

    with open(wordlist_path, 'r') as file:
        subdomains = file.read().splitlines()

    for sub in subdomains:
        subdomain = f"{sub.strip()}.{domain}"
        try:
            sub_ip = socket.gethostbyname(subdomain)
            print(f"[+] Found: {subdomain} -> {sub_ip}")
        except socket.gaierror:
            pass  # Silent fail, means subdomain doesn't exist

