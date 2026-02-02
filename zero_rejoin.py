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

# --- CẤU HÌNH GIAO DIỆN ---
def get_W():
    # Lấy chiều rộng màn hình thực tế mỗi lần gọi
    return shutil.get_terminal_size((80, 24)).columns

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_len_visual(text):
    ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
    return len(ansi_escape.sub('', str(text)))

# --- LOGIC GỐC (GIỮ NGUYÊN KHÔNG ĐỔI) ---
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
        mem = subprocess.check_output(["free", "-m"], stderr=subprocess.DEVNULL).decode().splitlines()
        parts = mem[1].split()
        ram_percent = (int(parts[2]) / int(parts[1])) * 100
        return 2.5, ram_percent
    except:
        return 2.5, 45.0

# --- GIAO DIỆN ĐÃ FIX LỖI ZOOM VÀ CĂN CHỈNH ---
def draw_line_content(content_str, text_color=Fore.WHITE, align='center'):
    W = get_W()
    visual_len = get_len_visual(content_str)
    padding = W - 2 - visual_len
    if padding < 0: padding = 0
    
    if align == 'center':
        pad_left = padding // 2
        pad_right = padding - pad_left
    else:
        pad_left = 0
        pad_right = padding
        
    print(Fore.WHITE + "┃" + " " * pad_left + text_color + content_str + " " * pad_right + Fore.WHITE + "┃")

def draw_logo():
    # Logo Zero Manager trên 1 dòng duy nhất
    lines_raw = [
        "███████╗███████╗██████╗  ██████╗     ███╗   ███╗ █████╗ ███╗   ██╗ █████╗  ██████╗ ███████╗██████╗ ",
        "╚══███╔╝██╔════╝██╔══██╗██╔═══██╗    ████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝ ██╔════╝██╔══██╗",
        "  ███╔╝ █████╗  ██████╔╝██║   ██║    ██╔████╔██║███████║██╔██╗ ██║███████║██║  ███╗█████╗  ██████╔╝",
        " ███╔╝  ██╔══╝  ██╔══██╗██║   ██║    ██║╚██╔╝██║██╔══██║██║╚██╗██║██╔══██║██║   ██║██╔══╝  ██╔══██╗",
        "███████╗███████╗██║  ██║╚██████╔╝    ██║ ╚═╝ ██║██║  ██║██║ ╚████║██║  ██║╚██████╔╝███████╗██║  ██║",
        "╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝     ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝"
    ]
    
    W = get_W()
    # Lấy chiều dài thực của logo (dòng đầu tiên)
    logo_content_width = len(lines_raw[0])
    
    # Tính toán khung bao quanh: +2 ký tự cho '║ ' và +2 cho ' ║'
    box_width = logo_content_width + 4
    
    # Tính khoảng cách lề trái để căn giữa khung vào màn hình
    margin_left_len = (W - box_width) // 2
    
    # Nếu màn hình quá nhỏ so với logo, ép lề trái về 0 để tránh lỗi
    if margin_left_len < 0: margin_left_len = 0
    
    margin_left = " " * margin_left_len

    # --- VẼ KHUNG TRÊN ---
    # margin + ╔ + ═ (bằng chiều dài chữ + 2 khoảng trắng) + ╗
    print(margin_left + Fore.WHITE + "╔" + "═" * (logo_content_width + 2) + "╗")
    
    # --- VẼ NỘI DUNG LOGO ---
    for line in lines_raw:
        # Tách màu: 41 ký tự đầu là ZERO, phần sau là MANAGER
        # Số 41 được chọn vì nó nằm ở khoảng trắng giữa chữ O và M
        part1 = line[:41] 
        part2 = line[41:]
        
        # In ra: Lề màn hình + Cạnh trái + (Cách 1) + Chữ + (Cách 1) + Cạnh phải
        # Lưu ý: '║ ' và ' ║' tạo ra khoảng cách 1 space giữa viền và chữ
        print(margin_left + Fore.WHITE + "║ " + Fore.RED + part1 + Fore.CYAN + part2 + Fore.WHITE + " ║")
        
    # --- VẼ KHUNG DƯỚI ---
    print(margin_left + Fore.WHITE + "╚" + "═" * (logo_content_width + 2) + "╝")

def banner():
    clear()
    W = get_W()
    print(Fore.WHITE + "┏" + "━" * (W - 2) + "┓")
    
    # Logo tự động căn giữa
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
        visual_len = len(content)
        padding_right = W - 2 - visual_len
        if padding_right < 0: padding_right = 0
        print(Fore.WHITE + "┃" + col + content + " " * padding_right + Fore.WHITE + "┃")
        
    print(Fore.WHITE + "┗" + "━" * (W - 2) + "┛")

def status_box():
    cpu, ram = get_system_info()
    clear()
    W = get_W()
    print(Fore.WHITE + "┏" + "━" * (W - 2) + "┓")
    
    # Logo cũng hiển thị trong màn hình status
    draw_logo()
    
    print(Fore.WHITE + "┣" + "━" * (W - 2) + "┫")
    
    header = f" MONITOR: CPU {cpu:.1f}% | RAM {ram:.1f}% "
    draw_line_content(header, Fore.CYAN + Style.BRIGHT, 'center')
    print(Fore.WHITE + "┣" + "━" * (W - 2) + "┫")
    
    u_w = int(W * 0.35) 
    p_w = int(W * 0.35)
    rem_s = W - 2 - u_w - 1 - p_w - 1
    if rem_s < 10: 
        u_w = 20
        p_w = 20
        rem_s = W - 2 - u_w - 1 - p_w - 1
        
    h1 = " USER"
    h2 = " PACKAGE"
    h3 = " STATUS"
    
    h1 = h1[:u_w]
    h2 = h2[:p_w]
    
    print(Fore.WHITE + "┃" + f"{h1:<{u_w}}│{h2:<{p_w}}│{h3:<{rem_s}}" + "┃")
    print(Fore.WHITE + "┣" + "━" * u_w + "┿" + "━" * p_w + "┿" + "━" * rem_s + "┫")
    
    for pkg in sorted(package_data.keys()):
        data = package_data[pkg]
        user_display = data.get('user', "Scanning...")
        user_str = str(user_display)[:u_w-1]
        p_name = str(pkg.split('.')[-1])[:p_w-1]
        st_color = data['status']
        clean_st = get_len_visual(st_color)
        
        col1 = f" {Fore.GREEN}{user_str:<{u_w-1}}{Fore.WHITE}"
        col2 = f" {p_name:<{p_w-1}}"
        space_needed = rem_s - 1 - clean_st
        if space_needed < 0: space_needed = 0
        col3 = f" {st_color}" + " " * space_needed
        
        print(Fore.WHITE + "┃" + col1 + "│" + col2 + "│" + col3 + Fore.WHITE + "┃")
    
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
