# Import modules
from modules.dns_analysis import domain_to_ip
from modules.live_host_identification import ping_sweep
import sys

# Colors
GREEN = "\033[38;5;46m"
RESET = "\033[0m"

def print_logo():
    print(rf"""{GREEN}
      _     _____      _  ___       _       _ 
  ___| |__ |___ / _ __| |/ _ \  ___| | ____| |
 / __| '_ \  |_ \| '__| | | | |/ __| |/ / _` |
 \__ \ | | |___) | |  | | |_| | (__|   < (_| |
 |___/_| |_|____/|_|  |_|\___/ \___|_|\_\__,_|

sh3rl0ckd - Reconnaissance Toolkit v1.1
{RESET}""")

def main_menu():
    while True:
        try:
            print(f"\n{GREEN}Select an option:{RESET}")
            print("1. DNS Analysis")
            print("2. Live Host Identification")
            print("0. Exit\n")

            choice = input("Enter your choice: ").strip()

            if choice == '1':
                domain_to_ip()
            elif choice == '2':
                ping_sweep()
            elif choice == '0':
                print("\nExiting... Goodbye!\n")
                sys.exit(0)
            else:
                print("\nInvalid option. Please try again.\n")

        except KeyboardInterrupt:
            print()  # Silent Ctrl+C exit
            sys.exit(0)

if __name__ == '__main__':
    print_logo()
    print(f"{GREEN}Welcome to sh3rl0ckd - Information Gathering Toolkit v1.1{RESET}\n")
    main_menu()
