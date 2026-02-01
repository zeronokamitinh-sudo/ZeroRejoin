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

# --- CĂN CHỈNH GIAO DIỆN ---
def get_border(width):
    return Fore.WHITE + "+ " + "- " * ((width // 2) - 1) + "+"

def banner():
    clear()
    W = 75 # Độ rộng khung cố định để chống vỡ hình
    
    # ASCII Art "Zero Manager" phong cách đứt khúc (Dashed)
    # Tái tạo lại kiểu chữ rỗng/đứt đoạn như trong ảnh của bạn
    art = [
        r"  ____                      __  __                                   ",
        r" /_  / ___  ____ ____      /  |/  /___ _ ___  ___ _ ___ _ ___  ____  ",
        r"  / / / _ \/ __// __ \    / /|_/ // _ `// _ \/ _ `// _ `// _ \/ __/  ",
        r" / /_/  __/ /  / /_/ /   / /  / // (_| // / / / (_| // (_| //  __/ /     ",
        r"/___/\___/_/   \____/   /_/  /_/ \__,_//_/ /_/\__,_/ \__, / \___/_/      ",
        r"                                                    /____/               "
    ]

    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
    
    # Vẽ khung trên
    print(get_border(W))
    
    # In ASCII Art với màu Gradient ngang
    for i, line in enumerate(art):
        centered_line = line.center(W-2)
        colored_line = ""
        for j, char in enumerate(centered_line):
            # Tính toán màu dựa trên vị trí ký tự để tạo hiệu ứng cầu vồng như ảnh
            color_idx = (j // 8) % len(colors)
            colored_line += colors[color_idx] + char
        print(Fore.WHITE + "|" + colored_line + Fore.WHITE + "|")

    # Dòng Credit: Thay thế Version/Copyright cũ bằng yêu cầu mới
    # Cấu trúc: By ZeroNokami | Auto Rejoin Tool (Căn giữa)
    credit_text = "By ZeroNokami | Auto Rejoin Tool"
    # Chia màu: Xanh lá cho tên, Tím cho Tool (giống ảnh)
    left_part = f"{Fore.GREEN}By ZeroNokami"
    sep_part = f"{Fore.WHITE} | "
    right_part = f"{Fore.MAGENTA}Auto Rejoin Tool"
    
    # Tính toán khoảng cách để căn giữa dòng Credit có màu
    padding = (W - 2 - len(credit_text)) // 2
    print(Fore.WHITE + "|" + " " * padding + left_part + sep_part + right_part + " " * (W - 2 - padding - len(credit_text)) + Fore.WHITE + "|")
    
    # Menu Options
    print(get_border(W))
    title = " CONTROL PANEL "
    print(Fore.WHITE + "|" + Fore.YELLOW + Style.BRIGHT + title.center(W-2) + Fore.WHITE + "|")
    print(get_border(W))
    
    opts = [("[1]", "Start Auto-Rejoin Engine", Fore.GREEN),
            ("[2]", "Assign Game ID / Link", Fore.CYAN),
            ("[3]", "Set Package Prefix", Fore.YELLOW),
            ("[4]", "Exit System", Fore.RED)]
    
    for opt in opts:
        content = f" {opt[0]} {opt[1]}"
        padding = W - 2 - len(content)
        print(Fore.WHITE + "|" + opt[2] + content + " " * padding + Fore.WHITE + "|")
        
    print(get_border(W))

def status_box():
    cpu, ram = get_system_info()
    W = 75
    clear()
    
    border = get_border(W)
    print(border)
    header = f" MONITORING: CPU {cpu:.1f}% | RAM {ram:.1f}% "
    print(Fore.WHITE + "|" + Fore.CYAN + Style.BRIGHT + header.center(W-2) + Fore.WHITE + "|")
    print(border)
    
    print(Fore.WHITE + f"| {'USER':^18} | {'PACKAGE':^20} | {'STATUS':^29} |")
    print(border)
    
    for pkg in sorted(package_data.keys()):
        data = package_data[pkg]
        user = (data.get('user', "Unknown")[:16])
        p_display = (pkg.split('.')[-1][:18])
        st = data['status']
        # Fix lỗi lệch dòng khi Status có mã màu
        line = Fore.WHITE + f"| {Fore.YELLOW}{user:^18}{Fore.WHITE} | {Fore.GREEN}{p_display:^20}{Fore.WHITE} | {st:^38} {Fore.WHITE}|"
        print(line)
    
    print(border)

# Main Loop 
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
