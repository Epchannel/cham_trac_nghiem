# 🎯 Quick Start - Chạy App Với Webcam & Tunnel

## ⚡ Bắt Đầu Nhanh Nhất

### 1️⃣ Chạy App (Local)
```bash
cd "e:\Co Oanh\OMR-Sheet-Evaluation-System"
streamlit run main.py
```
→ Mở: `http://localhost:8501`

### 2️⃣ Truy Cập Từ Điện Thoại (Cùng WiFi)
```bash
# Terminal lấy IP
ipconfig

# Giả sử IP là 192.168.1.100
# Trên điện thoại, mở: http://192.168.1.100:8501
```

### 3️⃣ Truy Cập Từ Xa (Dev Tunnel)
```bash
# Terminal 1: Mở tunnel
code tunnel

# Terminal 2: Chạy app
streamlit run main.py
```
→ Dùng URL từ code tunnel

---

## 📱 Các Tab Trong App

| Tab | Chức Năng | Dùng Khi Nào |
|-----|----------|------------|
| **📝 Chấm Điểm** | Upload ảnh từ file | Có ảnh sẵn |
| **📷 Webcam** ⭐ | Chụp + auto detect | Cần detect nhanh |
| **🔧 Debug** | Điều chỉnh vùng | Cấu hình phiếu |

---

## 🚀 Tính Năng Mới

✅ **Webcam Input** - Chụp trực tiếp từ camera  
✅ **Auto Detect** - Tự động chấm điểm sau khi chụp  
✅ **Dev Tunnel** - Truy cập từ điện thoại/máy khác  
✅ **LAN Access** - Không cần internet, chỉ cần WiFi  

---

## 📖 Tài Liệu Chi Tiết

Xem file: `WEBCAM_TUNNEL_GUIDE.md`

---

## 💡 Tips

- 📸 **Webcam:** Chụp góc 0-20°, ánh sáng tốt
- 🌐 **IP:** Dùng `ipconfig` (Windows) để lấy IP
- 🔐 **Bảo Mật:** Dev Tunnel yêu cầu đăng nhập GitHub
- ⚡ **Nhanh Nhất:** Chạy local trên máy tính

---

**Được hỗ trợ:** Streamlit, OpenCV, Webcam, Dev Tunnel  
**Cập nhật:** 2025-12-30 v3.0
