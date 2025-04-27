import socket
import dns.resolver
import dns.exception
import dns.query
import dns.zone
import concurrent.futures
import threading
import os
import sys

# Global stop event
stop_event = threading.Event()

def domain_to_ip():
    domain = input("\nEnter the domain name (e.g., example.com): ").strip()

    if not domain:
        print("[-] Error: Domain name cannot be empty.")
        return

    try:
        ip_address = socket.gethostbyname(domain)
        print(f"\n[+] {domain} resolved to IP: {ip_address}\n")
    except socket.gaierror:
        print("\n[-] Error: Unable to resolve domain's main IP.\n")
        return

    record_types = ['A', 'AAAA', 'MX', 'TXT', 'CNAME', 'NS', 'SOA']
    nameservers = []

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
                    target = target.rstrip('.')
                    if record == 'NS':
                        nameservers.append(target)
                    try:
                        target_ip = socket.gethostbyname(target)
                        print(f"   [IP] {target}: {target_ip}")
                    except socket.gaierror:
                        print(f"   [IP] {target}: Unable to resolve IP")
        except dns.resolver.NoAnswer:
            print(f"-> No {record} records found.")
        except dns.resolver.NXDOMAIN:
            print("-> Domain does not exist.")
            return
        except dns.exception.Timeout:
            print(f"-> Timeout while resolving {record} records.")
        except dns.resolver.NoNameservers:
            print(f"-> No nameservers could be reached.")

    # -------- Zone Transfer Testing --------
    print("\n\n=== Zone Transfer Testing ===\n")

    if not nameservers:
        print("[-] No nameservers found, skipping zone transfer test.\n")
    else:
        for ns in nameservers:
            print(f"[i] Attempting zone transfer from NS: {ns}")
            try:
                zone = dns.zone.from_xfr(dns.query.xfr(ns, domain, lifetime=5))
                names = zone.nodes.keys()
                print(f"[+] Zone Transfer successful on {ns}!\n")
                for n in names:
                    record = zone[n].to_text(n)
                    print(record)
            except Exception as e:
                print(f"[-] Zone transfer failed on {ns}: {str(e)}\n")

    # -------- Subdomain Brute Forcing (Threaded) --------
    print("\n\n=== Subdomain Bruteforce ===\n")

    wordlist_path = os.path.join("subdomains.txt")
    if not os.path.isfile(wordlist_path):
        print(f"[-] Wordlist file not found: {wordlist_path}")
        return

    with open(wordlist_path, 'r') as file:
        subdomains = [line.strip() for line in file if line.strip() and not line.startswith("#")]

    found = []

    def resolve_sub(sub):
        if stop_event.is_set():
            return

        subdomain = f"{sub}.{domain}"
        try:
            answers = resolver.resolve(subdomain, 'A')
            for rdata in answers:
                found.append((subdomain, rdata.to_text()))
                print(f"[+] Found: {subdomain} -> {rdata.to_text()}")
                return
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout, dns.resolver.NoNameservers):
            pass

        # Try CNAME if A fails
        try:
            answers = resolver.resolve(subdomain, 'CNAME')
            for rdata in answers:
                cname_target = str(rdata.target)
                found.append((subdomain, cname_target))
                print(f"[+] Found (CNAME): {subdomain} -> {cname_target}")
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout, dns.resolver.NoNameservers):
            pass

    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            executor.map(resolve_sub, subdomains)
    except KeyboardInterrupt:
        stop_event.set()
        print()  # Silent exit, no ugly error
        sys.exit(0)

    print(f"\n\n[+] Total found: {len(found)} subdomains.\n")

    # -------- Reverse DNS Lookup --------
    if found:
        print("\n\n=== Reverse DNS Lookup of Found Subdomains ===\n")

        def reverse_lookup(item):
            if stop_event.is_set():
                return

            domain_found, ip_or_cname = item
            ip = None
            if ip_or_cname.replace('.', '').isdigit():  # basic check if it's IP
                ip = ip_or_cname
            else:
                try:
                    ip = socket.gethostbyname(ip_or_cname.rstrip('.'))
                except:
                    pass
            if ip:
                try:
                    rev_name = socket.gethostbyaddr(ip)
                    print(f"[PTR] {ip} -> {rev_name[0]}")
                except (socket.herror, socket.gaierror):
                    pass

        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
                executor.map(reverse_lookup, found)
        except KeyboardInterrupt:
            stop_event.set()
            print()
            sys.exit(0)

    # -------- Final Message --------
    GREEN = "\033[38;5;46m"
    RESET = "\033[0m"

    print(f"\n{GREEN}{domain} just got sh3rl0ckd 🚀{RESET}\n")
