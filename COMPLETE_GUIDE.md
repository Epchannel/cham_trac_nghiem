# 🎓 Hướng Dẫn Hoàn Chỉnh - Webcam + Remote Access

## 📦 File Cấu Trúc Dự Án

```
OMR-Sheet-Evaluation-System/
├── main.py                      ← App chính (có tab webcam mới)
├── functions.py                 ← Hàm detect & xử lý
├── util.py                      ← Hàm tiện ích
├── style.py                     ← Styling
├── requirements.txt             ← Dependencies
│
├── 🎯 HƯỚNG DẪN
├── QUICK_START.md              ← Bắt đầu nhanh
├── WEBCAM_TUNNEL_GUIDE.md      ← Hướng dẫn chi tiết
├── IMPROVEMENT_NOTES.md        ← Chi tiết cải tiến detect
│
├── 🚀 SCRIPTS KHỞI ĐỘNG
├── start.bat                   ← Chạy bình thường
├── start_network.bat           ← Chạy trên mạng (0.0.0.0)
├── run_with_tunnel.py          ← Chạy với thông tin IP
├── setup_tunnel.py             ← Setup Dev Tunnel/ngrok
├── setup_tunnel.bat            ← Setup tunnel (batch)
│
├── 🧪 TEST & DEBUG
├── test_detection.py           ← Test detect từ CLI
│
└── .streamlit/
    └── config.toml             ← Cấu hình Streamlit
```

---

## 🚀 Cách Chạy (Bước-Bước)

### ✅ Cách Đơn Giản Nhất

**Windows:**
```bash
start.bat
```

**macOS/Linux:**
```bash
python run_with_tunnel.py
```

### ✅ Chạy Trên Mạng (Tất Cả Host)

**Windows:**
```bash
start_network.bat
```

**Hoặc thủ công:**
```bash
streamlit run main.py --server.address=0.0.0.0
```

---

## 📱 Kết Nối Từ Điện Thoại

### 🔷 Cách 1: LAN (Cùng WiFi)

1. **Lấy IP của máy:**
   ```bash
   ipconfig
   # Tìm dòng: IPv4 Address (ví dụ: 192.168.1.100)
   ```

2. **Trên điện thoại, mở:**
   ```
   http://192.168.1.100:8501
   ```

3. **Cho phép webcam khi hỏi**

✅ **Ưu điểm:** Nhanh, không cần internet  
❌ **Nhược điểm:** Chỉ dùng được trên WiFi nhà

---

### 🔷 Cách 2: Dev Tunnel (Qua Internet)

1. **Chạy Setup:**
   ```bash
   python setup_tunnel.py
   # Hoặc: code tunnel
   ```

2. **Chọn: 1 (VS Code Dev Tunnel)**

3. **Đăng nhập GitHub** (nếu được yêu cầu)

4. **Sao chép URL được cung cấp**

5. **Trên điện thoại:**
   - Truy cập URL đó
   - Hoặc quét QR code

✅ **Ưu điểm:** Truy cập từ bất kỳ đâu, an toàn  
❌ **Nhược điểm:** Cần GitHub account, chậm hơn

---

### 🔷 Cách 3: ngrok (Qua Internet)

1. **Cài ngrok:**
   ```bash
   choco install ngrok  # Nếu có Chocolatey
   # Hoặc download từ: https://ngrok.com
   ```

2. **Chạy Setup:**
   ```bash
   python setup_tunnel.py
   # Chọn: 2 (ngrok)
   ```

3. **Sao chép URL từ ngrok**

4. **Trên điện thoại:**
   - Truy cập URL đó

✅ **Ưu điểm:** Đơn giản, nhanh  
❌ **Nhược điểm:** Miễn phí có giới hạn

---

## 📸 Sử Dụng Webcam

### 📷 Tab Webcam

1. **Click nút "Take a picture"**
   - Cho phép truy cập webcam
   - Chụp ảnh phiếu

2. **Chấm điểm tự động**
   - Nếu bật ✅ Auto Detect
   - Xem kết quả ngay lập tức

3. **Điều chỉnh (nếu cần)**
   - Nhập đáp án custom
   - Bật Debug mode để xem detail

### 💡 Mẹo Chụp

```
✅ TỐT                          ❌ XẤU
├─ Góc vuông (0-20°)           ├─ Góc lệch > 30°
├─ Ánh sáng từ trên              ├─ Ánh sáng từ cạnh
├─ Khoảng cách 30-40cm          ├─ Quá gần (< 20cm)
├─ Toàn bộ phiếu có trong hình  ├─ Phiếu bị cắt mép
├─ Ảnh rõ ràng                  └─ Ảnh mờ/bị rung
└─ Phông nền không phản quang
```

---

## 🔧 Các Tab Trong App

### 1️⃣ 📝 **Chấm Điểm** (Upload Ảnh)

**Dùng khi:** Có ảnh sẵn, muốn chấm điểm chi tiết

