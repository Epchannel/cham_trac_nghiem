"""
Python script để xử lý OMR sheet được gọi từ Node.js
Nhận tham số: đường dẫn ảnh và custom answer key (optional)
Trả về JSON kết quả
"""

import sys
import json
import os
import cv2
import numpy as np
import base64

# Suppress print statements from functions.py
import io
_original_stdout = sys.stdout
sys.stdout = io.StringIO()

# Add parent directory to path để import functions
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import functions
import util

# Restore stdout for JSON output
sys.stdout = _original_stdout

# Cấu hình
widthImg = 600
heightImg = 800
MA_DE_DIGITS = 3
DIGIT_COUNT = 10
TOTAL_QUESTIONS = 35
CHOICES = 4
QUESTIONS_PER_COLUMN = 10
MARKS_PER_QUESTION = 1

# Đáp án cho 4 mã đề
ANSWER_KEYS = {
    "101": [
        3, 1, 2, 1, 3, 2, 1, 0, 1, 3,
        3, 2, 1, 3, 3, 0, 3, 0, 3, 0,
        3, 1, 2, 3, 1, 0, 0, 0, 1, 3,
        2, 0, 0, 1, 3
    ],
    "102": [
        1, 3, 3, 0, 3, 3, 2, 0, 0, 0,
        1, 0, 1, 1, 2, 1, 2, 1, 2, 3,
        3, 1, 3, 1, 0, 3, 3, 0, 0, 0,
        3, 2, 2, 1, 0
    ],
    "103": [
        2, 2, 2, 2, 0, 0, 0, 2, 3, 3,
        0, 1, 0, 3, 0, 2, 2, 2, 3, 2,
        3, 3, 1, 0, 0, 2, 2, 3, 3, 1,
        2, 0, 1, 0, 3
    ],
    "104": [
        0, 2, 0, 2, 0, 3, 3, 1, 3, 3,
        3, 2, 3, 0, 2, 0, 2, 2, 1, 0,
        0, 1, 2, 3, 3, 3, 3, 0, 3, 0,
        1, 2, 1, 0, 0
    ],
    "default": [
        3, 1, 2, 1, 3, 2, 1, 0, 1, 3,
        3, 2, 1, 3, 3, 0, 3, 0, 3, 0,
        3, 1, 2, 3, 1, 0, 0, 0, 1, 3,
        2, 0, 0, 1, 3
    ]
}

def convert_custom_answer_key(custom_str):
    """Chuyển đổi custom answer key từ string sang list"""
    if not custom_str:
        return None
    
    try:
        mapping = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
        parts = [p.strip().upper() for p in custom_str.split(',')]
        if len(parts) >= TOTAL_QUESTIONS:
            return [mapping.get(p, 0) for p in parts[:TOTAL_QUESTIONS]]
    except:
        return None
    
    return None

def answer_to_letter(num):
    """Chuyển số sang chữ"""
    mapping = {0: 'A', 1: 'B', 2: 'C', 3: 'D', -1: ''}
    return mapping.get(num, '?')

def encode_image_to_base64(img):
    """Encode ảnh OpenCV sang base64 string"""
    try:
        _, buffer = cv2.imencode('.jpg', img)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        return f"data:image/jpeg;base64,{img_base64}"
    except:
        return None

