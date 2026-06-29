import streamlit as st
import pandas as pd
import requests

# 1. Update the function to receive the unique vehicle_id variable from App1.py
def show_dashboard(vehicle_id):
    # ==================================================
    # THEME CONTEXT CONFIGURATION
    # ==================================================
    theme = st.session_state.get("theme", "Dark")

    if theme == "Dark":
        bg_card = "#1F2937"       # Slate 800
        border_color = "#374151"  # Slate 700
        text_color = "#FFFFFF"    # Pure White
        muted_text = "#9CA3AF"    # Slate 400
    else:
        bg_card = "#FFFFFF"       # Brilliant White
        border_color = "#E5E7EB"  # Slate 200
        text_color = "#0F172A"    # Pitch Dark Slate
        muted_text = "#4B5563"    # Slate 600

    # Deep CSS enforcer injection to style layout blocks across Light/Dark modes
    st.html(f"""
        <style>
            div[data-testid="stVerticalBlockBorderWrapper"]:has(.premium-card) {{
                background-color: {bg_card} !important;
                border: 1px solid {border_color} !important;
                padding: 22px !important;
                border-radius: 16px !important;
                margin-bottom: 20px !important;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
            }}
            .premium-card-title {{
                margin: 0 0 15px 0 !important; 
                font-size: 18px !important; 
                font-weight: 700 !important; 
                color: {text_color} !important;
            }}
            .success-banner {{
                padding: 14px 18px !important;
                border-radius: 8px !important;
                border-left: 4px solid #10B981 !important;
                background: rgba(16, 185, 129, 0.08) !important;
                color: {text_color} !important;
                font-weight: 600 !important;
                font-size: 14px !important;
            }}
        </style>
    """)

    def premium_card(title_text=""):
        card_container = st.container()
        card_container.html(f'<span class="premium-card"></span>')
        if title_text:
            card_container.html(f'<h3 class="premium-card-title">{title_text}</h3>')
        return card_container

    # ==================================================
    # FETCH REAL TIME DATA FROM THE BACKEND PIPELINE
    # ==================================================
    api_url = f"http://127.0.0.1:8000/api/v1/dashboard-complete/{vehicle_id}"
    
    total_viol = 0
    pending_cases = 0
    pending_amt = 0
    score = 100
    car_model = "Hyundai Creta"
    violations_list = []
    payments_list = []
    
    try:
        response = requests.get(api_url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            summary = data["summary"]
            
            total_viol = summary["total_violations"]
            pending_cases = summary["pending_violations"]
            pending_amt = summary["pending_amount"]
            score = data["ai_score"]["score"]
            violations_list = data["violations"]
            payments_list = data["payments"]
            
            if data["vehicles"]:
                car_model = data["vehicles"][0]["model"]
    except Exception as e:
        st.sidebar.error(f"Backend Sync Offline: {e}")

    # ==================================================
    # HEADER
    # ==================================================
    st.title("DriveLegal 🚗")
    st.write("Drive Smart • Stay Safe • Stay Legal")
    st.markdown("<br>", unsafe_allow_html=True)

    # ==================================================
    # KPI CARDS (DYNAMICS INJECTED)
    # ==================================================
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("🚨 Total Violations", f"{total_viol}", "+8%" if total_viol > 0 else "0", delta_color="inverse")
    with c2:
        st.metric("⚠️ Pending Cases", f"{pending_cases}", "-2%" if pending_cases > 0 else "Clean", delta_color="normal")
    with c3:
        # 💡 UPDATE: Added delta_arrow="off" to clear the arrow graphics while preserving text labels
        st.metric("💰 Pending Amount", f"₹{pending_amt:,}", "Unpaid" if pending_amt > 0 else "Cleared", delta_color="off", delta_arrow="off")
    with c4:
        # 💡 UPDATE: Added delta_arrow="off" to clear the arrow graphics while preserving text labels
        st.metric("🛡️ Compliance Score", f"{score}%", "Excellent" if score >= 80 else "Review", delta_color="off", delta_arrow="off")

    st.markdown("<br>", unsafe_allow_html=True)

    # ==================================================
    # AI DRIVING SCORE (DYNAMICS INJECTED)
    # ==================================================
    with premium_card("🛡️ AI Driving Score Analysis"):
        st.progress(score / 100)
        st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)

        if score >= 80:
            st.markdown(f'<div class="success-banner">Excellent Driving Score: {score}/100</div>', unsafe_allow_html=True)
        elif score >= 60:
            st.markdown(f'<div class="success-banner" style="background: rgba(245, 158, 11, 0.08) !important; border-left-color: #F59E0B !important;">Average Driving Score: {score}/100</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="success-banner" style="background: rgba(239, 68, 68, 0.08) !important; border-left-color: #EF4444 !important;">Poor Driving Score: {score}/100</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ==================================================
    # ALERTS + VEHICLE OVERVIEW
    # ==================================================
    left, right = st.columns([2, 1])

    with left:
        with premium_card("🔔 Live Operations Alerts"):
            if pending_cases > 0:
                st.error(f"🚦 Active traffic infractions detected on history records.")
                st.warning(f"⚠️ {pending_cases} Pending Challans Require Attention")
            else:
                st.success("✅ System check nominal. No active operational issues flagged.")
            st.info("📅 Insurance renewal in 45 days")
            st.warning("📄 RC Verification Required")

    with right:
        with premium_card("🚘 Vehicle Details"):
            lbl1, val1 = st.columns([1, 1])
            lbl1.markdown(f"<span style='color: {muted_text}; font-weight: 500; font-size: 14px;'>Plate No</span>", unsafe_allow_html=True)
            val1.markdown(f"<span style='font-weight: 600; font-size: 14px; float: right; color: {text_color};'>{vehicle_id}</span>", unsafe_allow_html=True)
            
            st.markdown(f"<hr style='margin: 12px 0; border-color: {border_color};'>", unsafe_allow_html=True)
            
            lbl2, val2 = st.columns([1, 1])
            lbl2.markdown(f"<span style='color: {muted_text}; font-weight: 500; font-size: 14px;'>Model</span>", unsafe_allow_html=True)
            val2.markdown(f"<span style='font-weight: 600; font-size: 14px; float: right; color: {text_color};'>{car_model}</span>", unsafe_allow_html=True)
                
            st.markdown(f"<hr style='margin: 12px 0; border-color: {border_color};'>", unsafe_allow_html=True)
            
            lbl3, val3 = st.columns([1, 1])
            lbl3.markdown(f"<span style='color: {muted_text}; font-weight: 500; font-size: 14px;'>Status</span>", unsafe_allow_html=True)
            val3.markdown("<span style='color: #10B981; font-weight: 600; background: rgba(16, 185, 129, 0.1); padding: 3px 10px; border-radius: 6px; font-size: 13px; float: right;'>Active</span>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ==================================================
    # RECENT VIOLATIONS DATA VIEW (DYNAMICS INJECTED)
    # ==================================================
    st.subheader("📋 Recent Violations")
    if violations_list:
        df = pd.DataFrame(violations_list)
        df_display = df[["type", "amt", "status", "loc"]].rename(
            columns={"type": "Violation", "amt": "Fine Amount", "status": "Status", "loc": "Location"}
        )
        st.dataframe(df_display, use_container_width=True, hide_index=True)
    else:
        st.info("🎉 Clean profile record! No traffic citations issued on this account.")

    st.markdown("<br>", unsafe_allow_html=True)

    # ==================================================
    # TELEMETRY LOGS ACTIVITY FEED (DYNAMICS INJECTED)
    # ==================================================
    with premium_card("📍 Recent Activity Feed"):
        if violations_list:
            for v in violations_list[:3]:
                if v["status"] == "Pending":
                    st.error(f"🚗 {v['type']} violation logged at {v['loc']} • ₹{v['amt']:,}")
                else:
                    st.success(f"✅ {v['type']} challan resolved successfully at {v['loc']}")
        else:
            st.success("📡 Vehicle location tracking online • All system sync telemetry streams nominal")
        st.warning("⚠️ Insurance renewal due next month")