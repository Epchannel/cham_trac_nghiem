import cv2
import numpy as np


def rectContours(contours, min_area):
    """Lọc các contour hình chữ nhật có diện tích > min_area"""
    rectCon = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > min_area:
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
            if len(approx) == 4:
                rectCon.append(contour)
    rectCon = sorted(rectCon, key=cv2.contourArea, reverse=True)
    return rectCon


def getCornerPoints(contour):
    """Lấy 4 điểm góc của contour"""
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
    return approx


def reorder(points):
    """Sắp xếp lại 4 điểm theo thứ tự: top-left, top-right, bottom-left, bottom-right"""
    points = points.reshape((4, 2))
    pointsNew = np.zeros((4, 1, 2), dtype=np.int32)
    
    add = points.sum(1)
    pointsNew[0] = points[np.argmin(add)]  # Top-left
    pointsNew[3] = points[np.argmax(add)]  # Bottom-right
    
    diff = np.diff(points, axis=1)
    pointsNew[1] = points[np.argmin(diff)]  # Top-right
    pointsNew[2] = points[np.argmax(diff)]  # Bottom-left
    
    return pointsNew


def splitBoxes(img, rows, cols):
    """Chia ảnh thành grid rows × cols"""
    boxes = []
    row_splits = np.vsplit(img, rows)
    for r in row_splits:
        col_splits = np.hsplit(r, cols)
        for box in col_splits:
            boxes.append(box)
    return boxes


def determineGrade(percentage):
    """Xác định xếp loại dựa trên phần trăm điểm"""
    if percentage >= 90:
        return 'A+'
    elif percentage >= 85:
        return 'A'
    elif percentage >= 80:
        return 'B+'
    elif percentage >= 70:
        return 'B'
    elif percentage >= 60:
        return 'C+'
    elif percentage >= 50:
        return 'C'
    elif percentage >= 40:
        return 'D'
    else:
        return 'F'


def showAnswers(img, answers, grading, correct_answers, num_questions, num_choices):
    """Hiển thị câu trả lời lên ảnh"""
    h, w = img.shape[:2]
    secW = w // num_choices
    secH = h // num_questions
    
    for i in range(num_questions):
        answer = answers[i] if i < len(answers) else -1
        is_correct = grading[i] == 1 if i < len(grading) else False
        correct_ans = correct_answers[i] if i < len(correct_answers) else -1
        
        if answer >= 0:
            # Vẽ câu trả lời
            cX = answer * secW + secW // 2
            cY = i * secH + secH // 2
            
            color = (0, 255, 0) if is_correct else (0, 0, 255)
            cv2.circle(img, (cX, cY), 20, color, cv2.FILLED)
        
        # Vẽ đáp án đúng nếu sai
        if not is_correct and correct_ans >= 0:
            cX = correct_ans * secW + secW // 2
            cY = i * secH + secH // 2
            cv2.circle(img, (cX, cY), 20, (0, 255, 255), 3)
    
    return img


def biggestContour(contours):
    """Tìm contour lớn nhất có 4 cạnh"""
    biggest = np.array([])
    max_area = 0
    
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 5000:
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area
    
    return biggest, max_area


def drawRectangle(img, points, color=(0, 255, 0), thickness=3):
    """Vẽ hình chữ nhật từ 4 điểm"""
    points = points.reshape(4, 2)
    cv2.polylines(img, [points.astype(int)], True, color, thickness)
    return img


def stackImages(imgArray, scale):
    """Xếp chồng nhiều ảnh để hiển thị"""
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    
    if rowsAvailable:
        for x in range(rows):
            for y in range(cols):
                imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                if len(imgArray[x][y].shape) == 2:
                    imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        
        for x in range(rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(rows):
            imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            if len(imgArray[x].shape) == 2:
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        ver = np.hstack(imgArray)
    
    return ver
