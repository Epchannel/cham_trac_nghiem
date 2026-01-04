import streamlit as st
from PIL import Image
import numpy as np
import cv2
import functions
import util
import style

# ============== CẤU HÌNH PHIẾU MẪU CÁ NHÂN ==============
widthImg = 600
heightImg = 800

# Cấu hình mã đề
MA_DE_DIGITS = 3
DIGIT_COUNT = 10

# Cấu hình câu hỏi
TOTAL_QUESTIONS = 35
CHOICES = 4
QUESTIONS_PER_COLUMN = 10
MARKS_PER_QUESTION = 1

# Đáp án đúng - 35 câu (0=A, 1=B, 2=C, 3=D)
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
    ],
    "default": [
        # Mặc định dùng đáp án mã đề 101
        3, 1, 2, 1, 3, 2, 1, 0, 1, 3,
        3, 2, 1, 3, 3, 0, 3, 0, 3, 0,
        3, 1, 2, 3, 1, 0, 0, 0, 1, 3,
        2, 0, 0, 1, 3
    ]
}


def find_marks(image, answer_key=None, debug_mode=False, custom_regions=None):
    """Xử lý phiếu trắc nghiệm và trả về kết quả"""
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    warped, success = functions.detect_and_warp(img, widthImg, heightImg)
    
    if not success:
        return None, None, None, None, None
    
    if custom_regions:
        original_regions = {
            'MA_DE_REGION': functions.MA_DE_REGION.copy(),
            'QUESTIONS_1_10': functions.QUESTIONS_1_10.copy(),
            'QUESTIONS_11_20': functions.QUESTIONS_11_20.copy(),
            'QUESTIONS_21_30': functions.QUESTIONS_21_30.copy(),
            'QUESTIONS_31_40': functions.QUESTIONS_31_40.copy(),
        }
        
        functions.MA_DE_REGION = custom_regions['ma_de']
        functions.QUESTIONS_1_10 = custom_regions['q1_10']
        functions.QUESTIONS_11_20 = custom_regions['q11_20']
        functions.QUESTIONS_21_30 = custom_regions['q21_30']
        functions.QUESTIONS_31_40 = custom_regions['q31_40']
    
    debug_image = functions.draw_debug_regions(warped) if debug_mode else None
    
    ma_de = functions.read_ma_de(warped, MA_DE_DIGITS, DIGIT_COUNT)
    ma_de_str = ''.join(map(str, ma_de))
    
    if answer_key is None:
        if ma_de_str in ANSWER_KEYS:
            answer_key = ANSWER_KEYS[ma_de_str]
        else:
            answer_key = ANSWER_KEYS["default"]
    
    answers, multiple_marks = functions.read_answers(warped, TOTAL_QUESTIONS, CHOICES, QUESTIONS_PER_COLUMN)
    results = functions.grade_answers(answers, answer_key, TOTAL_QUESTIONS, multiple_marks)
    
    correct_count = sum(results['grading'][:TOTAL_QUESTIONS])
    total_marks = MARKS_PER_QUESTION * TOTAL_QUESTIONS
    marks_obtained = MARKS_PER_QUESTION * correct_count
    percentage = (correct_count / TOTAL_QUESTIONS) * 100
    grade = util.determineGrade(percentage)
    
    result_image = functions.draw_results(
        warped.copy(), 
        answers, 
        results['grading'], 
        answer_key,
        TOTAL_QUESTIONS,
        CHOICES,
        QUESTIONS_PER_COLUMN,
        multiple_marks
    )
    
    result_info = {
        'ma_de': ma_de_str,
        'answers': answers[:TOTAL_QUESTIONS],
        'correct_count': correct_count,
        'total_questions': TOTAL_QUESTIONS,
        'marks_obtained': marks_obtained,
        'total_marks': total_marks,
        'percentage': percentage,
        'grade': grade,
        'grading': results['grading'][:TOTAL_QUESTIONS]
    }
    
    if custom_regions:
        functions.MA_DE_REGION = original_regions['MA_DE_REGION']
        functions.QUESTIONS_1_10 = original_regions['QUESTIONS_1_10']
        functions.QUESTIONS_11_20 = original_regions['QUESTIONS_11_20']
        functions.QUESTIONS_21_30 = original_regions['QUESTIONS_21_30']
        functions.QUESTIONS_31_40 = original_regions['QUESTIONS_31_40']
    
    return result_image, warped, result_info, ma_de_str, debug_image


# ============== GIAO DIỆN STREAMLIT ==============
st.set_page_config(
    page_title="Chấm Phiếu Trắc Nghiệm", 
    page_icon="📝", 
    layout="wide",
    initial_sidebar_state="expanded"
)

style.apply_styling()

