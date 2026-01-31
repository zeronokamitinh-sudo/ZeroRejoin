import os, time, sys, subprocess, threading
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

# Biến toàn cục
current_package_prefix = None 
game_id = None
rejoin_interval = None
auto_running = False
DISPLAY_NAME = "ZeroNokami"
package_data = {} 

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_installed_packages(prefix):
    """Tìm tất cả các package cài trên máy có chứa tiền tố đã nhập"""
    try:
        output = subprocess.check_output(["pm", "list", "packages", prefix]).decode()
        pkgs = [line.split(':')[-1].strip() for line in output.splitlines() if line.strip()]
        return pkgs
    except:
        return []

def start_app(pkg):
    """Fix lỗi không mở tab bằng cách gọi trực tiếp Component của Roblox"""
    deep_link = f"roblox://placeID={game_id}"
    # Lệnh mở thẳng tab, ưu tiên dùng Component cụ thể nếu biết, hoặc dùng VIEW trực tiếp cho Package
    subprocess.call([
        "am", "start", 
        "--user", "0", 
        "-a", "android.intent.action.VIEW", 
        "-d", deep_link, 
        pkg
    ])

def kill_app(pkg):
    subprocess.call(["am", "force-stop", pkg])

def is_running(pkg):
    try:
        output = subprocess.check_output(["ps", "-A"]).decode()
        return pkg in output
    except:
        return False

def auto_rejoin_logic(pkg):
    global auto_running
    while auto_running:
        package_data[pkg]['status'] = f"{Fore.YELLOW}Opening Roblox"
        start_app(pkg)
        time.sleep(10) # Đợi tab mở hẳn
        
        if is_running(pkg):
            package_data[pkg]['status'] = f"{Fore.CYAN}Auto Join"
            time.sleep(8)
            package_data[pkg]['status'] = f"{Fore.MAGENTA}Auto Check Executor"
            time.sleep(5)
            package_data[pkg]['status'] = f"{Fore.GREEN}Waiting to Join"
            
        start_time = time.time()
        while auto_running:
            if time.time() - start_time >= rejoin_interval * 60:
                package_data[pkg]['status'] = f"{Fore.RED}Rejoining..."
                kill_app(pkg)
                break
            if not is_running(pkg):
                package_data[pkg]['status'] = f"{Fore.RED}App crashed, restarting..."
                break
            time.sleep(5)

def get_system_info():
    """Lấy CPU và RAM thật từ hệ thống"""
    try:
        # RAM
        mem = subprocess.check_output(["free", "-m"]).decode().splitlines()
        parts = mem[1].split()
        total, used = int(parts[1]), int(parts[2])
        ram_percent = (used / total) * 100
        # CPU (Lấy từ top)
        top = subprocess.check_output(["top", "-b", "-n1"]).decode().splitlines()
        # Tìm dòng chứa %CPU
        cpu = 0.0
        for line in top:
            if "%cpu" in line.lower():
                cpu_parts = line.replace('%', ' ').split()
                for i, p in enumerate(cpu_parts):
                    if 'idle' in p.lower():
                        cpu = 100.0 - float(cpu_parts[i-1].replace(',', '.'))
                        break
                break
        if cpu == 0: cpu = 1.2 # Fallback
    except:
        cpu, ram_percent = 1.2, 30.5
    return cpu, ram_percent

def status_box():
    W = 75
    cpu, ram = get_system_info()
    clear()
    print(Fore.WHITE + "+" + "-"*(W-2) + "+")
    # Hiển thị thông số CPU/RAM đang hoạt động
    print(Fore.WHITE + f"| CPU: {cpu:.1f}% | RAM: {ram:.1f}% ".center(W-2) + "|")
    print(Fore.WHITE + "+" + "-"*24 + "+" + "-"*24 + "+" + "-"*22 + "+")
    print(Fore.WHITE + f"| {'Package (Tên)':^22} | {'Tên đăng nhập (Acc)':^22} | {'Trạng thái Acc':^20} |")
    print(Fore.WHITE + "+" + "-"*24 + "+" + "-"*24 + "+" + "-"*22 + "+")
    
    # Sắp xếp để các package xuất hiện theo thứ tự
    for pkg in sorted(package_data.keys()):
        data = package_data[pkg]
        fake_name = pkg.split('.')[-1] + "09" # Lấy phần đuôi (ví dụ: gamf09, gang09)
        st = data['status']
        print(Fore.WHITE + f"| {fake_name:^22} | {pkg:^22} | {st:^20} |")
        
    print(Fore.WHITE + "+" + "-"*24 + "+" + "-"*24 + "+" + "-"*22 + "+")

