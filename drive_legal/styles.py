import streamlit as st

def load_css(theme):
    if theme == "Dark":
        bg = "#040509"         # Matches the pitch black background of your logo asset
        card = "#0C0E14"       # Dark charcoal color for sidebar and card components
        text = "#FFFFFF"       # High-Contrast White Text
        secondary = "#9CA3AF"  # Muted Gray
        border = "#171B26"     # Clean, subtle dark borders
        primary = "#3B82F6"    # Blue Accent
        
        # Hover states
        hover_bg = "#1B2D55"  
        hover_text = "#FFFFFF"
        
        # Native Alert Text Overrides
        alert_text = "#FFFFFF"
    else:
        # Background matching your light theme logo.png
        bg = "#F5F5F5"         
        
        # Sidebar background updated to match the logo container background
        card = "#F5F5F5"       
        
        text = "#0F172A"       # Pitch Dark Slate Text
        secondary = "#4B5563"  # Deep Gray Subtext
        border = "#E5E7EB"     # Light Edge Border
        primary = "#2563EB"    # Blue Accent
        
        # Hover states
        hover_bg = "#DBEAFE"  
        hover_text = "#1E40AF"
        
        # Native Alert Text Overrides (Forced High-Contrast for Light Theme)
        alert_text = "#0F172A"

    st.markdown(
        f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

/* --- Reset & High Contrast Typography --- */
html, body, [data-testid="stMarkdownContainer"] p {{
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: {text} !important;
}}

[data-testid="stAppViewContainer"] {{
    background: {bg};
}}

header [data-testid="stHeader"] {{
    display: none !important;
}}

[data-testid="stAppViewContainer"] .block-container, 
[data-testid="stMainBlockContainer"] {{
    padding-top: 0.5rem !important;
    max-width: 1400px;
}}

section[data-testid="stSidebar"] {{
    background: {card};
    border-right: 1px solid {border};
}}

/* --- Heading Enforcements --- */
h1, h2, h3, h4, h5, h6 {{
    color: {text} !important;
    font-weight: 700;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    letter-spacing: -0.02em;
}}

/* Targeted Typography Overrides (Prevents text collisions inside Inputs & Dropdowns) */
[data-testid="stAppViewContainer"] p, 
[data-testid="stWidgetLabel"] p,
[data-testid="stMarkdownContainer"] span {{
    color: {text} !important;
}}

small {{
    color: {secondary} !important;
}}

/* --- Streamlit Native Alert High-Contrast Overrides --- */
[data-testid="stAlert"] {{
    border-radius: 14px !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
    border: 1px solid {border} !important;
}}

[data-testid="stAlert"] p, [data-testid="stAlert"] div {{
    color: {alert_text} !important;
    font-weight: 600 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}}

/* --- Logo Wrapper Masking --- */
[data-testid="stSidebar"] [data-testid="stImage"] {{
    background-color: transparent !important;
    background: transparent !important;
}}

[data-testid="stSidebar"] [data-testid="stImage"] img {{
    border-radius: 0px !important;
    box-shadow: none !important;
    border: none !important;
    background-color: transparent !important;
    background: transparent !important;
}}

/* --- Metric Cards --- */
div[data-testid="metric-container"] {{
    background: {card} !important;
    border: 1px solid {border} !important;
    padding: 20px 24px !important;
    border-radius: 16px !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
    transition: all 0.2s ease;
}}

div[data-testid="metric-container"]:hover {{
    transform: translateY(-2px);
    border-color: {primary} !important;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1) !important;
}}

div[data-testid="stMetricLabel"] p {{
    color: {secondary} !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}

div[data-testid="stMetricValue"] {{
    color: {text} !important;
    font-size: 32px !important;
    font-weight: 700 !important;
    margin-top: 4px;
}}

/* --- Navigation Button Styling --- */
div.stButton > button {{
    width: 100%;
    border-radius: 12px;
    background: transparent !important;
    color: {text} !important;
    border: 1px solid {border} !important;
    padding: 0.65rem 1rem;
    font-weight: 500;
    font-size: 14px;
    transition: all 0.2s ease;
    text-align: left !important;
    background-color: {card} !important;
}}

div.stButton > button:hover {{
    background-color: {hover_bg} !important;
    color: {hover_text} !important;
    border-color: {primary} !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}}

div.stButton > button:focus, div.stButton > button:active {{
    background-color: {primary} !important;
    color: #FFFFFF !important;
    border-color: {primary} !important;
}}

/* --- Dynamic Theme-Agnostic Success Banner --- */
.success-banner {{
    background: rgba(34, 197, 94, 0.08);
    border: 1px solid rgba(34, 197, 94, 0.2);
    border-left: 5px solid #22C55E;
    padding: 14px 18px;
    border-radius: 12px;
    color: {text} !important;
    font-weight: 500;
    margin: 16px 0;
}}

hr {{
    border-color: {border} !important;
    opacity: 0.5;
}}

[data-testid="stDataFrame"] {{
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid {border};
}}
</style>
""",
        unsafe_allow_html=True
    )