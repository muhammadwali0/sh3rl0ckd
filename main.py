def print_logo():
    # Color code set kar rahe hain hacker green ke liye
    GREEN = "\033[92m"
    RESET = "\033[0m"

    # Apna ASCII logo hacker green me print karne ka scene
    print(rf"""{GREEN}
      _     _____      _  ___       _       _ 
  ___| |__ |___ / _ __| |/ _ \  ___| | ____| |
 / __| '_ \  |_ \| '__| | | | |/ __| |/ / _` |
 \__ \ | | |___) | |  | | |_| | (__|   < (_| |
 |___/_| |_|____/|_|  |_|\___/ \___|_|\_\__,_|
                                              
    {RESET}""")

def main():
    print_logo()  # Pehle logo print hoga jab program run hoga
    print("\033[92mWelcome to sh3rl0ckd - Information Gathering Toolkit\033[0m\n")
    print("\033[92mYahan pe main menu show hoga jab pura menu system bana lenge.\033[0m")
    print("\033[92mFuture features ka placeholder hai abhi.\033[0m\n")

if __name__ == '__main__':
    main()  # Yahan se program start hota hai jab file directly run karte hain
