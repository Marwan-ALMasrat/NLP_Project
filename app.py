import streamlit as st
import pickle
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Spam Message Detector",
    page_icon="📧",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTitle {
        color: #2c3e50;
        font-size: 3rem !important;
        padding-bottom: 2rem;
    }
    .stTextInput {
        margin: 2rem 0;
    }
    .prediction-box {
        padding: 2rem;
        border-radius: 10px;
        margin: 2rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for history
if 'history' not in st.session_state:
    st.session_state.history = []

def load_model():
    try:
        return pickle.load(open('model.pkl', 'rb'))
    except FileNotFoundError:
        st.error("⚠️ Model file not found. Please ensure 'model.pkl' exists in the same directory.")
        return None

# Main title with emoji
st.title('✉️ Smart Spam Detective')

# Create two columns for layout
col1, col2 = st.columns([2, 1])

with col1:
    # Main input section
    st.markdown("### 📝 Enter Your Message")
    message = st.text_area(
        "Type or paste your message here:",
        height=150,
        key="message_input",
        help="Enter the message you want to analyze for spam"
    )

    # Prediction button with custom styling
    if st.button('🔍 Analyze Message', use_container_width=True):
        if message.strip() == "":
            st.warning("⚠️ Please enter a message first!")
        else:
            model = load_model()
            if model:
                # Make prediction
                prediction = model.predict([message])
                
                # Store in history
                timestamp = datetime.now().strftime("%H:%M:%S")
                st.session_state.history.append({
                    "message": message[:50] + "..." if len(message) > 50 else message,
                    "prediction": prediction[0],
                    "timestamp": timestamp
                })
                
                # Display result with custom styling
                if prediction[0] == 'spam':
                    st.error("🚫 SPAM DETECTED!")
                    st.markdown("""
                        <div style='background-color: #ffebee; padding: 20px; border-radius: 10px;'>
                            <h3 style='color: #c62828;'>⚠️ Warning: This message appears to be spam!</h3>
                            <p>This message shows characteristics commonly associated with spam content.</p>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.success("✅ MESSAGE SAFE!")
                    st.markdown("""
                        <div style='background-color: #e8f5e9; padding: 20px; border-radius: 10px;'>
                            <h3 style='color: #2e7d32;'>🛡️ This message appears to be legitimate!</h3>
                            <p>Our analysis suggests this is a safe, non-spam message.</p>
                        </div>
                    """, unsafe_allow_html=True)
                    st.balloons()

with col2:
    # History section
    st.markdown("### 📊 Analysis History")
    if st.session_state.history:
        for item in reversed(st.session_state.history[-5:]):  # Show last 5 entries
            if item["prediction"] == 'spam':
                st.error(f"🕒 {item['timestamp']} - {item['message']}")
            else:
                st.success(f"🕒 {item['timestamp']} - {item['message']}")
    else:
        st.info("No messages analyzed yet!")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Built with ❤️ using Streamlit | Model: Spam Detection v1.0</p>
    </div>
""", unsafe_allow_html=True)

# Add some helpful information
with st.expander("ℹ️ About This Tool"):
    st.markdown("""
        This spam detection tool uses machine learning to analyze messages and determine if they're likely to be spam. 
        
        **Features:**
        - Real-time message analysis
        - Message history tracking
        - Beautiful user interface
        - Instant visual feedback
        
        **How to use:**
        1. Enter your message in the text area
        2. Click the 'Analyze Message' button
        3. Get instant results with visual indicators
    """)
