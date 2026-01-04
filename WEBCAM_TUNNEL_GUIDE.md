# 📱 Hệ Thống Chấm Phiếu OMR - Với Webcam & Remote Access

## 🎯 Tính Năng Mới

### 📷 Tab Webcam (Webcam Auto-Detect)
- **Chụp trực tiếp** từ webcam
- **Auto-detect tự động** sau khi chụp
- **Xem kết quả tức thì** (không cần bấn nút)
- **Debug mode** tùy chọn

### 🌐 Remote Access (Truy cập từ xa)
- **Cùng mạng LAN:** Truy cập qua IP local
- **Qua Internet:** Dùng Dev Tunnel hoặc ngrok
- **Trên điện thoại:** Mở browser và truy cập URL

---

## 🚀 Cách Chạy

### Cách 1️⃣: Chạy Thường (Local Machine)

```bash
cd "e:\Co Oanh\OMR-Sheet-Evaluation-System"
streamlit run main.py
```

Truy cập: `http://localhost:8501`

### Cách 2️⃣: Chạy Với Thông Tin Kết Nối (Khuyến Nghị)

```bash
python run_with_tunnel.py
```

Hiển thị:
```
📱 Thông Tin Kết Nối:
  • Local:  http://localhost:8501
  • Network: http://192.168.1.100:8501
```

### Cách 3️⃣: Chạy Với Dev Tunnel (Truy Cập Từ Xa)

**Yêu cầu:** Cài đặt VS Code

```bash
# Option A: Chạy script batch
setup_tunnel.bat

# Option B: Chạy thủ công
code tunnel
```

Rồi ở terminal khác:
```bash
streamlit run main.py
```

---

## 📱 Kết Nối Từ Điện Thoại

### Trên Cùng Mạng LAN

1. Xác định IP của máy tính (ví dụ: `192.168.1.100`)
2. Trên điện thoại, mở Chrome/Safari
3. Truy cập: `http://192.168.1.100:8501`
4. Cho phép truy cập webcam khi hỏi

### Qua Internet (Dev Tunnel)

1. Chạy: `code tunnel`
2. Đăng nhập GitHub account
3. Sao chép URL được cung cấp
4. Trên điện thoại, truy cập URL đó
5. Hoặc quét QR code

### Qua Internet (ngrok - Thay Thế)

```bash
# Cài ngrok (nếu chưa có)
choco install ngrok
# hoặc download từ https://ngrok.com

# Tạo tunnel
ngrok http 8501
```

Sao chép URL từ ngrok và chia sẻ

---

## 📋 Các Tab Trong App

### 1️⃣ **📝 Chấm Điểm** (Tab Upload Ảnh)
- Upload ảnh phiếu từ file
- Chấm điểm thủ công (click nút)
- Xem chi tiết kết quả

### 2️⃣ **📷 Webcam** (Tab Mới ⭐)
- Chụp ảnh trực tiếp từ webcam
- **Auto-detect** tự động chấm điểm
- Xem kết quả ngay lập tức
- Debug mode tùy chọn

### 3️⃣ **🔧 Debug Vùng**
- Điều chỉnh vùng detect bằng slider
- Xem preview real-time
- Export code để update `functions.py`

---

## ⚙️ Cấu Hình Webcam

### Trong App

**Thanh Sidebar:**
- ✅ `🔍 Hiển thị vùng detect (Debug)` - Xem chi tiết detect
- ✅ `⚡ Auto Detect Khi Chụp` - Tự động chấm điểm (mặc định ON)
- 📋 Nhập đáp án (nếu muốn tùy chỉnh)

### Hướng Dẫn Chụp Tốt

```
✅ Tốt                          ❌ Xấu
├─ Góc vuông (0-20°)           ├─ Góc lệch > 30°
├─ Ánh sáng từ trên              ├─ Ánh sáng từ cạnh
├─ Toàn bộ phiếu trong khung    ├─ Phiếu bị cắt mép
├─ Ảnh rõ ràng                  ├─ Ảnh mơ
└─ Khoảng cách 30-40cm         └─ Quá gần hoặc quá xa
```

---

## 🔐 Bảo Mật

### Dev Tunnel
- Cần đăng nhập GitHub
- Các tunnel được mã hóa
- Có thể revoke bất cứ lúc nào

### ngrok
- Miễn phí cho local (1 tunnel)
- Cần token nếu múi tinh

### Không Nên
- ❌ Chia sẻ URL công khai lâu dài
- ❌ Chạy trên WiFi không bảo mật
- ❌ Mở firewall cho tất cả port

---

## 🆘 Troubleshooting

### Webcam không hoạt động
```
❌ "Permission denied" hoặc "No camera"

✅ Giải pháp:
1. Kiểm tra quyền trong Settings > Privacy
2. Cho phép browser truy cập webcam
3. Chạy Streamlit với admin nếu cần
```

### Không kết nối được qua mạng
```
❌ "Connection refused" hoặc timeout

✅ Giải pháp:
1. Kiểm tra IP: ipconfig (Windows)
2. Ping máy từ điện thoại
3. Kiểm tra Firewall cho port 8501
4. Chạy: streamlit run main.py --server.address=0.0.0.0
```

### Dev Tunnel không hoạt động
```
❌ "Code tunnel not found"

✅ Giải pháp:
1. Cài VS Code mới nhất
2. Đăng nhập: code tunnel user login
3. Hoặc dùng ngrok thay thế
```

### Auto-detect quá chậm
```
❌ Mất 2-3 giây để detect

✅ Giải pháp:
1. Tắt Debug mode (🔍)
2. Chạy trên máy mạnh hơn
3. Giảm kích thước ảnh (scale down)
```

---

## 📊 Performance

| Metric | Local | LAN | Dev Tunnel |
|--------|-------|-----|-----------|
| Latency | <1ms | 5-50ms | 50-200ms |
| Bandwidth | Unlimited | Limited by WiFi | 1-10 Mbps |
| Webcam Latency | <100ms | <150ms | 200-500ms |

---

## 🎓 Ví Dụ URL Kết Nối

### Local (Máy tính)
```
http://localhost:8501
```

### LAN (Cùng mạng WiFi)
```
http://192.168.1.100:8501
http://192.168.0.50:8501
```

### Dev Tunnel (Qua Internet)
```
https://xxxxxxxx-xx-xx-xxxx.githubpreview.dev
```

### ngrok (Qua Internet)
```
https://xxxxxxxx-ngrok-io.tunnels.ngrok.io
```

---

## 💡 Tips & Tricks

1. **Lưu URL**: Bookmark URL Dev Tunnel để không phải chạy lại
2. **Tăng Timeout**: Nếu mạng chậm, tăng timeout trong settings
3. **Disable HTTPS**: Nếu lỗi SSL, thêm `--server.ssl_certfile=...`
4. **Multiple Users**: Dev Tunnel hỗ trợ many users cùng lúc
5. **Auto Refresh**: Browser auto-refresh khi code thay đổi

---

## 📞 Support

Nếu gặp vấn đề:
1. Check console log (Streamlit terminal)
2. Tắt Extensions trên browser
3. Xóa cache & cookies
4. Chạy lại Streamlit
5. Restart máy nếu cần

---

**Cập nhật:** 2025-12-30  
**Phiên bản:** v3.0 - Webcam + Remote Access
