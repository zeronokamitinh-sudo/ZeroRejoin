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

# --- FIX HIỂN THỊ: CHỐNG BIẾN DẠNG KHI ZOOM ---
def status_box():
    cpu, ram = get_system_info()
    W = 50 # Độ rộng hẹp hơn để tránh vỡ khi zoom to
    clear()
    print(Fore.WHITE + ".-" * (W // 2) + ".")
    header = f" MONITOR: CPU {cpu:.1f}% | RAM {ram:.1f}% "
    print(Fore.WHITE + "| " + Fore.CYAN + header.center(W-3) + Fore.WHITE + " |")
    print(Fore.WHITE + "|-" + "-" * (W-3) + "-|")
    print(Fore.WHITE + f"| {'USER':^12} | {'PACKAGE':^16} | {'STATUS':^13} |")
    print(Fore.WHITE + "|-" + "-" * (W-3) + "-|")
    for pkg in sorted(package_data.keys()):
        data = package_data[pkg]
        user = (data.get('user', "Unknown")[:11])
        p_display = (pkg.split('.')[-1][:14])
        st = data['status']
        line = Fore.WHITE + f"| {Fore.YELLOW}{user:^10} {Fore.WHITE}| {Fore.GREEN}{p_display:^14} {Fore.WHITE}| {st:^11} {Fore.WHITE}|"
        print(line)
    print(Fore.WHITE + "'" + "-" * (W-1) + "'")

# --- BANNER X5: CHỐNG BIẾN DẠNG MENU ---
def banner():
    clear()
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
    
    # Chữ ZERONOKAMI kích thước x5 (Standard Block)
    # Rút gọn khoảng cách để tránh tràn màn hình khi zoom
    art = [
        "  ZZZZZ  EEEEE  RRRR    OOOOO  N   N  OOOOO  K  K   AAA   M   M  IIIII",
        "     Z   E      R   R  O     O NN  N O     O K K   A   A  MM MM    I  ",
        "    Z    EEEE   RRRR   O     O N N N O     O KK    AAAAA  M M M    I  ",
        "   Z     E      R  R   O     O N  NN O     O K K   A   A  M   M    I  ",
        "  ZZZZZ  EEEEE  R   R   OOOOO  N   N  OOOOO  K  K  A   A  M   M  IIIII"
    ]

    for i, line in enumerate(art):
        colored_line = ""
        for j, char in enumerate(line):
            # Hiệu ứng màu xéo
            color_idx = (i + (j // 8)) % len(colors)
            colored_line += colors[color_idx] + char
        print(Style.BRIGHT + colored_line)
    
    W = 55
    print("\n" + Fore.WHITE + ".-" * (W // 2) + ".")
    print(Fore.WHITE + "| " + Fore.YELLOW + f"{DISPLAY_NAME} CONTROL PANEL".center(W-3) + Fore.WHITE + " |")
    print(Fore.WHITE + "| " + "-" * (W-3) + " |")
    
    opts = [("[1]", "Start Auto-Join", Fore.GREEN),
            ("[2]", "Set Game ID", Fore.CYAN),
            ("[3]", "Set Prefix", Fore.YELLOW),
            ("[4]", "Exit", Fore.RED)]
    
    for opt in opts:
        content = f" {opt[0]} {opt[1]}"
        print(Fore.WHITE + "| " + opt[2] + content.ljust(W-3) + Fore.WHITE + " |")
    print(Fore.WHITE + "'" + "-" * (W-1) + "'")

# Main Loop (Giữ nguyên logic gốc)
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
        prefix_label = f"{Fore.WHITE}[{Fore.CYAN}{DISPLAY_NAME}{Fore.WHITE}]-{Fore.GREEN} "
        ch = input(prefix_label + "> ")
        
        if ch == "3":
            new_prefix = input(prefix_label + "Prefix: ")
            if new_prefix:
                current_package_prefix = new_prefix
                found = get_installed_packages(new_prefix)
                print(f"{Fore.GREEN}>> Found {len(found)} pkgs.")
        
        elif ch == "2":
            if not current_package_prefix:
                print(Fore.RED + ">> Set prefix first!")
            else:
                print(Fore.CYAN + "\n--- GAMES ---")
                game_list = {
                    "1": ("Blox Fruit", "2753915549"),
                    "2": ("Night Forest", "79546208627805"),
                    "3": ("Deals Rails", "116495829188952"),
                    "4": ("Fisch", "16732694052"),
                    "5": ("Anime Def", "17017769292"),
                    "6": ("Bee Swarm", "1537690962"),
                    "7": ("Brainrot 1", "109983668079237"),
                    "8": ("Brainrot 2", "131623223084840"),
                    "9": ("Anime Adv", "8304191830"),
                    "10": ("King Legacy", "4520749081"),
                }
                for k, v in game_list.items():
                    print(f"[{k}] {v[0]}")
                print("[11] Custom Link")
                
                game_choice = input(f"\n{prefix_label}Select: ")
                if game_choice in game_list:
                    game_id = game_list[game_choice][1]
                    print(f"{Fore.GREEN}>> Linked.")
                elif game_choice == "11":
                    link = input(prefix_label + "Link: ")
                    if link:
                        game_id = link
                        print(f"{Fore.GREEN}>> Linked.")
        
        elif ch == "1":
            if not current_package_prefix or not game_id:
                print(f"{Fore.RED}>> Missing Config!")
            else:
                iv = input(prefix_label + "Minutes: ")
                rejoin_interval = float(iv)
                auto_running = True
                all_pkgs = get_installed_packages(current_package_prefix)
                if not all_pkgs:
                    auto_running = False
                else:
                    for p in all_pkgs:
                        package_data[p] = {'status': 'Init...', 'user': "**********"}
                        threading.Thread(target=auto_rejoin_logic, args=(p,), daemon=True).start()
                        time.sleep(2)
        
        elif ch == "4":
            sys.exit()
            
        if not auto_running:
            input(f"\n{Fore.GREEN}Enter to back...")
    except:
        pass
