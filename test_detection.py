"""
Script test để kiểm tra khả năng detect phiếu từ các góc chụp khác nhau
Chạy: python test_detection.py <đường_dẫn_ảnh>
"""

import sys
import cv2
import numpy as np
import functions

if len(sys.argv) < 2:
    print("❌ Cách dùng: python test_detection.py <đường_dẫn_ảnh>")
    print("Ví dụ: python test_detection.py sample.jpg")
    sys.exit(1)

image_path = sys.argv[1]

try:
    img = cv2.imread(image_path)
    if img is None:
        print(f"❌ Không thể mở file: {image_path}")
        sys.exit(1)
    
    print(f"📷 Đọc ảnh: {image_path}")
    print(f"   Kích thước: {img.shape}")
    
    print("\n🔍 Bắt đầu detect...")
    warped, success = functions.detect_and_warp(img, 600, 800)
    
    if success:
        print("✅ DETECT THÀNH CÔNG!")
        
        # Lưu ảnh đã warp
        output_path = image_path.replace('.', '_warped.')
        cv2.imwrite(output_path, warped)
        print(f"   Ảnh đã warp lưu tại: {output_path}")
        
        # Hiển thị ảnh (nếu chạy trên desktop)
        cv2.imshow('Original', img)
        cv2.imshow('Warped', warped)
        print("\n   Nhấn bất kỳ phím nào để đóng cửa sổ...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("❌ DETECT THẤT BẠI!")
        print("\n💡 Gợi ý:")
        print("   1. Chụp phiếu rõ ràng hơn (không bị mơ)")
        print("   2. Chụp góc lệch không quá 30°")
        print("   3. Đảm bảo phiếu không bị cắt mép ngoài khung ảnh")
        print("   4. Chụp lại với ánh sáng tốt hơn")

except Exception as e:
    print(f"❌ Lỗi: {e}")
    import traceback
    traceback.print_exc()
