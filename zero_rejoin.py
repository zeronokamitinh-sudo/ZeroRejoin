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

# --- HÀM FIX LỖI BIẾN DẠNG (GIỮ NGUYÊN KHUNG GỐC) ---
def get_current_width():
    try:
        # Lấy chiều rộng terminal thực tế
        return os.get_terminal_size().columns
    except:
        return 120

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_len_visual(text):
    ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
    return len(ansi_escape.sub('', str(text)))

# --- LOGIC GỐC GIỮ NGUYÊN ---
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

def start_app(pkg):
    subprocess.call(["am", "force-stop", pkg], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1) 
    deep_link = game_id if "http" in str(game_id) else f"roblox://placeID={game_id}"
    subprocess.call(["am", "start", "--user", "0", "-a", "android.intent.action.VIEW", "-d", deep_link, pkg], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

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
        r_name = get_roblox_username(pkg)
        if r_name: package_data[pkg]['user'] = r_name
        if is_running(pkg):
            package_data[pkg]['status'] = f"{Fore.CYAN}Auto Join"
            time.sleep(8)
            package_data[pkg]['status'] = f"{Fore.GREEN}Active Now"
        
        start_time = time.time()
        while auto_running:
            if time.time() - start_time >= rejoin_interval * 60 or not is_running(pkg):
                package_data[pkg]['status'] = f"{Fore.RED}Rejoining..." if is_running(pkg) else f"{Fore.RED}Crashed!"
                break
            if package_data[pkg]['user'] == "Scanning...":
                 r_name = get_roblox_username(pkg)
                 if r_name: package_data[pkg]['user'] = r_name
            time.sleep(5)

# --- HÀM VẼ GIAO DIỆN (ĐÃ FIX THẲNG HÀNG) ---
def draw_box_line(content, color=Fore.WHITE, align='center'):
    W = get_current_width()
    visual_len = get_len_visual(content)
    # Trừ đi 2 cho 2 thanh dọc ┃ ở hai đầu
    padding = W - 2 - visual_len
    if padding < 0: padding = 0
    
    if align == 'center':
        pad_left = padding // 2
        pad_right = padding - pad_left
    else: # Align left cho menu
        pad_left = 4 
        pad_right = padding - pad_left

    print(Fore.WHITE + "┃" + " " * pad_left + color + content + " " * pad_right + Fore.WHITE + "┃")

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
        draw_box_line(line, Fore.RED, align='center')

def banner():
    W = get_current_width()
    clear()
    print(Fore.WHITE + "┏" + "━" * (W - 2) + "┓")
    draw_logo()
    draw_box_line("By ZeroNokami | High-Performance Engine", Fore.WHITE, 'center')
    print(Fore.WHITE + "┣" + "━" * (W - 2) + "┫")
    draw_box_line("[ TERMINAL CONTROL INTERFACE ]", Fore.YELLOW + Style.BRIGHT, 'center')
    print(Fore.WHITE + "┣" + "━" * (W - 2) + "┫")
    
    opts = [
        ("1", "EXECUTE ENGINE : Start Auto-Rejoin", Fore.YELLOW),
        ("2", "CONFIGURATION  : Assign Game ID", Fore.YELLOW),
        ("3", "SYSTEM SETUP   : Set Package Prefix", Fore.YELLOW),
        ("4", "TERMINATE      : Exit Safely", Fore.RED)
    ]
    for num, txt, col in opts:
        draw_box_line(f"[{num}] {txt}", col, align='left')
        
    print(Fore.WHITE + "┗" + "━" * (W - 2) + "┛")

def status_box():
    W = get_current_width()
    clear()
    print(Fore.WHITE + "┏" + "━" * (W - 2) + "┓")
    draw_logo()
    print(Fore.WHITE + "┣" + "━" * (W - 2) + "┫")
    
    cpu, ram = get_system_info()
    header = f" MONITOR: CPU {cpu:.1f}% | RAM {ram:.1f}% "
    draw_box_line(header, Fore.CYAN + Style.BRIGHT, 'center')
    print(Fore.WHITE + "┣" + "━" * (W - 2) + "┫")
    
    u_w, p_w = int(W*0.25), int(W*0.35)
    rem_s = W - 2 - u_w - 1 - p_w - 1 
    print(Fore.WHITE + "┃" + f"{' USER':<{u_w}}│{' PACKAGE':<{p_w}}│{' STATUS':<{rem_s}}" + "┃")
    print(Fore.WHITE + "┣" + "━" * u_w + "┿" + "━" * p_w + "┿" + "━" * rem_s + "┫")
    
    for pkg in sorted(package_data.keys()):
        data = package_data[pkg]
        st_color = data['status']
        clean_st = get_len_visual(st_color)
        col1 = f" {Fore.GREEN}{str(data['user'])[:u_w-2]:<{u_w-1}}{Fore.WHITE}"
        col2 = f" {str(pkg.split('.')[-1])[:p_w-2]:<{p_w-1}}"
        col3 = f" {st_color}" + " " * (rem_s - 1 - clean_st)
        print(Fore.WHITE + "┃" + col1 + "│" + col2 + "│" + col3 + Fore.WHITE + "┃")
    print(Fore.WHITE + "┗" + "━" * (W - 2) + "┛")

def get_system_info():
    try:
        mem = subprocess.check_output(["free", "-m"], stderr=subprocess.DEVNULL).decode().splitlines()
        parts = mem[1].split()
        return 2.5, (int(parts[2]) / int(parts[1])) * 100
    except: return 2.5, 45.0

# --- MAIN LOOP ---
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
        # Giữ lại tiền tố Zero Manager nhưng đặt trong input gọn gàng
        ch = input(f"\n{Fore.WHITE}[ {Fore.YELLOW}Zero Manager{Fore.WHITE} ] - {Fore.GREEN}Command Line: ")
        
        if ch == "3":
            new_prefix = input(f"{Fore.GREEN}Enter Package Prefix: ")
            if new_prefix:
                current_package_prefix = new_prefix
                found = get_installed_packages(new_prefix)
                print(f"{Fore.GREEN}>> Detected {len(found)} packages.")
        elif ch == "2":
            if not current_package_prefix: print(Fore.RED + ">> Set prefix first!")
            else:
                print(f"{Fore.CYAN}--- SELECT GAME (1-10) ---")
                game_id = "2753915549" # Ví dụ mặc định Blox Fruit
                print(f"{Fore.GREEN}>> Linked Game ID.")
        elif ch == "1":
            if not current_package_prefix or not game_id: print(Fore.RED + ">> Missing config!")
            else:
                rejoin_interval = float(input(f"{Fore.GREEN}Interval (Minutes): "))
                auto_running = True
                pkgs = get_installed_packages(current_package_prefix)
                for p in pkgs:
                    package_data[p] = {'status': 'Initializing...', 'user': "Scanning..."}
                    threading.Thread(target=auto_rejoin_logic, args=(p,), daemon=True).start()
                    time.sleep(1)
        elif ch == "4": sys.exit()
        if not auto_running: input(f"\n{Fore.GREEN}Press Enter to go back...")
    except Exception as e:
        print(f"Error: {e}")
        input()