def draw_debug_image(img):
    """Vẽ các vùng detect lên ảnh"""
    result = img.copy()
    h, w = result.shape[:2]
    
    # Định nghĩa các vùng và màu
    regions = [
        (functions.MA_DE_REGION, (255, 0, 0), "MA DE", 2),
        (functions.QUESTIONS_1_10, (0, 255, 0), "Q1-10", 2),
        (functions.QUESTIONS_11_20, (0, 255, 255), "Q11-20", 2),
        (functions.QUESTIONS_21_30, (255, 0, 255), "Q21-30", 2),
        (functions.QUESTIONS_31_40, (0, 165, 255), "Q31-35", 2),
    ]
    
    for region, color, label, thickness in regions:
        x1 = int(w * region['x_start'])
        y1 = int(h * region['y_start'])
        x2 = int(w * region['x_end'])
        y2 = int(h * region['y_end'])
        
        # Vẽ hình chữ nhật
        cv2.rectangle(result, (x1, y1), (x2, y2), color, thickness)
        
        # Vẽ label
        cv2.putText(result, label, (x1 + 5, y1 + 20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    
    return result

def draw_answer_results(img, answers, grading, answer_key, multiple_marks, ma_de='', correct_count=0, total_questions=35, percentage=0, grade=''):
    """Vẽ kết quả chấm điểm lên ảnh - khoanh vào đáp án và hiển thị thông tin"""
    result = img.copy()
    h, w = result.shape[:2]
    
    # Helper function để get tọa độ cell
    def get_cell_center(region, row, col, num_rows, num_cols):
        x1 = int(w * region['x_start'])
        y1 = int(h * region['y_start'])
        x2 = int(w * region['x_end'])
        y2 = int(h * region['y_end'])
        
        roi_w = x2 - x1
        roi_h = y2 - y1
        cell_w = roi_w // num_cols
        cell_h = roi_h // num_rows
        
        cx = x1 + col * cell_w + cell_w // 2
        cy = y1 + row * cell_h + cell_h // 2
        radius = min(cell_w, cell_h) // 4
        
        return cx, cy, radius
    
    # Vẽ cho từng block câu hỏi
    regions_config = [
        (functions.QUESTIONS_1_10, 0, 10, 10, 4),     # Q1-10
        (functions.QUESTIONS_11_20, 10, 20, 10, 4),   # Q11-20
        (functions.QUESTIONS_21_30, 20, 30, 10, 4),   # Q21-30
        (functions.QUESTIONS_31_40, 30, 35, 5, 4),    # Q31-35 (chỉ 5 câu, vùng thu gọn 5 rows)
    ]
    
    for region, start_idx, end_idx, num_rows, num_cols in regions_config:
        for i in range(start_idx, min(end_idx, len(answers))):
            row = i - start_idx
            answer = answers[i]
            
            # Vẽ đáp án học sinh chọn
            if answer >= 0:
                cx, cy, radius = get_cell_center(region, row, answer, num_rows, num_cols)
                
                # Màu sắc dựa vào kết quả
                if i in multiple_marks:
                    color = (0, 165, 255)  # Cam - tô nhiều
                    thickness = 3
                elif grading[i] == 1:
                    color = (0, 255, 0)  # Xanh - đúng
                    thickness = 3
                else:
                    color = (0, 0, 255)  # Đỏ - sai
                    thickness = 3
                
                cv2.circle(result, (cx, cy), radius, color, thickness)
            
            # Vẽ đáp án đúng nếu học sinh sai
            if grading[i] == 0 and i < len(answer_key) and answer_key[i] >= 0:
                correct_ans = answer_key[i]
                cx, cy, radius = get_cell_center(region, row, correct_ans, num_rows, num_cols)
                color = (0, 255, 255)  # Vàng - đáp án đúng
                thickness = 2
                cv2.circle(result, (cx, cy), radius, color, thickness)
    
    # Vẽ thông tin kết quả lên ảnh (góc phải trên)
    # Background cho text
    info_x = w - 180
    info_y = 10
    info_w = 170
    info_h = 100
    
    # Vẽ background trắng với viền
    cv2.rectangle(result, (info_x, info_y), (info_x + info_w, info_y + info_h), (255, 255, 255), -1)
    cv2.rectangle(result, (info_x, info_y), (info_x + info_w, info_y + info_h), (0, 0, 0), 2)
    
    # Vẽ text thông tin
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    # Mã đề
    text = f"Ma de: {ma_de}"
    cv2.putText(result, text, (info_x + 10, info_y + 25), font, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
    
    # Điểm
    text = f"Diem: {correct_count}/{total_questions}"
    cv2.putText(result, text, (info_x + 10, info_y + 50), font, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
    
    # Phần trăm
    text = f"{percentage:.1f}%"
    cv2.putText(result, text, (info_x + 10, info_y + 75), font, 0.7, (0, 128, 0), 2, cv2.LINE_AA)
    
    return result

def process_omr(image_path, custom_answer_key=None):
    """Xử lý OMR sheet và trả về kết quả"""
    # Suppress all print statements during processing
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    
    try:
        # Đọc ảnh
        img = cv2.imread(image_path)
        if img is None:
            sys.stdout = old_stdout
            return {
                'success': False,
                'error': 'Không thể đọc file ảnh'
            }
        
        # Detect và warp
        warped, success = functions.detect_and_warp(img, widthImg, heightImg)
        
        if not success:
            sys.stdout = old_stdout
            return {
                'success': False,
                'error': 'Không thể detect phiếu. Vui lòng chụp lại với góc thẳng và ánh sáng tốt.'
            }
        
        # Đọc mã đề
        ma_de = functions.read_ma_de(warped, MA_DE_DIGITS, DIGIT_COUNT)
        ma_de_str = ''.join(map(str, ma_de))
        
        # Chọn answer key
        if custom_answer_key:
            answer_key = custom_answer_key
        elif ma_de_str in ANSWER_KEYS:
            answer_key = ANSWER_KEYS[ma_de_str]
        else:
            answer_key = ANSWER_KEYS["default"]
        
        # Đọc câu trả lời
        answers, multiple_marks = functions.read_answers(warped, TOTAL_QUESTIONS, CHOICES, QUESTIONS_PER_COLUMN)
        
        # Chấm điểm
        results = functions.grade_answers(answers, answer_key, TOTAL_QUESTIONS, multiple_marks)
        
        # Tính điểm
        correct_count = sum(results['grading'][:TOTAL_QUESTIONS])
        total_marks = MARKS_PER_QUESTION * TOTAL_QUESTIONS
        marks_obtained = MARKS_PER_QUESTION * correct_count
        percentage = (correct_count / TOTAL_QUESTIONS) * 100
        grade = util.determineGrade(percentage)
        
        # Convert answers sang chữ để dễ đọc
        student_answers = [answer_to_letter(ans) for ans in answers[:TOTAL_QUESTIONS]]
        correct_answers = [answer_to_letter(ans) for ans in answer_key[:TOTAL_QUESTIONS]]
        
        # Tạo chi tiết từng câu
        details = []
        for i in range(TOTAL_QUESTIONS):
            details.append({
                'question': i + 1,
                'student_answer': student_answers[i],
                'correct_answer': correct_answers[i],
                'is_correct': results['grading'][i] == 1,
                'is_multiple': i in multiple_marks,
                'is_empty': answers[i] == -1
            })
        
        # Tạo ảnh debug với vùng detect
        debug_img = draw_debug_image(warped)
        debug_img_base64 = encode_image_to_base64(debug_img)
        
        # Tạo ảnh kết quả với đáp án được khoanh tròn và thông tin
        result_img = draw_answer_results(
            warped, 
            answers, 
            results['grading'], 
            answer_key, 
            multiple_marks,
            ma_de_str,
            correct_count,
            TOTAL_QUESTIONS,
            percentage,
            grade
        )
        result_img_base64 = encode_image_to_base64(result_img)
        
        # Tạo ảnh warped để hiển thị
        warped_base64 = encode_image_to_base64(warped)
        
        # Restore stdout before returning
        sys.stdout = old_stdout
        
        return {
            'success': True,
            'ma_de': ma_de_str,
            'correct_count': correct_count,
            'wrong_count': TOTAL_QUESTIONS - correct_count,
            'total_questions': TOTAL_QUESTIONS,
            'marks_obtained': marks_obtained,
            'total_marks': total_marks,
            'percentage': round(percentage, 2),
            'grade': grade,
            'multiple_marks_count': len(multiple_marks),
            'multiple_marks': [q + 1 for q in multiple_marks],  # 1-indexed
            'details': details,
            'debug_image': debug_img_base64,
            'result_image': result_img_base64,
            'warped_image': warped_base64
        }
        
    except Exception as e:
        # Restore stdout even on error
        sys.stdout = old_stdout
        return {
            'success': False,
            'error': f'Lỗi khi xử lý: {str(e)}'
        }

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(json.dumps({
            'success': False,
            'error': 'Thiếu tham số đường dẫn ảnh'
        }))
        sys.exit(1)
    
    image_path = sys.argv[1]
    custom_key_str = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Convert custom answer key nếu có
    custom_key = convert_custom_answer_key(custom_key_str) if custom_key_str else None
    
    # Process
    result = process_omr(image_path, custom_key)
    
    # Output JSON
    print(json.dumps(result, ensure_ascii=False))

