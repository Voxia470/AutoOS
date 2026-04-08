import streamlit as st

# Page Configuration
st.set_page_config(page_title="Voxia AI | Executive Manager", page_icon="🦁", layout="wide")

# Custom Styling
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #00ffcc; color: black; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🦁 VOXIA AI: The €30M Executive Assistant")
st.write("---")

# Dashboard Layout
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🤖 AI System Status")
    st.success("🟢 System Live & Monitoring Emails")
    
    st.info("💡 **AI Tip:** Today I filtered 4 spam emails and saved 2 hours of your time.")

with col2:
    st.subheader("💳 Subscription")
    st.write("Current Plan: **FREE TRIAL**")
    if st.button("UPGRADE TO PRO (€29.99/mo)"):
        st.write("Redirecting to Stripe...")

st.write("---")
st.subheader("📅 Recent AI Actions")
# Yahan hum SQL database se actions show karenge
st.write("1. Meeting Scheduled: Alpha-Lion Project (Tomorrow 10:00 AM)")
st.write("2. Bill Detected: Office Rent ($1200) - WhatsApp Sent")