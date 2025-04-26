def print_logo():
    # matrix green color code
    GREEN = "\033[38;5;46m"
    RESET = "\033[0m"

    # ascii logo
    print(rf"""{GREEN}
      _     _____      _  ___       _       _ 
  ___| |__ |___ / _ __| |/ _ \  ___| | ____| |
 / __| '_ \  |_ \| '__| | | | |/ __| |/ / _` |
 \__ \ | | |___) | |  | | |_| | (__|   < (_| |
 |___/_| |_|____/|_|  |_|\___/ \___|_|\_\__,_|
                                              
    {RESET}""")

def main():
    print_logo()  # ye start mein chalega
    print("\033[38;5;46mWelcome to sh3rl0ckd - Information Gathering Toolkit\033[0m\n")
    print("\033[38;5;46mYahan pe menu system banega — press 1 for DNS etc.\033[0m")
    print("\033[38;5;46mFilhal placeholder hai... aur cheezein add karni hain.\033[0m\n")

if __name__ == '__main__':
    main()  
