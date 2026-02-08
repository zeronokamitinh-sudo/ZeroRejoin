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

def get_W():
    try:
        columns = shutil.get_terminal_size().columns
        return columns if columns > 20 else 80
    except:
        return 80

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

# --- GIAO DIỆN (FIX ZOOM, MANAGER & CREDIT) ---
def draw_logo():
    Y = Fore.YELLOW + Style.BRIGHT
    # Fix MANAGER: Căn chỉnh lại các khoảng trắng để tránh biến dạng khi zoom
    lines = [
        "███████╗███████╗██████╗  ██████╗      ███╗   ███╗ █████╗ ███╗   ██╗ █████╗  ██████╗ ███████╗██████╗ ",
        "╚══███╔╝██╔════╝██╔══██╗██╔═══██╗      ████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝ ██╔════╝██╔══██╗",
        "  ███╔╝ █████╗  ██████╔╝██║   ██║      ██╔████╔██║███████║██╔██╗ ██║███████║██║  ███╗█████╗  ██████╔╝",
        " ███╔╝  ██╔══╝  ██╔══██╗██║   ██║      ██║╚██╔╝██║██╔══██║██║╚██╗██║██╔══██║██║   ██║██╔══╝  ██╔══██╗",
        "███████╗███████╗██║  ██║╚██████╔╝      ██║ ╚═╝ ██║██║  ██║██║ ╚████║██║  ██║╚██████╔╝███████╗██║  ██║",
        "╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝       ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝"
    ]
    W = get_W()
    logo_w = len(lines[0])
    pad = max(0, (W - logo_w) // 2)
    for line in lines:
        print(" " * pad + Y + line)

def banner():
    clear()
    Y = Fore.YELLOW + Style.BRIGHT
    W = get_W()
    draw_logo()
    
    # Header Info - Đã đổi theo yêu cầu
    print(f"\n{Fore.WHITE} - Version: {Fore.GREEN}3.6.7 | By ZeroNokami | Bugs Fixes By ZeroNokami")
    print(f"{Fore.WHITE} - Credit : {Fore.YELLOW}ZeroNokami\n")

    # Bảng Menu - Thu nhỏ menu_w để khung vào trong
    menu_w = 50
    margin = " " * max(0, (W - menu_w) // 2)
    
    print(margin + Y + "╭──────┬──────────────────────────────────────╮")
    print(margin + Y + "│  No  │ Service Name                         │")
    print(margin + Y + "├──────┼──────────────────────────────────────┤")
    
    menu_items = [
        ("1", "Start Auto Rejoin (Auto setup User ID)"),
        ("2", "Setup Game ID for Packages"),
        ("3", "Auto Login with Cookie"),
        ("4", "Enable Discord Webhook"),
        ("5", "Auto Check User Setup"),
        ("6", "Configure Package Prefix"),
        ("7", "Auto Change Android ID"),
    ]
    
    for no, name in menu_items:
        # Căn chỉnh văn bản bên trong khung gọn hơn
        print(margin + Y + f"│ {Fore.WHITE}[{no:^2}]{Y} │ {Fore.BLUE}{name:<36}{Y} │")
        
    print(margin + Y + "╰──────┴──────────────────────────────────────╯")
    print(f"\n{margin}{Fore.WHITE}[ {Y}ZeroNokami{Fore.WHITE} ] - {Fore.YELLOW}Enter command: ", end="")

def status_box():
    clear()
    Y = Fore.YELLOW + Style.BRIGHT
    W = get_W()
    draw_logo()
    print(f"\n{Fore.CYAN + Style.BRIGHT} MONITOR: SYSTEM ACTIVE\n")
    
    u_w, p_w = int(W * 0.25), int(W * 0.35)
    rem_s = max(10, W - u_w - p_w - 5)
    
    print(Fore.WHITE + f" {'USER':<{u_w}} │ {'PACKAGE':<{p_w}} │ {'STATUS':<{rem_s}}")
    print(Y + "─" * W)
    
    for pkg in sorted(package_data.keys()):
        data = package_data[pkg]
        user_str = str(data.get('user', "Scanning..."))[:u_w-1]
        p_name = str(pkg.split('.')[-1])[:p_w-1]
        st_text = data['status']
        print(f" {Fore.GREEN}{user_str:<{u_w}} {Fore.WHITE}│ {p_name:<{p_w}} │ {st_text}")

# --- MAIN LOOP (GIỮ NGUYÊN LOGIC) ---
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
        
        if ch == "6":
            new_prefix = input(f"{Fore.YELLOW}>> Enter Package Prefix: ")
            if new_prefix:
                current_package_prefix = new_prefix
                found = get_installed_packages(new_prefix)
                print(f"{Fore.GREEN}>> Detected {len(found)} matching packages.")
        
        elif ch == "2":
            if not current_package_prefix:
                print(Fore.RED + ">> Error: Please set package prefix (Option 6) first!")
            else:
                print(Fore.CYAN + "\n --- SELECT GAME ---")
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
                    print(f"{Fore.WHITE} [{k}] {v[0]}")
                print(Fore.WHITE + " [11] Other Game / Private Server Link")
                
                gc = input(f"\n{Fore.YELLOW}>> Select Option: ")
                if gc in game_list:
                    game_id = game_list[gc][1]
                    print(f"{Fore.GREEN}>> Linked: {game_list[gc][0]}")
                elif gc == "11":
                    game_id = input(f"{Fore.YELLOW}>> Paste Link: ")
        
        elif ch == "1":
            if not current_package_prefix or not game_id:
                print(f"{Fore.RED}>> Error: Configuration missing!")
            else:
                iv = input(f"{Fore.YELLOW}>> Interval (Min): ")
                try:
                    rejoin_interval = float(iv)
                    auto_running = True
                    pkgs = get_installed_packages(current_package_prefix)
                    for p in pkgs:
                        package_data[p] = {'status': 'Starting...', 'user': "Scanning..."}
                        threading.Thread(target=auto_rejoin_logic, args=(p,), daemon=True).start()
                except: print(Fore.RED + ">> Error!")
        
        elif ch in ["3", "4", "5", "7"]:
            print(f"{Fore.RED}>> Feature coming soon in this Version!")
            time.sleep(1)

        if not auto_running: input(f"\n{Fore.GREEN}Press Enter to continue...")
    except Exception as e:
        print(f"Error: {e}")
        input()
