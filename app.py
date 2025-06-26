# Main App: app.py
import streamlit as st
from plant_analysis import predict_grape_condition
from chatbot import chatbot_response

st.set_page_config(page_title="🍇 Grape Health Analyzer & Chatbot", layout="wide")

# Sidebar
st.sidebar.title("🍇 Grape Health Analyzer")
st.sidebar.write("Upload an image of a grape to analyze its condition or chat for advice!")

# Image Analysis Section
st.header("📷 Grape Health Analysis")
uploaded_image = st.file_uploader("Upload an image of a grape", type=["jpg", "png", "jpeg"])
if uploaded_image:
    with open("uploaded_grape.jpg", "wb") as f:
        f.write(uploaded_image.getbuffer())
    result = predict_grape_condition("uploaded_grape.jpg")
    st.image("uploaded_grape.jpg", caption="Uploaded Grape", use_column_width=True)
    st.write(f"**Condition**: {result['status']}, **Confidence**: {result['confidence']:.2f}")

# Chatbot Section
st.header("💬 Grape Health Chatbot")
user_input = st.text_input("Ask the chatbot about grape care or health:")
if user_input:
    chatbot_reply = chatbot_response(user_input)
    st.write(f"🤖 **Chatbot**: {chatbot_reply}")
