import os, time, sys, subprocess, threading, re

# --- AUTO DEPENDENCY FIX ---
def install_dependencies():
    try:
        from colorama import init, Fore, Style
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama"], 
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.execv(sys.executable, ['python'] + sys.argv)

install_dependencies()
from colorama import init, Fore, Style

init(autoreset=True)

# Global Variables
current_package_prefix = None 
game_id = None
rejoin_interval = None
auto_running = False
DISPLAY_NAME = "ZeroNokami"
package_data = {} 

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_roblox_username(pkg):
    """Quét giao diện để tìm Username thực tế"""
    try:
        # Dump giao diện ra file xml
        subprocess.run(["uiautomator", "dump", "/sdcard/view.xml"], 
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        with open("/sdcard/view.xml", "r", encoding="utf-8") as f:
            content = f.read()
            # Tìm pattern @username (thường thấy trong Roblox mobile)
            match = re.search(r'@[a-zA-Z0-9._]+', content)
            if match:
                return match.group(0)
    except:
        pass
    # Nếu chưa quét được, trả về placeholder chờ cập nhật
    return "Scanning..."

def get_installed_packages(prefix):
    try:
        output = subprocess.check_output(["pm", "list", "packages", prefix], stderr=subprocess.DEVNULL).decode()
        pkgs = [line.split(':')[-1].strip() for line in output.splitlines() if line.strip()]
        return pkgs
    except:
        return []

def kill_app(pkg):
    subprocess.call(["am", "force-stop", pkg], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def start_app(pkg):
    kill_app(pkg)
    time.sleep(1) 
    deep_link = game_id if "http" in str(game_id) else f"roblox://placeID={game_id}"
    subprocess.call([
        "am", "start", "--user", "0", 
        "-a", "android.intent.action.VIEW", 
        "-d", deep_link, pkg
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def is_running(pkg):
    try:
        output = subprocess.check_output(["ps", "-A"], stderr=subprocess.DEVNULL).decode()
        return pkg in output
    except:
        return False

def auto_rejoin_logic(pkg):
    global auto_running
    while auto_running:
        package_data[pkg]['status'] = f"{Fore.YELLOW}Restarting..."
        start_app(pkg)
        
        # Đợi app load để lấy username thật
        time.sleep(15) 
        real_user = get_roblox_username(pkg)
        if real_user != "Scanning...":
            package_data[pkg]['user'] = real_user
        
        if is_running(pkg):
            package_data[pkg]['status'] = f"{Fore.CYAN}Auto Join"
            time.sleep(8)
            package_data[pkg]['status'] = f"{Fore.MAGENTA}Executor"
            time.sleep(5)
            package_data[pkg]['status'] = f"{Fore.GREEN}Active Now"
            
        start_time = time.time()
        while auto_running:
            if time.time() - start_time >= rejoin_interval * 60:
                break
            if not is_running(pkg):
                package_data[pkg]['status'] = f"{Fore.RED}Crashed!"
                break
            time.sleep(5)

def get_system_info():
    try:
        # Lấy kích thước terminal hiện tại để chống biến dạng
        columns, rows = os.get_terminal_size()
        mem = subprocess.check_output(["free", "-m"], stderr=subprocess.DEVNULL).decode().splitlines()
        parts = mem[1].split()
        ram_percent = (int(parts[2]) / int(parts[1])) * 100
        return 2.5, ram_percent, columns
    except:
        return 2.5, 45.0, 80

def status_box():
    cpu, ram, W = get_system_info()
    # Giới hạn chiều rộng tối thiểu để không bị vỡ chữ
    if W < 80: W = 80
    
    clear()
    # Header linh hoạt theo chiều rộng màn hình
    print(Fore.CYAN + "╔" + "═"*(W-2) + "╗")
    title = f" MONITORING SYSTEM - CPU: {cpu:.1f}% | RAM: {ram:.1f}% "
    print(Fore.CYAN + "║" + Fore.WHITE + Style.BRIGHT + title.center(W-2) + Fore.CYAN + "║")
    
    # Chia cột tỉ lệ: 30% - 40% - 30%
    w1, w2, w3 = int(W*0.3), int(W*0.35), (W - int(W*0.3) - int(W*0.35) - 4)
    
    print(Fore.CYAN + "╠" + "═"*w1 + "╦" + "═"*w2 + "╦" + "═"*w3 + "╣")
    print(Fore.CYAN + "║" + f"{Fore.YELLOW} Name ".center(w1) + "║" + f"{Fore.YELLOW} Package ID ".center(w2) + "║" + f"{Fore.YELLOW} Status ".center(w3) + "║")
    print(Fore.CYAN + "╠" + "═"*w1 + "╬" + "═"*w2 + "╬" + "═"*w3 + "╣")
    
    for pkg in sorted(package_data.keys()):
        data = package_data[pkg]
        user = data.get('user', "Scanning...")
        st = data['status']
        
        # Cắt bớt package name nếu màn hình quá nhỏ
        display_pkg = (pkg[:w2-2] + "..") if len(pkg) > w2-2 else pkg
        
        print(Fore.CYAN + "║" + f"{Fore.WHITE} {user:^{w1-2}} " + Fore.CYAN + "║" + 
              f"{Fore.WHITE} {display_pkg:^{w2-2}} " + Fore.CYAN + "║" + 
              f" {st:^{w3-2}} " + Fore.CYAN + "║")
        
    print(Fore.CYAN + "╚" + "═"*w1 + "╩" + "═"*w2 + "╩" + "═"*w3 + "╝")

def banner():
    clear()
    columns, _ = os.get_terminal_size()
    logo = f"""{Fore.CYAN}{Style.BRIGHT}
    ███████╗███████╗██████╗  ██████╗ ███╗   ██╗ ██████╗ ██╗  ██╗ █████╗ ███╗   ███╗██╗
    ╚══███╔╝██╔════╝██╔══██╗██╔═══██╗████╗  ██║██╔═══██╗██║ ██╔╝██╔══██╗████╗ ████║██║
      ███╔╝ █████╗  ██████╔╝██║   ██║██╔██╗ ██║██║   ██║█████╔╝ ███████║██╔████╔██║██║
     ███╔╝  ██╔══╝  ██╔══██╗██║   ██║██║╚██╗██║██║   ██║██╔═██╗ ██╔══██║██║╚██╔╝██║██║
    ███████╗███████╗██║  ██║╚██████╔╝██║ ╚████║╚██████╔╝██║  ██╗██║  ██║██║ ╚═╝ ██║██║
    ╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝
    """
    # Căn giữa logo theo chiều rộng màn hình
    for line in logo.split('\n'):
        print(line.center(columns))

    W = 60 if columns > 60 else columns
    print(Fore.BLUE + "╔" + "═" * (W-2) + "╗")
    header = f" {DISPLAY_NAME} - CONTROL PANEL "
    print(Fore.BLUE + "║" + Fore.WHITE + Style.BRIGHT + header.center(W-2) + Fore.BLUE + "║")
    print(Fore.BLUE + "╠" + "═" * (W-2) + "╣")
    
    def print_item(cmd, desc, color=Fore.GREEN):
        content = f"  {Fore.YELLOW}{cmd}  {color}{desc}"
        # Tính toán padding để không bị tràn khung
        padding = (W - 4)
        print(Fore.BLUE + "║" + content.ljust(padding + 14) + Fore.BLUE + "║")
        
    print_item("[1]", "Start Auto-Rejoin Engine")
    print_item("[2]", "Assign Game ID / Link")
    print_item("[3]", "Set Package Prefix")
    print_item("[4]", "Exit System", color=Fore.RED)
    print(Fore.BLUE + "╚" + "═" * (W-2) + "╝\n")

# Main Loop (giữ nguyên logic gốc)
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
        prefix_label = f"{Fore.WHITE}[ {Fore.CYAN}{DISPLAY_NAME}{Fore.WHITE} ] - {Fore.GREEN}"
        ch = input(prefix_label + "Command Line: ")
        
        if ch == "3":
            new_prefix = input(prefix_label + "Enter Package Prefix: ")
            if new_prefix:
                current_package_prefix = new_prefix
                found = get_installed_packages(new_prefix)
                print(f"{Fore.GREEN}>> Detected {len(found)} matching packages.")
        
        elif ch == "2":
            if not current_package_prefix:
                print(Fore.RED + ">> Error: Please set package prefix first!")
            else:
                print(Fore.CYAN + "\n --- SELECT GAME ---")
                game_list = {
                    "1": ("Blox Fruit", "2753915549"),
                    "2": ("99 Night In The Forest", "79546208627805"),
                    "3": ("Deals Rails", "116495829188952"),
                    "4": ("Fisch", "16732694052"),
                    "5": ("Anime Defenders", "17017769292"),
                    "10": ("King Legacy", "4520749081"),
                }
                for k, v in game_list.items():
                    print(f"{Fore.WHITE} [{k}] {v[0]}")
                
                game_choice = input(f"\n{prefix_label}Select Option: ")
                if game_choice in game_list:
                    game_id = game_list[game_choice][1]
                    print(f"{Fore.GREEN}>> Linked: {game_list[game_choice][0]}")
        
        elif ch == "1":
            if not current_package_prefix or not game_id:
                print(f"{Fore.RED}>> Error: Missing configuration!")
            else:
                interval_input = input(prefix_label + "Interval (Minutes): ")
                rejoin_interval = float(interval_input)
                auto_running = True
                all_pkgs = get_installed_packages(current_package_prefix)
                
                if all_pkgs:
                    for p in all_pkgs:
                        package_data[p] = {
                            'status': 'Starting...',
                            'user': 'Waiting...' 
                        }
                        threading.Thread(target=auto_rejoin_logic, args=(p,), daemon=True).start()
                        time.sleep(1)
        
        elif ch == "4":
            sys.exit()
            
        if not auto_running:
            input(f"\n{Fore.GREEN}Press Enter to go back...")
    except Exception:
        pass
