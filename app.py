import streamlit as st
import pandas as pd
from datetime import datetime

# --- PAGE CONFIGURATION (Professional Branding) ---
st.set_page_config(page_title="AutoOS | Global Executive", layout="wide")

# --- THE LUXURY UI (CSS Injection) ---
st.markdown("""
    <style>
    /* Full Page Background */
    .stApp {
        background: radial-gradient(circle at top right, #050a14, #020408);
        color: #f0f0f0;
    }
    
    /* Header Styling */
    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: -1px;
        background: -webkit-linear-gradient(#fff, #888);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }

    /* Luxury Cards */
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
    }

    /* Sidebar - Clean & Sharp */
    [data-testid="stSidebar"] {
        background-color: #03060b;
        border-right: 1px solid #161b22;
    }

    /* Professional Buttons */
    .stButton>button {
        background: linear-gradient(145deg, #00d4ff, #0055ff);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: bold;
        letter-spacing: 1px;
        transition: 0.4s ease;
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(0, 85, 255, 0.4);
    }

    /* Status Indicator */
    .status-active {
        color: #00ffcc;
        font-family: monospace;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(0, 255, 204, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR (Minimalist & Powerful) ---
with st.sidebar:
    st.markdown("<h2 style='letter-spacing: 2px;'>AUTO OPERATING SYSTEM</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #666;'>SYSTEM CORE: v2.1.0</p>", unsafe_allow_html=True)
    st.write("---")
    
    nav = st.radio("COMMANDS", ["EXECUTIVE OVERVIEW", "GMAIL INTELLIGENCE", "REVENUE TRACKER", "CORE SETTINGS"])
    
    st.write("---")
    st.markdown("### CONNECTION")
    st.markdown("🌐 <span class='status-active'>SERVER: OPTIMIZED</span>", unsafe_allow_html=True)
    st.markdown("🛡️ <span class='status-active'>AES-256: ACTIVE</span>", unsafe_allow_html=True)

# --- MAIN INTERFACE LOGIC ---
if nav == "EXECUTIVE OVERVIEW":
    st.markdown("<h1 class='main-header'>AUTO OPERATING SYSTEM</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #888; font-size: 1.2rem;'>The Global Standard for Autonomous Business Operations.</p>", unsafe_allow_html=True)
    
    st.write("---")
    
    # KPIs (Key Performance Indicators)
    c1, c2, c3 = st.columns(3)
    c1.metric("TOTAL AUTOMATIONS", "128,402", "+14.2%")
    c2.metric("MONTHLY REVENUE", "€425,000", "TARGET: €30M")
    c3.metric("AI EFFICIENCY", "99.98%", "OPTIMAL")

    st.write("---")
    
    col_a, col_b = st.columns([2, 1])
    
    with col_a:
        st.subheader("LIVE INTELLIGENCE LOG")
        log_data = {
            "TIME": [datetime.now().strftime("%H:%M:%S") for _ in range(4)],
            "PROCESS": ["GMAIL_SYNC", "INVOICE_GEN", "REPLY_DRAFT", "WHATSAPP_ALERT"],
            "TARGET": ["CEO_TECH_CORP", "FINANCE_DEPT", "INVESTOR_RELATIONS", "OFFICE_ADMIN"],
            "RESULT": ["COMPLETED", "SENT", "WAITING_APPROVAL", "NOTIFIED"]
        }
        st.dataframe(pd.DataFrame(log_data), use_container_width=True)

    with col_b:
        st.subheader("SYSTEM HEALTH")
        st.info("AI is currently analyzing 42 high-value threads.")
        if st.button("CONNECT GMAIL (OAUTH 2.0)"):
            st.write("Redirecting to Secure Google Login...")

elif nav == "GMAIL INTELLIGENCE":
    st.header("GMAIL INTELLIGENCE HUB")
    st.write("Automated parsing and responding engine.")
    
    email_view = st.container()
    with email_view:
        st.markdown("<div style='background: #0f141f; padding: 20px; border-radius: 10px;'>", unsafe_allow_html=True)
        st.write("**Subject:** Partnership Opportunity - Series A Funding")
        st.write("**From:** silicon_v@vc_funds.com")
        st.write("**AI Suggestion:** This is a high-priority investment inquiry. Suggest scheduling a call for Monday.")
        st.button("APPROVE AI REPLY")
        st.markdown("</div>", unsafe_allow_html=True)

# --- FOOTER ---
st.write("---")
st.markdown("<p style='text-align: center; color: #444;'>AUTO OPERATING SYSTEM | ENTERPRISE GRADE | © 2026</p>", unsafe_allow_html=True)