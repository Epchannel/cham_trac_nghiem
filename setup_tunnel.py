"""
Setup Dev Tunnel cho Streamlit OMR App
Tự động kiểm tra và thiết lập kết nối từ xa
"""

import subprocess
import sys
import os
from pathlib import Path

def check_vscode():
    """Kiểm tra VS Code CLI có được cài không"""
    try:
        result = subprocess.run(['code', '--version'], 
                              capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except:
        return False

def check_ngrok():
    """Kiểm tra ngrok có được cài không"""
    try:
        result = subprocess.run(['ngrok', '--version'], 
                              capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except:
        return False

def setup_dev_tunnel():
    """Setup VS Code Dev Tunnel"""
    print("🔐 Setting up VS Code Dev Tunnel...")
    print()
    
    if not check_vscode():
        print("❌ VS Code CLI không được tìm thấy!")
        print()
        print("📥 Hãy cài đặt VS Code Dev Tunnel:")
        print("   1. Cài VS Code (nếu chưa): https://code.visualstudio.com")
        print("   2. Mở VS Code")
        print("   3. Nhấn Ctrl+Shift+P → "Dev Tunnels: Open Tunnel..."")
        print("   4. Hoặc chạy: code tunnel")
        print()
        return False
    
    print("✅ VS Code CLI tìm thấy!")
    print()
    print("⏳ Khởi động tunnel...")
    print()
    print("   1. Bạn sẽ được yêu cầu đăng nhập GitHub")
    print("   2. Sao chép URL được cung cấp")
    print("   3. Chia sẻ URL với người khác")
    print()
    
    try:
        subprocess.run(['code', 'tunnel'])
        return True
    except KeyboardInterrupt:
        print("\n\n❌ Hủy bỏ")
        return False

def setup_ngrok():
    """Setup ngrok (thay thế cho Dev Tunnel)"""
    print("🔗 Setting up ngrok...")
    print()
    
    if not check_ngrok():
        print("❌ ngrok không được tìm thấy!")
        print()
        print("📥 Hãy cài đặt ngrok:")
        print("   1. Download: https://ngrok.com/download")
        print("   2. Hoặc: choco install ngrok (nếu có Chocolatey)")
        print("   3. Rồi chạy: ngrok http 8501")
        print()
        return False
    
    print("✅ ngrok tìm thấy!")
    print()
    print("⏳ Khởi động tunnel...")
    print()
    
    try:
        subprocess.run(['ngrok', 'http', '8501'])
        return True
    except KeyboardInterrupt:
        print("\n\n❌ Hủy bỏ")
        return False

def main():
    print("=" * 70)
    print("  🚀 Dev Tunnel Setup for OMR Streamlit App")
    print("=" * 70)
    print()
    
    print("Chọn cách kết nối từ xa:")
    print()
    print("1️⃣  VS Code Dev Tunnel (Khuyến nghị - Bảo mật hơn)")
    print("2️⃣  ngrok (Đơn giản - Cần tài khoản)")
    print("3️⃣  Kết nối Local LAN (Không cần setup)")
    print("0️⃣  Thoát")
    print()
    
    choice = input("Nhập lựa chọn (0-3): ").strip()
    
    if choice == '1':
        if setup_dev_tunnel():
            print("\n✅ Dev Tunnel đã được thiết lập!")
        else:
            print("\n❌ Thiết lập thất bại")
    
    elif choice == '2':
        if setup_ngrok():
            print("\n✅ ngrok đã được thiết lập!")
        else:
            print("\n❌ Thiết lập thất bại")
    
    elif choice == '3':
        print("\n💡 Hướng dẫn kết nối LAN:")
        print()
        print("   1. Lấy IP máy tính: ipconfig")
        print("   2. Chạy Streamlit: streamlit run main.py")
        print("   3. Trên điện thoại, mở: http://<IP>:8501")
        print()
        print("   Ví dụ: http://192.168.1.100:8501")
        print()
    
    elif choice == '0':
        print("\n👋 Tạm biệt!")
        sys.exit(0)
    
    else:
        print("\n❌ Lựa chọn không hợp lệ")

if __name__ == "__main__":
    main()
