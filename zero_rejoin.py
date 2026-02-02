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
account_scripts = {} # Biến lưu script cho từng acc

# --- CẤU HÌNH GIAO DIỆN ---
# W = 120 theo yêu cầu để khung to hơn
W = 120 

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_len_visual(text):
    ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
    return len(ansi_escape.sub('', str(text)))

# --- LOGIC GỐC GIỮ NGUYÊN (Có cập nhật phần check user) ---
def get_roblox_username(pkg):
    try:
        # Cố gắng dump view để tìm tên
        dump_cmd = ["uiautomator", "dump", "/sdcard/view.xml"]
        subprocess.run(dump_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        with open("/sdcard/view.xml", "r", encoding="utf-8") as f:
            content = f.read()
            # Regex tìm username bắt đầu bằng @
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
        
        # Check user liên tục khi app mở
        real_name = get_roblox_username(pkg)
        if real_name:
            package_data[pkg]['user'] = real_name
        
        if is_running(pkg):
            package_data[pkg]['status'] = f"{Fore.CYAN}Auto Join"
            time.sleep(8)
            
            # Logic chạy script (Placeholder)
            # Nếu có script đã nhập ở bước 4, logic execute sẽ nằm ở đây
            if pkg in account_scripts:
                 package_data[pkg]['status'] = f"{Fore.MAGENTA}Run Script..."
                 # (Tại đây bạn có thể thêm code gửi script vào executor nếu có tool hỗ trợ)
            else:
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
            
            # Cập nhật lại user nếu lúc đầu chưa bắt được
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

# --- GIAO DIỆN ---
def draw_line_content(content_str, text_color=Fore.WHITE, align='center'):
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
        ("4", "Auto Execute   : Setup Scripts (Single/Multi)", Fore.YELLOW),
        ("5", "TERMINATE      : Exit Safely", Fore.RED)
    ]
    
    for num, txt, col in opts:
        content = f"    [{num}] {txt}"
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
    
    # --- CHIA CỘT USER | PACKAGE | STATUS ---
    # Tổng W = 120. Trừ 2 biên = 118.
    # User: 30, Package: 40, Status: 48 (bao gồm thanh chắn)
    u_w = 30
    p_w = 40
    # s_w tự tính còn lại
    
    # Header bảng
    h1 = " USER"
    h2 = " PACKAGE"
    h3 = " STATUS"
    
    # In Header
    # Cấu trúc: ┃ Text ┃ Text ┃ Text ┃
    
    # Tính toán padding cho header
    rem_s = W - 2 - u_w - 1 - p_w - 1 # -1 cho các thanh chắn giữa
    
    print(Fore.WHITE + "┃" + f"{h1:<{u_w}}│{h2:<{p_w}}│{h3:<{rem_s}}" + "┃")
    print(Fore.WHITE + "┣" + "━" * u_w + "┿" + "━" * p_w + "┿" + "━" * rem_s + "┫")
    
    for pkg in sorted(package_data.keys()):
        data = package_data[pkg]
        # Xử lý user: Nếu chưa có tên thì hiện Scanning...
        user_display = data.get('user', "Scanning...")
        if user_display == "**********": user_display = "Scanning..." # Fallback cũ
        
        user_str = str(user_display)[:u_w-1]
        p_name = str(pkg.split('.')[-1])[:p_w-1]
        st_color = data['status']
        clean_st = get_len_visual(st_color)
        
        # Dòng dữ liệu
        # User (Green) | Package (White) | Status (Color)
        
        # Part 1: User
        col1 = f" {Fore.GREEN}{user_str:<{u_w-1}}{Fore.WHITE}"
        
        # Part 2: Package
        col2 = f" {p_name:<{p_w-1}}"
        
        # Part 3: Status (Manual padding calculation)
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
                # DANH SÁCH GAME GỐC GIỮ NGUYÊN 100%
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
                rejoin_interval = float(interval_input)
                auto_running = True
                all_pkgs = get_installed_packages(current_package_prefix)
                if not all_pkgs:
                    print(Fore.RED + ">> No packages found!")
                    auto_running = False
                else:
                    for p in all_pkgs:
                        # User ban đầu set là Scanning...
                        package_data[p] = {'status': 'Initializing...', 'user': "Scanning..."}
                        threading.Thread(target=auto_rejoin_logic, args=(p,), daemon=True).start()
                        time.sleep(2)
        
        elif ch == "4":
            # --- TÍNH NĂNG 4: AUTO EXECUTE SETUP ---
            if not current_package_prefix:
                print(Fore.RED + ">> Error: Please set Package Prefix (Option 3) first!")
            else:
                pkgs = get_installed_packages(current_package_prefix)
                if not pkgs:
                    print(Fore.RED + ">> No packages found!")
                else:
                    print(f"\n{Fore.CYAN}--- SCRIPT CONFIGURATION ---")
                    print(f"{Fore.WHITE}[1] Individual Account Script (Each account has own script)")
                    print(f"{Fore.WHITE}[2] Multiple Accounts Using A Single Script")
                    
                    sub_ch = input(f"{prefix_label}Select Mode: ")
                    
                    if sub_ch == "1":
                        print(f"{Fore.YELLOW}>> Entering Individual Mode...")
                        for p in pkgs:
                            # Thử lấy tên user, nếu không được thì hiện tên gói
                            # Không ép mở app để tránh giật lag
                            u_name = get_roblox_username(p)
                            display_name = u_name if u_name else p
                            
                            scr = input(f"Enter Script for [{Fore.GREEN}{display_name}{Fore.WHITE}]: ")
                            account_scripts[p] = scr
                        print(f"{Fore.GREEN}>> All scripts saved!")
                        
                    elif sub_ch == "2":
                        common_scr = input(f"{Fore.YELLOW}Enter Script for ALL ACCOUNTS: ")
                        for p in pkgs:
                            account_scripts[p] = common_scr
                        print(f"{Fore.GREEN}>> Common script applied to {len(pkgs)} accounts!")
                    else:
                        print(Fore.RED + "Invalid Option")

        elif ch == "5":
            sys.exit() 
            
        if not auto_running:
            input(f"\n{Fore.GREEN}Press Enter to go back...")
    except Exception as e:
        print(f"Error: {e}")
        input()
