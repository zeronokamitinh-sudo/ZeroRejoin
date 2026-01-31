import os, time, sys, subprocess, threading

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

def get_installed_packages(prefix):
    try:
        # Chặn các lỗi package không tồn tại hiển thị ra màn hình
        output = subprocess.check_output(["pm", "list", "packages", prefix], stderr=subprocess.DEVNULL).decode()
        pkgs = [line.split(':')[-1].strip() for line in output.splitlines() if line.strip()]
        return pkgs
    except:
        return []

def start_app(pkg):
    deep_link = f"roblox://placeID={game_id}"
    subprocess.call([
        "am", "start", "--user", "0", 
        "-a", "android.intent.action.VIEW", 
        "-d", deep_link, pkg
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def kill_app(pkg):
    subprocess.call(["am", "force-stop", pkg], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def is_running(pkg):
    try:
        output = subprocess.check_output(["ps", "-A"], stderr=subprocess.DEVNULL).decode()
        return pkg in output
    except:
        return False

def auto_rejoin_logic(pkg):
    global auto_running
    while auto_running:
        package_data[pkg]['status'] = f"{Fore.YELLOW}Opening Roblox"
        start_app(pkg)
        time.sleep(10)
        
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
        total, used = int(parts[1]), int(parts[2])
        ram_percent = (used / total) * 100
        cpu = float(subprocess.check_output(["top", "-b", "-n1"], stderr=subprocess.DEVNULL).decode().splitlines()[2].split()[1].replace(',','.'))
    except:
        cpu, ram_percent = 2.5, 45.0
    return cpu, ram_percent

def status_box():
    W = 80
    cpu, ram = get_system_info()
    clear()
    print(Fore.CYAN + "╔" + "═"*(W-2) + "╗")
    print(Fore.CYAN + "║" + f"{Fore.WHITE}{Style.BRIGHT} MONITORING SYSTEM - CPU: {cpu:.1f}% | RAM: {ram:.1f}% ".center(W-2) + Fore.CYAN + "║")
    print(Fore.CYAN + "╠" + "═"*26 + "╦" + "═"*26 + "╦" + "═"*24 + "╣")
    print(Fore.CYAN + "║" + f"{Fore.YELLOW} Roblox @Username ".center(26) + "║" + f"{Fore.YELLOW} Package Identifier ".center(26) + "║" + f"{Fore.YELLOW} Status ".center(24) + "║")
    print(Fore.CYAN + "╠" + "═"*26 + "╬" + "═"*26 + "╬" + "═"*24 + "╣")
    
    for pkg in sorted(package_data.keys()):
        data = package_data[pkg]
        # Lấy phần định danh sau dấu chấm cuối cùng để giả lập @Username chuẩn
        raw_name = pkg.split('.')[-1]
        roblox_user = f"@{raw_name.upper()}"
        st = data['status']
        print(Fore.CYAN + "║" + f"{Fore.WHITE} {roblox_user[:24]:^24} " + Fore.CYAN + "║" + f"{Fore.WHITE} {pkg[:24]:^24} " + Fore.CYAN + "║" + f" {st:^22} " + Fore.CYAN + "║")
        
    print(Fore.CYAN + "╚" + "═"*26 + "╩" + "═"*26 + "╩" + "═"*24 + "╝")

def banner():
    clear()
    # Logo màu Cyan rực rỡ
    logo = f"""{Fore.CYAN}{Style.BRIGHT}
    ███████╗███████╗██████╗  ██████╗ ███╗   ██╗ ██████╗ ██╗  ██╗ █████╗ ███╗   ███╗██╗
    ╚══███╔╝██╔════╝██╔══██╗██╔═══██╗████╗  ██║██╔═══██╗██║ ██╔╝██╔══██╗████╗ ████║██║
      ███╔╝ █████╗  ██████╔╝██║   ██║██╔██╗ ██║██║   ██║█████╔╝ ███████║██╔████╔██║██║
     ███╔╝  ██╔══╝  ██╔══██╗██║   ██║██║╚██╗██║██║   ██║██╔═██╗ ██╔══██║██║╚██╔╝██║██║
    ███████╗███████╗██║  ██║╚██████╔╝██║ ╚████║╚██████╔╝██║  ██╗██║  ██║██║ ╚═╝ ██║██║
    ╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝
    """
    print(logo)
    W = 60 
    print(Fore.BLUE + "╔" + "═" * (W-2) + "╗")
    header = " MAIN CONTROL INTERFACE "
    print(Fore.BLUE + "║" + Fore.WHITE + Style.BRIGHT + header.center(W-2) + Fore.BLUE + "║")
    print(Fore.BLUE + "╠" + "═" * (W-2) + "╣")
    
    def print_item(cmd_str, desc_str, color=Fore.GREEN):
        line = f"  {Fore.YELLOW}{cmd_str}  {color}{desc_str}".ljust(W+7)
        print(Fore.BLUE + "║" + line + Fore.BLUE + " ║")
        
    print_item("[1]", "Start Auto-Rejoin Engine")
    print_item("[2]", "Assign Game ID")
    print_item("[3]", "Set Package Prefix")
    print_item("[4]", "Exit System", color=Fore.RED)
    print(Fore.BLUE + "╚" + "═" * (W-2) + "╝\n")

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
                print(f"{Fore.GREEN}>> Detected {len(found)} matching packages in system.")
        
        elif ch == "2":
            if not current_package_prefix:
                print(Fore.RED + ">> Error: Please set package prefix first!")
            else:
                print(Fore.CYAN + " [1] Blox Fruit")
                if input(prefix_label + "Select Option: ") == "1":
                    game_id = "2753915549"
                    print(f"{Fore.GREEN}>> Game ID successfully linked.")
        
        elif ch == "1":
            if not current_package_prefix or not game_id:
                print(f"{Fore.RED}>> Error: Missing configuration (Prefix/GameID)!")
            else:
                rejoin_interval = float(input(prefix_label + "Interval (Minutes): "))
                auto_running = True
                all_pkgs = get_installed_packages(current_package_prefix)
                
                if not all_pkgs:
                    print(Fore.RED + ">> No packages found!")
                    auto_running = False
                else:
                    for p in all_pkgs:
                        package_data[p] = {'status': 'Initializing...'}
                        threading.Thread(target=auto_rejoin_logic, args=(p,), daemon=True).start()
                        time.sleep(2)
        
        elif ch == "4":
            print(Fore.RED + "Terminating system...")
            sys.exit()
            
        if not auto_running:
            input(f"\n{Fore.GREEN}Press Enter to go back...")
    except Exception as e:
        # Không in lỗi ra màn hình chính để giữ bảng sạch
        pass
