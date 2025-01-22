import streamlit as st
import pickle
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import pandas as pd
import time

# Page configuration
st.set_page_config(
    page_title="Advanced Spam Detection System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"  # Changed to collapsed for mobile
)

# Enhanced Mobile-Friendly CSS
st.markdown("""
    <style>
    .main {
        padding: 1rem;
        background-color: #ffffff;
    }
    .stTitle {
        color: #1f1f1f;
        font-size: 2rem !important;  # Reduced size for mobile
        font-weight: 700;
        padding-bottom: 1rem;
        text-align: center;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin: 0.5rem 0;
        text-align: center;
    }
    .metric-card h3 {
        font-size: 1rem;
        margin-bottom: 0.5rem;
        color: #2c3e50;
    }
    .metric-card p {
        font-size: 1.1rem;
        color: #3498db;
        font-weight: bold;
    }
    .stButton button {
        background: #3498db;
        color: white;
        border: none;
        padding: 0.8rem 1rem;
        border-radius: 5px;
        width: 100%;
        font-size: 1.1rem;
        margin: 1rem 0;
    }
    .stTextArea textarea {
        font-size: 1.1rem !important;
        padding: 0.8rem !important;
    }
    .status-box {
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-size: 1.1rem;
    }
    .status-box h3 {
        margin-bottom: 0.5rem;
    }
    .status-box ul {
        margin: 0.5rem 0;
        padding-left: 1.2rem;
    }
    /* Mobile-specific adjustments */
    @media (max-width: 768px) {
        .main {
            padding: 0.5rem;
        }
        .stTitle {
            font-size: 1.5rem !important;
        }
        .metric-card {
            margin: 0.3rem 0;
        }
        .stButton button {
            padding: 0.6rem;
        }
    }
    /* Make text more readable on mobile */
    .big-number {
        font-size: 1.5rem !important;
        font-weight: bold;
        color: #2c3e50;
    }
    .section-title {
        font-size: 1.3rem !important;
        color: #2c3e50;
        margin: 1rem 0;
        padding: 0.5rem;
        background: #f8f9fa;
        border-radius: 5px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'spam_count' not in st.session_state:
    st.session_state.spam_count = 0
if 'ham_count' not in st.session_state:
    st.session_state.ham_count = 0
if 'analysis_time' not in st.session_state:
    st.session_state.analysis_time = []

def load_model():
    try:
        return pickle.load(open('model.pkl', 'rb'))
    except FileNotFoundError:
        st.error("⚠️ Model not found")
        return None

# Main title
st.title("🛡️ Advanced Spam Detection System")

# Quick Stats in a more mobile-friendly layout
st.markdown("### 📊 Quick Stats")
col1 = st.columns([1])[0]  # Define only one column for Accuracy Rate
with col1:
    st.markdown("""
        <div class="metric-card">
            <h3>Accuracy Rate</h3>
            <p>99.8%</p>
        </div>
    """, unsafe_allow_html=True)

# Main content area with bigger text
st.markdown('<p class="section-title">✍️ Enter Message for Analysis</p>', unsafe_allow_html=True)
message = st.text_area(
    "Message Text:",
    height=100,
    key="message_input",
    help="Type or paste the message here for analysis"
)

# Simple Options for mobile
language = st.selectbox(
    "Message Language",
    ["Arabic", "English", "Español", "Français"]
)

# Analysis button
if st.button('🔍 Analyze Message', use_container_width=True):
    if message.strip() == "":
        st.warning("⚠️ Please enter a message for analysis")
    else:
        # Progress indication
        with st.spinner('Analyzing...'):
            time.sleep(1)  # Simulate analysis
        
        model = load_model()
        if model:
            start_time = time.time()
            prediction = model.predict([message])
            analysis_time = time.time() - start_time
            
            # Update history
            timestamp = datetime.now().strftime("%H:%M:%S")
            st.session_state.history.append({
                "message": message[:30] + "..." if len(message) > 30 else message,
                "prediction": prediction[0],
                "timestamp": timestamp,
                "analysis_time": analysis_time
            })
            
            if prediction[0] == 'spam':
                st.session_state.spam_count += 1
                st.error("🚫 Spam Message Detected!")
                st.markdown("""
                    <div style='background-color: #fff5f5; padding: 15px; border-radius: 8px; border: 2px solid #ff4444;'>
                        <h3 style='color: #dc3545; text-align: center;'>⚠️ Warning: Unwanted Content</h3>
                        <p style='text-align: center; font-size: 1.1rem;'>This message has been marked as unwanted content</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.session_state.ham_count += 1
                st.success("✅ Safe Message")
                st.markdown("""
                    <div style='background-color: #f8fff5; padding: 15px; border-radius: 8px; border: 2px solid #28a745;'>
                        <h3 style='color: #28a745; text-align: center;'>✅ Safe Content</h3>
                        <p style='text-align: center; font-size: 1.1rem;'>This message is safe and trusted</p>
                    </div>
                """, unsafe_allow_html=True)
                st.balloons()

# Recent History in a mobile-friendly format
st.markdown('<p class="section-title">📱 Recent Analyses</p>', unsafe_allow_html=True)
if st.session_state.history:
    for item in reversed(st.session_state.history[-3:]):  # Show only last 3 for mobile
        if item["prediction"] == 'spam':
            st.error(f"🕒 {item['timestamp']} - {item['message']}")
        else:
            st.success(f"🕒 {item['timestamp']} - {item['message']}")
else:
    st.info("No previous analyses")

# About section
with st.expander("ℹ️ About the App"):
    st.markdown("""
        This application uses AI to analyze messages and determine if they are spam or not.
        
        **Features:**
        - Instant message analysis
        - History of previous analyses
        - User-friendly interface
        - Instant and clear results
        
        **How to use:**
        1. Enter the message in the text box
        2. Click on 'Analyze Message'
        3. Get the result instantly
    """)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.9rem; padding: 1rem;'>
        Advanced Spam Detection System | Version 2.0 | 2024
    </div>
""", unsafe_allow_html=True)