# Tab selection
tab1, tab2 = st.tabs(["📝 Chấm Điểm", "🔧 Debug Vùng"])

# ============== TAB 1: CHẤM ĐIỂM ==============
with tab1:
    st.title("📝 Hệ Thống Chấm Phiếu Trắc Nghiệm")
    st.write("Upload ảnh phiếu trả lời trắc nghiệm và nhấn **Chấm Điểm** để xem kết quả.")

    with st.sidebar:
        st.header("⚙️ Cấu hình")
        st.write(f"**Số câu hỏi:** {TOTAL_QUESTIONS}")
        st.write(f"**Số lựa chọn:** {CHOICES} (A, B, C, D)")
        st.write(f"**Điểm/câu:** {MARKS_PER_QUESTION}")
        
        st.divider()
        debug_mode = st.checkbox("🔍 Hiển thị vùng detect (Debug)", value=True)
        
        st.divider()
        st.subheader("📋 Nhập đáp án (tùy chọn)")
        custom_answer = st.text_area(
            "Đáp án (A/B/C/D, cách nhau bởi dấu phẩy):",
            placeholder="A, D, C, A, A, A, A, A, A, A, A, A, A, A, A, A, A, A, A, B, A, A, A, A, A, A, A, A, A, A, A, A, D, A, A",
            help="Nhập 35 đáp án, mỗi đáp án là A, B, C hoặc D"
        )

    uploaded_file = st.file_uploader("📤 Chọn ảnh phiếu trắc nghiệm...", type=["jpg", "jpeg", "png"], key="tab1")

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("📷 Ảnh gốc")
            st.image(image, use_container_width=True)
        
        if st.button('🎯 Chấm Điểm', type='primary', key="btn1"):
            custom_key = None
            if custom_answer.strip():
                try:
                    mapping = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
                    parts = [p.strip().upper() for p in custom_answer.split(',')]
                    if len(parts) >= TOTAL_QUESTIONS:
                        custom_key = [mapping.get(p, 0) for p in parts[:TOTAL_QUESTIONS]]
                except:
                    st.warning("Đáp án không hợp lệ, sử dụng đáp án mặc định.")
            
            with st.spinner('Đang xử lý...'):
                result_image, warped, result_info, ma_de, debug_image = find_marks(
                    image, custom_key, debug_mode
                )
                
                if result_image is not None:
                    with col2:
                        if debug_mode and debug_image is not None:
                            st.subheader("🔍 Vùng Detect")
                            st.image(cv2.cvtColor(debug_image, cv2.COLOR_BGR2RGB), use_container_width=True)
                            st.caption("🔵 Mã đề | 🟢 Q1-10 | 🟡 Q11-20 | 🟣 Q21-30 | 🟠 Q31-40")
                        else:
                            st.subheader("📄 Ảnh đã xử lý")
                            st.image(cv2.cvtColor(warped, cv2.COLOR_BGR2RGB), use_container_width=True)
                    
                    with col3:
                        st.subheader("✅ Kết quả chấm")
                        st.image(cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB), use_container_width=True)
                    
                    st.divider()
                    st.subheader("📊 Kết Quả")
                    
                    col_a, col_b, col_c, col_d = st.columns(4)
                    with col_a:
                        st.metric("📝 Mã đề", ma_de)
                    with col_b:
                        st.metric("✓ Số câu đúng", f"{result_info['correct_count']}/{result_info['total_questions']}")
                    with col_c:
                        st.metric("📊 Điểm", f"{result_info['marks_obtained']}/{result_info['total_marks']}")
                    with col_d:
                        st.metric("🏆 Xếp loại", result_info['grade'])
                    
                    st.progress(result_info['percentage'] / 100)
                    st.write(f"**Phần trăm:** {result_info['percentage']:.1f}%")
                    
                    with st.expander("📋 Chi tiết câu trả lời", expanded=False):
                        answer_mapping = {0: 'A', 1: 'B', 2: 'C', 3: 'D', -1: '⚠️ Trống'}
                        key_to_use = custom_key if custom_key else ANSWER_KEYS.get(ma_de, ANSWER_KEYS["default"])
                        
                        cols = st.columns(4)
                        col_labels = ["Câu 1-10", "Câu 11-20", "Câu 21-30", "Câu 31-35"]
                        
                        for col_idx, col in enumerate(cols):
                            with col:
                                st.write(f"**{col_labels[col_idx]}**")
                                start = col_idx * 10
                                end = min(start + 10, TOTAL_QUESTIONS)
                                
                                for i in range(start, end):
                                    if i < len(result_info['answers']):
                                        ans = result_info['answers'][i]
                                        correct = result_info['grading'][i] == 1
                                        status = "✅" if correct else "❌"
                                        correct_ans = answer_mapping.get(key_to_use[i], '?')
                                        student_ans = answer_mapping.get(ans, '?')
                                        st.write(f"{i+1}. {student_ans} {status} ({correct_ans})")
                else:
                    st.error("❌ Không thể detect phiếu. Vui lòng kiểm tra lại ảnh.")

