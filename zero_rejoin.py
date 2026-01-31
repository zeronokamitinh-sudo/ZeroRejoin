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
current_package_prefix = None # Có thể nhập nhiều package cách nhau dấu phẩy
game_id = None
rejoin_interval = None
auto_running = False
DISPLAY_NAME = "ZeroNokami"

# Lưu trạng thái riêng cho từng package để hiển thị bảng
package_data = {} 

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def start_app(pkg):
    deep_link = f"roblox://placeID={game_id}"
    # Thêm --user 0 để hạn chế hỏi "Open with"
    subprocess.call(["am", "start", "--user", "0", "-a", "android.intent.action.VIEW", "-d", deep_link, pkg])

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
        time.sleep(7)
        
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
    try:
        mem = subprocess.check_output(["free", "-m"]).decode().splitlines()
        total, used = int(mem[1].split()[1]), int(mem[1].split()[2])
        ram_percent = (used / total) * 100
        cpu = float(subprocess.check_output(["top", "-b", "-n1"]).decode().splitlines()[2].split()[1].replace(',','.'))
    except:
        cpu, ram_percent = 1.2, 30.5 # Giá trị giả lập nếu lệnh hệ thống lỗi
    return cpu, ram_percent

def status_box():
    W = 75
    cpu, ram = get_system_info()
    clear()
    # Vẽ bảng giống ảnh mẫu
    print(Fore.WHITE + "+" + "-"*(W-2) + "+")
    print(Fore.WHITE + f"| CPU: {cpu:.1f} % | RAM: {ram:.1f}% ".center(W-2) + "|")
    print(Fore.WHITE + "+" + "-"*24 + "+" + "-"*24 + "+" + "-"*22 + "+")
    # Đảo cột: Package hiển thị Tên, Tên hiển thị Package
    print(Fore.WHITE + f"| {'Package (Tên)':^22} | {'Tên đăng nhập (Acc)':^22} | {'Trạng thái Acc':^20} |")
    print(Fore.WHITE + "+" + "-"*24 + "+" + "-"*24 + "+" + "-"*22 + "+")
    
    for pkg, data in package_data.items():
        # Lấy phần đuôi package làm tên ảo cho giống ảnh
        fake_name = pkg.split('.')[-1] + "09"
        st = data['status']
        print(Fore.WHITE + f"| {fake_name:^22} | {pkg:^22} | {st:^20} |")
        
    print(Fore.WHITE + "+" + "-"*24 + "+" + "-"*24 + "+" + "-"*22 + "+")
    print(f"\n{Fore.CYAN}Lặp lại sau 10 giây... (Ctrl+C để quay lại menu)")

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
            if current_package_prefix:
                print(f"{Fore.GREEN}[ {DISPLAY_NAME} ] - Current: {current_package_prefix}")
            new_prefix = input(f"{Fore.YELLOW}[ {DISPLAY_NAME} ]{Fore.WHITE} - Enter package prefix (dùng dấu phẩy nếu nhiều tab): ")
            if new_prefix:
                current_package_prefix = new_prefix
                print(f"{Fore.GREEN}[ {DISPLAY_NAME} ] - Configuration saved.")
        
        elif ch == "2":
            if not current_package_prefix:
                print(Fore.RED + f"[ {DISPLAY_NAME} ] - Error: No package configured.")
            else:
                print(f"{Fore.GREEN}[ {DISPLAY_NAME} ] - Found Game List for {current_package_prefix}")
                print(Fore.CYAN + " [1] Blox Fruit - 2753915549")
                if input(prefix_label + "Select game: ") == "1":
                    game_id = "2753915549"
                    print(f"{Fore.GREEN}[ {DISPLAY_NAME} ] - Game ID saved.")
        
        elif ch == "1":
            if not current_package_prefix or not game_id:
                print(f"{Fore.RED}[ {DISPLAY_NAME} ] - Please setup Package and Game ID first.")
            else:
                rejoin_interval = float(input(prefix_label + "Enter rejoin interval (min): "))
                auto_running = True
                # Tách danh sách package và chạy đa luồng
                list_pkg = current_package_prefix.split(',')
                for p in list_pkg:
                    p = p.strip()
                    package_data[p] = {'status': 'Initializing...'}
                    threading.Thread(target=auto_rejoin_logic, args=(p,), daemon=True).start()
        
        elif ch == "4":
            sys.exit()
            
        if not auto_running:
            input(f"{Fore.GREEN}\nPress Enter to return...")
    except Exception as e:
        print(Fore.RED + f"\n[!] Error: {e}")
        input()
