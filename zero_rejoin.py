import os, time, sys
from colorama import init, Fore, Style

# Khởi tạo colorama, autoreset=True để tự động reset màu sau mỗi lệnh print
init(autoreset=True)

def clear():
    # Lệnh xóa màn hình cho cả Windows và Linux/Mac
    os.system('cls' if os.name == 'nt' else 'clear')

def print_line(left, right, width=60):
    # Hàm hỗ trợ in dòng menu để không bị lệch khung
    # Cấu trúc: ║ [1]  │ Start Auto Rejoin... ║
    content_len = width - 8 - len(left) # 8 là trừ đi các ký tự viền và khoảng cách
    print(Fore.YELLOW + "║ " + Fore.GREEN + f"{left:<4}" + Fore.YELLOW + " │ " + Fore.BLUE + f"{right:<{content_len}}" + Fore.YELLOW + " ║")

def banner():
    clear()
    
    # 1. PHẦN TÊN TOOL (ASCII ART) - Màu Đỏ, Bỏ khung viền
    # Font chữ dạng Blocky giống ảnh
    ascii_art = """
███████╗███████╗██████╗  ██████╗ ███╗   ██╗ ██████╗ ██╗  ██╗ █████╗ ███╗   ███╗██╗
╚══███╔╝██╔════╝██╔══██╗██╔═══██╗████╗  ██║██╔═══██╗██║ ██╔╝██╔══██╗████╗ ████║██║
  ███╔╝ █████╗  ██████╔╝██║   ██║██╔██╗ ██║██║   ██║█████╔╝ ███████║██╔████╔██║██║
 ███╔╝  ██╔══╝  ██╔══██╗██║   ██║██║╚██╗██║██║   ██║██╔═██╗ ██╔══██║██║╚██╔╝██║██║
███████╗███████╗██║  ██║╚██████╔╝██║ ╚████║╚██████╔╝██║  ██╗██║  ██║██║ ╚═╝ ██║██║
╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝
    """
    print(Fore.RED + Style.BRIGHT + ascii_art)

    # 2. PHẦN THÔNG TIN (INFO)
    print(Fore.RED + "=> " + Fore.YELLOW + "★ VIET NAM VERSION ★" + Fore.RED + " <=")
    print(Fore.GREEN + "- Version: " + Fore.WHITE + "5.0.0 | Created By ZeroNokami | Bản hoàn chỉnh")
    print(Fore.GREEN + "- Credit:  " + Fore.WHITE + "zeronokami.shop")
    print(Fore.GREEN + "- Method:  " + Fore.WHITE + "Check Executor\n")

    # 3. PHẦN MENU (BẢNG VIP) - Cố định độ rộng để không vỡ khung
    # URL ở trên viền
    url_text = " ZERONOKAMI - MENU "
    print(Fore.YELLOW + "┌" + Fore.GREEN + url_text + Fore.YELLOW + ("─" * (52 - len(url_text))) + "┐")
    
    # Header của bảng
    print(Fore.YELLOW + "│ " + Fore.WHITE + "LỆNH" + " " * 3 + Fore.YELLOW + "│ " + Fore.WHITE + "MÔ TẢ LỆNH" + " " * 39 + Fore.YELLOW + "│")
    print(Fore.YELLOW + "├───────┼────────────────────────────────────────────────────┤")
    
    # Nội dung menu (Dùng format để căn lề chuẩn từng milimet)
    # Cấu trúc: │ [x]   │ Tên chức năng                                      │
    menu_items = [
        ("[ 1 ]", "Start Auto Rejoin (Auto setup User ID)"),
        ("[ 2 ]", "Setup Game ID for Packages"),
        ("[ 3 ]", "Auto Login with Cookie"),
        ("[ 4 ]", "Enable Discord Webhook"),
        ("[ 5 ]", "Auto Check User Setup"),
        ("[ 6 ]", "Configure Package Prefix"),
        ("[ 7 ]", "Auto Change Android ID"),
        ("[ 0 ]", "Exit Tool")
    ]

    for cmd, desc in menu_items:
        # {:<5} nghĩa là dành 5 khoảng trống canh lề trái cho cột lệnh
        # {:<50} nghĩa là dành 50 khoảng trống canh lề trái cho mô tả
        print(Fore.YELLOW + "│ " + Fore.GREEN + f"{cmd:<5}" + Fore.YELLOW + " │ " + Fore.BLUE + f"{desc:<50}" + Fore.YELLOW + " │")

    # Đóng khung
    print(Fore.YELLOW + "└───────┴────────────────────────────────────────────────────┘")

while True:
    banner()
    try:
        # Dòng nhập lệnh style giống ảnh
        print("") # Xuống dòng cho thoáng
        cmd_input = input(Fore.YELLOW + "[ zeronokami.shop ]" + Fore.WHITE + " - Enter command: ")
        
        if cmd_input == "1":
            print(Fore.GREEN + "\n[+] Đang khởi động Auto Rejoin...")
            for i in range(1, 6):
                print(Fore.CYAN + f"[*] Đang kết nối lại lần {i}...", end="\r")
                time.sleep(1)
            print(Fore.GREEN + "\n[+] Hoàn tất! (Demo)")
            
        elif cmd_input == "2":
            gameid = input(Fore.CYAN + "\nNhập Game ID: ")
            print(Fore.GREEN + f"[+] Đã lưu Game ID: {gameid}")
            
        elif cmd_input == "3":
            print(Fore.MAGENTA + "\n[!] Đang check cookie (Demo)...")
            
        elif cmd_input == "0":
            print(Fore.RED + "\nGoodbye!")
            sys.exit()
            
        else:
            print(Fore.RED + "\n[!] Lệnh không hợp lệ!")
            
        input(Fore.WHITE + "\nNhấn Enter để quay lại menu...")
        
    except KeyboardInterrupt:
        print(Fore.RED + "\nĐã dừng tool.")
        sys.exit()
    except Exception as e:
        print(Fore.RED + f"Lỗi: {e}")
        input()