# ============== TAB 2: DEBUG VÙNG ==============
with tab2:
    st.title("🔧 Debug và Điều Chỉnh Vùng Detect")
    st.write("Sử dụng sliders để điều chỉnh tọa độ các vùng detect. Xem preview real-time bên dưới.")
    
    uploaded_file_debug = st.file_uploader("📤 Chọn ảnh phiếu...", type=["jpg", "jpeg", "png"], key="tab2")
    
    if uploaded_file_debug is not None:
        image_debug = Image.open(uploaded_file_debug)
        img_cv = cv2.cvtColor(np.array(image_debug), cv2.COLOR_RGB2BGR)
        
        warped_debug, success_debug = functions.detect_and_warp(img_cv, widthImg, heightImg)
        
        if not success_debug:
            st.error("Không thể detect phiếu. Vui lòng upload ảnh khác.")
        else:
            st.success("✅ Đã detect phiếu thành công!")
            
            # Sliders cho từng vùng
            st.subheader("⚙️ Điều chỉnh tọa độ (tỷ lệ 0.0 - 1.0)")
            
            # Mã đề
            with st.expander("🔵 Mã đề (MA_DE_REGION)", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    ma_de_x1 = st.slider("X Start", 0.0, 1.0, float(functions.MA_DE_REGION['x_start']), 0.001, key="ma_de_x1")
                    ma_de_y1 = st.slider("Y Start", 0.0, 1.0, float(functions.MA_DE_REGION['y_start']), 0.001, key="ma_de_y1")
                with col2:
                    ma_de_x2 = st.slider("X End", 0.0, 1.0, float(functions.MA_DE_REGION['x_end']), 0.001, key="ma_de_x2")
                    ma_de_y2 = st.slider("Y End", 0.0, 1.0, float(functions.MA_DE_REGION['y_end']), 0.001, key="ma_de_y2")
                
                st.code(f"MA_DE_REGION = {{'x_start': {ma_de_x1:.3f}, 'x_end': {ma_de_x2:.3f}, 'y_start': {ma_de_y1:.3f}, 'y_end': {ma_de_y2:.3f}}}")
            
            # Câu 1-10
            with st.expander("🟢 Câu 1-10 (QUESTIONS_1_10)", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    q1_x1 = st.slider("X Start", 0.0, 1.0, float(functions.QUESTIONS_1_10['x_start']), 0.001, key="q1_x1")
                    q1_y1 = st.slider("Y Start", 0.0, 1.0, float(functions.QUESTIONS_1_10['y_start']), 0.001, key="q1_y1")
                with col2:
                    q1_x2 = st.slider("X End", 0.0, 1.0, float(functions.QUESTIONS_1_10['x_end']), 0.001, key="q1_x2")
                    q1_y2 = st.slider("Y End", 0.0, 1.0, float(functions.QUESTIONS_1_10['y_end']), 0.001, key="q1_y2")
                
                st.code(f"QUESTIONS_1_10 = {{'x_start': {q1_x1:.3f}, 'x_end': {q1_x2:.3f}, 'y_start': {q1_y1:.3f}, 'y_end': {q1_y2:.3f}}}")
            
            # Câu 11-20
            with st.expander("🟡 Câu 11-20 (QUESTIONS_11_20)", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    q11_x1 = st.slider("X Start", 0.0, 1.0, float(functions.QUESTIONS_11_20['x_start']), 0.001, key="q11_x1")
                    q11_y1 = st.slider("Y Start", 0.0, 1.0, float(functions.QUESTIONS_11_20['y_start']), 0.001, key="q11_y1")
                with col2:
                    q11_x2 = st.slider("X End", 0.0, 1.0, float(functions.QUESTIONS_11_20['x_end']), 0.001, key="q11_x2")
                    q11_y2 = st.slider("Y End", 0.0, 1.0, float(functions.QUESTIONS_11_20['y_end']), 0.001, key="q11_y2")
                
                st.code(f"QUESTIONS_11_20 = {{'x_start': {q11_x1:.3f}, 'x_end': {q11_x2:.3f}, 'y_start': {q11_y1:.3f}, 'y_end': {q11_y2:.3f}}}")
            
            # Câu 21-30
            with st.expander("🟣 Câu 21-30 (QUESTIONS_21_30)", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    q21_x1 = st.slider("X Start", 0.0, 1.0, float(functions.QUESTIONS_21_30['x_start']), 0.001, key="q21_x1")
                    q21_y1 = st.slider("Y Start", 0.0, 1.0, float(functions.QUESTIONS_21_30['y_start']), 0.001, key="q21_y1")
                with col2:
                    q21_x2 = st.slider("X End", 0.0, 1.0, float(functions.QUESTIONS_21_30['x_end']), 0.001, key="q21_x2")
                    q21_y2 = st.slider("Y End", 0.0, 1.0, float(functions.QUESTIONS_21_30['y_end']), 0.001, key="q21_y2")
                
                st.code(f"QUESTIONS_21_30 = {{'x_start': {q21_x1:.3f}, 'x_end': {q21_x2:.3f}, 'y_start': {q21_y1:.3f}, 'y_end': {q21_y2:.3f}}}")
            
            # Câu 31-40
            with st.expander("🟠 Câu 31-40 (QUESTIONS_31_40)", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    q31_x1 = st.slider("X Start", 0.0, 1.0, float(functions.QUESTIONS_31_40['x_start']), 0.001, key="q31_x1")
                    q31_y1 = st.slider("Y Start", 0.0, 1.0, float(functions.QUESTIONS_31_40['y_start']), 0.001, key="q31_y1")
                with col2:
                    q31_x2 = st.slider("X End", 0.0, 1.0, float(functions.QUESTIONS_31_40['x_end']), 0.001, key="q31_x2")
                    q31_y2 = st.slider("Y End", 0.0, 1.0, float(functions.QUESTIONS_31_40['y_end']), 0.001, key="q31_y2")
                
                st.code(f"QUESTIONS_31_40 = {{'x_start': {q31_x1:.3f}, 'x_end': {q31_x2:.3f}, 'y_start': {q31_y1:.3f}, 'y_end': {q31_y2:.3f}}}")
            
            # Tạo config từ sliders
            custom_regions = {
                'ma_de': {'x_start': ma_de_x1, 'x_end': ma_de_x2, 'y_start': ma_de_y1, 'y_end': ma_de_y2},
                'q1_10': {'x_start': q1_x1, 'x_end': q1_x2, 'y_start': q1_y1, 'y_end': q1_y2},
                'q11_20': {'x_start': q11_x1, 'x_end': q11_x2, 'y_start': q11_y1, 'y_end': q11_y2},
                'q21_30': {'x_start': q21_x1, 'x_end': q21_x2, 'y_start': q21_y1, 'y_end': q21_y2},
                'q31_40': {'x_start': q31_x1, 'x_end': q31_x2, 'y_start': q31_y1, 'y_end': q31_y2},
            }
            
            # Preview
            st.divider()
            st.subheader("👁️ Preview")
            
            preview_image = functions.draw_regions_with_custom_coords(warped_debug.copy(), custom_regions)
            st.image(cv2.cvtColor(preview_image, cv2.COLOR_BGR2RGB), use_container_width=True)
            
            # Export code
            st.divider()
            st.subheader("📋 Code để copy vào functions.py")
            code_block = f"""# Vùng MÃ ĐỀ: 3 cột × 10 hàng (số 0-9)
MA_DE_REGION = {{
    'x_start': {ma_de_x1:.3f},
    'x_end': {ma_de_x2:.3f},
    'y_start': {ma_de_y1:.3f},
    'y_end': {ma_de_y2:.3f}
}}

# Vùng CÂU 1-10: bên phải, cùng hàng với mã đề
QUESTIONS_1_10 = {{
    'x_start': {q1_x1:.3f},
    'x_end': {q1_x2:.3f},
    'y_start': {q1_y1:.3f},
    'y_end': {q1_y2:.3f}
}}

# Vùng CÂU 11-20: cột trái dưới
QUESTIONS_11_20 = {{
    'x_start': {q11_x1:.3f},
    'x_end': {q11_x2:.3f},
    'y_start': {q11_y1:.3f},
    'y_end': {q11_y2:.3f}
}}

# Vùng CÂU 21-30: cột giữa dưới
QUESTIONS_21_30 = {{
    'x_start': {q21_x1:.3f},
    'x_end': {q21_x2:.3f},
    'y_start': {q21_y1:.3f},
    'y_end': {q21_y2:.3f}
}}

# Vùng CÂU 31-40: cột phải dưới
QUESTIONS_31_40 = {{
    'x_start': {q31_x1:.3f},
    'x_end': {q31_x2:.3f},
    'y_start': {q31_y1:.3f},
    'y_end': {q31_y2:.3f}
}}"""
            
            st.code(code_block, language='python')
            st.info("💡 Copy code trên và thay thế vào file functions.py tại phần định nghĩa vùng (khoảng dòng 174-216)")

st.divider()
st.caption("💡 Hệ thống chấm phiếu trắc nghiệm tự động | Phiếu mẫu cá nhân - 35 câu")

