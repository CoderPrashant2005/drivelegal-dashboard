# App1.py
import streamlit as st
import random
import base64
import os
from pages.dashboard import show_dashboard
from pages.violations import show_violations
from pages.traffic_laws import render_traffic_laws
from pages.vehicles import show_vehicles
from pages.safety_tips import show_safety_tips
from styles import load_css
from streamlit_autorefresh import st_autorefresh

# ===================================
# 1. READ SECRET LINK PARAMETERS (HACKATHON QUICK-SYNC)
# ===================================
# Grab the car plate parameter directly out of the browser address bar
if "car" in st.query_params:
    st.session_state.user_plate = st.query_params["car"]
else:
    # Default fallback test car so your app works cleanly if opened directly
    st.session_state.user_plate = "DL01AB1234"

# ===================================
# 2. PAGE CONFIGURATION & INITIALIZATION
# ===================================
st.set_page_config(
    page_title="DriveLegal",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Trigger auto-refresh every 5 seconds to catch live telemetry events
st_autorefresh(interval=5000, key="dashboard_refresh")

# Hide default Streamlit sidebar menu items
st.markdown("""
<style>
[data-testid="stSidebarNav"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

# Initialize Session State Variables
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Dashboard"

# ===================================
# 3. LOAD UNIFIED CSS
# ===================================
load_css(st.session_state.theme)

# Map dynamic variables for custom elements in app.py
if st.session_state.theme == "Dark":
    card_bg = "#0C0E14"
    border_color = "#171B26"
    text_color = "#FFFFFF"
else:
    card_bg = "#F3F4F6"
    border_color = "#E5E7EB"
    text_color = "#0F172A"

# ============================================
# 4. ROAD SAFETY QUOTES DATABASE
# =============================================
SAFETY_QUOTES = [
    "🚦 Safety is not automatic, think before you drive.",
    "🛑 Better late than never. Slow down and stay safe.",
    "💺 Seatbelts save lives. Buckle up every trip.",
    "📵 A text can wait. Your life cannot.",
    "🚗 Drive responsibly, arrive safely.",
    "⚠️ Speed thrills but kills."
]

if "safety_quote" not in st.session_state:
    st.session_state.safety_quote = random.choice(SAFETY_QUOTES)

# ===================================
# 5. UNIFIED SIDEBAR (Sequential Component Flow)
# ===================================
with st.sidebar:
    st.markdown(
        """
        <style>
            [data-testid="stSidebarContent"] { padding-top: 0rem !important; }
            [data-testid="stSidebarContent"] > div:first-child { padding-top: 0px !important; margin-top: 0px !important; }
            .brand-container { margin-top: -60px !important; padding-top: 0px !important; }
        </style>
        """,
        unsafe_allow_html=True
    )

    if st.session_state.theme == "Dark":
        logo_path = "dark_theme_logo.png"
    else:
        logo_path = "logo.png"

    if os.path.exists(logo_path):
        with open(logo_path, "rb") as image_file:
            encoded_logo = base64.b64encode(image_file.read()).decode()
        logo_src = f"data:image/png;base64,{encoded_logo}"
    else:
        logo_src = ""

    st.markdown(
        f"""
        <div id="sidebar_branding" class="brand-container" style="text-align: center; padding: 0; margin-bottom: 15px;">
            <img src="{logo_src}" style="width: 80%; max-width: 180px; margin: 0 auto 8px auto; display: block;">
            <h2 style="text-align: center; margin: 0 0 2px 0; padding: 0; font-size: 26px; font-weight: 700; letter-spacing: -0.03em; color: #00A3C4; line-height: 1.2;">DriveLegal</h2>
            <p style="text-align: center; font-size: 12px; color: #FFFFFF; margin: 0; padding: 0; line-height: 1.2; opacity: 0.8;">Drive Smart • Stay Safe • Stay Legal</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("""
        <div style="text-align: center; margin-bottom: 5px;">
            <h3 style="margin: 0; font-size: 16px; font-weight: 700; letter-spacing: -0.01em;">💡 JUST FOR YOU</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style="background: {card_bg}; border: 1px solid {border_color}; padding: 16px 18px; border-radius: 14px; margin-bottom: 15px; text-align: center;">
            <p style="margin: 0; font-size: 14px; line-height: 1.6; font-weight: 500; color: {text_color} !important;">
                {st.session_state.safety_quote}
            </p>
        </div>
    """, unsafe_allow_html=True)

    if st.button("🔄 Refresh Dashboard", use_container_width=True):
        current_quote = st.session_state.safety_quote
        available_quotes = [q for q in SAFETY_QUOTES if q != current_quote]
        st.session_state.safety_quote = random.choice(available_quotes)
        st.cache_data.clear()
        st.cache_resource.clear()
        st.rerun()

    st.divider()

    st.markdown("""
        <div style="text-align: center; margin-top: 5px; margin-bottom: 15px;">
            <h3 style="margin: 0; font-size: 22px; font-weight: 700;">Navigation</h3>
        </div>
    """, unsafe_allow_html=True)

    if st.button("📊 Dashboard", use_container_width=True):
        st.session_state.active_tab = "Dashboard"
        st.rerun()

    if st.button("⚠️ My Violations", use_container_width=True):
        st.session_state.active_tab = "My Violations"
        st.rerun()

    if st.button("⚖️ Traffic Laws", use_container_width=True):
        st.session_state.active_tab = "Traffic Laws"
        st.rerun()

    if st.button("🚘 My Vehicles", use_container_width=True):
        st.session_state.active_tab = "My Vehicles"
        st.rerun()

    if st.button("🛡️ Safety Tips", use_container_width=True):
        st.session_state.active_tab = "Safety Tips"
        st.rerun()

    st.divider()

    st.markdown("""
        <div style="text-align: center; margin-top: 5px; margin-bottom: 15px;">
            <h3 style="margin: 0; font-size: 22px; font-weight: 700;">Appearance</h3>
        </div>
    """, unsafe_allow_html=True)
    
    theme_choice = st.selectbox(
        "Select Theme", ["Dark", "Light"],
        index=0 if st.session_state.theme == "Dark" else 1,
        label_visibility="collapsed"
    )
    
    if theme_choice != st.session_state.theme:
        st.session_state.theme = theme_choice
        st.rerun()

# ===================================
# 6. CENTRAL CONTROL ROUTER (USER ISOLATED)
# ===================================
# Pass the dynamically selected browser parameter directly down into your sub-views
if st.session_state.active_tab == "Dashboard":
    show_dashboard(vehicle_id=st.session_state.user_plate)
elif st.session_state.active_tab == "My Violations":
    show_violations(vehicle_id=st.session_state.user_plate)
elif st.session_state.active_tab == "Traffic Laws":
    render_traffic_laws()
elif st.session_state.active_tab == "My Vehicles":
    show_vehicles(vehicle_id=st.session_state.user_plate)
elif st.session_state.active_tab == "Safety Tips":
    show_safety_tips()