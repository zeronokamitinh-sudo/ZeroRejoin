# --- CẤU HÌNH GIAO DIỆN (ĐÃ FIX ZOOM & CĂN CHỈNH KHUNG) ---
def get_W():
    try:
        # Lấy kích thước terminal, tối thiểu là 90 để không vỡ logo ASCII
        columns = shutil.get_terminal_size().columns
        return max(90, columns) 
    except:
        return 90

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_len_visual(text):
    ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
    return len(ansi_escape.sub('', str(text)))

def draw_line_content(content_str, text_color=Fore.WHITE, align='center', padding_vertical=False):
    W = get_W()
    visual_len = get_len_visual(content_str)
    
    # Tính toán khoảng trống an toàn
    total_space = max(0, W - 2 - visual_len)
    
    if align == 'center':
        pad_left = total_space // 2
    else:
        pad_left = 1 # Cách lề trái 1 chút cho đẹp
        
    # Pad_right tự động tính phần còn lại để đảm bảo KHÔNG BAO GIỜ LỆCH
    pad_right = total_space - pad_left
    
    # Vẽ dòng nội dung
    print(Fore.WHITE + "┃" + " " * pad_left + text_color + content_str + " " * pad_right + Fore.WHITE + "┃")

def draw_empty_line():
    # Hàm vẽ dòng trống để tạo độ thoáng cho khung
    W = get_W()
    print(Fore.WHITE + "┃" + " " * (W - 2) + "┃")

def draw_logo():
    lines_raw = [
        "███████╗███████╗██████╗  ██████╗      ███╗   ███╗ █████╗ ███╗   ██╗ █████╗  ██████╗ ███████╗██████╗ ",
        "╚══███╔╝██╔════╝██╔══██╗██╔═══██╗     ████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝ ██╔════╝██╔══██╗",
        "  ███╔╝ █████╗  ██████╔╝██║   ██║     ██╔████╔██║███████║██╔██╗ ██║███████║██║  ███╗█████╗  ██████╔╝",
        " ███╔╝  ██╔══╝  ██╔══██╗██║   ██║     ██║╚██╔╝██║██╔══██║██║╚██╗██║██╔══██║██║   ██║██╔══╝  ██╔══██╗",
        "███████╗███████╗██║  ██║╚██████╔╝     ██║ ╚═╝ ██║██║  ██║██║ ╚████║██║  ██║╚██████╔╝███████╗██║  ██║",
        "╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝      ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝"
    ]
    
    W = get_W()
    # Tính toán để logo nằm giữa khung to
    logo_width = len(lines_raw[0])
    padding_left = max(0, (W - 2 - logo_width) // 2)
    padding_right = max(0, W - 2 - logo_width - padding_left)
    
    # Vẽ Logo trực tiếp vào khung chính (Bỏ khung phụ bao quanh logo để trông to và sạch hơn)
    for line in lines_raw:
        part1 = line[:41] 
        part2 = line[41:]
        # In logo căn giữa, nằm gọn trong khung viền chính
        print(Fore.WHITE + "┃" + " " * padding_left + Fore.RED + part1 + Fore.CYAN + part2 + " " * padding_right + Fore.WHITE + "┃")

def banner():
    clear()
    W = get_W()
    # Nắp trên cùng
    print(Fore.WHITE + "┏" + "━" * (W - 2) + "┓")
    
    # Khoảng trống trên logo cho thoáng
    draw_empty_line()
    
    # Vẽ Logo
    draw_logo()
    
    # Khoảng trống dưới logo
    draw_empty_line()
    
    # Đường phân cách
    print(Fore.WHITE + "┣" + "━" * (W - 2) + "┫")
    
    # Dòng Credit & Title (Có thêm dòng trống cho rộng rãi)
    draw_empty_line()
    draw_line_content("By ZeroNokami | High-Performance Engine", Fore.WHITE, 'center')
    draw_line_content("[ TERMINAL CONTROL INTERFACE ]", Fore.YELLOW + Style.BRIGHT, 'center')
    draw_empty_line()
    
    print(Fore.WHITE + "┣" + "━" * (W - 2) + "┫")
    
    # Menu Options (Căn trái nhẹ nhàng thay vì sát lề)
    opts = [
        ("1", "EXECUTE ENGINE : Start Auto-Rejoin", Fore.YELLOW),
        ("2", "CONFIGURATION : Assign Game ID", Fore.YELLOW),
        ("3", "SYSTEM SETUP : Set Package Prefix", Fore.YELLOW),
        ("4", "TERMINATE : Exit Safely", Fore.RED)
    ]
    
    draw_empty_line() # Thêm khoảng trống đầu menu
    for num, txt, col in opts:
        content = f" [{num}] {txt}"
        draw_line_content(content, col, 'left') # Căn lề trái đẹp hơn
    draw_empty_line() # Thêm khoảng trống cuối menu
    
    # Đáy khung
    print(Fore.WHITE + "┗" + "━" * (W - 2) + "┛")

def status_box():
    cpu, ram = get_system_info()
    clear()
    W = get_W()
    
    print(Fore.WHITE + "┏" + "━" * (W - 2) + "┓")
    draw_empty_line()
    draw_logo()
    draw_empty_line()
    
    print(Fore.WHITE + "┣" + "━" * (W - 2) + "┫")
    header = f" MONITOR: CPU {cpu:.1f}% | RAM {ram:.1f}% "
    draw_empty_line()
    draw_line_content(header, Fore.CYAN + Style.BRIGHT, 'center')
    draw_empty_line()
    print(Fore.WHITE + "┣" + "━" * (W - 2) + "┫")
    
    # Bảng Monitor
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
        
        # Fix lỗi lệch dòng ở cột Status
        space_needed = max(0, rem_s - 1 - clean_st_len)
        col3 = f" {st_color}" + " " * space_needed
        
        print(Fore.WHITE + "┃" + col1 + "│" + col2 + "│" + col3 + Fore.WHITE + "┃")
    
    print(Fore.WHITE + "┗" + "━" * (W - 2) + "┛")
