#!/data/data/com.termux/files/usr/bin/bash

echo "======================================"
echo "     ZeroNokami Rejoin Tool Setup     "
echo "     Version: 1.0.0 - ZeroNokami      "
echo "======================================"

pkg update -y
pkg install python git -y

pip install requests urllib3 colorama

echo ""
echo "Setup xong! Bây giờ chạy lệnh sau để start tool:"
echo "su -c \"export PATH=\$PATH:/data/data/com.termux/files/usr/bin && export TERM=xterm-256color && python <(curl -s https://raw.githubusercontent.com/YOURUSERNAME/ToolRejoin/main/zero_rejoin.py)\""
echo ""
echo "Hoặc vào thư mục Download rồi chạy python zero_rejoin.py"
