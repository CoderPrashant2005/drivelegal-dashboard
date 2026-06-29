import streamlit as st
import pandas as pd
import plotly.express as px
import requests

def show_violations(vehicle_id=None):
    theme = st.session_state.get("theme", "Dark")

    # Match exact dashboard layout palette
    if theme == "Dark":
        bg_card = "#1F2937"       # Slate 800
        border_color = "#374151"  # Slate 700
        text_color = "#FFFFFF"    # Pure White
        muted_text = "#9CA3AF"    # Slate 400
        
        pie_pending = "#374151"   # Deep Charcoal
        pie_resolved = "#9CA3AF"  # Light Silver-Gray
        chart_text_color = "#BFC0C0"
        plotly_template = "plotly_dark"
        
        # Updated bar and line chart color for Dark Theme only
        assigned_chart_color = "#9CA3AF"
    else:
        bg_card = "#FFFFFF"       # Brilliant White
        border_color = "#E5E7EB"  # Slate 200
        text_color = "#000000"    # Pitch Dark Slate
        muted_text = "#252525"    # Slate 600
        
        pie_pending = "#344966"   # Custom slate blue selection
        pie_resolved = "#1E293B"  # High-contrast dark slate blue
        chart_text_color = "#010102"
        plotly_template = "plotly_white"
        
        # Restored original light theme chart color
        assigned_chart_color = "#374151"

    # Deep layout enforcer injection to make the first two buttons mirror the input styles
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
            
            /* FORCES THE BUTTON BOXES TO BECOME IDENTICAL COPIES OF THE DROP-DOWNS */
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
            
            /* COMPLETELY FIXES THE TEXT LABELS TO REMAIN ALIGNED & WHITE IN LIGHT MODE */
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
    # HEADER
    # ==================================================
    st.title("⚠️ Violation Intelligence Center")
    st.write("Track challans, monitor fines, analyze violation trends, and receive compliance insights.")
    st.markdown("<br>", unsafe_allow_html=True)

    # ==================================================
    # FETCH REAL DATA FROM THE BACKEND (per-user, not hardcoded)
    # ==================================================
    api_url = f"http://127.0.0.1:8000/api/v1/user-vehicles/{vehicle_id}"

    violations = []
    monthly_trend = {"Jan": 0, "Feb": 0, "Mar": 0, "Apr": 0, "May": 0, "Jun": 0}
    backend_error = None

    try:
        response = requests.get(api_url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            violations = [
                {
                    "ID": v["id"],
                    "Type": v["type"],
                    "Location": v["loc"],
                    "Amount": v["amt"],
                    "Status": v["status"],
                    "Date": v["time"],
                }
                for v in data.get("violations", [])
            ]
            full_trend = data.get("monthly_trend", {})
            monthly_trend = {m: full_trend.get(m, 0) for m in ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]}
        elif response.status_code == 404:
            backend_error = "No user record linked to this account yet."
        else:
            backend_error = f"Backend returned status {response.status_code}."
    except Exception as e:
        backend_error = f"Backend Sync Offline: {e}"

    if backend_error:
        st.error(f"⚠️ {backend_error}")
        return

    df = pd.DataFrame(violations, columns=["ID", "Type", "Location", "Amount", "Status", "Date"])

    if "alerts_enabled" not in st.session_state:
        st.session_state.alerts_enabled = False

    # ==================================================
    # CONTROL CENTER CARD
    # ==================================================
    with premium_card("🛠️ Control Center"):
        a1, a2, a3, a4 = st.columns([1.5, 1.5, 2, 1.5])
        with a1:
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📄 Export Data",
                data=csv_data,
                file_name="DriveLegal_Report.csv",
                mime="text/csv",
                use_container_width=True
            )
        with a2:
            alert_btn_label = "🔕 Disable Alerts" if st.session_state.alerts_enabled else "🔔 Enable Alerts"
            if st.button(alert_btn_label, use_container_width=True):
                st.session_state.alerts_enabled = not st.session_state.alerts_enabled
                st.rerun()
        with a3:
            search_text = st.text_input("Search Location / Violation", placeholder="Type to filter...", label_visibility="collapsed")
        with a4:
            severity_filter = st.selectbox("Severity", ["All Severity", "Critical", "High", "Medium", "Low"], label_visibility="collapsed")

    # ==================================================
    # APPLY FILTERS BEFORE METRICS AND VISUALS
    # ==================================================
    filtered_df = df.copy()
    if search_text and not filtered_df.empty:
        filtered_df = filtered_df[
            filtered_df["Type"].str.contains(search_text, case=False, na=False) |
            filtered_df["Location"].str.contains(search_text, case=False, na=False)
        ]
    # NOTE: "Severity" isn't tracked in the database yet, so this filter is
    # currently a no-op against real data. Wire it up once a severity field
    # exists on the Violation model / MySQL source.
    if severity_filter != "All Severity":
        st.caption("ℹ️ Severity data isn't tracked yet — showing all matching records regardless of severity.")

    # ==================================================
    # DYNAMIC KPI METRICS
    # ==================================================
    total_cases = len(filtered_df)
    pending_cases = len(filtered_df[filtered_df["Status"] == "Pending"]) if not filtered_df.empty else 0
    resolved_cases = len(filtered_df[filtered_df["Status"] == "Paid"]) if not filtered_df.empty else 0
    total_fines = filtered_df["Amount"].sum() if not filtered_df.empty else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("🚨 Total Violations", total_cases)
    with c2:
        st.metric("⏳ Pending Cases", pending_cases)
    with c3:
        st.metric("✅ Resolved Cases", resolved_cases)
    with c4:
        st.metric("💰 Total Fines", f"₹{total_fines:,.0f}")

    st.markdown("<br>", unsafe_allow_html=True)

    # ==================================================
    # DATA GRID VIEW
    # ==================================================
    st.subheader("🚨 Live Violation Records")
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if filtered_df.empty:
        st.info("No records found matching the active filters.")
        return

    # ==================================================
    # VISUALIZATION ROW 1: Pie Chart & Hotspot Table
    # ==================================================
    chart_col1, chart_col2 = st.columns([1.2, 1.8])

    with chart_col1:
        with premium_card("📊 Status Distribution"):
            status_chart_data = filtered_df["Status"].value_counts().reset_index()
            status_chart_data.columns = ["Status", "Count"]
            
            fig_pie = px.pie(
                status_chart_data, 
                values="Count", 
                names="Status",
                hole=0.5, 
                color="Status",
                color_discrete_map={"Pending": pie_pending, "Paid": pie_resolved}
            )
            fig_pie.update_layout(
                template=plotly_template,
                height=280,
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5, font=dict(color=chart_text_color, size=11)),
                font=dict(color=chart_text_color, family="Plus Jakarta Sans")
            )
            
            # FIXED: Text color shifts to white, size defaults dynamically matching your dark layout
            fig_pie.update_traces(
                textposition='inside', 
                textinfo='percent', 
                insidetextfont=dict(color="#FFFFFF")
            )
            st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False}, theme=None)

    with chart_col2:
        with premium_card("📍 Frequent Violation Hotspots"):
            hotspot_df = (
                filtered_df.dropna(subset=["Location"])
                .groupby("Location")
                .size()
                .reset_index(name="Count")
                .sort_values("Count", ascending=False)
            )
            if hotspot_df.empty:
                st.info("No location data recorded yet.")
            else:
                st.dataframe(hotspot_df, use_container_width=True, hide_index=True, height=280)

    # ==================================================
    # VISUALIZATION ROW 2: Fine Allocations
    # ==================================================
    with premium_card("💰 Fine Allocations by Major Type"):
        fine_chart_data = filtered_df.groupby("Type")["Amount"].sum().reset_index().sort_values("Amount", ascending=True)
        
        fig_bar = px.bar(
            fine_chart_data,
            x="Amount",
            y="Type",
            orientation='h',
            color_discrete_sequence=[assigned_chart_color]
        )
        fig_bar.update_layout(
            template=plotly_template,
            height=320,
            margin=dict(l=160, r=20, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(
                title=dict(text="Fine Amount (₹)", font=dict(color=chart_text_color)), 
                color=muted_text, 
                gridcolor=border_color, 
                showgrid=True
            ),
            yaxis=dict(
                title="", 
                color=chart_text_color,
                ticklabelstandoff=15 
            ),
            font=dict(color=chart_text_color, family="Plus Jakarta Sans")
        )
        st.plotly_chart(fig_bar, use_container_width=True, theme=None)

    # ==================================================
    # VISUALIZATION ROW 3: Monthly Trend
    # ==================================================
    with premium_card("📈 Monthly Violation Trend"):
        trend_df = pd.DataFrame({
            "Month": list(monthly_trend.keys()),
            "Violations": list(monthly_trend.values())
        })
        
        fig_line = px.line(
            trend_df,
            x="Month",
            y="Violations",
            markers=True,
            color_discrete_sequence=[assigned_chart_color]
        )
        fig_line.update_layout(
            template=plotly_template,
            height=280,
            margin=dict(l=10, r=20, t=15, b=15),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(title="", color=muted_text, showgrid=False),
            yaxis=dict(
                title=dict(text="Incident Count", font=dict(color=chart_text_color)), 
                color=muted_text, 
                gridcolor=border_color, 
                dtick=1
            ),
            font=dict(color=chart_text_color, family="Plus Jakarta Sans")
        )
        st.plotly_chart(fig_line, use_container_width=True, theme=None)