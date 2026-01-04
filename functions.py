import cv2
import numpy as np
import util

# Kích thước chuẩn hóa
widthImg = 600
heightImg = 800


def preProcess(img, blur_kernel=(5, 5), canny_low=50, canny_high=150):
    """Tiền xử lý ảnh: Grayscale -> Blur -> Canny với tham số linh hoạt"""
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, blur_kernel, 1)
    imgCanny = cv2.Canny(imgBlur, canny_low, canny_high)
    return imgCanny


def find_corner_markers(img):
    """
    Tìm 4 marker vuông đen ở 4 GÓC NGOÀI CÙNG của phiếu.
    Chọn 4 marker ở vị trí xa nhất về 4 góc.
    Thử nhiều threshold khác nhau để tăng độ robust.
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = img.shape[:2]
    img_area = w * h
    
    # Thử nhiều giá trị threshold
    threshold_values = [100, 120, 80, 140, 60]
    
    for thresh_val in threshold_values:
        _, thresh = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY_INV)
        
        # Làm sạch noise
        kernel = np.ones((3, 3), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Điều chỉnh min/max area linh hoạt hơn
        min_area = img_area * 0.0002  # Giảm xuống
        max_area = img_area * 0.03    # Tăng lên
        
        square_contours = []
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if min_area < area < max_area:
                peri = cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
                
                if len(approx) == 4:
                    x, y, w_rect, h_rect = cv2.boundingRect(approx)
                    aspect_ratio = w_rect / float(h_rect) if h_rect > 0 else 0
                    
                    # Linh hoạt hơn với aspect ratio
                    if 0.4 < aspect_ratio < 2.5:
                        center = (x + w_rect // 2, y + h_rect // 2)
                        square_contours.append({
                            'contour': approx,
                            'center': center,
                            'area': area,
                            'bbox': (x, y, w_rect, h_rect)
                        })
        
        if len(square_contours) < 4:
            continue
        
        # Tìm 4 marker ở 4 góc
        top_left = min(square_contours, key=lambda m: m['center'][0] + m['center'][1])
        top_right = max(square_contours, key=lambda m: m['center'][0] - m['center'][1])
        bottom_left = max(square_contours, key=lambda m: m['center'][1] - m['center'][0])
        bottom_right = max(square_contours, key=lambda m: m['center'][0] + m['center'][1])
        
        markers = [top_left, top_right, bottom_left, bottom_right]
        centers = [m['center'] for m in markers]
        
        # Giảm yêu cầu khoảng cách tối thiểu
        min_dist = min(w, h) * 0.25  # Giảm từ 0.3 xuống 0.25
        
        valid = True
        for i in range(4):
            for j in range(i + 1, 4):
                dist = np.sqrt((centers[i][0] - centers[j][0])**2 + 
                              (centers[i][1] - centers[j][1])**2)
                if dist < min_dist:
                    valid = False
                    break
            if not valid:
                break
        
        if valid:
            return markers
    
    return None


def detect_paper_boundary(img):
    """
    Detect biên của phiếu bài thi với nhiều phương pháp fallback.
    Thử nhiều cách khác nhau để tăng độ robust.
    """
    h, w = img.shape[:2]
    img_area = w * h
    
    # Phương pháp 1: Tìm 4 marker góc (nếu có)
    markers = find_corner_markers(img)
    if markers is not None:
        pts = np.array([
            markers[0]['center'],
            markers[1]['center'],
            markers[2]['center'],
            markers[3]['center']
        ], dtype=np.float32)
        return pts, "markers"
    
    # Phương pháp 2: Canny với nhiều tham số khác nhau
    canny_params = [
        (50, 150),   # Mặc định
        (30, 100),   # Nhạy hơn
        (70, 200),   # Ít nhạy hơn
        (20, 80),    # Rất nhạy
    ]
    
    for canny_low, canny_high in canny_params:
        processed = preProcess(img, canny_low=canny_low, canny_high=canny_high)
        
        # Morphological operations để kết nối các cạnh
        kernel = np.ones((3, 3), np.uint8)
        processed = cv2.dilate(processed, kernel, iterations=1)
        processed = cv2.erode(processed, kernel, iterations=1)
        
        contours, _ = cv2.findContours(processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Thử với min_area thấp hơn (15%)
        min_area = img_area * 0.15
        
        for contour in sorted(contours, key=cv2.contourArea, reverse=True)[:10]:
            area = cv2.contourArea(contour)
            if area > min_area:
                peri = cv2.arcLength(contour, True)
                # Thử nhiều epsilon khác nhau
                for epsilon_factor in [0.02, 0.03, 0.015, 0.04]:
                    approx = cv2.approxPolyDP(contour, epsilon_factor * peri, True)
                    if len(approx) == 4:
                        pts = util.reorder(approx)
                        pts = pts.reshape(4, 2).astype(np.float32)
                        return pts, f"canny_{canny_low}_{canny_high}"
    
    # Phương pháp 3: Adaptive Threshold với nhiều tham số
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    adaptive_params = [
        (11, 2),   # Mặc định
        (15, 5),   # Block size lớn hơn
        (9, 2),    # Block size nhỏ hơn
        (21, 10),  # Aggressive
    ]
    
    for block_size, c_value in adaptive_params:
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                       cv2.THRESH_BINARY_INV, block_size, c_value)
        
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        min_area = img_area * 0.15
        
        for contour in sorted(contours, key=cv2.contourArea, reverse=True)[:10]:
            area = cv2.contourArea(contour)
            if area > min_area:
                peri = cv2.arcLength(contour, True)
                for epsilon_factor in [0.02, 0.03, 0.015]:
                    approx = cv2.approxPolyDP(contour, epsilon_factor * peri, True)
                    if len(approx) == 4:
                        pts = util.reorder(approx)
                        pts = pts.reshape(4, 2).astype(np.float32)
                        return pts, f"adaptive_{block_size}"
    
    # Phương pháp 4: Simple threshold với nhiều giá trị
    for threshold_value in [127, 100, 150, 80, 180]:
        _, thresh = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY_INV)
        
        # Làm sạch noise
        kernel = np.ones((5, 5), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        min_area = img_area * 0.15
        
        for contour in sorted(contours, key=cv2.contourArea, reverse=True)[:10]:
            area = cv2.contourArea(contour)
            if area > min_area:
                peri = cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
                if len(approx) == 4:
                    pts = util.reorder(approx)
                    pts = pts.reshape(4, 2).astype(np.float32)
                    return pts, f"threshold_{threshold_value}"
    
    # Phương pháp 5: Otsu's thresholding (tự động tìm threshold tốt nhất)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    kernel = np.ones((5, 5), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    min_area = img_area * 0.15
    
    for contour in sorted(contours, key=cv2.contourArea, reverse=True)[:10]:
        area = cv2.contourArea(contour)
        if area > min_area:
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
            if len(approx) == 4:
                pts = util.reorder(approx)
                pts = pts.reshape(4, 2).astype(np.float32)
                return pts, "otsu"
    
    return None, None


def resize_for_detection(img, max_width=1500):
    """
    Resize ảnh về kích thước phù hợp để detect tốt hơn.
    Ảnh quá lớn làm chậm và ảnh quá nhỏ giảm độ chính xác.
    """
    h, w = img.shape[:2]
    
    if w > max_width:
        ratio = max_width / w
        new_w = max_width
        new_h = int(h * ratio)
        resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
        return resized, ratio
    
    return img, 1.0


def detect_and_warp(img, target_width, target_height):
    """
    Detect toàn bộ phiếu bài thi và warp perspective.
    Tự động resize ảnh để tăng độ chính xác detect.
    """
    original_img = img.copy()
    h_orig, w_orig = img.shape[:2]
    
    # Resize ảnh để detect tốt hơn
    img_detect, scale = resize_for_detection(img, max_width=1500)
    
    pts, method = detect_paper_boundary(img_detect)
    
    if pts is None:
        print("Cannot detect paper! Trying with original image...")
        # Thử lại với ảnh gốc
        pts, method = detect_paper_boundary(original_img)
        
        if pts is None:
            print("Still cannot detect paper!")
            return cv2.resize(original_img, (target_width, target_height)), False
        else:
            # Sử dụng ảnh gốc
            img_to_warp = original_img
    else:
        # Scale lại tọa độ về ảnh gốc
        if scale != 1.0:
            pts = pts / scale
        img_to_warp = original_img
    
    print(f"Detected using method: {method}")
    
    dst = np.array([
        [0, 0],
        [target_width, 0],
        [0, target_height],
        [target_width, target_height]
    ], dtype=np.float32)
    
    matrix = cv2.getPerspectiveTransform(pts, dst)
    warped = cv2.warpPerspective(img_to_warp, matrix, (target_width, target_height))
    
    return warped, True


# ============== ĐỊNH NGHĨA VÙNG DETECT ==============
# Vùng MÃ ĐỀ: 3 cột × 10 hàng (số 0-9)
MA_DE_REGION = {
    'x_start': 0.162,
    'x_end': 0.293,
    'y_start': 0.281,
    'y_end': 0.595
}

# Vùng CÂU 1-10: bên phải, cùng hàng với mã đề
QUESTIONS_1_10 = {
    'x_start': 0.650,
    'x_end': 0.812,
    'y_start': 0.285,
    'y_end': 0.602
}

# Vùng CÂU 11-20: cột trái dưới
QUESTIONS_11_20 = {
    'x_start': 0.154,
    'x_end': 0.322,
    'y_start': 0.631,
    'y_end': 0.957
}

# Vùng CÂU 21-30: cột giữa dưới
QUESTIONS_21_30 = {
    'x_start': 0.409,
    'x_end': 0.570,
    'y_start': 0.630,
    'y_end': 0.960
}

# Vùng CÂU 31-40: cột phải dưới
QUESTIONS_31_40 = {
    'x_start': 0.649,
    'x_end': 0.813,
    'y_start': 0.631,
    'y_end': 0.788
}


def get_region_coords(img, region):
    """Chuyển đổi tọa độ % sang pixel"""
    h, w = img.shape[:2]
    return {
        'x_start': int(w * region['x_start']),
        'x_end': int(w * region['x_end']),
        'y_start': int(h * region['y_start']),
        'y_end': int(h * region['y_end'])
    }


def draw_debug_regions(img):
    """Vẽ các vùng detect lên ảnh để debug"""
    result = img.copy()
    
    regions = [
        (MA_DE_REGION, (255, 0, 0), "MA DE"),
        (QUESTIONS_1_10, (0, 255, 0), "Q1-10"),
        (QUESTIONS_11_20, (0, 255, 255), "Q11-20"),
        (QUESTIONS_21_30, (255, 0, 255), "Q21-30"),
        (QUESTIONS_31_40, (0, 165, 255), "Q31-35"),
    ]
    
    for region, color, label in regions:
        coords = get_region_coords(img, region)
        x1, y1 = coords['x_start'], coords['y_start']
        x2, y2 = coords['x_end'], coords['y_end']
        
        cv2.rectangle(result, (x1, y1), (x2, y2), color, 2)
        cv2.putText(result, label, (x1 + 5, y1 + 20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
    return result


def draw_regions_with_custom_coords(img, regions_config):
    """Vẽ các vùng với tọa độ tùy chỉnh"""
    result = img.copy()
    h, w = img.shape[:2]
    
    colors = {
        'ma_de': (255, 0, 0),
        'q1_10': (0, 255, 0),
        'q11_20': (0, 255, 255),
        'q21_30': (255, 0, 255),
        'q31_40': (0, 165, 255),
    }
    
    labels = {
        'ma_de': 'MA DE',
        'q1_10': 'Q1-10',
        'q11_20': 'Q11-20',
        'q21_30': 'Q21-30',
        'q31_40': 'Q31-40',
    }
    
    for key, region in regions_config.items():
        if key in colors:
            x1 = int(w * region['x_start'])
            y1 = int(h * region['y_start'])
            x2 = int(w * region['x_end'])
            y2 = int(h * region['y_end'])
            
            color = colors[key]
            cv2.rectangle(result, (x1, y1), (x2, y2), color, 2)
            cv2.putText(result, labels[key], (x1 + 5, y1 + 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    
    return result


def read_ma_de(img, num_digits=3, digit_count=10):
    """Đọc mã đề từ phiếu (3 cột × 10 hàng)"""
    coords = get_region_coords(img, MA_DE_REGION)
    
    roi = img[coords['y_start']:coords['y_end'], 
              coords['x_start']:coords['x_end']]
    
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 140, 255, cv2.THRESH_BINARY_INV)
    
    roi_h, roi_w = thresh.shape
    cell_w = roi_w // num_digits
    cell_h = roi_h // digit_count
    
    ma_de = []
    for col in range(num_digits):
        max_pixels = 0
        selected_digit = 0
        
        for row in range(digit_count):
            x1 = col * cell_w + int(cell_w * 0.15)
            x2 = (col + 1) * cell_w - int(cell_w * 0.15)
            y1 = row * cell_h + int(cell_h * 0.15)
            y2 = (row + 1) * cell_h - int(cell_h * 0.15)
            
            cell = thresh[y1:y2, x1:x2]
            pixels = cv2.countNonZero(cell)
            
            if pixels > max_pixels:
                max_pixels = pixels
                selected_digit = row
        
        ma_de.append(selected_digit)
    
    print(f"Ma de detected: {ma_de} -> {''.join(map(str, ma_de))}")
    return ma_de


def read_answer_block(img, region, num_questions, num_choices):
    """Đọc một block câu trả lời và phát hiện tô nhiều đáp án"""
    coords = get_region_coords(img, region)
    
    roi = img[coords['y_start']:coords['y_end'], 
              coords['x_start']:coords['x_end']]
    
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 140, 255, cv2.THRESH_BINARY_INV)
    
    roi_h, roi_w = thresh.shape
    cell_h = roi_h // num_questions
    cell_w = roi_w // num_choices
    
    answers = []
    multiple_marks = []
    
    for row in range(num_questions):
        threshold_pixels = cell_h * cell_w * 0.05
        marked_choices = []
        
        # Đếm tất cả các ô được tô
        for col in range(num_choices):
            x1 = col * cell_w + int(cell_w * 0.2)
            x2 = (col + 1) * cell_w - int(cell_w * 0.2)
            y1 = row * cell_h + int(cell_h * 0.15)
            y2 = (row + 1) * cell_h - int(cell_h * 0.15)
            
            cell = thresh[y1:y2, x1:x2]
            pixels = cv2.countNonZero(cell)
            
            if pixels > threshold_pixels:
                marked_choices.append((col, pixels))
        
        # Xử lý kết quả
        if len(marked_choices) == 0:
            answers.append(-1)  # Không tô
        elif len(marked_choices) == 1:
            answers.append(marked_choices[0][0])  # Tô 1 đáp án
        else:
            # Tô nhiều đáp án - chọn đáp án có pixels cao nhất
            marked_choices.sort(key=lambda x: x[1], reverse=True)
            answers.append(marked_choices[0][0])
            multiple_marks.append(row)  # Đánh dấu câu này tô nhiều
    
    return answers, multiple_marks


def read_answers(img, total_questions=35, choices=4, questions_per_col=10):
    """Đọc câu trả lời từ phiếu và trả về cả answers và multiple_marks"""
    answers = []
    multiple_marks = []
    
    answers_1_10, multiple_1_10 = read_answer_block(img, QUESTIONS_1_10, 10, choices)
    answers.extend(answers_1_10)
    multiple_marks.extend(multiple_1_10)
    print(f"Q1-10: {answers_1_10}")
    
    answers_11_20, multiple_11_20 = read_answer_block(img, QUESTIONS_11_20, 10, choices)
    answers.extend(answers_11_20)
    multiple_marks.extend([m + 10 for m in multiple_11_20])  # Offset câu hỏi
    print(f"Q11-20: {answers_11_20}")
    
    answers_21_30, multiple_21_30 = read_answer_block(img, QUESTIONS_21_30, 10, choices)
    answers.extend(answers_21_30)
    multiple_marks.extend([m + 20 for m in multiple_21_30])  # Offset câu hỏi
    print(f"Q21-30: {answers_21_30}")
    
    # Vùng Q31-35 đã thu gọn chỉ còn 5 rows (thay vì 10)
    answers_31_40, multiple_31_40 = read_answer_block(img, QUESTIONS_31_40, 5, choices)
    remaining = total_questions - 30
    if remaining > 0:
        answers.extend(answers_31_40[:remaining])
        # Chỉ thêm multiple marks cho các câu trong phạm vi
        multiple_marks.extend([m + 30 for m in multiple_31_40 if m < remaining])
        print(f"Q31-{30+remaining}: {answers_31_40[:remaining]}")
    
    return answers, multiple_marks


def grade_answers(answers, answer_key, total_questions, multiple_marks):
    """Grade answers"""
    grading = []
    
    for i in range(min(len(answers), total_questions)):
        if i < len(answer_key):
            # Nếu tô nhiều đáp án thì tính sai
            if i in multiple_marks:
                grading.append(0)
            elif answers[i] == answer_key[i] and answers[i] != -1:
                grading.append(1)
            else:
                grading.append(0)
        else:
            grading.append(0)
    
    return {
        'grading': grading,
        'correct': sum(grading),
        'wrong': len(grading) - sum(grading)
    }


def draw_answer_block_results(img, answers, grading, answer_key, region, num_questions, num_choices, multiple_marks):
    """Vẽ kết quả lên một block câu trả lời"""
    coords = get_region_coords(img, region)
    
    roi_w = coords['x_end'] - coords['x_start']
    roi_h = coords['y_end'] - coords['y_start']
    cell_h = roi_h // num_questions
    cell_w = roi_w // num_choices
    
    for row in range(min(len(answers), num_questions)):
        answer = answers[row]
        is_correct = grading[row] == 1 if row < len(grading) else False
        correct_answer = answer_key[row] if row < len(answer_key) else -1
        
        if answer >= 0:
            cx = coords['x_start'] + answer * cell_w + cell_w // 2
            cy = coords['y_start'] + row * cell_h + cell_h // 2
            
            # Nếu tô nhiều thì màu cam, sai là đỏ, đúng là xanh
            if row in multiple_marks:
                color = (0, 165, 255)  # Cam cho tô nhiều
            else:
                color = (0, 255, 0) if is_correct else (0, 0, 255)
            
            radius = min(cell_w, cell_h) // 4
            cv2.circle(img, (cx, cy), radius, color, 3)
        
        if not is_correct and correct_answer >= 0:
            cx = coords['x_start'] + correct_answer * cell_w + cell_w // 2
            cy = coords['y_start'] + row * cell_h + cell_h // 2
            radius = min(cell_w, cell_h) // 4
            cv2.circle(img, (cx, cy), radius, (0, 255, 255), 2)


def draw_results(img, answers, grading, answer_key, total_questions, choices, questions_per_col, multiple_marks):
    """Vẽ kết quả lên ảnh"""
    result = img.copy()
    
    draw_answer_block_results(
        result, answers[0:10], grading[0:10], answer_key[0:10],
        QUESTIONS_1_10, 10, choices, [m for m in multiple_marks if m < 10]
    )
    
    draw_answer_block_results(
        result, answers[10:20], grading[10:20], answer_key[10:20],
        QUESTIONS_11_20, 10, choices, [m - 10 for m in multiple_marks if 10 <= m < 20]
    )
    
    draw_answer_block_results(
        result, answers[20:30], grading[20:30], answer_key[20:30],
        QUESTIONS_21_30, 10, choices, [m - 20 for m in multiple_marks if 20 <= m < 30]
    )
    
    remaining = total_questions - 30
    if remaining > 0:
        draw_answer_block_results(
            result, answers[30:35], grading[30:35], answer_key[30:35],
            QUESTIONS_31_40, remaining, choices, [m - 30 for m in multiple_marks if 30 <= m < 35]
        )
    
    h, w = result.shape[:2]
    correct_count = sum(grading)
    percentage = (correct_count / total_questions) * 100
    
    cv2.rectangle(result, (w - 180, 10), (w - 10, 100), (255, 255, 255), -1)
    cv2.rectangle(result, (w - 180, 10), (w - 10, 100), (0, 0, 0), 2)
    cv2.putText(result, f"Diem: {correct_count}/{total_questions}", (w - 170, 40), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv2.putText(result, f"{percentage:.1f}%", (w - 170, 70), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 128, 0), 2)
    
    return result
