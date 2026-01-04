"""
Script test để kiểm tra hệ thống với các mã đề khác nhau
"""

import sys
import io

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Đáp án cho các mã đề (0=A, 1=B, 2=C, 3=D)
ANSWER_KEYS = {
    "101": [
        # Câu 1-10: D, B, C, B, D, C, B, A, B, D
        3, 1, 2, 1, 3, 2, 1, 0, 1, 3,
        # Câu 11-20: D, C, B, D, D, A, D, A, D, A
        3, 2, 1, 3, 3, 0, 3, 0, 3, 0,
        # Câu 21-30: D, B, C, D, B, A, A, A, B, D
        3, 1, 2, 3, 1, 0, 0, 0, 1, 3,
        # Câu 31-35: C, A, A, B, D
        2, 0, 0, 1, 3
    ],
    "102": [
        # Câu 1-10: B, D, D, A, D, D, C, A, A, A
        1, 3, 3, 0, 3, 3, 2, 0, 0, 0,
        # Câu 11-20: B, A, B, B, C, B, C, B, C, D
        1, 0, 1, 1, 2, 1, 2, 1, 2, 3,
        # Câu 21-30: D, B, D, B, A, D, D, A, A, A
        3, 1, 3, 1, 0, 3, 3, 0, 0, 0,
        # Câu 31-35: D, C, C, B, A
        3, 2, 2, 1, 0
    ],
    "103": [
        # Câu 1-10: C, C, C, C, A, A, A, C, D, D
        2, 2, 2, 2, 0, 0, 0, 2, 3, 3,
        # Câu 11-20: A, B, A, D, A, C, C, C, D, C
        0, 1, 0, 3, 0, 2, 2, 2, 3, 2,
        # Câu 21-30: D, D, B, A, A, C, C, D, D, B
        3, 3, 1, 0, 0, 2, 2, 3, 3, 1,
        # Câu 31-35: C, A, B, A, D
        2, 0, 1, 0, 3
    ],
    "104": [
        # Câu 1-10: A, C, A, C, A, D, D, B, D, D
        0, 2, 0, 2, 0, 3, 3, 1, 3, 3,
        # Câu 11-20: D, C, D, A, C, A, C, C, B, A
        3, 2, 3, 0, 2, 0, 2, 2, 1, 0,
        # Câu 21-30: A, B, C, D, D, D, D, A, D, A
        0, 1, 2, 3, 3, 3, 3, 0, 3, 0,
        # Câu 31-35: B, C, B, A, A
        1, 2, 1, 0, 0
    ]
}

def answer_to_letter(num):
    """Chuyển số sang chữ"""
    mapping = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}
    return mapping.get(num, '?')

def print_answer_key(ma_de):
    """In đáp án của một mã đề"""
    if ma_de not in ANSWER_KEYS:
        print(f"❌ Mã đề {ma_de} không tồn tại!")
        return
    
    print(f"\n{'='*60}")
    print(f"  MÃ ĐỀ {ma_de}")
    print(f"{'='*60}")
    
    answers = ANSWER_KEYS[ma_de]
    
    # In theo từng dòng 5 câu
    for i in range(0, 35, 5):
        line = []
        for j in range(5):
            idx = i + j
            if idx < 35:
                ans_letter = answer_to_letter(answers[idx])
                line.append(f"Câu {idx+1:2d}: {ans_letter}")
        print("  " + "    ".join(line))
    
    print(f"{'='*60}\n")

def compare_answer_keys():
    """So sánh các mã đề xem có câu nào trùng đáp án không"""
    print("\n" + "="*60)
    print("  SO SÁNH ĐÁP ÁN GIỮA CÁC MÃ ĐỀ")
    print("="*60 + "\n")
    
    ma_de_list = ["101", "102", "103", "104"]
    
    # Đếm số câu giống nhau giữa các cặp mã đề
    for i, ma_de_1 in enumerate(ma_de_list):
        for ma_de_2 in ma_de_list[i+1:]:
            same_count = sum(1 for a, b in zip(ANSWER_KEYS[ma_de_1], ANSWER_KEYS[ma_de_2]) if a == b)
            percent = (same_count / 35) * 100
            print(f"  Mã {ma_de_1} vs Mã {ma_de_2}: {same_count}/35 câu giống ({percent:.1f}%)")
    
    print()

def verify_all_keys():
    """Kiểm tra tính hợp lệ của tất cả các bộ đáp án"""
    print("\n" + "="*60)
    print("  KIỂM TRA TÍNH HỢP LỆ CỦA ĐÁP ÁN")
    print("="*60 + "\n")
    
    all_valid = True
    
    for ma_de, answers in ANSWER_KEYS.items():
        # Kiểm tra số lượng câu
        if len(answers) != 35:
            print(f"❌ Mã đề {ma_de}: Số câu không đúng ({len(answers)}/35)")
            all_valid = False
            continue
        
        # Kiểm tra giá trị hợp lệ (0-3)
        invalid = [i+1 for i, a in enumerate(answers) if a not in [0, 1, 2, 3]]
        if invalid:
            print(f"❌ Mã đề {ma_de}: Có {len(invalid)} câu có giá trị không hợp lệ: {invalid[:10]}...")
            all_valid = False
            continue
        
        # Đếm số lượng mỗi đáp án
        count_a = answers.count(0)
        count_b = answers.count(1)
        count_c = answers.count(2)
        count_d = answers.count(3)
        
        print(f"✅ Mã đề {ma_de}: A={count_a}, B={count_b}, C={count_c}, D={count_d}")
    
    print()
    if all_valid:
        print("✅ Tất cả các bộ đáp án đều hợp lệ!")
    else:
        print("❌ Có lỗi trong các bộ đáp án!")
    print()

def main():
    """Hàm chính"""
    print("\n" + "="*60)
    print("  🎯 KIỂM TRA HỆ THỐNG MÃ ĐỀ")
    print("="*60)
    
    # Kiểm tra tính hợp lệ
    verify_all_keys()
    
    # So sánh các mã đề
    compare_answer_keys()
    
    # In từng mã đề
    if len(sys.argv) > 1:
        # In mã đề cụ thể
        for ma_de in sys.argv[1:]:
            print_answer_key(ma_de)
    else:
        # In tất cả
        print("📋 In tất cả đáp án (hoặc chỉ định mã đề: python test_ma_de.py 101 102):\n")
        for ma_de in ["101", "102", "103", "104"]:
            print_answer_key(ma_de)
    
    print("\n" + "="*60)
    print("  ✅ HOÀN THÀNH!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()

