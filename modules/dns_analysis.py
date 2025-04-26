import socket

def domain_to_ip():
    domain = input("\nEnter the domain name (e.g., example.com): ").strip()

    try:
        ip_address = socket.gethostbyname(domain)
        print(f"\nResolved IP address of {domain} is: {ip_address}\n")
    except socket.gaierror:
        print("\nError: Unable to resolve domain. Check the domain name.\n")
