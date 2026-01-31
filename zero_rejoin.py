import os, time, sys, subprocess

# --- TỰ ĐỘNG FIX LỖI THIẾU THƯ VIỆN ---
def install_dependencies():
    try:
        from colorama import init, Fore, Style
    except ImportError:
        print(">> Đang cài đặt thư viện colorama để sửa lỗi...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama"])
        print(">> Đã cài đặt xong! Vui lòng đợi khởi động...")
        time.sleep(1)
        os.execv(sys.executable, ['python'] + sys.argv)

install_dependencies()
from colorama import init, Fore, Style

# Khởi tạo colorama
init(autoreset=True)

# Biến toàn cục để lưu package
current_package_prefix = None
# Đổi tên hiển thị thành ZeroNokami theo yêu cầu
DISPLAY_NAME = "ZeroNokami"

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    clear()
    # LOGO ZERONOKAMI
    logo = """
 ███████╗███████╗██████╗  ██████╗ ███╗   ██╗ ██████╗ ██╗  ██╗ █████╗ ███╗   ███╗██╗
 ╚══███╔╝██╔════╝██╔══██╗██╔═══██╗████╗  ██║██╔═══██╗██║ ██╔╝██╔══██╗████╗ ████║██║
    ███╔╝ █████╗  ██████╔╝██║   ██║██╔██╗ ██║██║   ██║█████╔╝ ███████║██╔████╔██║██║
   ███╔╝  ██╔══╝  ██╔══██╗██║   ██║██║╚██╗██║██║   ██║██╔═██╗ ██╔══██║██║╚██╔╝██║██║
  ███████╗███████╗██║  ██║╚██████╔╝██║ ╚████║╚██████╔╝██║  ██╗██║  ██║██║ ╚═╝ ██║██║
  ╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝
    """
    print(Fore.BLUE + Style.BRIGHT + logo)
    print("\n")

    # KHUNG MENU
    W = 60 
    print(Fore.YELLOW + Style.BRIGHT + " ╔" + "═" * (W-2) + "╗")
    header = " ZERONOKAMI - MENU "
    print(Fore.YELLOW + Style.BRIGHT + " ║" + Fore.CYAN + Style.BRIGHT + header.center(W-2) + Fore.YELLOW + Style.BRIGHT + "║")
    print(Fore.YELLOW + Style.BRIGHT + " ╠" + "═" * (W-2) + "╣")

    def print_item(cmd_str, desc_str, color=Fore.CYAN):
        content = f" {cmd_str}  {desc_str}"
        line = content.ljust(W-4)
        print(Fore.YELLOW + Style.BRIGHT + " ║ " + color + Style.BRIGHT + line + Fore.YELLOW + Style.BRIGHT + " ║")

    print_item("[3]", "Auto Login with Cookie")
    print_item("[4]", "Enable Discord Webhook")
    print_item("[5]", "Auto Check User Setup")
    print_item("[6]", "Configure Package Prefix")
    print_item("[7]", "Auto Change Android ID")
    print_item("[0]", "Exit", color=Fore.RED)

    print(Fore.YELLOW + Style.BRIGHT + " ╚" + "═" * (W-2) + "╝\n")

# Vòng lặp xử lý
while True:
    banner()
    try:
        # Tiền tố lệnh chính
        prefix_label = f"{Fore.YELLOW}[ {DISPLAY_NAME} ]{Fore.WHITE} - "
        ch = input(prefix_label + "Enter command: ")
        
        if ch == "6":
            # 1. Chỉ hiện dòng Current package prefix (Màu xanh lá) nếu đã có dữ liệu
            if current_package_prefix:
                print(f"{Fore.GREEN}[ {DISPLAY_NAME} ] - Current package prefix: {current_package_prefix}")
            
            # 2. Dòng nhập liệu (Vàng - Trắng) theo đúng format ảnh 1
            prompt = f"{Fore.YELLOW}[ {DISPLAY_NAME} ]{Fore.WHITE} - Enter new package prefix (or press Enter to keep current): "
            new_prefix = input(prompt)
            
            if new_prefix:
                current_package_prefix = new_prefix
                # 3. Thông báo lưu thành công và cập nhật theo format ảnh 2
                print(f"{Fore.GREEN}[ {DISPLAY_NAME} ] - Configuration saved successfully.")
                print(f"{Fore.GREEN}[ {DISPLAY_NAME} ] - Package prefix updated to: {current_package_prefix}")
            
        elif ch == "0":
            print(Fore.RED + Style.BRIGHT + f"\n[ {DISPLAY_NAME} ] - Tạm biệt!")
            sys.exit()
            
        elif ch == "":
            continue
            
        else:
            print(f"{Fore.RED}[ {DISPLAY_NAME} ] - Command not implemented yet.")
            
        input(f"{Fore.GREEN}\nPress Enter to return...")
        
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        print(Fore.RED + f"\n[!] Có lỗi xảy ra: {e}")
        input()
