import os, time, sys
from colorama import init, Fore, Style

# Khởi tạo colorama
init(autoreset=True)

def clear():
    # Xóa màn hình phù hợp cho cả Windows và Linux/Termux
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    clear()
    
    # 1. LOGO ZERONOKAMI (Chữ lớn, màu đỏ rực)
    logo = """
 ███████╗███████╗██████╗  ██████╗ ███╗   ██╗ ██████╗ ██╗  ██╗ █████╗ ███╗   ███╗██╗
 ╚══███╔╝██╔════╝██╔══██╗██╔═══██╗████╗  ██║██╔═══██╗██║ ██╔╝██╔══██╗████╗ ████║██║
   ███╔╝ █████╗  ██████╔╝██║   ██║██╔██╗ ██║██║   ██║█████╔╝ ███████║██╔████╔██║██║
  ███╔╝  ██╔══╝  ██╔══██╗██║   ██║██║╚██╗██║██║   ██║██╔═██╗ ██╔══██║██║╚██╔╝██║██║
 ███████╗███████╗██║  ██║╚██████╔╝██║ ╚████║╚██████╔╝██║  ██╗██║  ██║██║ ╚═╝ ██║██║
 ╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝
    """
    print(Fore.RED + Style.BRIGHT + logo)

    # 2. THÔNG TIN PHỤ
    print(Fore.RED + " => " + Fore.WHITE + "★ VIET NAM VERSION ★" + Fore.RED + " <=")
    print(Fore.RED + " - Version:" + Fore.WHITE + " 5.0.0 | Created By zeronokami.shop | Bản hoàn chỉnh")
    print(Fore.RED + " - Credit: " + Fore.WHITE + " zeronokami.shop")
    print(Fore.RED + " - Method: " + Fore.WHITE + " Check Executor\n")

    # 3. KHUNG MENU (Đã đổi tiêu đề thành ZERONOKAMI - MENU)
    # W là độ rộng cố định, giúp khung không bị vỡ khi resize terminal
    W = 60 
    
    # Viền trên
    print(Fore.YELLOW + " ╔" + "═" * (W-2) + "╗")
    
    # Tiêu đề bảng mới: ZERONOKAMI - MENU
    header = " ZERONOKAMI - MENU "
    print(Fore.YELLOW + " ║" + Fore.CYAN + Style.BRIGHT + header.center(W-2) + Fore.YELLOW + "║")
    
    # Đường kẻ ngăn cách tiêu đề và cột
    print(Fore.YELLOW + " ╠" + "═" * 7 + "╦" + "═" * (W-10) + "╣")
    
    # Tiêu đề cột
    print(Fore.YELLOW + " ║ " + Fore.WHITE + "LỆNH" + "  ║ " + Fore.WHITE + "MÔ TẢ LỆNH" + " " * (W-22) + Fore.YELLOW + "║")
    print(Fore.YELLOW + " ╠" + "═" * 7 + "╬" + "═" * (W-10) + "╣")

    # Danh sách chức năng
    menu = [
        (" 1 ", "Start Auto Rejoin (Auto setup User ID)"),
        (" 2 ", "Setup Game ID for Packages"),
        (" 3 ", "Auto Login with Cookie"),
        (" 4 ", "Enable Discord Webhook"),
        (" 5 ", "Auto Check User Setup"),
        (" 6 ", "Configure Package Prefix"),
        (" 7 ", "Auto Change Android ID"),
        (" 0 ", "Exit Tool")
    ]

    for code, desc in menu:
        # ljust tự động bù khoảng trắng để viền bên phải luôn thẳng hàng
        line_desc = desc.ljust(W-12)
        print(Fore.YELLOW + f" ║ {Fore.GREEN}{code}{Fore.YELLOW}  ║ {Fore.BLUE}{line_desc}{Fore.YELLOW} ║")

    # Viền dưới
    print(Fore.YELLOW + " ╚" + "═" * 7 + "╩" + "═" * (W-10) + "╝")

while True:
    banner()
    try:
        # Dòng nhập lệnh bên dưới menu
        print("") 
        cmd = input(f"{Fore.YELLOW}[ {Fore.WHITE}zeronokami.shop{Fore.YELLOW} ] - {Fore.WHITE}Enter command: {Fore.GREEN}")
        
        if cmd == "0":
            print(Fore.RED + "\n[!] Đang thoát chương trình...")
            time.sleep(1)
            break
        elif cmd == "1":
            print(Fore.CYAN + "\n[+] Đang thực hiện Auto Rejoin...")
            time.sleep(2)
        # Bạn có thể thêm các điều kiện elif cmd == "2", "3"... tại đây
        else:
            print(Fore.RED + "\n[!] Lệnh không hợp lệ, vui lòng thử lại!")
            time.sleep(1)
            
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Đã dừng bởi người dùng.")
        break
    except Exception as e:
        print(Fore.RED + f"\n[!] Có lỗi xảy ra: {e}")
        break
