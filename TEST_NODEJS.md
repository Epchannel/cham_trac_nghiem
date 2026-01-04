# 🧪 TEST HƯỚNG DẪN - NODE.JS VERSION

## ✅ Đã Fix Bug JSON Parse!

Hệ thống đã được fix và đang chạy tốt. Hãy test ngay!

---

## 🚀 Test Nhanh (3 bước)

### 1️⃣ Kiểm Tra Server

```bash
# Mở trình duyệt:
http://localhost:3000
```

**Kết quả mong đợi:**
- ✅ Trang web hiển thị đầy đủ
- ✅ Có form upload ảnh
- ✅ Giao diện đẹp, responsive

### 2️⃣ Test API Health

```bash
# Trong browser console (F12) hoặc terminal:
curl http://localhost:3000/api/health
```

**Response:**
```json
{
  "status": "OK",
  "timestamp": "2026-01-04T...",
  "uptime": 123.456
}
```

### 3️⃣ Upload và Chấm Phiếu

1. **Upload ảnh** phiếu OMR (drag & drop hoặc click)
2. **Click "Chấm Điểm"**
3. **Xem kết quả** (2-5 giây)

**Kết quả mong đợi:**
- ✅ Mã đề được nhận diện
- ✅ Số câu đúng/sai
- ✅ Điểm số và xếp loại
- ✅ Chi tiết từng câu
- ✅ **KHÔNG CÓ LỖI!**

---

## 📸 Test Với Ảnh Mẫu

### Option 1: Ảnh Mẫu Có Sẵn

```bash
# Nếu có ảnh mẫu trong assets/
http://localhost:3000
# Upload: assets/Sample_OMR/OMR_20_4.jpg
```

### Option 2: Test Với cURL

```bash
curl -X POST http://localhost:3000/api/process \
  -F "image=@assets/Sample_OMR/OMR_20_4.jpg"
```

**Response mẫu:**
```json
{
  "success": true,
  "data": {
    "success": true,
    "ma_de": "101",
    "correct_count": 26,
    "total_questions": 35,
    "percentage": 74.29,
    "grade": "B",
    "details": [...]
  }
}
```

---

## 🎯 Test Cases

### Test Case 1: Mã Đề 101

**Input:**
- Ảnh phiếu có mã đề 101 tô rõ ràng

**Expected Output:**
- ✅ Mã đề: 101
- ✅ Sử dụng đáp án mã đề 101
- ✅ Chấm điểm chính xác

### Test Case 2: Mã Đề 102, 103, 104

**Input:**
- Ảnh phiếu có mã đề khác

**Expected Output:**
- ✅ Nhận diện đúng mã đề
- ✅ Chọn đáp án tương ứng

### Test Case 3: Tô Nhiều Đáp Án

**Input:**
- Phiếu có câu tô nhiều đáp án

**Expected Output:**
- ✅ Câu đó bị tính SAI
- ⚠️ Cảnh báo: "Có X câu tô nhiều đáp án"

### Test Case 4: Không Tô Đáp Án

**Input:**
- Phiếu có câu không tô

**Expected Output:**
- ✅ Câu đó bị tính SAI
- ✅ Hiển thị "(Trống)" trong chi tiết

### Test Case 5: Custom Answer Key

**Input:**
1. Upload phiếu
2. Mở "Nhập đáp án tùy chỉnh"
3. Nhập: `A,B,C,D,A,B,C,D,...` (35 đáp án)
4. Chấm điểm

**Expected Output:**
- ✅ Sử dụng đáp án tùy chỉnh
- ✅ Bỏ qua đáp án theo mã đề

---

## 🔍 Kiểm Tra Logs

### Server Logs (Terminal)

Logs **TRƯỚC** khi fix:
```
Processing OMR sheet: ...
JSON parse error: Unexpected token 'D'
Result data: Detected using method: markers  ← LỖI!
Ma de detected: [1, 0, 1] -> 101             ← LỖI!
{"success": true, ...}
```

