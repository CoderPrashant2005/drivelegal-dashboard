# pages/vehicles.py

import os
import io
import streamlit as st
import pandas as pd
import plotly.express as px
import requests

def show_vehicles(vehicle_id=None):
    # ==================================================
    # THEME CONTEXT CONFIGURATION
    # ==================================================
    theme = st.session_state.get("theme", "Dark")

    if theme == "Dark":
        bg_card = "#1F2937"       # Slate 800
        border_color = "#374151"  # Slate 700
        text_color = "#FFFFFF"    # Pure White
        muted_text = "#9CA3AF"    # Slate 400
        
        pie_pending = "#374151"   # Deep Charcoal
        pie_resolved = "#9CA3AF"  # Light Silver-Gray
        chart_text_color = "#FFFFFF"
        plotly_template = "plotly_dark"
        assigned_chart_color = "#9CA3AF" # Gray color code for dark theme bars & lines
    else:
        bg_card = "#FFFFFF"       # Brilliant White
        border_color = "#E5E7EB"  # Slate 200
        text_color = "#0F172A"    # Pitch Dark Slate
        muted_text = "#4B5563"    # Slate 600
        
        pie_pending = "#344966"   # Custom slate blue
        pie_resolved = "#1E293B"  # High-contrast dark slate blue
        chart_text_color = "#FFFFFF"
        plotly_template = "plotly_white"
        assigned_chart_color = "#545F70"

    # Deep CSS enforcer injection to stylize cards, layout blocks and action buttons
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
            
            /* Forces system buttons to adapt to premium themes */
            div[data-testid="stMainBlockContainer"] div.stButton > button,
            div[data-testid="stMainBlockContainer"] div.stDownloadButton > button {{
                background-color: #1E293B !important;
                border: 1px solid #1E293B !important;
                border-radius: 8px !important;
                height: 38px !important;
                width: 100% !important;
                text-align: center !important;
                padding: 0 !important;
                line-height: 38px !important;
            }}
            
            /* Keeps text alignments pristine inside the custom action wrappers */
            div[data-testid="stMainBlockContainer"] div.stButton > button *,
            div[data-testid="stMainBlockContainer"] div.stDownloadButton > button * {{
                color: #FFFFFF !important;
                font-weight: 500 !important;
                font-size: 14px !important;
            }}
            div[data-testid="stMainBlockContainer"] div.stButton > button p,
            div[data-testid="stMainBlockContainer"] div.stDownloadButton > button p {{
                color: #FFFFFF !important;
                line-height: 38px !important;
                margin: 0 !important;
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
    # FETCH REAL DATA FROM THE BACKEND (per-user, not per-plate)
    # ==================================================
    api_url = f"http://127.0.0.1:8000/api/v1/user-vehicles/{vehicle_id}"

    owner_name = "Unknown"
    all_vehicles = []
    all_violations = []
    monthly_trend = {"Jan": 0, "Feb": 0, "Mar": 0, "Apr": 0, "May": 0, "Jun": 0}
    backend_error = None

    try:
        response = requests.get(api_url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            owner_name = data.get("owner") or "Unknown"
            all_vehicles = data.get("vehicles", [])
            all_violations = data.get("violations", [])
            # Only keep the first 6 months for the existing Jan-Jun chart shape
            full_trend = data.get("monthly_trend", {})
            monthly_trend = {m: full_trend.get(m, 0) for m in ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]}
        elif response.status_code == 404:
            backend_error = "This vehicle has no linked owner record yet (run the MySQL migration, or it was created without owner data)."
        else:
            backend_error = f"Backend returned status {response.status_code}."
    except Exception as e:
        backend_error = f"Backend Sync Offline: {e}"

    # ==================================================
    # HEADER
    # ==================================================
    st.markdown("## 🚘 My Vehicle Command Center")
    st.caption("Unified vehicle profile, challan history, compliance status and AI-powered risk insights.")

    if backend_error:
        st.error(f"⚠️ {backend_error}")
        return

    if not all_vehicles:
        st.info("No vehicles found for this account yet.")
        return

    # ==================================================
    # VEHICLE PICKER (only shown when the user owns more than one)
    # ==================================================
    if len(all_vehicles) > 1:
        plate_options = [v["plate"] for v in all_vehicles]
        selected_plate = st.selectbox("Select Vehicle", plate_options, index=0)
    else:
        selected_plate = all_vehicles[0]["plate"]

    vehicle = next(v for v in all_vehicles if v["plate"] == selected_plate)
    vehicle_violations = [v for v in all_violations if v["vehicle_plate"] == selected_plate]

    # Derive display fields with safe fallbacks for missing data
    model_display = vehicle.get("model") or "Not specified"
    tag_display = vehicle.get("tag") or "Secondary"
    total_violations = vehicle.get("total_violations", 0)
    pending_violations = vehicle.get("pending_violations", 0)
    total_fines = vehicle.get("total_fines", 0)
    # Simple health score: starts at 100, loses points per pending case (matches dashboard.py's logic)
    vehicle_health = max(100 - (pending_violations * 7), 30)

    # ==================================================
    # VEHICLE PROFILE CARD
    # ==================================================
    st.markdown(
        f"""
        <div style="
            background:#0F172A;
            padding:20px;
            border-radius:15px;
            border:1px solid #334155;
            margin-bottom:20px;
        ">
        <h3 style="margin:0;color:white;">
            {model_display}
        </h3>
        <p style="color:#94A3B8; margin: 5px 0;">
            Registration Number: {selected_plate}
        </p>
        <p style="color:#38BDF8; margin: 0;">
            {tag_display}
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ==================================================
    # KPI CARDS
    # ==================================================
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Violations", total_violations)
    c2.metric("Pending", pending_violations)
    c3.metric("Total Fines", f"₹{total_fines:,.0f}")
    c4.metric("Health Score", f"{vehicle_health}%")
    c5.metric("Owner", owner_name)

    st.markdown("<br>", unsafe_allow_html=True)

    # ==================================================
    # CHARTS INTERACTIVE ROW (PIE & TREND LINE)
    # ==================================================
    left, right = st.columns([1.2, 1.8])

    with left:
        with premium_card("📊 Violation Distribution"):
            pending = pending_violations
            resolved = max(total_violations - pending, 0)
            pie_data = pd.DataFrame({"Status": ["Pending", "Resolved"], "Count": [pending, resolved]})

            if pending == 0 and resolved == 0:
                st.info("No violations on record for this vehicle yet.")
            else:
                fig_pie = px.pie(
                    pie_data, values="Count", names="Status", hole=0.5,
                    color="Status", color_discrete_map={"Pending": pie_pending, "Resolved": pie_resolved}
                )
                fig_pie.update_layout(
                    template=plotly_template, height=240, margin=dict(l=10, r=10, t=10, b=10),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", showlegend=True,
                    legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5, font=dict(color=chart_text_color, size=11)),
                    font=dict(color=chart_text_color, family="Plus Jakarta Sans")
                )
                fig_pie.update_traces(textposition='inside', textinfo='percent', insidetextfont=dict(color="#FFFFFF" if theme=="Dark" else "#0F172A"))
                st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False}, theme=None)

    with right:
        with premium_card("📈 Monthly Violation Trend"):
            trend_df = pd.DataFrame({
                "Month": list(monthly_trend.keys()),
                "Violations": list(monthly_trend.values())
            })
            fig_line = px.line(trend_df, x="Month", y="Violations", markers=True, color_discrete_sequence=[assigned_chart_color])
            fig_line.update_layout(
                template=plotly_template, height=240, margin=dict(l=10, r=20, t=15, b=15),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(title="", color=muted_text, showgrid=False),
                yaxis=dict(title=dict(text="Incident Count", font=dict(color=chart_text_color)), color=muted_text, gridcolor=border_color, showgrid=True, dtick=1),
                font=dict(color=chart_text_color, family="Plus Jakarta Sans")
            )
            st.plotly_chart(fig_line, use_container_width=True, theme=None)

    # ==================================================
    # AI RISK ASSESSMENT
    # ==================================================
    st.subheader("🤖 AI Risk Assessment")
    if pending_violations >= 5:
        st.error("**Risk Level: HIGH**\n\nYour vehicle has multiple unresolved violations.\n\n*Recommended Actions:*\n* Clear pending fines\n* Review traffic behavior\n* Enable speed alerts")
    elif pending_violations >= 2:
        st.warning("**Risk Level: MEDIUM**\n\nRepeated violations detected.\n\n*Recommended Actions:*\n* Resolve pending challans\n* Follow speed compliance")
    else:
        st.success("**Risk Level: LOW**\n\nExcellent compliance history. Keep maintaining safe driving habits.")

    st.markdown("<br>", unsafe_allow_html=True)

    # ==================================================
    # RECENT VIOLATIONS GRID VIEW
    # ==================================================
    st.subheader("🚨 Recent Violations")
    if vehicle_violations:
        df_history = pd.DataFrame([
            {
                "ID": v["id"],
                "Type": v["type"],
                "Location": v["loc"],
                "Fine": f"₹{v['amt']:,.0f}",
                "Status": v["status"],
                "Date": v["time"]
            }
            for v in vehicle_violations
        ])
        st.dataframe(df_history, use_container_width=True, hide_index=True)
    else:
        st.info("No violations recorded for this vehicle.")
    st.markdown("<br>", unsafe_allow_html=True)

    # ==================================================
    # QUICK ACTIONS FOOTER
    # ==================================================
    st.subheader("⚡ Quick Actions")
    a1, a2, a3 = st.columns(3)
    
    with a1:
        st.button("💳 Pay Pending Fines", use_container_width=True)
        
    with a2:
        pdf_filename = "vehicle_report.pdf"

        # Safe system look-ahead to check if file physically exists
        if os.path.exists(pdf_filename):
            with open(pdf_filename, "rb") as f:
                pdf_data = f.read()
        else:
            # Safer fallback block: dynamically structures mock in-memory data streams to bypass errors
            buffer = io.BytesIO()
            buffer.write(b"%PDF-1.5 ... Mock DriveLegal Vehicle Report ... Sync dynamic cloud profile.")
            pdf_data = buffer.getvalue()

        st.download_button(
            label="📄 Download Vehicle Report",
            data=pdf_data,
            file_name="vehicle_report.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        
    with a3:
        st.button("🔔 Enable Alerts", use_container_width=True)