**Quy trình:**
1. Upload ảnh
2. (Tùy chọn) Nhập đáp án
3. Bấn nút "Chấm Điểm"
4. Xem kết quả

**Output:**
- Ảnh gốc
- Ảnh detect (debug)
- Ảnh kết quả (với vòng tròn)
- Điểm, % phần trăm
- Chi tiết từng câu

---

### 2️⃣ 📷 **Webcam** ⭐ (Mới)

**Dùng khi:** Cần chấm điểm nhanh

**Quy trình:**
1. Click "Take a picture"
2. Chụp phiếu
3. Auto detect (nếu bật)
4. Xem kết quả liền

**Tính năng:**
- ✅ Auto detect
- ✅ Debug mode
- ✅ Custom đáp án
- ✅ Real-time result

---

### 3️⃣ 🔧 **Debug Vùng**

**Dùng khi:** Cấu hình phiếu mới

**Quy trình:**
1. Upload ảnh phiếu mẫu
2. Dùng sliders điều chỉnh vùng
3. Xem preview real-time
4. Copy code → cập nhật `functions.py`

---

## 🛠️ Troubleshooting

### ❌ Webcam không hoạt động

**Nguyên nhân:** Quyền truy cập bị từ chối

**Giải pháp:**
```
Windows:
1. Settings > Privacy & Security > Camera
2. Cho phép ứng dụng truy cập camera
3. Cho phép browser (Chrome/Edge) truy cập

macOS:
1. System Preferences > Security & Privacy
2. Cho phép camera access

Linux:
1. Kiểm tra: ls /dev/video*
2. Chmod: sudo chmod 666 /dev/video0
```

---

### ❌ Không kết nối được trên điện thoại

**Nguyên nhân:** IP sai, Firewall, WiFi khác

**Giải pháp:**
1. **Kiểm tra IP:**
   ```bash
   ipconfig  # Windows
   ifconfig  # macOS/Linux
   ```

2. **Test kết nối:**
   ```bash
   ping 192.168.1.100  # Từ điện thoại thử
   ```

3. **Firewall:**
   - Cho phép port 8501
   - Hoặc tắt tạm để test

4. **Restart WiFi:**
   - Tắt/bật WiFi trên điện thoại
   - Reconnect vào WiFi

---

### ❌ Auto detect quá chậm

**Nguyên nhân:** Máy yếu, image lớn

**Giải pháp:**
1. Tắt Debug mode
2. Giảm kích thước ảnh
3. Chạy trên máy mạnh hơn
4. Chuẩn bị ảnh rõ ràng

---

### ❌ Dev Tunnel không hoạt động

**Nguyên nhân:** Code CLI không cài

**Giải pháp:**
```bash
# Cài VS Code mới nhất từ: code.visualstudio.com

# Hoặc dùng ngrok thay thế
python setup_tunnel.py  # Chọn 2
```

---

## 📊 Performance

| Metric | Local | LAN | Dev Tunnel | ngrok |
|--------|-------|-----|-----------|-------|
| **Latency** | <1ms | 5-50ms | 100-200ms | 50-150ms |
| **Speed** | Fastest | Fast | Slow | Medium |
| **WiFi Dependent** | No | Yes | No | No |
| **Webcam** | < 100ms | < 150ms | 200-500ms | 150-300ms |

---

## 🎯 Use Cases

### 📚 Trường Học
- Test nhanh một câu hỏi
- Webcam -> Auto detect -> Kết quả
- Giáo viên có thể kiểm tra từ điện thoại

### 🏪 Trung Tâm Kỳ Thi
- LAN setup -> Tất cả máy kết nối
- Chấm điểm hàng loạt
- Real-time statistics

### 💻 Remote Work
- Dev Tunnel -> Làm việc từ nhà
- Test trên điện thoại
- Backup online

---

## 📞 Liên Hệ Support

Nếu gặp lỗi:

1. ✅ Check console log của Streamlit
2. ✅ Xem dòng lỗi đầu tiên
3. ✅ Restart Streamlit
4. ✅ Xóa cache `.streamlit/` nếu cần
5. ✅ Restart máy tính

---

## 📋 Checklist Chuẩn Bị

- ✅ Cài Python 3.8+
- ✅ Cài requirements: `pip install -r requirements.txt`
- ✅ Cấu hình phiếu (vùng detect)
- ✅ Test webcam cục bộ
- ✅ Test kết nối mạng
- ✅ Setup tunnel (nếu cần truy cập từ xa)

---

## 🎉 Hoàn Thành!

Bây giờ bạn có thể:
- ✅ Chụp phiếu bằng webcam
- ✅ Detect tự động kết quả
- ✅ Truy cập từ điện thoại (LAN)
- ✅ Truy cập từ xa (Dev Tunnel/ngrok)
- ✅ Debug & customize phiếu

**Chúc bạn sử dụng vui vẻ! 🚀**

---

**Version:** 3.0  
**Cập nhật:** 2025-12-30  
**Features:** Webcam, Auto Detect, Remote Access, LAN Support
