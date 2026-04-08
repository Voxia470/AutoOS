import streamlit as st
import pandas as pd
import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Voxia AI | Executive Command Center", page_icon="🦁", layout="wide")

# --- CUSTOM CSS FOR PREMIUM LOOK ---
st.markdown("""
    <style>
    .main { background-color: #0b0e14; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    .stButton>button { background: linear-gradient(45deg, #00ffcc, #0099ff); color: black; border: none; font-weight: bold; }
    .status-live { color: #00ffcc; font-weight: bold; }
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR (Settings & Configuration) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=100)
    st.title("Voxia Settings")
    st.write("---")
    st.subheader("⚙️ AI Configuration")
    ai_mode = st.selectbox("AI Intelligence Level", ["Standard", "Executive", "Aggressive (Auto-Reply)"])
    st.toggle("Auto-Schedule Meetings", value=True)
    st.toggle("WhatsApp Alerts", value=True)
    st.toggle("Invoice Extraction", value=True)
    
    st.write("---")
    if st.button("🔄 Sync Gmail Now"):
        st.toast("Syncing with Google Servers...")

# --- MAIN DASHBOARD ---
st.title("🦁 VOXIA EXECUTIVE AI")
st.markdown(f"**Welcome, Admin** | System Status: <span class='status-live'>● ACTIVE</span>", unsafe_allow_html=True)
st.write("---")

# --- TOP METRICS (Executive View) ---
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
col_m1.metric("Emails Processed", "1,284", "+12% Today")
col_m2.metric("Hours Saved", "42 hrs", "+5.4")
col_m3.metric("Bills Detected", "€12,400", "Pending Review")
col_m4.metric("Meetings Booked", "18", "This Week")

st.write("---")

# --- MIDDLE SECTION (Real-time Operations) ---
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📈 Productivity Analysis")
    # Fake data for the chart
    chart_data = pd.DataFrame({
        'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        'Tasks Handled': [45, 52, 48, 70, 85, 30, 25]
    })
    st.line_chart(chart_data.set_index('Day'))

    st.subheader("📑 Recent Intelligence Logs")
    logs = [
        {"Time": "14:20", "Action": "Drafted Reply", "Target": "CEO of TechCorp", "Status": "Pending Approval"},
        {"Time": "13:45", "Action": "Invoice Found", "Target": "Server Hosting (€450)", "Status": "Logged to Sheets"},
        {"Time": "11:10", "Action": "Calendar Conflict", "Target": "Marketing Meet", "Status": "Rescheduled"},
    ]
    st.table(logs)

with col_right:
    st.subheader("💳 Subscription & Scalability")
    with st.container():
        st.write("**Current Tier:** Professional Enterprise")
        st.write("**Next Billing:** May 08, 2026")
        st.progress(85, text="API Usage: 850/1000 requests")
        if st.button("🚀 UPGRADE TO UNLIMITED"):
            st.balloons()
            
    st.write("---")
    st.subheader("🧠 Brain Activity")
    st.info("AI is currently analyzing 14 high-priority threads from your inbox.")
    if st.button("View AI Decision Logic"):
        st.code("IF email_priority > 8 AND contains('contract') -> Notify Admin via WhatsApp")

# --- FOOTER ---
st.write("---")
st.caption("Voxia AI v1.0.4 - Securely encrypted with AES-256")