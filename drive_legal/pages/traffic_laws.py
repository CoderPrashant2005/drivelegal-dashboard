import streamlit as st
import requests

# Import database connection utilities from your models architecture
try:
    from models import SessionLocal, TrafficLaw
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False

def render_traffic_laws():

    st.title("⚖️ Traffic Laws & Regulations")
    st.caption("Cross-reference motor vehicle laws across Indian states and union territories.")

    # ==================================================
    # LOCATION SELECTOR
    # ==================================================
    locations = [
    "Agartala, Tripura",
    "Ahmedabad, Gujarat",
    "Aizawl, Mizoram",
    "Amritsar, Punjab",
    "Bengaluru, Karnataka",
    "Bhopal, Madhya Pradesh",
    "Chandigarh, Chandigarh",
    "Chennai, Tamil Nadu",
    "Daman, Daman and Diu",
    "Dehradun, Uttarakhand",
    "Dispur(Guwahati), Assam",
    "Gangtok, Sikkim",
    "Gurugram, Haryana",
    "Hyderabad, Telangana",
    "Imphal, Manipur",
    "Itanagar, Arunachal Pradesh",
    "Jaipur, Rajasthan",
    "Kavaratti, Lakshadweep",
    "Kochi, Kerala",
    "Kohima, Nagaland",
    "Kolkata, West Bengal",
    "Leh, Ladakh",
    "Lucknow, Uttar Pradesh",
    "Mumbai, Maharashtra",
    "New Delhi, Delhi",
    "Panaji, Goa",
    "Patna, Bihar",
    "Pondicherry, Puducherry",
    "Port Blair, Andaman & Nicobar Islands",
    "Raipur, Chhattisgarh",
    "Shillong, Meghalaya",
    "Shimla, Himachal Pradesh",
    "Srinagar, Jammu and Kashmir",
    "Visakhapatnam, Andhra Pradesh",
]

    selected_location = st.selectbox("📍 Select Location", locations)
    selected_state = selected_location.split(",")[-1].strip()

    col1, col2 = st.columns([3, 1])
    with col1:
        st.success(f"Active Jurisdiction: {selected_state}")
    with col2:
        scan_all = st.checkbox("All States")

    st.divider()

    # ==================================================
    # PRIMARY API CALL PIPELINE
    # ==================================================
    laws_data = []
    backend_online = False

    try:
        state_param = "" if scan_all else selected_state
        response = requests.get(
            "http://localhost:8000/api/v1/laws/search",
            params={"state": state_param, "q": ""},
            timeout=2
        )
        if response.status_code == 200:
            laws_data = response.json()
            backend_online = True
    except Exception:
        backend_online = False

    # ==================================================
    # DIRECT NATIVE DATABASE FALLBACK CONNECTOR
    # ==================================================
    if not backend_online:
        if DB_AVAILABLE:
            db = SessionLocal()
            try:
                if scan_all:
                    query_results = db.query(TrafficLaw).all()
                else:
                    query_results = db.query(TrafficLaw).filter(
                        TrafficLaw.state.ilike(selected_state)
                    ).all()
                
                laws_data = [
                    {"state": row.state, "description": row.description} 
                    for row in query_results
                ]
            except Exception as e:
                st.error(f"Local Database error: {e}")
            finally:
                db.close()
        else:
            st.error("❌ Fatal: Database models architecture unlinked or missing.")
            return

    # ==================================================
    # CLEAN BANNER RENDERING ENGINE (SIMPLE & RELIABLE)
    # ==================================================
    if not laws_data:
        st.info(f"No specific records available in local seed registry for {selected_state} yet.")
        return

    st.markdown(f"### 📋 {selected_state} Regulations")

    for law in laws_data:
        description = law["description"]
        desc_lower = description.lower()

        # Dynamic visual indicator sorting
        if "speed" in desc_lower or "urban" in desc_lower:
            icon = "🚗"
        elif "helmet" in desc_lower:
            icon = "🪖"
        elif "park" in desc_lower:
            icon = "🅿️"
        elif "pedestrian" in desc_lower or "walking" in desc_lower:
            icon = "🚶"
        elif "seatbelt" in desc_lower or "seat belt" in desc_lower:
            icon = "💺"
        else:
            icon = "📝"

        # Renders the laws inside clean, built-in Streamlit informational banners
        st.info(f"**{icon} {law['state']} Rule:** {description}")
