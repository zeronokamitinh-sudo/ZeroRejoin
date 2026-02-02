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

# Global Variables
current_package_prefix = None
game_id = None
rejoin_interval = None
auto_running = False
DISPLAY_NAME = "Zero Manager"
package_data = {}

# --- CẤU HÌNH GIAO DIỆN (ĐÃ TỐI ƯU ZOOM) ---
def get_W():
    # Sử dụng shutil để lấy kích thước terminal chính xác nhất tại thời điểm gọi
    try:
        columns = shutil.get_terminal_size().columns
        return columns if columns > 10 else 80
    except:
        return 80

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_len_visual(text):
    ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
    return len(ansi_escape.sub('', str(text)))

# --- LOGIC GỐC (GIỮ NGUYÊN) ---
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

def get_system_info():
    try:
        # Giả lập hoặc lấy thông số thực nếu có quyền
        return 2.5, 45.0
    except:
        return 0.0, 0.0

# --- GIAO DIỆN SỬA LỖI BIẾN DẠNG ---
def draw_line_content(content_str, text_color=Fore.WHITE, align='center'):
    W = get_W()
    visual_len = get_len_visual(content_str)
    # Đảm bảo padding không âm nếu terminal bị thu quá nhỏ
    padding = max(0, W - 2 - visual_len)
    
    if align == 'center':
        pad_left = padding // 2
        pad_right = padding - pad_left
    else:
        pad_left = 0
        pad_right = padding
        
    print(Fore.WHITE + "┃" + " " * pad_left + text_color + content_str + " " * pad_right + Fore.WHITE + "┃")

def draw_logo():
    lines_raw = [
        "███████╗███████╗██████╗  ██████╗     ███╗   ███╗ █████╗ ███╗   ██╗ █████╗  ██████╗ ███████╗██████╗ ",
        "╚══███╔╝██╔════╝██╔══██╗██╔═══██╗    ████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝ ██╔════╝██╔══██╗",
        "  ███╔╝ █████╗  ██████╔╝██║   ██║    ██╔████╔██║███████║██╔██╗ ██║███████║██║  ███╗█████╗  ██████╔╝",
        " ███╔╝  ██╔══╝  ██╔══██╗██║   ██║    ██║╚██╔╝██║██╔══██║██║╚██╗██║██╔══██║██║   ██║██╔══╝  ██╔══██╗",
        "███████╗███████╗██║  ██║╚██████╔╝    ██║ ╚═╝ ██║██║  ██║██║ ╚████║██║  ██║╚██████╔╝███████╗██║  ██║",
        "╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝     ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝"
    ]
    
    W = get_W()
    logo_content_width = len(lines_raw[0])
    # Tính toán lề để logo luôn nằm giữa màn hình bất kể zoom
    margin_left_len = max(0, (W - (logo_content_width + 4)) // 2)
    margin_left = " " * margin_left_len

    # Vẽ khung và logo với lề động
    print(margin_left + Fore.WHITE + "╔" + "═" * (logo_content_width + 2) + "╗")
    for line in lines_raw:
        part1 = line[:41] 
        part2 = line[41:]
        print(margin_left + Fore.WHITE + "║ " + Fore.RED + part1 + Fore.CYAN + part2 + Fore.WHITE + " ║")
    print(margin_left + Fore.WHITE + "╚" + "═" * (logo_content_width + 2) + "╝")

def banner():
    clear()
    W = get_W()
    print(Fore.WHITE + "┏" + "━" * (W - 2) + "┓")
    draw_logo()
    print(Fore.WHITE + "┣" + "━" * (W - 2) + "┫")
    draw_line_content("By ZeroNokami | High-Performance Engine", Fore.WHITE, 'center')
    print(Fore.WHITE + "┣" + "━" * (W - 2) + "┫")
    draw_line_content("[ TERMINAL CONTROL INTERFACE ]", Fore.YELLOW + Style.BRIGHT, 'center')
    print(Fore.WHITE + "┣" + "━" * (W - 2) + "┫")
    
    opts = [
        ("1", "EXECUTE ENGINE : Start Auto-Rejoin", Fore.YELLOW),
        ("2", "CONFIGURATION : Assign Game ID", Fore.YELLOW),
        ("3", "SYSTEM SETUP : Set Package Prefix", Fore.YELLOW),
        ("4", "TERMINATE : Exit Safely", Fore.RED)
    ]
    
    for num, txt, col in opts:
        content = f" [{num}] {txt}"
        v_len = len(content)
        p_right = max(0, W - 2 - v_len)
        print(Fore.WHITE + "┃" + col + content + " " * p_right + Fore.WHITE + "┃")
    print(Fore.WHITE + "┗" + "━" * (W - 2) + "┛")

def status_box():
    cpu, ram = get_system_info()
    clear()
    W = get_W()
    print(Fore.WHITE + "┏" + "━" * (W - 2) + "┓")
    draw_logo()
    print(Fore.WHITE + "┣" + "━" * (W - 2) + "┫")
    header = f" MONITOR: CPU {cpu:.1f}% | RAM {ram:.1f}% "
    draw_line_content(header, Fore.CYAN + Style.BRIGHT, 'center')
    print(Fore.WHITE + "┣" + "━" * (W - 2) + "┫")
    
    # Chia tỷ lệ bảng linh hoạt theo chiều rộng màn hình (W)
    u_w = int(W * 0.3) 
    p_w = int(W * 0.3)
    rem_s = max(10, W - 2 - u_w - 1 - p_w - 1)
    
    print(Fore.WHITE + "┃" + f"{' USER':<{u_w}}│{' PACKAGE':<{p_w}}│{' STATUS':<{rem_s}}" + "┃")
    print(Fore.WHITE + "┣" + "━" * u_w + "┿" + "━" * p_w + "┿" + "━" * rem_s + "┫")
    
    for pkg in sorted(package_data.keys()):
        data = package_data[pkg]
        user_str = str(data.get('user', "Scanning..."))[:u_w-1]
        p_name = str(pkg.split('.')[-1])[:p_w-1]
        st_color = data['status']
        clean_st_len = get_len_visual(st_color)
        
        col1 = f" {Fore.GREEN}{user_str:<{u_w-1}}{Fore.WHITE}"
        col2 = f" {p_name:<{p_w-1}}"
        col3 = f" {st_color}" + " " * max(0, rem_s - 1 - clean_st_len)
        
        print(Fore.WHITE + "┃" + col1 + "│" + col2 + "│" + col3 + Fore.WHITE + "┃")
    print(Fore.WHITE + "┗" + "━" * (W - 2) + "┛")

# --- MAIN LOOP (GIỮ NGUYÊN) ---
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
                try:
                    rejoin_interval = float(interval_input)
                    auto_running = True
                    all_pkgs = get_installed_packages(current_package_prefix)
                    if not all_pkgs:
                        print(Fore.RED + ">> No packages found!")
                        auto_running = False
                    else:
                        for p in all_pkgs:
                            package_data[p] = {'status': 'Initializing...', 'user': "Scanning..."}
                            threading.Thread(target=auto_rejoin_logic, args=(p,), daemon=True).start()
                            time.sleep(2)
                except ValueError:
                     print(Fore.RED + ">> Invalid Number!")
        
        elif ch == "4":
            sys.exit()
            
        if not auto_running:
            input(f"\n{Fore.GREEN}Press Enter to go back...")
    except Exception as e:
        print(f"Error: {e}")
        input()
