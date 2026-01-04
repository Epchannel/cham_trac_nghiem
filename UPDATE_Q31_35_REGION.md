# Update: Fix Vùng Q31-35 (Thu Gọn)

## 📋 Tổng Quan
Do đề thi chỉ có 35 câu (thay vì 40 câu), vùng Q31-40 đã được thu gọn còn một nửa (chỉ 5 rows thay vì 10 rows). Update này đảm bảo code detect và vẽ kết quả đúng với vùng đã thu gọn.

## 🔧 Thay Đổi

### 1. File: `functions.py`

#### a. Đọc Answers từ Vùng Q31-35
**Trước:**
```python
answers_31_40, multiple_31_40 = read_answer_block(img, QUESTIONS_31_40, 10, choices)
```

**Sau:**
```python
# Vùng Q31-35 đã thu gọn chỉ còn 5 rows (thay vì 10)
answers_31_40, multiple_31_40 = read_answer_block(img, QUESTIONS_31_40, 5, choices)
```

**Lý do:** Vùng chỉ còn 5 rows, nên khi chia ô phải dùng `num_rows=5` để tính đúng chiều cao mỗi ô.

#### b. Update Label trong Debug Regions
**Trước:**
```python
(QUESTIONS_31_40, (0, 165, 255), "Q31-40"),
```

**Sau:**
```python
(QUESTIONS_31_40, (0, 165, 255), "Q31-35"),
```

**Lý do:** Cập nhật label cho đúng với số câu thực tế (Q31-35).

### 2. File: `api/process_omr.py`

#### a. Vẽ Vòng Tròn Đáp Án
**Trước:**
```python
regions_config = [
    (functions.QUESTIONS_1_10, 0, 10, 10, 4),     # Q1-10
    (functions.QUESTIONS_11_20, 10, 20, 10, 4),   # Q11-20
    (functions.QUESTIONS_21_30, 20, 30, 10, 4),   # Q21-30
    (functions.QUESTIONS_31_40, 30, 35, 10, 4),   # Q31-35 (chỉ 5 câu)
]
```

**Sau:**
```python
regions_config = [
    (functions.QUESTIONS_1_10, 0, 10, 10, 4),     # Q1-10
    (functions.QUESTIONS_11_20, 10, 20, 10, 4),   # Q11-20
    (functions.QUESTIONS_21_30, 20, 30, 10, 4),   # Q21-30
    (functions.QUESTIONS_31_40, 30, 35, 5, 4),    # Q31-35 (chỉ 5 câu, vùng thu gọn 5 rows)
]
```

**Lý do:** Khi vẽ vòng tròn, phải dùng `num_rows=5` để tính đúng vị trí tâm của từng ô đáp án.

#### b. Update Label trong Debug Regions
**Trước:**
```python
(functions.QUESTIONS_31_40, (0, 165, 255), "Q31-40", 2),
```

**Sau:**
```python
(functions.QUESTIONS_31_40, (0, 165, 255), "Q31-35", 2),
```

## 📐 Giải Thích Kỹ Thuật

### Vấn Đề
- Vùng `QUESTIONS_31_40` có tọa độ:
  ```python
  QUESTIONS_31_40 = {
      'x_start': 0.649,
      'x_end': 0.813,
      'y_start': 0.631,
      'y_end': 0.788    # Đã thu gọn (trước đây: ~0.946)
  }
  ```

- Chiều cao vùng: `y_end - y_start = 0.788 - 0.631 = 0.157`
- Chiều cao này chỉ đủ cho **5 rows** (thay vì 10 rows)

### Công Thức Tính Vị Trí Ô
```python
roi_h = y_end - y_start
cell_h = roi_h / num_rows

# Vị trí tâm ô tại row i:
cy = y_start + i * cell_h + cell_h / 2
```

### So Sánh
| Trường hợp | `num_rows` | `cell_h` | Kết quả |
|------------|------------|----------|---------|
| **SAI** (trước) | 10 | roi_h / 10 | Các ô quá nhỏ, vị trí vẽ sai |
| **ĐÚNG** (sau) | 5 | roi_h / 5 | Các ô có kích thước vừa, vị trí chính xác |

## ✅ Test
1. Truy cập: http://localhost:3000
2. Upload ảnh OMR sheet có 35 câu
3. Kiểm tra:
   - ✅ Ảnh "Vùng Detect": khung "Q31-35" bao đúng 5 câu
   - ✅ Ảnh "Kết Quả Chấm": vòng tròn khoanh đúng vị trí đáp án câu 31-35
   - ✅ Không có vòng tròn bị lệch vị trí

## 📝 Lưu Ý
- Nếu sau này có đề 40 câu:
  1. Mở rộng vùng `QUESTIONS_31_40` bằng cách tăng `y_end`
  2. Đổi `num_rows=5` → `num_rows=10` ở cả 2 file
  3. Đổi label `"Q31-35"` → `"Q31-40"`

- Cấu trúc hiện tại:
  ```
  Q1-10:  10 rows (10 câu)
  Q11-20: 10 rows (10 câu)
  Q21-30: 10 rows (10 câu)
  Q31-35: 5 rows (5 câu)   ← Đặc biệt
  ```

## 🎯 Kết Quả
- ✅ Detect đúng vùng Q31-35 (5 câu)
- ✅ Vẽ vòng tròn đúng vị trí cho câu 31-35
- ✅ Label hiển thị "Q31-35" thay vì "Q31-40"
- ✅ Code dễ điều chỉnh nếu cần thay đổi số câu

---
*Cập nhật: 2026-01-04*

