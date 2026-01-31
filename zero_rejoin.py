import os, time, sys, random
from colorama import init, Fore

init()

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def banner():
    clear()
    print(Fore.RED + """
╔════════════════════════════════════╗
║     ZERONOKAMI REJOIN TOOL v1.0    ║
║     Created by ZeroNokami          ║
╚════════════════════════════════════╝
    """)
    print(Fore.YELLOW + "=> VIET NAM VERSION <=")
    print("Method: Check Executor & Auto Rejoin")
    print(Fore.CYAN + "\n[1] Start Auto Rejoin")
    print("[2] Setup Game ID")
    print("[3] Auto Login Cookie")
    print("[4] Enable Webhook")
    print("[5] Auto Check User")
    print("[0] Exit\n")

while True:
    banner()
    try:
        ch = input(Fore.GREEN + "[ ZeroNokami ] - Enter command: ")
        if ch == "1":
            print(Fore.GREEN + "Đang auto rejoin... (giả lập)")
            for i in range(1, 11):
                print(f"Rejoin lần {i}... ", end="\r")
                time.sleep(1)
            print(Fore.YELLOW + "\nHoàn tất 10 lần rejoin (demo)")
        elif ch == "2":
            gameid = input("Nhập Game ID: ")
            print(f"Đã set Game ID: {gameid} (demo)")
        elif ch == "3":
            print("Auto login với cookie... (chức năng này cần code thật, hiện chỉ demo)")
        elif ch == "0":
            print("Tạm biệt!")
            sys.exit()
        else:
            print("Lệnh không hợp lệ!")
        input("\nNhấn Enter để tiếp tục...")
    except:
        print("Có lỗi xảy ra.")
