import os, time, sys
from colorama import init, Fore, Style

init(autoreset=True)

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def banner():
    clear()
    # Banner to, nổi bật nhưng giảm đỏ: dùng MAGENTA cho tên tool
    print(Fore.MAGENTA + Style.BRIGHT + "╔════════════════════════════════════════════════════════════╗")
    print(Fore.MAGENTA + Style.BRIGHT + "║                                                            ║")
    print(Fore.MAGENTA + Style.BRIGHT + "║               ZERONOKAMI AUTO REJOIN               ║")
    print(Fore.MAGENTA + Style.BRIGHT + "║                                                            ║")
    print(Fore.MAGENTA + Style.BRIGHT + "║                    by ZeroNokami                     ║")
    print(Fore.MAGENTA + Style.BRIGHT + "║                                                            ║")
    print(Fore.MAGENTA + Style.BRIGHT + "╚════════════════════════════════════════════════════════════╝")
    
    print(Fore.YELLOW + Style.NORMAL + "\n          => VIET NAM VERSION <=")
    print(Fore.WHITE + Style.NORMAL + "          Method: Check Executor & Auto Rejoin\n")
    
    # Khung menu nhẹ nhàng hơn, CYAN cho border, GREEN cho text
    print(Fore.CYAN + "╔════════════════════════════════════════════════════════════╗")
    print(Fore.CYAN + "║                     MENU CHỨC NĂNG                         ║")
    print(Fore.CYAN + "╠════════════════════════════════════════════════════════════╣")
    print(Fore.GREEN + "║ [1]  Start Auto Rejoin                                     ║")
    print(Fore.GREEN + "║ [2]  Setup Game ID                                         ║")
    print(Fore.GREEN + "║ [3]  Auto Login Cookie                                     ║")
    print(Fore.GREEN + "║ [4]  Enable Webhook                                        ║")
    print(Fore.GREEN + "║ [5]  Auto Check User                                       ║")
    print(Fore.RED + Style.NORMAL + "║ [0]  Exit                                                  ║")
    print(Fore.CYAN + "╚════════════════════════════════════════════════════════════╝\n")

while True:
    banner()
    try:
        ch = input(Fore.GREEN + Style.BRIGHT + "[ ZeroNokami ] - Enter command: ")
        if ch == "1":
            print(Fore.GREEN + "\nĐang auto rejoin... (giả lập)")
            for i in range(1, 11):
                print(Fore.YELLOW + f"Rejoin lần {i}... ", end="\r")
                time.sleep(1)
            print(Fore.YELLOW + "\nHoàn tất 10 lần rejoin (demo)")
        elif ch == "2":
            gameid = input(Fore.CYAN + "Nhập Game ID: ")
            print(Fore.GREEN + f"Đã set Game ID: {gameid} (demo)")
        elif ch == "3":
            print(Fore.YELLOW + "Auto login với cookie... (chức năng này cần code thật, hiện chỉ demo)")
        elif ch == "0":
            print(Fore.RED + "Tạm biệt!")
            sys.exit()
        else:
            print(Fore.RED + "Lệnh không hợp lệ!")
        input(Fore.WHITE + "\nNhấn Enter để tiếp tục...")
    except:
        print(Fore.RED + "Có lỗi xảy ra.")
