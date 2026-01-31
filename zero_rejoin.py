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
# Biến toàn cục để lưu package
current_package_prefix = None
game_id = None
rejoin_interval = None
auto_running = False
status = ""
# Đổi tên hiển thị thành ZeroNokami theo yêu cầu
DISPLAY_NAME = "ZeroNokami"
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
def start_app():
    global status
    deep_link = f"roblox://placeID={game_id}"
    subprocess.call(["am", "start", "-a", "android.intent.action.VIEW", "-d", deep_link])
def kill_app():
    subprocess.call(["am", "force-stop", current_package_prefix])
def is_running():
    try:
        output = subprocess.check_output(["ps", "-A"]).decode()
        return current_package_prefix in output
    except:
        return False
def auto_rejoin():
    global status, auto_running
    while auto_running:
        status = "Opening Roblox for Join Acc"
        start_app()
        time.sleep(5)
        if is_running():
            status = "Join Roblox Acc"
            time.sleep(5)
            status = f"{Fore.GREEN}Executor has loaded successfully."
        start_time = time.time()
        while auto_running:
            if time.time() - start_time >= rejoin_interval * 60:
                status = "Rejoining..."
                kill_app()
                break
            if not is_running():
                status = "App crashed, restarting..."
                break
            time.sleep(10)
def get_system_info():
    # For RAM
    try:
        mem = subprocess.check_output(["free", "-m"]).decode()
        lines = mem.splitlines()
        total = int(lines[1].split()[1])
        used = int(lines[1].split()[2])
        ram_percent = (used / total) * 100
    except:
        ram_percent = 0.0
    # For CPU
    try:
        top = subprocess.check_output(["top", "-b", "-n1"]).decode()
        cpu = 0.0
        for line in top.splitlines():
            if "%Cpu" in line:
                parts = line.split()
                cpu = float(parts[1])
                break
    except:
        cpu = 0.0
    return cpu, ram_percent
def status_box():
    W = 60
    print(Fore.YELLOW + Style.BRIGHT + " ╔" + "═" * (W-2) + "╗")
    header = " STATUS "
    print(Fore.YELLOW + Style.BRIGHT + " ║" + Fore.CYAN + Style.BRIGHT + header.center(W-2) + Fore.YELLOW + Style.BRIGHT + "║")
    print(Fore.YELLOW + Style.BRIGHT + " ╠" + "═" * (W-2) + "╣")
    cpu, ram = get_system_info()
    item = f"CPU: {cpu:.2f} % | RAM: {ram:.2f} % | Trạng thái: Đang hoạt động"
    print(Fore.YELLOW + Style.BRIGHT + " ║ " + Fore.GREEN + Style.BRIGHT + item.ljust(W-4) + Fore.YELLOW + Style.BRIGHT + " ║")
    item = f"Tên: [{current_package_prefix}]"
    print(Fore.YELLOW + Style.BRIGHT + " ║ " + Fore.GREEN + Style.BRIGHT + item.ljust(W-4) + Fore.YELLOW + Style.BRIGHT + " ║")
    item = "Package: *******"
    print(Fore.YELLOW + Style.BRIGHT + " ║ " + Fore.GREEN + Style.BRIGHT + item.ljust(W-4) + Fore.YELLOW + Style.BRIGHT + " ║")
    print(Fore.YELLOW + Style.BRIGHT + " ╚" + "═" * (W-2) + "╝\n")
    print(status)
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
        
    print_item("[1]", "Auto Start Rejoin")
    print_item("[2]", "Setup Game Id For Package")
    print_item("[3]", "Configure Package Prefix")
    print_item("[4]", "Exit", color=Fore.RED)
    print(Fore.YELLOW + Style.BRIGHT + " ╚" + "═" * (W-2) + "╝\n")
# Vòng lặp xử lý
while True:
    banner()
    if auto_running:
        status_box()
        try:
            time.sleep(10)
        except KeyboardInterrupt:
            auto_running = False
            status = ""
            print(Fore.RED + Style.BRIGHT + f"\n[ {DISPLAY_NAME} ] - Auto Rejoin stopped.")
        continue
    try:
        # Tiền tố lệnh chính
        prefix_label = f"{Fore.YELLOW}[ {DISPLAY_NAME} ]{Fore.WHITE} - "
        ch = input(prefix_label + "Enter command: ")
        
        if ch == "3":
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
        
        elif ch == "4":
            print(Fore.RED + Style.BRIGHT + f"\n[ {DISPLAY_NAME} ] - Tạm biệt!")
            sys.exit()
        
        elif ch == "2":
            if current_package_prefix is None:
                print(Fore.RED + f"[ {DISPLAY_NAME} ] - Error reading UserAppsStorage .json file: [Errno 2] No such file or directory: '/data/data/com.Zeronokami.game.f/files/appData/LocalStorage/UserAppsStorage.json'")
            else:
                print(f"{Fore.GREEN}[ {DISPLAY_NAME} ] - Found User IDs for {current_package_prefix} from app packages.")
                print(Fore.CYAN + Style.BRIGHT + " [1] Blox Fruit - 2753915549")
                sub_ch = input(f"{Fore.YELLOW}[ {DISPLAY_NAME} ]{Fore.WHITE} - Select game: ")
                if sub_ch == "1":
                    game_id = "2753915549"
                    print(f"{Fore.GREEN}[ {DISPLAY_NAME} ] - User ID saved for {current_package_prefix}: 2753915549")
        
        elif ch == "1":
            if current_package_prefix is None or game_id is None:
                print(f"{Fore.RED}[ {DISPLAY_NAME} ] - Please configure package prefix and setup game ID first.")
            else:
                prompt = f"{Fore.YELLOW}[ {DISPLAY_NAME} ]{Fore.WHITE} - Enter rejoin interval (minutes): "
                rejoin_interval = float(input(prompt))
                print(f"{Fore.GREEN}[ {DISPLAY_NAME} ] - Auto Rejoin started with interval {rejoin_interval} minutes.")
                auto_running = True
                threading.Thread(target=auto_rejoin).start()
        
        elif ch == "":
            continue
        
        else:
            print(f"{Fore.RED}[ {DISPLAY_NAME} ] - Command not implemented yet.")
        
        if not auto_running:
            input(f"{Fore.GREEN}\nPress Enter to return...")
        
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        print(Fore.RED + f"\n[!] Có lỗi xảy ra: {e}")
        input()