Logs **SAU** khi fix:
```
Processing OMR sheet: ...
::1 - - [...] "POST /api/process HTTP/1.1" 200 ...  ← OK!
```

### Browser Console (F12)

**Không có lỗi:**
```
API Health: {status: "OK", ...}
```

**Khi upload thành công:**
```
Network -> POST /api/process -> Status: 200
Response: {success: true, data: {...}}
```

---

## 🐛 Debug Nếu Gặp Lỗi

### Lỗi: "Không thể detect phiếu"

**Nguyên nhân:**
- Ảnh bị mờ, tối
- Góc chụp quá lệch
- Phiếu bị che khuất

**Giải pháp:**
- Chụp lại với ánh sáng tốt hơn
- Góc thẳng hoặc lệch < 20°
- Đảm bảo toàn bộ phiếu trong khung

### Lỗi: "JSON parse error"

**Nguyên nhân:**
- Bug chưa được fix (unlikely)
- Python script có vấn đề

**Giải pháp:**
1. Restart server
2. Test Python script:
   ```bash
   python api/process_omr.py test.jpg
   ```
3. Kiểm tra output phải là pure JSON

### Lỗi: "File quá lớn"

**Nguyên nhân:**
- File > 10MB

**Giải pháp:**
- Resize ảnh xuống < 10MB
- Hoặc đổi limit trong `server.js`:
  ```javascript
  limits: {
      fileSize: 20 * 1024 * 1024  // 20MB
  }
  ```

---

## 📊 Performance Test

### Test Tốc Độ

```bash
# Test 1 request
time curl -X POST http://localhost:3000/api/process \
  -F "image=@test.jpg"

# Expected: 2-5 seconds
```

### Test Nhiều Requests

```bash
# Test 10 requests liên tiếp
for i in {1..10}; do
  curl -X POST http://localhost:3000/api/process \
    -F "image=@test.jpg"
done
```

**Expected:**
- ✅ Tất cả requests thành công
- ✅ Không bị rate limit (< 100 req/15min)

---

## ✅ Checklist Test

### Basic Functionality
- [ ] Server khởi động thành công
- [ ] Web UI hiển thị đúng
- [ ] API health check OK
- [ ] Upload ảnh thành công
- [ ] Detect phiếu thành công
- [ ] Nhận diện mã đề đúng
- [ ] Chấm điểm chính xác
- [ ] Hiển thị kết quả đầy đủ

### Edge Cases
- [ ] Tô nhiều đáp án → Cảnh báo
- [ ] Không tô → Tính SAI
- [ ] Mã đề không rõ → Dùng default
- [ ] Custom answer key hoạt động
- [ ] File quá lớn → Báo lỗi
- [ ] File không phải ảnh → Báo lỗi

### Performance
- [ ] Xử lý trong 2-5 giây
- [ ] Không bị crash khi upload liên tục
- [ ] Memory không leak

### Security
- [ ] Rate limiting hoạt động
- [ ] File validation hoạt động
- [ ] Upload folder tự động xóa
- [ ] CORS configured

---

## 🎉 Test Thành Công!

Nếu tất cả test cases pass:
- ✅ **Hệ thống hoạt động tốt**
- ✅ **Sẵn sàng sử dụng**
- ✅ **Có thể deploy**

---

## 📞 Báo Lỗi

Nếu gặp lỗi:

1. **Kiểm tra logs** trong terminal
2. **Mở Browser Console** (F12)
3. **Test Python script** độc lập
4. **Xem** `BUGFIX_NODEJS.md` để debug

---

## 🚀 Next: Deploy

Sau khi test thành công local:
- 📖 Đọc `DEPLOY.md` để deploy lên server
- 🌐 Test trên production
- 📊 Monitor logs

---

**Status:** ✅ READY FOR TESTING  
**Last Updated:** 04/01/2026  
**Bug Status:** Fixed & Tested

