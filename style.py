import streamlit as st


def apply_styling():
    """Áp dụng CSS styling cho giao diện Streamlit"""
    st.markdown(
        """
        <style>
        /* Main background */
        .main {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        .stApp {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        }
        
        /* Header styling */
        h1 {
            color: #00d4ff !important;
            text-align: center;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        h2, h3 {
            color: #e94560 !important;
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(90deg, #00d4ff 0%, #00ff88 100%);
            color: #1a1a2e !important;
            border: none;
            padding: 12px 28px;
            text-align: center;
            font-size: 16px;
            font-weight: bold;
            margin: 8px 4px;
            cursor: pointer;
            border-radius: 25px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 212, 255, 0.4);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 212, 255, 0.6);
            background: linear-gradient(90deg, #00ff88 0%, #00d4ff 100%);
        }
        
        .stButton > button:active {
            transform: translateY(0);
        }
        
        /* File uploader */
        .stFileUploader {
            border: 2px dashed #00d4ff;
            border-radius: 15px;
            padding: 20px;
            background: rgba(0, 212, 255, 0.05);
        }
        
        /* Metrics styling */
        [data-testid="stMetricValue"] {
            font-size: 2rem;
            color: #00ff88 !important;
            font-weight: bold;
        }
        
        [data-testid="stMetricLabel"] {
            color: #00d4ff !important;
            font-weight: 600;
        }
        
        /* Progress bar */
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, #00d4ff 0%, #00ff88 100%);
        }
        
        /* Expander */
        .streamlit-expanderHeader {
            background-color: rgba(0, 212, 255, 0.1);
            border-radius: 10px;
            color: #00d4ff !important;
        }
        
        /* Info, success, error boxes */
        .stAlert {
            border-radius: 10px;
        }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        }
        
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: #00d4ff !important;
        }
        
        /* Divider */
        hr {
            border-color: rgba(0, 212, 255, 0.3);
        }
        
        /* Text */
        p, span, label {
            color: #ffffff !important;
        }
        
        /* Caption */
        .stCaption {
            color: rgba(255, 255, 255, 0.7) !important;
        }
        
        /* Cards effect for columns */
        [data-testid="column"] {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 10px;
            backdrop-filter: blur(10px);
        }
        
        /* Image container */
        [data-testid="stImage"] {
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        }
        
        /* Spinner */
        .stSpinner > div {
            border-color: #00d4ff transparent transparent transparent;
        }
        
        /* Text area */
        .stTextArea textarea {
            background-color: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(0, 212, 255, 0.3);
            border-radius: 10px;
            color: white !important;
        }
        
        .stTextArea textarea:focus {
            border-color: #00d4ff;
            box-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
        }
        
        /* Custom animation */
        @keyframes glow {
            0% { box-shadow: 0 0 5px #00d4ff; }
            50% { box-shadow: 0 0 20px #00d4ff, 0 0 30px #00ff88; }
            100% { box-shadow: 0 0 5px #00d4ff; }
        }
        
        .stButton > button[kind="primary"] {
            animation: glow 2s ease-in-out infinite;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
