import os, time, sys
from colorama import init, Fore, Style

# Khởi tạo colorama
init(autoreset=True)

# Biến toàn cục để lưu package
current_package_prefix = None

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    clear()
    
    # 1. LOGO ZERONOKAMI (Đã đổi sang màu XANH DƯƠNG)
    logo = """
 ███████╗███████╗██████╗  ██████╗ ███╗   ██╗ ██████╗ ██╗  ██╗ █████╗ ███╗   ███╗██╗
 ╚══███╔╝██╔════╝██╔══██╗██╔═══██╗████╗  ██║██╔═══██╗██║ ██╔╝██╔══██╗████╗ ████║██║
    ███╔╝ █████╗  ██████╔╝██║   ██║██╔██╗ ██║██║   ██║█████╔╝ ███████║██╔████╔██║██║
   ███╔╝  ██╔══╝  ██╔══██╗██║   ██║██║╚██╗██║██║   ██║██╔═██╗ ██╔══██║██║╚██╔╝██║██║
  ███████╗███████╗██║  ██║╚██████╔╝██║ ╚████║╚██████╔╝██║  ██╗██║  ██║██║ ╚═╝ ██║██║
  ╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝
    """
    print(Fore.BLUE + Style.BRIGHT + logo)

    # 2. THÔNG TIN PHỤ
    print(Fore.RED + Style.BRIGHT + " => " + Fore.WHITE + Style.BRIGHT + "★ VIET NAM VERSION ★" + Fore.RED + Style.BRIGHT + " <=")
    print(Fore.RED + Style.BRIGHT + " - Version:" + Fore.WHITE + " 5.0.0 | Created By zeronokami.shop | Bản hoàn chỉnh")
    print(Fore.RED + Style.BRIGHT + " - Credit: " + Fore.WHITE + " zeronokami.shop")
    print(Fore.RED + Style.BRIGHT + " - Method: " + Fore.WHITE + " Check Executor & Auto Rejoin\n")

    # 3. KHUNG MENU
    W = 60 
    print(Fore.YELLOW + Style.BRIGHT + " ╔" + "═" * (W-2) + "╗")
    
    header = " ZERONOKAMI - MENU "
    print(Fore.YELLOW + Style.BRIGHT + " ║" + Fore.CYAN + Style.BRIGHT + header.center(W-2) + Fore.YELLOW + Style.BRIGHT + "║")
    print(Fore.YELLOW + Style.BRIGHT + " ╠" + "═" * (W-2) + "╣")

    def print_item(cmd_str, desc_str, color=Fore.GREEN):
        content = f" {cmd_str}  {desc_str}"
        line = content.ljust(W-4)
        print(Fore.YELLOW + Style.BRIGHT + " ║ " + color + Style.BRIGHT + line + Fore.YELLOW + Style.BRIGHT + " ║")

    print_item("[1]", "Start Auto Rejoin")
    print_item("[2]", "Setup Game ID")
    print_item("[3]", "Auto Login Cookie")
    print_item("[4]", "Enable Webhook")
    print_item("[5]", "Auto Check User")
    print_item("[6]", "Configure Package Prefix")
    print_item("[0]", "Exit", color=Fore.RED)

    print(Fore.YELLOW + Style.BRIGHT + " ╚" + "═" * (W-2) + "╝\n")

# Vòng lặp xử lý
while True:
    banner()
    try:
        # Thay đổi dòng nhập lệnh theo yêu cầu
        ch = input(Fore.GREEN + Style.BRIGHT + "[ ZeroNokami ] - Enter command: ")
        
        if ch == "1":
            print(Fore.GREEN + Style.BRIGHT + "\n[+] Đang auto rejoin... (giả lập)")
            time.sleep(1)
            
        elif ch == "2":
            gameid = input(Fore.CYAN + Style.BRIGHT + "\n[?] Nhập Game ID: ")
            print(Fore.GREEN + Style.BRIGHT + f"[+] Đã set Game ID: {gameid}")
            
        elif ch == "3":
            print(Fore.YELLOW + Style.BRIGHT + "\n[!] Chức năng Auto Login đang bảo trì...")

        elif ch == "6":
            print("") # Xuống dòng cho đẹp
            if current_package_prefix:
                print(Fore.CYAN + Style.BRIGHT + f"Current package prefix: {current_package_prefix}")
            
            new_prefix = input(Fore.WHITE + Style.BRIGHT + "Enter new pack prefix: ")
            
            if new_prefix:
                current_package_prefix = new_prefix
                print(Fore.GREEN + Style.BRIGHT + "Save the package successfully")
            else:
                print(Fore.RED + "Package prefix cannot be empty!")

        elif ch == "0":
            print(Fore.RED + Style.BRIGHT + "\n[!] Tạm biệt!")
            sys.exit()
            
        else:
            print(Fore.RED + Style.BRIGHT + "\n[!] Lệnh không hợp lệ!")
            
        # Dòng Enter to continue theo yêu cầu
        input(Fore.WHITE + Style.BRIGHT + "\nEnter to continue...")
        
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        print(Fore.RED + f"\n[!] Có lỗi xảy ra: {e}")
        input()
