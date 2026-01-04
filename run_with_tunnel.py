"""
Script để khởi động Streamlit với Dev Tunnel
Cho phép truy cập từ điện thoại hoặc máy khác
"""

import subprocess
import sys
import os
import socket
import webbrowser
from time import sleep

def get_local_ip():
    """Lấy IP local của máy"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

def main():
    print("=" * 60)
    print("  🚀 Streamlit OMR App - Với Webcam & Dev Tunnel")
    print("=" * 60)
    print()
    
    # Thông tin kết nối
    local_ip = get_local_ip()
    port = "8501"
    
    print("📱 Thông Tin Kết Nối:")
    print(f"  • Local:  http://localhost:{port}")
    print(f"  • Network: http://{local_ip}:{port}")
    print()
    print("🌐 Để kết nối từ điện thoại cùng mạng:")
    print(f"  → Mở trình duyệt và truy cập: http://{local_ip}:{port}")
    print()
    print("🔐 Để kết nối từ xa (qua Dev Tunnel):")
    print("  → Chạy: code tunnel")
    print("  → Hoặc sử dụng: ngrok http 8501")
    print()
    print("-" * 60)
    print()
    
    # Khởi động Streamlit
    try:
        print("⏳ Khởi động Streamlit...")
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "main.py",
            "--logger.level=info"
        ], cwd=os.path.dirname(os.path.abspath(__file__)))
    except KeyboardInterrupt:
        print("\n\n❌ Streamlit đã dừng")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
