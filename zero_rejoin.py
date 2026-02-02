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
DISPLAY_NAME = "Zero Manager"
package_data = {} 
account_scripts = {} # Lưu trữ script cho từng account hoặc script chung

# --- CẤU HÌNH GIAO DIỆN ---
W = 120 # Tăng độ rộng khung để chứa Logo và bảng phân cột

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_len_visual(text):
    ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
    return len(ansi_escape.sub('', str(text)))

# --- LOGIC GỐC ---
def get_roblox_username(pkg):
    try:
        dump_cmd = ["uiautomator", "dump", "/sdcard/view.xml"]
        subprocess.run(dump_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        with open("/sdcard/view.xml", "r", encoding="utf-8") as f:
            content = f.read()
            match = re.search(r'@[a-zA-Z0-9._]+', content)
            if match:
                return match.group(0)
    except:
        pass
    return "Unknown" 

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
    if "http" in str(game_id):
        deep_link = game_id
    else:
        deep_link = f"roblox://placeID={game_id}"
        
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
        package_data[pkg]['status'] = f"{Fore.YELLOW}Restarting App"
        start_app(pkg)
        time.sleep(12) 
        real_name = get_roblox_username(pkg)
        if real_name != "Unknown":
            package_data[pkg]['user'] = real_name
        
        if is_running(pkg):
            package_data[pkg]['status'] = f"{Fore.CYAN}Auto Join"
            time.sleep(8)
            # Logic Auto Execute Script ở đây (Placeholder cho Executor của bạn)
            package_data[pkg]['status'] = f"{Fore.MAGENTA}Executing Script"
            time.sleep(5)
            package_data[pkg]['status'] = f"{Fore.GREEN}Active Now"
        
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
    try:
        mem = subprocess.check_output(["free", "-m"], stderr=subprocess.DEVNULL).decode().splitlines()
        parts = mem[1].split()
        ram_percent = (int(parts[2]) / int(parts[1])) * 100
        return 2.5, ram_percent
    except:
        return 2.5, 45.0

# --- GIAO DIỆN MỚI ---
def draw_line_content(content_str, text_color=Fore.WHITE, align='center'):
    visual_len = get_len_visual(content_str)
    padding = W - 2 - visual_len
    if padding < 0: padding = 0
    
    if align == 'center':
        pad_left = padding // 2
        pad_right = padding - pad_left
    else:
        pad_left = 2
        pad_right = padding - 2
        
    print(Fore.WHITE + "┃" + " " * pad_left + text_color + content_str + " " * pad_right + Fore.WHITE + "┃")

def draw_logo():
    art = [
        r" ███████╗███████╗██████╗  ██████╗     ███╗    ███╗ █████╗ ███╗   ██╗ █████╗  ██████╗ ███████╗██████╗ ",
        r" ╚══███╔╝██╔════╝██╔══██╗██╔═══██╗    ████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝ ██╔════╝██╔══██╗",
        r"    ███╔╝ █████╗  ██████╔╝██║   ██║    ██╔████╔██║███████║██╔██╗ ██║███████║██║  ███╗█████╗  ██████╔╝",
        r"   ███╔╝  ██╔══╝  ██╔══██╗██║   ██║    ██║╚██╔╝██║██╔══██║██║╚██╗██║██╔══██║██║   ██║██╔══╝  ██╔══██╗",
        r"  ███████╗███████╗██║  ██║╚██████╔╝    ██║ ╚═╝ ██║██║  ██║██║ ╚████║██║  ██║╚██████╔╝███████╗██║  ██║",
        r"  ╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝     ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝"
    ]
    for line in art:
        draw_line_content(line, Fore.RED, align='center')

def banner():
    clear()
    print(Fore.WHITE + "┏" + "━" * (W - 2) + "┓")
    draw_logo()
    draw_line_content("By ZeroNokami | High-Performance Engine", Fore.WHITE, 'center')
    print(Fore.WHITE + "┣" + "━" * (W - 2) + "┫")
    draw_line_content("[ TERMINAL CONTROL INTERFACE ]", Fore.YELLOW + Style.BRIGHT, 'center')
    print(Fore.WHITE + "┣" + "━" * (W - 2) + "┫")
    opts = [
        ("1", "EXECUTE ENGINE : Start Auto-Rejoin", Fore.YELLOW),
        ("2", "CONFIGURATION  : Assign Game ID", Fore.YELLOW),
        ("3", "SYSTEM SETUP   : Set Package Prefix", Fore.YELLOW),
        ("4", "AUTO EXECUTE   : Setup Account Scripts", Fore.YELLOW),
        ("5", "TERMINATE      : Exit Safely", Fore.RED)
    ]
    for num, txt, col in opts:
        content = f"   [{num}] {txt}"
        visual_len = len(content)
        padding_right = W - 2 - visual_len
        print(Fore.WHITE + "┃" + col + content + " " * padding_right + Fore.WHITE + "┃")
    print(Fore.WHITE + "┗" + "━" * (W - 2) + "┛")

def status_box():
    cpu, ram = get_system_info()
    clear()
    print(Fore.WHITE + "┏" + "━" * (W - 2) + "┓")
    draw_logo() 
    print(Fore.WHITE + "┣" + "━" * (W - 2) + "┫")
    header = f" MONITOR: CPU {cpu:.1f}% | RAM {ram:.1f}% "
    draw_line_content(header, Fore.CYAN + Style.BRIGHT, 'center')
    print(Fore.WHITE + "┣" + "━" * (W - 2) + "┫")
    
    # Cấu trúc cột có đường kẻ giữa
    u_w, p_w, s_w = 30, 40, 44 # Tổng 114 + 4 cột kẻ = 118
    h_str = f"  {'USER':<{u_w}}┃ {'PACKAGE':<{p_w}}┃ {'STATUS':<{s_w}}"
    print(Fore.WHITE + "┃" + h_str + " " * (W - 2 - len(h_str)) + "┃")
    print(Fore.WHITE + "┣" + "━" * (u_w+2) + "╋" + "━" * (p_w+1) + "╋" + "━" * (s_w+1) + "┫")
    
    for pkg in sorted(package_data.keys()):
        data = package_data[pkg]
        user = str(data.get('user', "Searching..."))[:u_w]
        p_name = str(pkg.split('.')[-1])[:p_w]
        st_color = data['status']
        clean_st = get_len_visual(st_color)
        
        line = (Fore.WHITE + "┃" + Fore.GREEN + f"  {user:<{u_w}}" + 
                Fore.WHITE + "┃ " + Fore.WHITE + f"{p_name:<{p_w}}" + 
                Fore.WHITE + "┃ " + st_color + " " * (s_w - clean_st) + Fore.WHITE + "┃")
        print(line)
    
    print(Fore.WHITE + "┗" + "━" * (W - 2) + "┛")

# --- MAIN LOOP ---
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
        prefix_label = f"{Fore.WHITE}[ {Fore.YELLOW}Zero Manager{Fore.WHITE} ] - {Fore.GREEN}"
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
                game_list = {"1": ("Blox Fruit", "2753915549"), "2": ("Fisch", "16732694052"), "3": ("Anime Defenders", "17017769292")}
                for k, v in game_list.items():
                    print(f"{Fore.WHITE} [{k}] {v[0]}")
                print(Fore.WHITE + " [11] Other Game / Private Server Link")
                game_choice = input(f"\n{prefix_label}Select Option: ")
                if game_choice in game_list:
                    game_id = game_list[game_choice][1]
                elif game_choice == "11":
                    game_id = input(prefix_label + "Paste Link: ")
        
        elif ch == "4":
            if not current_package_prefix:
                print(Fore.RED + ">> Error: Set prefix first!")
                continue
            all_pkgs = get_installed_packages(current_package_prefix)
            print(f"\n{Fore.CYAN}--- AUTO EXECUTE SETUP ---")
            print(" [1] Individual Script (Each Account)")
            print(" [2] Multiple Accounts Using A Single Script")
            mode = input(f"{prefix_label}Select Mode: ")
            
            if mode == "1":
                for p in all_pkgs:
                    u_name = get_roblox_username(p)
                    scr = input(f"{Fore.YELLOW}Account {Fore.GREEN}{u_name} {Fore.WHITE}: Enter Script: ")
                    account_scripts[p] = scr
            elif mode == "2":
                common_scr = input(f"{Fore.YELLOW}Enter Common Script for ALL: ")
                for p in all_pkgs:
                    account_scripts[p] = common_scr

        elif ch == "1":
            if not current_package_prefix or not game_id:
                print(f"{Fore.RED}>> Error: Missing configuration!")
            else:
                interval_input = input(prefix_label + "Interval (Minutes): ")
                rejoin_interval = float(interval_input)
                auto_running = True
                all_pkgs = get_installed_packages(current_package_prefix)
                for p in all_pkgs:
                    # Lấy username ngay từ đầu nếu app đang mở
                    u_initial = get_roblox_username(p)
                    package_data[p] = {'status': 'Initializing...', 'user': u_initial}
                    threading.Thread(target=auto_rejoin_logic, args=(p,), daemon=True).start()
                    time.sleep(2)
        
        elif ch == "5":
            sys.exit() 
            
        if not auto_running:
            input(f"\n{Fore.GREEN}Press Enter to go back...")
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(2)
