import streamlit as st
import pickle
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Spam Detector",
    page_icon="📧",
    layout="wide"
)

# Custom CSS for dark theme
st.markdown("""
    <style>
    .stApp {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    .main {
        padding: 1.5rem;
    }
    .stTitle {
        color: #ffffff;
        font-size: 2.5rem !important;
        padding-bottom: 1.5rem;
    }
    .stTextInput {
        background-color: #2d2d2d;
        color: #ffffff;
        margin: 1.5rem 0;
    }
    .prediction-box {
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1.5rem 0;
    }
    .stButton button {
        background-color: #4a4a4a;
        color: #ffffff;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
    }
    .stButton button:hover {
        background-color: #5a5a5a;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []

def load_model():
    try:
        return pickle.load(open('model.pkl', 'rb'))
    except FileNotFoundError:
        st.error("⚠️ Model file not found.")
        return None

# Main title
st.title('📧 Spam Detective')

# Create two columns
col1, col2 = st.columns([2, 1])

with col1:
    message = st.text_area(
        "Enter your message:",
        height=120,
        key="message_input"
    )

    if st.button('🔍 Analyze', use_container_width=True):
        if message.strip() == "":
            st.warning("Please enter a message.")
        else:
            model = load_model()
            if model:
                prediction = model.predict([message])
                timestamp = datetime.now().strftime("%H:%M:%S")
                
                st.session_state.history.append({
                    "message": message[:40] + "..." if len(message) > 40 else message,
                    "prediction": prediction[0],
                    "timestamp": timestamp
                })
                
                if prediction[0] == 'spam':
                    st.error("🚫 Spam Detected")
                    st.markdown("""
                        <div style='background-color: #3d1f1f; padding: 15px; border-radius: 8px; border: 1px solid #ff4444;'>
                            <h3 style='color: #ff4444;'>Warning: Spam Content</h3>
                            <p style='color: #dddddd;'>This message has been identified as spam.</p>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.success("✅ Message Safe")
                    st.markdown("""
                        <div style='background-color: #1f3d1f; padding: 15px; border-radius: 8px; border: 1px solid #44ff44;'>
                            <h3 style='color: #44ff44;'>Safe Content</h3>
                            <p style='color: #dddddd;'>This message appears to be legitimate.</p>
                        </div>
                    """, unsafe_allow_html=True)
                    st.balloons()

with col2:
    st.markdown("### Recent Analysis")
    if st.session_state.history:
        for item in reversed(st.session_state.history[-5:]):
            if item["prediction"] == 'spam':
                st.error(f"{item['timestamp']} - {item['message']}")
            else:
                st.success(f"{item['timestamp']} - {item['message']}")
    else:
        st.info("No messages analyzed yet")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #888888;'>
        Spam Detection System v1.0
    </div>
""", unsafe_allow_html=True)

# About section
with st.expander("About"):
    st.markdown("""
        **Quick Guide:**
        1. Enter your message
        2. Click 'Analyze'
        3. View results and history
        
        This tool uses machine learning to detect spam messages in real-time.
    """)
