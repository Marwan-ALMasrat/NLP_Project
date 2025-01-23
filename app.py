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

# Simplified Mobile-Friendly CSS
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
st.title("🛡️ Spam Detection")

# Message Input
message = st.text_area("Enter your message:", 
                       help="Type or paste the message to check for spam")

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
                
                # Display result
                if prediction[0] == 'spam':
                    st.error("🚫 Spam Detected!")
                else:
                    st.success("✅ Message is Safe")

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
    This app uses AI to check if a message is spam.
    
    How to use:
    1. Enter your message
    2. Click 'Check Message'
    3. See the result
    """)