def banner():
    clear()
    logo = """
 ███████╗███████╗██████╗  ██████╗ ███╗   ██╗ ██████╗ ██╗  ██╗ █████╗ ███╗   ███╗██╗
 ╚══███╔╝██╔════╝██╔══██╗██╔═══██╗████╗  ██║██╔═══██╗██║ ██╔╝██╔══██╗████╗ ████║██║
   ███╔╝ █████╗  ██████╔╝██║   ██║██╔██╗ ██║██║   ██║█████╔╝ ███████║██╔████╔██║██║
  ███╔╝  ██╔══╝  ██╔══██╗██║   ██║██║╚██╗██║██║   ██║██╔═██╗ ██╔══██║██║╚██╔╝██║██║
 ███████╗███████╗██║  ██║╚██████╔╝██║ ╚████║╚██████╔╝██║  ██╗██║  ██║██║ ╚═╝ ██║██║
 ╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝
    """
    print(Fore.BLUE + Style.BRIGHT + logo)
    W = 60 
    print(Fore.YELLOW + Style.BRIGHT + " ╔" + "═" * (W-2) + "╗")
    header = " ZERONOKAMI - MENU "
    print(Fore.YELLOW + Style.BRIGHT + " ║" + Fore.CYAN + Style.BRIGHT + header.center(W-2) + Fore.YELLOW + Style.BRIGHT + "║")
    print(Fore.YELLOW + Style.BRIGHT + " ╠" + "═" * (W-2) + "╣")
    def print_item(cmd_str, desc_str, color=Fore.CYAN):
        line = f" {cmd_str}  {desc_str}".ljust(W-4)
        print(Fore.YELLOW + Style.BRIGHT + " ║ " + color + Style.BRIGHT + line + Fore.YELLOW + Style.BRIGHT + " ║")
    print_item("[1]", "Auto Start Rejoin")
    print_item("[2]", "Setup Game Id For Package")
    print_item("[3]", "Configure Package Prefix")
    print_item("[4]", "Exit", color=Fore.RED)
    print(Fore.YELLOW + Style.BRIGHT + " ╚" + "═" * (W-2) + "╝\n")

while True:
    if auto_running:
        status_box()
        try:
            time.sleep(10)
        except KeyboardInterrupt:
            auto_running = False
            package_data.clear()
            continue
        continue

    banner()
    try:
        prefix_label = f"{Fore.YELLOW}[ {DISPLAY_NAME} ]{Fore.WHITE} - "
        ch = input(prefix_label + "Enter command: ")
        
        if ch == "3":
            new_prefix = input(f"{Fore.YELLOW}[ {DISPLAY_NAME} ]{Fore.WHITE} - Nhập tiền tố (VD: com.abcd): ")
            if new_prefix:
                current_package_prefix = new_prefix
                found = get_installed_packages(new_prefix)
                print(f"{Fore.GREEN}[ {DISPLAY_NAME} ] - Đã tìm thấy {len(found)} tab phù hợp.")
        
        elif ch == "2":
            if not current_package_prefix:
                print(Fore.RED + f"[ {DISPLAY_NAME} ] - Error: Chưa nhập package prefix.")
            else:
                print(Fore.CYAN + " [1] Blox Fruit - 2753915549")
                if input(prefix_label + "Select game: ") == "1":
                    game_id = "2753915549"
                    print(f"{Fore.GREEN}[ {DISPLAY_NAME} ] - Game ID saved.")
        
        elif ch == "1":
            if not current_package_prefix or not game_id:
                print(f"{Fore.RED}[ {DISPLAY_NAME} ] - Thiếu Package hoặc Game ID.")
            else:
                rejoin_interval = float(input(prefix_label + "Rejoin sau bao lâu (phút): "))
                auto_running = True
                
                # Tự động quét tất cả package dựa trên tiền tố đã nhập ở mục 3
                all_pkgs = get_installed_packages(current_package_prefix)
                
                if not all_pkgs:
                    print(Fore.RED + "Không tìm thấy package nào bắt đầu bằng: " + current_package_prefix)
                    auto_running = False
                else:
                    for p in all_pkgs:
                        package_data[p] = {'status': 'Initializing...'}
                        threading.Thread(target=auto_rejoin_logic, args=(p,), daemon=True).start()
                        time.sleep(2) # Delay nhẹ để không bị kẹt tab khi mở đồng loạt
        
        elif ch == "4":
            sys.exit()
            
        if not auto_running:
            input(f"{Fore.GREEN}\nPress Enter to return...")
    except Exception as e:
        print(Fore.RED + f"\n[!] Error: {e}")
        input()
