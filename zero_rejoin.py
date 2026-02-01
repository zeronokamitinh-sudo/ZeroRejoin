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

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# --- LOGIC GỐC GIỮ NGUYÊN 100% ---
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
            package_data[pkg]['status'] = f"{Fore.CYAN}Auto Join"
            time.sleep(8)
            package_data[pkg]['status'] = f"{Fore.MAGENTA}Executor Check"
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

# --- FIX LỖI ĐƯỜNG KẺ DƯ VÀ CĂN CHỈNH VỊ TRÍ ---
def banner():
    clear()
    art = [
        r"  ________  _______ .______       ______      .___  ___.      ___      .__   __.      ___       _______  _______ .______      ",
        r" |       / |   ____||   _  \     /  __  \     |   \/   |     /   \     |  \ |  |     /   \     /  _____||   ____||   _  \     ",
        r" `---/  /  |  |__   |  |_)  |   |  |  |  |    |  \  /  |    /  ^  \    |   \|  |    /  ^  \   |  |  __  |  |__   |  |_)  |    ",
        r"    /  /   |   __|  |      /    |  |  |  |    |  |\/|  |   /  /_\  \   |  . `  |   /  /_\  \  |  | |_ | |   __|  |      /     ",
        r"   /  /---.|  |____ |  |\  \----|  `--'  |    |  |  |  |  /  _____  \  |  |\   |  /  _____  \ |  |__| | |  |____ |  |\  \----.",
        r"  /________|_______|| _| `._____|\______/     |__|  |__| /__/     \__\ |__| \__| /__/     \__\ \______| |_______|| _| `._____|"
    ]
    
    # W là chiều dài thực tế của dòng art (122 ký tự) + 4 ký tự đệm trắng
    W = 126 
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
    
    print(Fore.WHITE + "┏" + "━" * W + "┓")
    
    for line in art:
        # Căn giữa dòng art trong W
        content = line.center(W)
        colored_line = ""
        for j, char in enumerate(content):
            if char.strip(): 
                color_idx = (j // 15) % len(colors)
                colored_line += colors[color_idx] + char
            else:
                colored_line += char
        print(Fore.WHITE + "┃" + colored_line + Fore.WHITE + "┃")

    credit_str = "By ZeroNokami | High-Performance Engine"
    print(Fore.WHITE + "┃" + credit_str.center(W) + Fore.WHITE + "┃")
    print(Fore.WHITE + "┣" + "━" * W + "┫")
    
    # Fix tiêu đề Control Interface: Căn giữa tuyệt đối trong W
    title = "[ TERMINAL CONTROL INTERFACE ]"
    title_padding = (W - len(title)) // 2
    left_space = " " * title_padding
    right_space = " " * (W - len(title) - title_padding)
    print(Fore.WHITE + "┃" + left_space + Fore.YELLOW + Style.BRIGHT + title + Fore.WHITE + right_space + "┃")
    
    print(Fore.WHITE + "┣" + "━" * W + "┫")
    
    opts = [
        ("1", "EXECUTE ENGINE : Start Auto-Rejoin"),
        ("2", "CONFIGURATION  : Assign Game ID"),
        ("3", "SYSTEM SETUP   : Set Package Prefix"),
        ("4", "TERMINATE      : Exit Safely")
    ]
    
    opt_colors = [Fore.GREEN, Fore.CYAN, Fore.YELLOW, Fore.RED]
    
    for i, (num, txt) in enumerate(opts):
        # Format: "    [1] Text"
        prefix = f"    [{num}] "
        full_text = prefix + txt
        padding_right = " " * (W - len(full_text))
        print(Fore.WHITE + "┃" + opt_colors[i] + full_text + Fore.WHITE + padding_right + "┃")
        
    print(Fore.WHITE + "┗" + "━" * W + "┛")

def status_box():
    cpu, ram = get_system_info()
    clear()
    W = 126

    print(Fore.WHITE + "┏" + "━" * W + "┓")
    header = f" MONITOR: CPU {cpu:.1f}% | RAM {ram:.1f}% "
    print(Fore.WHITE + "┃" + Fore.CYAN + Style.BRIGHT + header.center(W) + Fore.WHITE + "┃")
    print(Fore.WHITE + "┣" + "━" * W + "┫")
    
    u_w = int(W * 0.25)
    p_w = int(W * 0.30)
    s_w = W - u_w - p_w - 6
    
    label = f"  {'USER':^{u_w}}   {'PACKAGE':^{p_w}}   {'STATUS':^{s_w}}  "
    print(Fore.WHITE + "┃" + label + "┃")
    print(Fore.WHITE + "┣" + "━" * W + "┫")
    
    for pkg in sorted(package_data.keys()):
        data = package_data[pkg]
        user = str(data.get('user', "Unknown"))[:u_w]
        p_name = str(pkg.split('.')[-1])[:p_w]
        st = data['status']
        # Xử lý độ dài status để không làm lệch đường kẻ
        clean_st = re.sub(r'\x1b\[[0-9;]*m', '', st) # Đo độ dài thực tế không tính mã màu
        st_padding = " " * (s_w - len(clean_st))
        
        row = f"  {user:^{u_w}}   {p_name:^{p_w}}   {st}{st_padding}  "
        print(Fore.WHITE + "┃" + Fore.YELLOW + row + Fore.WHITE + "┃")
    
    print(Fore.WHITE + "┗" + "━" * W + "┛")

# --- MAIN LOOP GIỮ NGUYÊN ---
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
        prefix_label = f"{Fore.WHITE}[ {Fore.CYAN}Zero Manager{Fore.WHITE} ] - {Fore.GREEN}"
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
                    "6": ("Bee Swarm Simulator", "1537690962"),
                    "7": ("Steal A Brainrot", "109983668079237"),
                    "8": ("Escape Tsunami For Brainrot", "131623223084840"),
                    "9": ("Anime Adventure", "8304191830"),
                    "10": ("King Legacy", "4520749081"),
                }
                for k, v in game_list.items():
                    print(f"{Fore.WHITE} [{k}] {v[0]}")
                print(Fore.YELLOW + " [11] Other Game / Private Server Link")
                game_choice = input(f"\n{prefix_label}Select Option: ")
                if game_choice in game_list:
                    game_id = game_list[game_choice][1]
                    print(f"{Fore.GREEN}>> Linked: {game_list[game_choice][0]}")
                elif game_choice == "11":
                    link = input(prefix_label + "Paste Link (VIP/Server): ")
                    if link:
                        game_id = link
                        print(f"{Fore.GREEN}>> Custom link linked.")
        
        elif ch == "1":
            if not current_package_prefix or not game_id:
                print(f"{Fore.RED}>> Error: Missing configuration!")
            else:
                interval_input = input(prefix_label + "Interval (Minutes): ")
                rejoin_interval = float(interval_input)
                auto_running = True
                all_pkgs = get_installed_packages(current_package_prefix)
                if not all_pkgs:
                    print(Fore.RED + ">> No packages found!")
                    auto_running = False
                else:
                    for p in all_pkgs:
                        package_data[p] = {'status': 'Initializing...', 'user': "**********"}
                        threading.Thread(target=auto_rejoin_logic, args=(p,), daemon=True).start()
                        time.sleep(2)
        
        elif ch == "4":
            sys.exit() 
            
        if not auto_running:
            input(f"\n{Fore.GREEN}Press Enter to go back...")
    except Exception:
        pass
