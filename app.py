import streamlit as st
import pickle
import time
from datetime import datetime

# Page configuration for responsiveness
st.set_page_config(
    page_title="Spam Detection",
    page_icon="🛡️",
    layout="wide"
)

# Responsive CSS for multiple screen sizes
st.markdown("""
    <style>
    /* Universal Responsive Styling */
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
    }
    
    /* Responsive Text Sizes */
    * {
        font-size: 16px;
    }
    
    /* Responsive Text Area */
    .stTextArea textarea {
        height: 200px;
        font-size: 16px;
        padding: 10px;
    }
    
    /* Responsive Buttons */
    .stButton button {
        width: 100%;
        padding: 12px;
        font-size: 16px;
    }
    
    /* Result Containers */
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
    
    /* Responsive Breakpoints */
    @media (max-width: 768px) {
        .stApp {
            padding: 10px;
        }
        * {
            font-size: 14px;
        }
    }
    
    @media (max-width: 480px) {
        * {
            font-size: 12px;
        }
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

# Main App with Responsive Layout
st.title("🛡️ Spam Detection System")

# Create columns for better layout
col1, col2 = st.columns([3, 1])

with col1:
    # Message Input
    message = st.text_area("Enter your message:", 
                           help="Type or paste the message to check for spam")

with col2:
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
                        <p>
                            This message appears to be suspicious and may contain unwanted content.
                            Proceed with caution.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class='result-container safe-result'>
                        <h2 style='color: #4ecdc4; margin-bottom: 10px;'>✅ Message is Safe</h2>
                        <p>
                            This message has been analyzed and appears to be legitimate.
                            You can confidently proceed.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

# Responsive Recent History
st.subheader("Recent Checks")
if st.session_state.history:
    # Use columns to make history more compact
    cols = st.columns(3)
    for i, item in enumerate(reversed(st.session_state.history[-3:])):
        with cols[i]:
            status = "🚫 Spam" if item["prediction"] == 'spam' else "✅ Safe"
            st.info(f"{item['timestamp']}\n{item['message']}\n{status}")
else:
    st.info("No previous checks")

# Responsive About Section
with st.expander("About"):
    st.markdown("""
    ### Spam Detection System
    
    #### Features
    - AI-powered spam detection
    - Multi-language support
    - Real-time analysis
    - User-friendly interface
    
    #### How to Use
    1. Enter message
    2. Select language
    3. Click 'Check Message'
    4. View instant results
    """)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.8rem; padding: 1rem;'>
        Spam Detection System | Version 2.0 | 2024
    </div>
""", unsafe_allow_html=True)
