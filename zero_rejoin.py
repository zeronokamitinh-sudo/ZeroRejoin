import os, time, sys
from colorama import init, Fore, Style

# Khởi tạo colorama
init(autoreset=True)

def clear():
    # Xóa màn hình phù hợp cho cả Windows và Linux/Termux
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    clear()
    
    # 1. LOGO ZERONOKAMI (Chữ lớn, màu đỏ rực - Style từ code 2)
    logo = """
 ███████╗███████╗██████╗  ██████╗ ███╗   ██╗ ██████╗ ██╗  ██╗ █████╗ ███╗   ███╗██╗
 ╚══███╔╝██╔════╝██╔══██╗██╔═══██╗████╗  ██║██╔═══██╗██║ ██╔╝██╔══██╗████╗ ████║██║
   ███╔╝ █████╗  ██████╔╝██║   ██║██╔██╗ ██║██║   ██║█████╔╝ ███████║██╔████╔██║██║
  ███╔╝  ██╔══╝  ██╔══██╗██║   ██║██║╚██╗██║██║   ██║██╔═██╗ ██╔══██║██║╚██╔╝██║██║
 ███████╗███████╗██║  ██║╚██████╔╝██║ ╚████║╚██████╔╝██║  ██╗██║  ██║██║ ╚═╝ ██║██║
 ╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝
    """
    print(Fore.RED + Style.BRIGHT + logo)

    # 2. THÔNG TIN PHỤ (Style từ code 2)
    print(Fore.RED + Style.BRIGHT + " => " + Fore.WHITE + Style.BRIGHT + "★ VIET NAM VERSION ★" + Fore.RED + Style.BRIGHT + " <=")
    print(Fore.RED + Style.BRIGHT + " - Version:" + Fore.WHITE + " 5.0.0 | Created By zeronokami.shop | Bản hoàn chỉnh")
    print(Fore.RED + Style.BRIGHT + " - Credit: " + Fore.WHITE + " zeronokami.shop")
    print(Fore.RED + Style.BRIGHT + " - Method: " + Fore.WHITE + " Check Executor & Auto Rejoin\n")

    # 3. KHUNG MENU (Sử dụng kỹ thuật fixed-width W để chống biến dạng)
    W = 60 
    
    # Viền trên
    print(Fore.YELLOW + Style.BRIGHT + " ╔" + "═" * (W-2) + "╗")
    
    # Tiêu đề bảng
    header = " ZERONOKAMI - MENU "
    print(Fore.YELLOW + Style.BRIGHT + " ║" + Fore.CYAN + Style.BRIGHT + header.center(W-2) + Fore.YELLOW + Style.BRIGHT + "║")
    print(Fore.YELLOW + Style.BRIGHT + " ╠" + "═" * (W-2) + "╣")

    # Hàm hỗ trợ in dòng menu để đảm bảo viền luôn thẳng (Fix lỗi kéo giãn)
    def print_item(cmd_str, desc_str, color=Fore.GREEN):
        content = f" {cmd_str}  {desc_str}"
        line = content.ljust(W-4)
        print(Fore.YELLOW + Style.BRIGHT + " ║ " + color + Style.BRIGHT + line + Fore.YELLOW + Style.BRIGHT + " ║")

    # Danh sách hiển thị dựa trên code gốc của bạn
    print_item("[1]", "Start Auto Rejoin")
    print_item("[2]", "Setup Game ID")
    print_item("[3]", "Auto Login Cookie")
    print_item("[4]", "Enable Webhook")
    print_item("[5]", "Auto Check User")
    print_item("[0]", "Exit", color=Fore.RED)

    # Viền dưới
    print(Fore.YELLOW + Style.BRIGHT + " ╚" + "═" * (W-2) + "╝\n")

# Vòng lặp giữ nguyên LOGIC xử lý từ code gốc 1 của bạn
while True:
    banner()
    try:
        # Sử dụng biến 'ch' và input style từ code của bạn
        ch = input(Fore.GREEN + Style.BRIGHT + "[ zeronokami.shop ] - Enter command: ")
        
        if ch == "1":
            print(Fore.GREEN + Style.BRIGHT + "\n[+] Đang auto rejoin... (giả lập)")
            for i in range(1, 11):
                print(Fore.YELLOW + f"[*] Rejoin lần {i}... ", end="\r")
                time.sleep(0.5)
            print(Fore.YELLOW + "\n[OK] Hoàn tất 10 lần rejoin (demo)")
            
        elif ch == "2":
            gameid = input(Fore.CYAN + Style.BRIGHT + "\n[?] Nhập Game ID: ")
            print(Fore.GREEN + Style.BRIGHT + f"[+] Đã set Game ID: {gameid} (demo)")
            
        elif ch == "3":
            print(Fore.YELLOW + Style.BRIGHT + "\n[!] Auto login với cookie... (chức năng này cần code thật, hiện chỉ demo)")
            
        elif ch == "0":
            print(Fore.RED + Style.BRIGHT + "\n[!] Tạm biệt!")
            sys.exit()
            
        else:
            print(Fore.RED + Style.BRIGHT + "\n[!] Lệnh không hợp lệ!")
            
        input(Fore.WHITE + Style.BRIGHT + "\nNhấn Enter để tiếp tục...")
        
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        print(Fore.RED + f"\n[!] Có lỗi xảy ra: {e}")
        input()
