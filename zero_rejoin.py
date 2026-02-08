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

# Global Variables (GIỮ NGUYÊN 100%)
current_package_prefix = None
game_id = None
rejoin_interval = None
auto_running = False
DISPLAY_NAME = "Zero Manager"
package_data = {}

# Cố định độ rộng để chống vỡ khung khi zoom
FIXED_WIDTH = 80
FIXED_MARGIN = "      " # Tạo khoảng cách lề trái để đẩy khung vào trong

def get_W():
    # Sử dụng độ rộng cố định để giao diện không bị nhảy khi zoom màn hình
    return FIXED_WIDTH

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# --- LOGIC GỐC (TUYỆT ĐỐI KHÔNG SỬA) ---
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
            if package_data[pkg]['user'] == "Scanning...":
                 r_name = get_roblox_username(pkg)
                 if r_name: package_data[pkg]['user'] = r_name
            time.sleep(5)

# --- GIAO DIỆN (KHÔI PHỤC LOGO GỐC & FIX LỖI ZOOM) ---

def draw_logo():
    Y = Fore.YELLOW + Style.BRIGHT
    # Đã khôi phục đúng định dạng chữ của bạn
    lines = [
        "███████╗███████╗██████╗  ██████╗      ███╗   ███╗ █████╗ ███╗   ██╗ █████╗  ██████╗ ███████╗██████╗ ",
        "╚══███╔╝██╔════╝██╔══██╗██╔═══██╗      ████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝ ██╔════╝██╔══██╗",
        "  ███╔╝ █████╗  ██████╔╝██║   ██║      ██╔████╔██║███████║██╔██╗ ██║███████║██║  ███╗█████╗  ██████╔╝",
        " ███╔╝  ██╔══╝  ██╔══██╗██║   ██║      ██║╚██╔╝██║██╔══██║██║╚██╗██║██╔══██║██║   ██║██╔══╝  ██╔══██╗",
        "███████╗███████╗██║  ██║╚██████╔╝      ██║ ╚═╝ ██║██║  ██║██║ ╚████║██║  ██║╚██████╔╝███████╗██║  ██║",
        "╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝       ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝"
    ]
    for line in lines:
        print(FIXED_MARGIN + Y + line)

def banner():
    clear()
    Y = Fore.YELLOW + Style.BRIGHT
    draw_logo()
    
    print(f"\n{FIXED_MARGIN}{Fore.WHITE} - Version: {Fore.GREEN}3.6.7 | By ZeroNokami | Bugs Fixes By ZeroNokami")
    print(f"{FIXED_MARGIN}{Fore.WHITE} - Credit : {Fore.YELLOW}ZeroNokami\n")

    # Khung menu sử dụng chiều rộng cố định để không bị vỡ khi zoom
    print(FIXED_MARGIN + Y + "╭──────┬──────────────────────────────────────────╮")
    print(FIXED_MARGIN + Y + "│  No  │ Service Name                             │")
    print(FIXED_MARGIN + Y + "├──────┼──────────────────────────────────────────┤")
    
    menu_items = [
        ("1", "Start Auto Rejoin (Auto setup User ID)"),
        ("2", "Setup Game ID for Packages"),
        ("3", "Auto Login with Cookie"),
        ("4", "Enable Discord Webhook"),
        ("5", "Configure Package Prefix"),
    ]
    
    for no, name in menu_items:
        print(FIXED_MARGIN + Y + f"│ {Fore.WHITE}[{no:^2}]{Y} │ {Fore.BLUE}{name:<40}{Y} │")
        
    print(FIXED_MARGIN + Y + "╰──────┴──────────────────────────────────────────╯")
    print(f"\n{FIXED_MARGIN}{Fore.WHITE}[ {Y}ZeroNokami{Fore.WHITE} ] - {Fore.YELLOW}Enter command: ", end="")

def status_box():
    clear()
    Y = Fore.YELLOW + Style.BRIGHT
    W = get_W()
    draw_logo()
    print(f"\n{FIXED_MARGIN}{Fore.CYAN + Style.BRIGHT} MONITOR: SYSTEM ACTIVE\n")
    
    # Cân đối tỷ lệ cột dựa trên FIXED_WIDTH
    u_w = 20
    p_w = 25
    rem_s = 25
    
    print(FIXED_MARGIN + Fore.WHITE + f" {'USER':<{u_w}} │ {'PACKAGE':<{p_w}} │ {'STATUS':<{rem_s}}")
    print(FIXED_MARGIN + Y + "─" * (u_w + p_w + rem_s + 6))
    
    for pkg in sorted(package_data.keys()):
        data = package_data[pkg]
        user_str = str(data.get('user', "Scanning..."))[:u_w-1]
        p_name = str(pkg.split('.')[-1])[:p_w-1]
        st_text = data['status']
        # In kèm lề để đẩy vào trong
        print(f"{FIXED_MARGIN} {Fore.GREEN}{user_str:<{u_w}} {Fore.WHITE}│ {p_name:<{p_w}} │ {st_text}")

# --- MAIN LOOP (GIỮ NGUYÊN 100%) ---
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
        ch = input()
        
        if ch == "5":
            new_prefix = input(f"\n{FIXED_MARGIN}{Fore.YELLOW}>> Enter Package Prefix: ")
            if new_prefix:
                current_package_prefix = new_prefix
                found = get_installed_packages(new_prefix)
                print(f"{FIXED_MARGIN}{Fore.GREEN}>> Detected {len(found)} matching packages.")
        
        elif ch == "2":
            if not current_package_prefix:
                print(f"\n{FIXED_MARGIN}{Fore.RED}>> Error: Please set package prefix first!")
            else:
                print(f"\n{FIXED_MARGIN}{Fore.CYAN} --- SELECT GAME ---")
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
                for k, v in game_list.items():
                    print(f"{FIXED_MARGIN}{Fore.WHITE} [{k}] {v[0]}")
                print(f"{FIXED_MARGIN}{Fore.WHITE} [11] Other Game / Private Server Link")
                
                gc = input(f"\n{FIXED_MARGIN}{Fore.YELLOW}>> Select Option: ")
                if gc in game_list:
                    game_id = game_list[gc][1]
                    print(f"{FIXED_MARGIN}{Fore.GREEN}>> Linked: {game_list[gc][0]}")
                elif gc == "11":
                    game_id = input(f"{FIXED_MARGIN}{Fore.YELLOW}>> Paste Link: ")
        
        elif ch == "1":
            if not current_package_prefix or not game_id:
                print(f"\n{FIXED_MARGIN}{Fore.RED}>> Error: Configuration missing!")
            else:
                iv = input(f"\n{FIXED_MARGIN}{Fore.YELLOW}>> Interval (Min): ")
                try:
                    rejoin_interval = float(iv)
                    auto_running = True
                    pkgs = get_installed_packages(current_package_prefix)
                    for p in pkgs:
                        package_data[p] = {'status': 'Starting...', 'user': "Scanning..."}
                        threading.Thread(target=auto_rejoin_logic, args=(p,), daemon=True).start()
                except: print(f"{FIXED_MARGIN}{Fore.RED}>> Error!")
        
        elif ch in ["3", "4", "5", "7"]:
            print(f"\n{FIXED_MARGIN}{Fore.RED}>> Feature coming soon in this Version!")
            time.sleep(1)

        if not auto_running: input(f"\n{FIXED_MARGIN}{Fore.GREEN}Press Enter to continue...")
    except Exception as e:
        print(f"Error: {e}")
        input()
