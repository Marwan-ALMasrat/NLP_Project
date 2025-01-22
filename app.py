# pip install -U streamlit
# pip install -U plotly

# you can run your app with: streamlit run app.py

import streamlit as st
import pickle

# loading the trained model

model = pickle.load(open('model.pkl', 'rb'))

# create title
st.title('Predicting If Your Message Is Spam Or Not Spam')

message = st.text_input('Enter a message')

submit = st.button('Predict')

if submit:
    prediction = model.predict([message])

  
    if prediction[0] == 'spam':
        st.warning('This message is spam')
        st.error('⚠️ Warning: This is a spam message!') 

    else:
        st.success('This message is not spam')
        st.balloons()
