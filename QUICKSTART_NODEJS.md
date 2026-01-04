# ⚡ QUICK START - NODE.JS VERSION

## 🚀 Bắt Đầu Ngay trong 3 Bước

### 1️⃣ Cài Đặt Dependencies

```bash
npm install
```

### 2️⃣ Khởi Động Server

```bash
# Windows
start_nodejs.bat

# Mac/Linux hoặc Windows PowerShell
npm start
```

### 3️⃣ Mở Trình Duyệt

Truy cập: **http://localhost:3000**

---

## ✅ Xong! Đơn Giản Thế Thôi!

Bây giờ bạn có thể:
1. Upload ảnh phiếu OMR
2. Click "Chấm Điểm"
3. Xem kết quả ngay lập tức

---

## 📱 Giao Diện

### Upload Phiếu
- Kéo thả ảnh vào khung upload
- Hoặc click để chọn file
- Preview ảnh trước khi xử lý

### Kết Quả
- Mã đề tự động nhận diện
- Số câu đúng/sai
- Điểm số và xếp loại
- Chi tiết từng câu

---

## 🎯 API Test

### Health Check
```bash
curl http://localhost:3000/api/health
```

### Process OMR
```bash
curl -X POST http://localhost:3000/api/process \
  -F "image=@path/to/omr-sheet.jpg"
```

---

## 📋 Mã Đề

Hệ thống hỗ trợ 4 mã đề:

| Mã Đề | Số Câu | Tự Động Chọn Đáp Án |
|-------|--------|---------------------|
| 101   | 35     | ✅                  |
| 102   | 35     | ✅                  |
| 103   | 35     | ✅                  |
| 104   | 35     | ✅                  |

---

## ⚠️ Yêu Cầu

### Phần Mềm
- ✅ Node.js >= 14.0.0
- ✅ Python >= 3.7
- ✅ npm >= 6.0.0

### Thư Viện Python
- ✅ opencv-python
- ✅ numpy
- ✅ Pillow

*Đã cài đặt từ trước (từ Streamlit version)*

---

## 🆚 So Sánh với Streamlit

| Tính Năng | Streamlit | Node.js |
|-----------|-----------|---------|
| Cài đặt | Python only | Node.js + Python |
| Giao diện | Auto-generated | Custom HTML/CSS |
| API | ❌ | ✅ |
| Tốc độ | Chậm hơn | Nhanh hơn |
| Deploy | Khó hơn | Dễ hơn |
| Tùy biến | Hạn chế | Linh hoạt |

---

## 💡 Tips

### Chụp Ảnh Tốt
- ✅ Góc thẳng hoặc lệch < 20°
- ✅ Ánh sáng đều, không bị tối
- ✅ Toàn bộ phiếu trong khung hình
- ✅ Tô rõ ràng mã đề

### Performance
- ✅ File size < 5MB tối ưu nhất
- ✅ Format: JPG (nhẹ hơn PNG)
- ✅ Resolution: 1000-2000px width

---

## 🔧 Cấu Hình

### Thay Đổi Port

```bash
# Tạo file .env
echo PORT=8080 > .env
```

### Tùy Chỉnh Upload Size

Edit `server.js`:
```javascript
limits: {
    fileSize: 20 * 1024 * 1024 // 20MB
}
```

---

## 📚 Tài Liệu

- 📖 [README_NODEJS.md](README_NODEJS.md) - Hướng dẫn đầy đủ
- 🚀 [DEPLOY.md](DEPLOY.md) - Hướng dẫn deploy
- 📋 [MA_DE_DAP_AN.md](MA_DE_DAP_AN.md) - Bảng đáp án

---

## 🐛 Gặp Lỗi?

### Port đã được sử dụng
```bash
# Thay đổi port
set PORT=3001
npm start
```

### Lỗi Python
```bash
# Kiểm tra Python
python --version

# Test script
python api/process_omr.py
```

### Lỗi Upload
```bash
# Kiểm tra thư mục uploads
mkdir uploads
```

---

## 🎉 Hoàn Thành!

Hệ thống đã sẵn sàng! Enjoy! 🚀📝

**Next Steps:**
- Test với ảnh mẫu
- Deploy lên server
- Tùy biến giao diện
- Thêm tính năng mới

---

**Version:** 2.0.0  
**Updated:** 04/01/2026  
**Ready for:** ✅ Development | ✅ Testing | ✅ Production

