# 🎯 HỆ THỐNG CHẤM ĐIỂM OMR - 4 MÃ ĐỀ

## 📋 Tóm Tắt Nhanh

Hệ thống đã được cập nhật để hỗ trợ **4 mã đề** (101, 102, 103, 104) với tự động nhận diện và chọn đáp án phù hợp.

---

## 🚀 Khởi Động Nhanh

```bash
# Chạy ứng dụng
streamlit run main.py
```

Hoặc:

```bash
streamlit run main_fixed.py
```

Sau đó mở trình duyệt: **http://localhost:8501**

---

## 📂 Các File Quan Trọng

### File Chính
- **`main.py`** - Ứng dụng chính (có Webcam)
- **`main_fixed.py`** - Ứng dụng không có Webcam
- **`functions.py`** - Các hàm xử lý OMR

### File Đáp Án
- **`MA_DE_DAP_AN.md`** - Bảng đáp án đầy đủ 4 mã đề
- **`test_ma_de.py`** - Script kiểm tra đáp án

### File Hướng Dẫn
- **`UPDATE_MA_DE.md`** - Hướng dẫn chi tiết
- **`CHANGELOG_MA_DE.md`** - Lịch sử thay đổi
- **`README_MA_DE.md`** - File này

---

## 📖 Cách Sử Dụng

### Bước 1: Upload Ảnh
- Tab **"📝 Chấm Điểm"**
- Click **"Chọn ảnh phiếu trắc nghiệm..."**
- Chọn ảnh phiếu đã chụp

### Bước 2: Chấm Điểm
- Click nút **"🎯 Chấm Điểm"**
- Đợi hệ thống xử lý (2-5 giây)

### Bước 3: Xem Kết Quả
Hệ thống hiển thị:
- ✅ Mã đề (tự động nhận diện)
- ✅ Số câu đúng/sai
- ✅ Điểm số và xếp loại
- ✅ Chi tiết từng câu

---

## 🎯 4 Mã Đề

| Mã Đề | Số Câu | Phân Bố Đáp Án |
|-------|--------|----------------|
| 101   | 35     | A=9, B=9, C=5, D=12 |
| 102   | 35     | A=10, B=9, C=6, D=10 |
| 103   | 35     | A=10, B=4, C=12, D=9 |
| 104   | 35     | A=11, B=7, C=7, D=10 |

**Xem chi tiết:** [`MA_DE_DAP_AN.md`](MA_DE_DAP_AN.md)

---

## ✅ Kiểm Tra Hệ Thống

```bash
# Kiểm tra đáp án
python test_ma_de.py

# Kiểm tra detect phiếu
python test_detection.py <đường_dẫn_ảnh>
```

---

## ⚠️ Lưu Ý

### Yêu Cầu Phiếu OMR
- ✅ Tô **rõ ràng** mã đề
- ✅ Chỉ tô **1 đáp án**/câu
- ✅ Chụp ảnh **rõ nét**
- ✅ Góc chụp < 30°
- ✅ Ánh sáng tốt

### Xử Lý Lỗi
- **Tô nhiều đáp án** → Sai ❌
- **Không tô** → Sai ❌
- **Mã đề không rõ** → Dùng mặc định (101)

---

## 📊 Tính Năng

✅ Tự động nhận diện mã đề  
✅ Chọn đáp án phù hợp  
✅ Chấm điểm chính xác  
✅ Cảnh báo tô nhiều đáp án  
✅ Hiển thị chi tiết kết quả  
✅ Hỗ trợ webcam (main.py)  
✅ Debug vùng detect  

---

## 📞 Tài Liệu Chi Tiết

- **Hướng dẫn sử dụng:** [`UPDATE_MA_DE.md`](UPDATE_MA_DE.md)
- **Lịch sử thay đổi:** [`CHANGELOG_MA_DE.md`](CHANGELOG_MA_DE.md)
- **Bảng đáp án:** [`MA_DE_DAP_AN.md`](MA_DE_DAP_AN.md)
- **Hướng dẫn chung:** [`README.md`](README.md)

---

## 🎉 Hoàn Thành

Hệ thống sẵn sàng chấm điểm với **4 mã đề**!

**Chúc bạn sử dụng hiệu quả!** 🚀

---

*Version 2.0 - Cập nhật: 04/01/2026*

