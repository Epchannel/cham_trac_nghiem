# 🎯 CẬP NHẬT: HỆ THỐNG HỖ TRỢ 4 MÃ ĐỀ

## ✨ Tính Năng Mới

Hệ thống đã được cập nhật để hỗ trợ **4 mã đề** với đáp án riêng biệt:

- **Mã đề 101** ✅
- **Mã đề 102** ✅
- **Mã đề 103** ✅
- **Mã đề 104** ✅

---

## 🔄 Cách Hoạt Động

1. **Học sinh tô mã đề** trên phiếu OMR (3 cột số từ 0-9)
2. **Hệ thống tự động nhận diện** mã đề
3. **Chọn đáp án tương ứng** với mã đề đã nhận diện
4. **Chấm điểm** và hiển thị kết quả

### Ví dụ:
- Học sinh tô mã đề **101** → Hệ thống dùng đáp án mã đề 101
- Học sinh tô mã đề **102** → Hệ thống dùng đáp án mã đề 102
- Không tô rõ hoặc mã không hợp lệ → Hệ thống dùng đáp án mặc định (mã đề 101)

---

## 📝 Chi Tiết Đáp Án

Xem file [`MA_DE_DAP_AN.md`](MA_DE_DAP_AN.md) để biết đầy đủ đáp án cho cả 4 mã đề.

### Tóm tắt:

#### MÃ ĐỀ 101
```
Câu 1-5:   D, B, C, B, D
Câu 6-10:  C, B, A, B, D
Câu 11-15: D, C, B, D, D
...và 20 câu còn lại
```

#### MÃ ĐỀ 102
```
Câu 1-5:   B, D, D, A, D
Câu 6-10:  D, C, A, A, A
Câu 11-15: B, A, B, B, C
...và 20 câu còn lại
```

#### MÃ ĐỀ 103
```
Câu 1-5:   C, C, C, C, A
Câu 6-10:  A, A, C, D, D
Câu 11-15: A, B, A, D, A
...và 20 câu còn lại
```

#### MÃ ĐỀ 104
```
Câu 1-5:   C, D, D, B, B
Câu 6-10:  A, A, D, B, C
Câu 11-15: C, A, D, D, A
...và 20 câu còn lại
```

---

## 🎨 Cách Sử Dụng

### 1. Khởi động ứng dụng:
```bash
# Cách 1: Chạy trực tiếp
streamlit run main.py

# Cách 2: Chạy với main_fixed.py
streamlit run main_fixed.py

# Cách 3: Chạy với tunnel (truy cập từ xa)
python run_with_tunnel.py
```

### 2. Upload ảnh phiếu:
- Chọn tab **"📝 Chấm Điểm"**
- Click **"📤 Chọn ảnh phiếu trắc nghiệm..."**
- Chọn ảnh phiếu OMR đã chụp

### 3. Xem kết quả:
- Nhấn nút **"🎯 Chấm Điểm"**
- Hệ thống sẽ tự động:
  - ✅ Nhận diện mã đề
  - ✅ Chọn đáp án phù hợp
  - ✅ Chấm điểm và hiển thị kết quả
  - ✅ Cảnh báo nếu có câu tô nhiều đáp án

---

## 🎯 Các Tính Năng Khác

### 1. **Debug Mode** (Tab 1)
- Bật checkbox **"🔍 Hiển thị vùng detect"**
- Xem các vùng được detect trên phiếu
- Giúp kiểm tra độ chính xác của hệ thống

### 2. **Webcam Mode** (Tab 2 - chỉ trong `main.py`)
- Chụp phiếu trực tiếp từ webcam
- Auto detect và chấm điểm ngay lập tức
- Thích hợp cho chấm điểm nhanh

### 3. **Debug Vùng** (Tab 2/3)
- Điều chỉnh tọa độ các vùng detect
- Preview real-time
- Export code để áp dụng vào `functions.py`

---

## ⚠️ Lưu Ý Quan Trọng

### ✅ Để hệ thống hoạt động tốt:

1. **Chất lượng ảnh:**
   - Chụp rõ ràng, không bị mờ
   - Ánh sáng đủ, không bị tối
   - Không bị che khuất hoặc nhàu nát

2. **Góc chụp:**
   - Chụp thẳng hoặc lệch không quá 20-30°
   - Toàn bộ phiếu phải nằm trong khung hình
   - 4 góc phiếu phải rõ ràng

3. **Cách tô:**
   - Tô rõ ràng, đầy đủ ô tròn/vuông
   - **Chỉ tô 1 đáp án** cho mỗi câu
   - Tô nhiều đáp án → Câu đó bị tính SAI ❌
   - Tô mã đề rõ ràng và chính xác

4. **Phiếu mẫu:**
   - Sử dụng đúng phiếu mẫu (35 câu, 4 lựa chọn)
   - Không sửa chữa, tẩy xóa quá nhiều

---

## 🛠️ Các File Đã Cập Nhật

1. **`functions.py`**
   - Cập nhật hàm `read_answers()` để trả về cả `multiple_marks`
   - Không thay đổi logic chính

2. **`main.py`**
   - Thêm 4 bộ đáp án: `101`, `102`, `103`, `104`
   - Cập nhật logic chọn đáp án theo mã đề
   - Hiển thị cảnh báo khi có câu tô nhiều

3. **`main_fixed.py`**
   - Cập nhật tương tự `main.py`
   - Không có tính năng webcam

4. **`MA_DE_DAP_AN.md`** (Mới)
   - Bảng đáp án chi tiết cho 4 mã đề
   - Dễ đọc, dễ kiểm tra

5. **`UPDATE_MA_DE.md`** (File này)
   - Hướng dẫn sử dụng hệ thống mới
   - Giải thích các tính năng

---

## 🚀 Bắt Đầu Ngay

```bash
# Bước 1: Kích hoạt môi trường (nếu có)
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Bước 2: Cài đặt dependencies (nếu cần)
pip install -r requirements.txt

# Bước 3: Chạy ứng dụng
streamlit run main.py
# Hoặc:
streamlit run main_fixed.py
```

---

## 📞 Hỗ Trợ

Nếu gặp vấn đề:

1. ✅ Kiểm tra lại chất lượng ảnh
2. ✅ Đảm bảo tô đúng mã đề
3. ✅ Sử dụng tab Debug để kiểm tra vùng detect
4. ✅ Thử với ảnh mẫu trước

---

## 🎉 Hoàn Thành!

Hệ thống đã sẵn sàng để chấm phiếu với **4 mã đề** khác nhau!

**Chúc bạn sử dụng hiệu quả!** 🚀📝

---

*Cập nhật: 04/01/2026*

