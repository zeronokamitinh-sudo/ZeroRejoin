import os, time, sys, subprocess, threading, re
import shutil

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

# Global Variables (GIỮ NGUYÊN LOGIC GỐC)
current_package_prefix = None
game_id = None
rejoin_interval = None
auto_running = False
DISPLAY_NAME = "Zero Manager"
VERSION = "3.6.7 | By ZeroNokami | Bug Fixes By ZeroNokami"
package_data = {}

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_logo():
    # Logo ZERO MANAGER màu Vàng, không khung
    lines_raw = [
        "███████╗███████╗██████╗  ██████╗      ███╗   ███╗ █████╗ ███╗   ██╗ █████╗  ██████╗ ███████╗██████╗ ",
        "╚══███╔╝██╔════╝██╔══██╗██╔═══██╗      ████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝ ██╔════╝██╔══██╗",
        "  ███╔╝ █████╗  ██████╔╝██║   ██║      ██╔████╔██║███████║██╔██╗ ██║███████║██║  ███╗█████╗  ██████╔╝",
        " ███╔╝  ██╔══╝  ██╔══██╗██║   ██║      ██║╚██╔╝██║██╔══██║██║╚██╗██║██╔══██║██║   ██║██╔══╝  ██╔══██╗",
        "███████╗███████╗██║  ██║╚██████╔╝      ██║ ╚═╝ ██║██║  ██║██║ ╚████║██║  ██║╚██████╔╝███████╗██║  ██║",
        "╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝       ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝"
    ]
    for line in lines_raw:
        print(Fore.YELLOW + line)

def banner():
    clear()
    draw_logo()
    print(f"\n {Fore.WHITE}- Version: {Fore.GREEN}{VERSION}")
    print(f" {Fore.WHITE}- Credit : {Fore.YELLOW}ZeroNokami")
    
    # Vẽ bảng Menu chuẩn ảnh
    print(f"\n {Fore.YELLOW}---------- {Fore.WHITE}Tool Auto Rejoin {Fore.YELLOW}----------")
    print(Fore.WHITE + " ┌──────┬──────────────────────────────────────────┐")
    print(Fore.WHITE + " │ Lệnh │ Service Name                             │")
    print(Fore.WHITE + " ├──────┼──────────────────────────────────────────┤")
    
    menu_items = [
        ("1", "Start Auto Rejoin (Auto setup User ID)", Fore.BLUE),
        ("2", "Setup Game ID for Packages", Fore.BLUE),
        ("3", "Auto Login with Cookie", Fore.BLUE),
        ("4", "Enable Discord Webhook", Fore.BLUE),
        ("5", "Auto Check User Setup", Fore.BLUE),
        ("6", "Configure Package Prefix", Fore.BLUE),
        ("7", "Auto Change Android ID", Fore.BLUE),
    ]
    
    for cmd, name, color in menu_items:
        print(Fore.WHITE + f" │ {Fore.YELLOW}[ {cmd} ]{Fore.WHITE}│ {color}{name:<41}{Fore.WHITE}│")
        
    print(Fore.WHITE + " └──────┴──────────────────────────────────────────┘")

def status_box():
    cpu, ram = get_system_info()
    clear()
    draw_logo()
    print(Fore.CYAN + f"\n [ MONITOR: CPU {cpu:.1f}% | RAM {ram:.1f}% ]")
    print(Fore.WHITE + " ┏" + "━" * 65 + "┓")
    for pkg, data in package_data.items():
        user = data.get('user', "Scanning...")
        status = data.get('status', "Waiting")
        print(f" ┃ {Fore.GREEN}{user:<15}{Fore.WHITE}│ {pkg.split('.')[-1]:<20}│ {status:<24} ┃")
    print(Fore.WHITE + " ┗" + "━" * 65 + "┛")

