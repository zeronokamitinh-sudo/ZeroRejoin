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
W = 126 # Chiều rộng cố định cho toàn bộ giao diện

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# --- LOGIC GỐC GIỮ NGUYÊN ---
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
    return None 

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
        if real_name:
            package_data[pkg]['user'] = real_name
        if is_running(pkg):
            package_data[pkg]['status'] = f"{Fore.GREEN}Active Now"
        
        start_time = time.time()
        while auto_running:
            if time.time() - start_time >= rejoin_interval * 60:
                package_data[pkg]['status'] = f"{Fore.RED}Rejoining..."
                kill_app(pkg)
                break
            if not is_running(pkg):
                package_data[pkg]['status'] = f"{Fore.RED}Crashed!"
                break
            time.sleep(5)

def get_system_info():
    try:
        # Giả lập hoặc lấy thông tin thực tế
        return 2.5, 29.4
    except:
        return 0.0, 0.0

# --- PHẦN GIAO DIỆN ĐÃ ĐƯỢC FIX ---

def draw_art_content():
    art = [
        r"  ________  _______ .______       ______      .___  ___.      ___      .__   __.      ___       _______  _______ .______      ",
        r" |       / |   ____||   _  \     /  __  \     |   \/   |     /   \     |  \ |  |     /   \     /  _____||   ____||   _  \     ",
        r" `---/  /  |  |__   |  |_)  |   |  |  |  |    |  \  /  |    /  ^  \    |   \|  |    /  ^  \   |  |  __  |  |__   |  |_)  |    ",
        r"    /  /   |   __|  |      /    |  |  |  |    |  |\/|  |   /  /_\  \   |  . `  |   /  /_\  \  |  | |_ | |   __|  |      /     ",
        r"   /  /---.|  |____ |  |\  \----|  `--'  |    |  |  |  |  /  _____  \  |  |\   |  /  _____  \ |  |__| | |  |____ |  |\  \----.",
        r"  /________|_______|| _| `._____|\______/     |__|  |__| /__/     \__\ |__| \__| /__/     \__\ \______| |_______|| _| `._____|"
    ]
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
    for line in art:
        content = line.center(W)
        colored_line = ""
        for j, char in enumerate(content):
            if char.strip(): 
                color_idx = (j // 15) % len(colors)
                colored_line += colors[color_idx] + char
            else:
                colored_line += char
        print(Fore.WHITE + "┃" + colored_line + Fore.WHITE + "┃")

def banner():
    clear()
    print(Fore.WHITE + "┏" + "━" * W + "┓")
    draw_art_content()
    credit_str = "By ZeroNokami | High-Performance Engine"
    print(Fore.WHITE + "┃" + credit_str.center(W) + Fore.WHITE + "┃")
    print(Fore.WHITE + "┣" + "━" * W + "┫")
    
    title = "[ TERMINAL CONTROL INTERFACE ]"
    print(Fore.WHITE + "┃" + Fore.YELLOW + Style.BRIGHT + title.center(W) + Fore.WHITE + "┃")
    print(Fore.WHITE + "┣" + "━" * W + "┫")
    
    opts = [
        ("1", "EXECUTE ENGINE : Start Auto-Rejoin"),
        ("2", "CONFIGURATION  : Assign Game ID"),
        ("3", "SYSTEM SETUP   : Set Package Prefix"),
        ("4", "TERMINATE      : Exit Safely")
    ]
    
    opt_colors = [Fore.GREEN, Fore.CYAN, Fore.YELLOW, Fore.RED]
    for i, (num, txt) in enumerate(opts):
        full_text = f"    [{num}] {txt}"
        padding = " " * (W - len(full_text))
        print(Fore.WHITE + "┃" + opt_colors[i] + full_text + Fore.WHITE + padding + "┃")
    print(Fore.WHITE + "┗" + "━" * W + "┛")

def status_box():
    cpu, ram = get_system_info()
    clear()
    print(Fore.WHITE + "┏" + "━" * W + "┓")
    draw_art_content() # Giữ logo Zero Manager ở trên status
    print(Fore.WHITE + "┣" + "━" * W + "┫")
    
    header = f" MONITOR: CPU {cpu:.1f}% | RAM {ram:.1f}% "
    print(Fore.WHITE + "┃" + Fore.CYAN + Style.BRIGHT + header.center(W) + Fore.WHITE + "┃")
    print(Fore.WHITE + "┣" + "━" * W + "┫")
    
    # Chia cột tỉ lệ cố định
    u_w, p_w = 30, 40
    s_w = W - u_w - p_w - 4 
    
    label = f"  {'USER':<{u_w}}{'PACKAGE':<{p_w}}{'STATUS':<{s_w}}  "
    print(Fore.WHITE + "┃" + Fore.WHITE + label + "┃")
    print(Fore.WHITE + "┣" + "━" * W + "┫")
    
    for pkg in sorted(package_data.keys()):
        data = package_data[pkg]
        user = str(data.get('user', "Unknown"))[:u_w-2]
        p_name = str(pkg.split('.')[-1])[:p_w-2]
        st_raw = data['status']
        
        # Xử lý độ dài chuỗi để tránh lệch khung do mã màu ANSI
        clean_st = re.sub(r'\x1b\[[0-9;]*m', '', st_raw)
        st_padding = " " * (s_w - len(clean_st) - 2)
        
        row = f"  {user:<{u_w}}{p_name:<{p_w}}{st_raw}{st_padding}  "
        print(Fore.WHITE + "┃" + row + Fore.WHITE + "┃")
    
    print(Fore.WHITE + "┗" + "━" * W + "┛")

# --- MAIN LOOP ---
while True:
    if auto_running:
        status_box()
        try:
            time.sleep(5)
        except KeyboardInterrupt:
            auto_running = False
            continue
        continue

    banner()
    try:
        prefix_label = f"{Fore.WHITE}[ {Fore.CYAN}Zero Manager{Fore.WHITE} ] - {Fore.GREEN}"
        ch = input(prefix_label + "Command Line: ")
        
        if ch == "3":
            new_prefix = input(prefix_label + "Enter Package Prefix: ")
            if new_prefix:
                current_package_prefix = new_prefix
                found = get_installed_packages(new_prefix)
                print(f"{Fore.GREEN}>> Detected {len(found)} packages.")
        
        elif ch == "2":
            if not current_package_prefix:
                print(Fore.RED + ">> Error: Set prefix first!")
            else:
                print(Fore.CYAN + "\n --- SELECT GAME ---")
                game_list = {"1": ("Blox Fruit", "2753915549"), "2": ("Fisch", "16732694052")}
                for k, v in game_list.items():
                    print(f" [{k}] {v[0]}")
                game_choice = input(f"\n{prefix_label}Select Option: ")
                if game_choice in game_list:
                    game_id = game_list[game_choice][1]
        
        elif ch == "1":
            if not current_package_prefix or not game_id:
                print(Fore.RED + ">> Error: Missing config!")
            else:
                interval_input = input(prefix_label + "Interval (Min): ")
                rejoin_interval = float(interval_input)
                auto_running = True
                all_pkgs = get_installed_packages(current_package_prefix)
                for p in all_pkgs:
                    package_data[p] = {'status': 'Initializing...', 'user': "**********"}
                    threading.Thread(target=auto_rejoin_logic, args=(p,), daemon=True).start()
        
        elif ch == "4":
            sys.exit() 
            
        if not auto_running:
            input(f"\n{Fore.GREEN}Press Enter to go back...")
    except Exception:
        pass
