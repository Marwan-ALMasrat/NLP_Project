import streamlit as st
import pickle
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Spam Detection",
    page_icon="🛡️",
    layout="wide"
)

# Mobile-Friendly CSS
st.markdown("""
    <style>
    .stTextArea textarea {
        font-size: 1rem;
        height: 150px;
    }
    .stButton button {
        width: 100%;
        padding: 10px;
    }
    .result-container {
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        margin-top: 20px;
    }
    .spam-result {
        background-color: #ffecb3;
        border: 2px solid #ff6b6b;
        color: #333;
    }
    .safe-result {
        background-color: #e6f3ff;
        border: 2px solid #4ecdc4;
        color: #333;
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
        st.error("Model not found")
        return None

# Main App
st.title("🛡️ Spam Detection System")

# Message Input
message = st.text_area("Enter your message:", 
                       help="Type or paste the message to check for spam")

# Language Selection
language = st.selectbox(
    "Message Language",
    ["English", "Español", "Français"]
)

# Analyze Button
if st.button('Check Message', key='analyze'):
    if message.strip() == "":
        st.warning("Please enter a message")
    else:
        with st.spinner('Analyzing...'):
            time.sleep(1)  # Simulate processing
            
            model = load_model()
            if model:
                prediction = model.predict([message])
                
                # Store in history
                timestamp = datetime.now().strftime("%H:%M:%S")
                st.session_state.history.append({
                    "message": message[:30] + "..." if len(message) > 30 else message,
                    "prediction": prediction[0],
                    "timestamp": timestamp
                })
                
                # Enhanced Result Display
                if prediction[0] == 'spam':
                    st.markdown("""
                    <div class='result-container spam-result'>
                        <h2 style='color: #ff6b6b; margin-bottom: 10px;'>⚠️ Potential Spam Detected</h2>
                        <p style='font-size: 16px;'>
                            This message appears to be suspicious and may contain unwanted content.
                            Proceed with caution and avoid interacting with its source.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class='result-container safe-result'>
                        <h2 style='color: #4ecdc4; margin-bottom: 10px;'>✅ Message is Safe</h2>
                        <p style='font-size: 16px;'>
                            This message has been analyzed and appears to be legitimate.
                            You can confidently proceed with reading or responding.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

# Recent History
st.subheader("Recent Checks")
if st.session_state.history:
    for item in reversed(st.session_state.history[-3:]):
        status = "🚫 Spam" if item["prediction"] == 'spam' else "✅ Safe"
        st.write(f"{item['timestamp']} - {item['message']} ({status})")
else:
    st.info("No previous checks")

# About Section
with st.expander("About"):
    st.write("""
    # Spam Detection System
    
    ## How It Works
    - Enter a message in the text area
    - Choose the message language
    - Click 'Check Message'
    - Get instant spam detection results
    
    ## Key Features
    - AI-powered spam detection
    - Multi-language support
    - Real-time analysis
    - Easy-to-understand results
    """)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.9rem; padding: 1rem;'>
        Spam Detection System | Version 2.0 | 2024
    </div>
""", unsafe_allow_html=True)
