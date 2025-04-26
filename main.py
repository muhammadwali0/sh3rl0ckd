# Apne modules ko import karna
from modules.dns_analysis import domain_to_ip

def print_logo():
    GREEN = "\033[38;5;46m"  # Hacker neon green
    RESET = "\033[0m"

    print(rf"""{GREEN}
      _     _____      _  ___       _       _ 
  ___| |__ |___ / _ __| |/ _ \  ___| | ____| |
 / __| '_ \  |_ \| '__| | | | |/ __| |/ / _` |
 \__ \ | | |___) | |  | | |_| | (__|   < (_| |
 |___/_| |_|____/|_|  |_|\___/ \___|_|\_\__,_|
                                              
    {RESET}""")

def main():
    print("\033[92mWelcome to sh3rl0ckd - Information Gathering Toolkit v1.1\033[0m\n")

def main_menu():
    while True:
        print("\033[38;5;46m")  # Green color start
        print("Select an option:")
        print("1. DNS Analysis (Domain to IP Resolution)")
        print("0. Exit")
        print("\033[0m")  # Color reset

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            domain_to_ip()  # Call karega DNS module ka function
        elif choice == '0':
            print("\nExiting... Goodbye!\n")
            break
        else:
            print("\nInvalid option. Please try again.\n")

if __name__ == '__main__':
    print_logo()
    main_menu()