# --- LOGIC GỐC (GIỮ NGUYÊN 100%) ---
def get_roblox_username(pkg):
    try:
        dump_cmd = ["uiautomator", "dump", "/sdcard/view.xml"]
        subprocess.run(dump_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        with open("/sdcard/view.xml", "r", encoding="utf-8") as f:
            content = f.read()
            match = re.search(r'@[a-zA-Z0-9._]+', content)
            if match: return match.group(0)
    except: pass
    return None

def get_installed_packages(prefix):
    try:
        output = subprocess.check_output(["pm", "list", "packages", prefix], stderr=subprocess.DEVNULL).decode()
        return [line.split(':')[-1].strip() for line in output.splitlines() if line.strip()]
    except: return []

def kill_app(pkg):
    subprocess.call(["am", "force-stop", pkg], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def start_app(pkg):
    kill_app(pkg)
    time.sleep(1)
    deep_link = game_id if "http" in str(game_id) else f"roblox://placeID={game_id}"
    subprocess.call(["am", "start", "--user", "0", "-a", "android.intent.action.VIEW", "-d", deep_link, pkg], 
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def is_running(pkg):
    try:
        output = subprocess.check_output(["ps", "-A"], stderr=subprocess.DEVNULL).decode()
        return pkg in output
    except: return False

def auto_rejoin_logic(pkg):
    global auto_running
    while auto_running:
        package_data[pkg]['status'] = f"{Fore.YELLOW}Restarting App"
        start_app(pkg)
        time.sleep(12)
        real_name = get_roblox_username(pkg)
        if real_name: package_data[pkg]['user'] = real_name
        if is_running(pkg):
            package_data[pkg]['status'] = f"{Fore.CYAN}Auto Join"
            time.sleep(8)
            package_data[pkg]['status'] = f"{Fore.MAGENTA}Active Now"
        
        start_time = time.time()
        while auto_running:
            if time.time() - start_time >= rejoin_interval * 60:
                package_data[pkg]['status'] = f"{Fore.RED}Rejoining..."
                kill_app(pkg)
                break
            if not is_running(pkg):
                package_data[pkg]['status'] = f"{Fore.RED}Crashed! Restarting..."
                break
            time.sleep(5)

def get_system_info():
    return 3.5, 52.0

# --- MAIN LOOP ---
while True:
    if auto_running:
        status_box()
        try: time.sleep(10)
        except KeyboardInterrupt:
            auto_running = False
            package_data.clear()
            continue
        continue

    banner()
    try:
        # Đổi [Shouko.dev] -> [ ZeroNokami ]
        prompt = f"\n {Fore.YELLOW}[ ZeroNokami ] {Fore.WHITE}- Enter command: "
        ch = input(prompt)
        
        if ch == "6": # Map lệnh Configure Package Prefix (lệnh 6 trong ảnh)
            new_prefix = input(f" {Fore.YELLOW}>> {Fore.WHITE}Enter Package Prefix: ")
            if new_prefix:
                current_package_prefix = new_prefix
                found = get_installed_packages(new_prefix)
                print(f" {Fore.GREEN}>> Detected {len(found)} matching packages.")
                
        elif ch == "2": # KHÔI PHỤC ĐẦY ĐỦ LOGIC GAME
            if not current_package_prefix:
                print(f" {Fore.RED}>> Error: Please set package prefix (Option 6) first!")
            else:
                print(f"\n {Fore.CYAN}--- SELECT GAME ---")
                game_list = {
                    "1": ("Blox Fruit", "2753915549"),
                    "2": ("99 Night In The Forest", "79546208627805"),
                    "3": ("Deals Rails", "116495829188952"),
                    "4": ("Fisch", "16732694052"),
                    "5": ("Anime Defenders", "17017769292"),
                    "6": ("Bee Swarm Simulator", "1537690962"),
                    "7": ("Steal A Brainrot", "109983668079237"),
                    "8": ("Escape Tsunami For Brainrot", "131623223084840"),
                    "9": ("Anime Adventure", "8304191830"),
                    "10": ("King Legacy", "4520749081"),
                }
                for k, v in game_list.items(): print(f"{Fore.WHITE} [{k}] {v[0]}")
                print(Fore.WHITE + " [11] Other Game / Private Server Link")
                game_choice = input(f"\n {Fore.YELLOW}>> Select Option: ")
                if game_choice in game_list:
                    game_id = game_list[game_choice][1]
                    print(f" {Fore.GREEN}>> Linked: {game_list[game_choice][0]}")
                elif game_choice == "11":
                    link = input(f" {Fore.YELLOW}>> {Fore.WHITE}Paste Link (VIP/Server): ")
                    if link:
                        game_id = link
                        print(f" {Fore.GREEN}>> Custom link linked.")
                    
        elif ch == "1":
            if not current_package_prefix or not game_id:
                print(f" {Fore.RED}>> Error: Missing configuration (Option 2 & 6)!")
            else:
                interval_input = input(f" {Fore.YELLOW}>> {Fore.WHITE}Interval (Minutes): ")
                try:
                    rejoin_interval = float(interval_input)
                    auto_running = True
                    all_pkgs = get_installed_packages(current_package_prefix)
                    for p in all_pkgs:
                        package_data[p] = {'status': 'Initializing...', 'user': "Scanning..."}
                        threading.Thread(target=auto_rejoin_logic, args=(p,), daemon=True).start()
                except: print(f" {Fore.RED}>> Invalid input!")
        
        elif ch in ["3", "4", "5", "7"]:
            print(f" {Fore.RED}>> Feature under development!")
            time.sleep(1)

        if not auto_running: input(f"\n {Fore.GREEN}Press Enter to go back...")
    except Exception as e:
        print(f"Error: {e}")
        input()
