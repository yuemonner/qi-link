"""
Qi-Link: The DePIN Fengshui Node
================================

Streamlit application combining ancient wisdom with modern technology.
"""

import time
from datetime import datetime, date

import streamlit as st

st.set_page_config(
    page_title="Qi-Link | DePIN Fengshui",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

from qi_link.sensor_array import SensorArray
from qi_link.fate_engine import FateEngine
from qi_link.alchemist import Alchemist
from qi_link.ether_link import EtherLink
from qi_link.talisman_generator import TalismanGenerator
from qi_link.location_service import LocationService
from qi_link.models import Element, EnergyState
from qi_link.config import get_settings


def inject_custom_css():
    """Inject custom CSS for vibrant tree aesthetic with glass morphism."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Space+Grotesk:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');
    
    :root {
        --canopy-bright: #7dd87d;
        --canopy-mid: #4a9f4a;
        --canopy-deep: #2d6a2d;
        --trunk-light: #5c4a3a;
        --trunk-mid: #3d2f24;
        --trunk-dark: #1a1410;
        --roots-deep: #0d0a08;
        --glass-white: rgba(255, 255, 255, 0.08);
        --glass-border: rgba(255, 255, 255, 0.12);
        --glass-highlight: rgba(255, 255, 255, 0.15);
        --text-bright: #f0f7f0;
        --text-mid: #c8e4c8;
        --text-muted: #a8c8a8;
        --accent-leaf: #8de88d;
        --accent-gold: #d4af37;
        --accent-amber: #ffbf47;
    }
    
    .stApp {
        background: linear-gradient(
            180deg,
            #1a2f1a 0%,
            #152515 8%,
            #0f1c0f 20%,
            #0c150c 35%,
            #0a100a 50%,
            #0d0c0a 65%,
            #0f0c08 80%,
            #0a0806 100%
        );
        background-attachment: fixed;
    }
    
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(ellipse 120% 60% at 50% 0%, rgba(77, 139, 77, 0.15) 0%, transparent 60%),
            radial-gradient(ellipse 80% 40% at 30% 10%, rgba(125, 216, 125, 0.08) 0%, transparent 50%),
            radial-gradient(ellipse 60% 30% at 70% 5%, rgba(141, 232, 141, 0.06) 0%, transparent 40%);
        pointer-events: none;
        z-index: 0;
    }
    
    .main .block-container {
        padding-top: 2rem;
        max-width: 1400px;
        position: relative;
        z-index: 1;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            rgba(26, 47, 26, 0.95) 0%,
            rgba(15, 28, 15, 0.98) 50%,
            rgba(10, 8, 6, 0.99) 100%
        );
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-right: 1px solid var(--glass-border);
    }
    
    [data-testid="stSidebar"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 200px;
        background: radial-gradient(ellipse 100% 100% at 50% 0%, rgba(125, 216, 125, 0.1) 0%, transparent 70%);
        pointer-events: none;
    }
    
    h1, h2, h3, h4 {
        font-family: 'Cormorant Garamond', serif !important;
        color: var(--text-bright) !important;
        font-weight: 600 !important;
    }
    
    p, span, div, label {
        font-family: 'Space Grotesk', sans-serif !important;
    }
    
    .main-title {
        font-family: 'Cormorant Garamond', serif;
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(
            135deg,
            var(--canopy-bright) 0%,
            var(--accent-leaf) 25%,
            var(--accent-gold) 50%,
            var(--accent-amber) 75%,
            var(--trunk-light) 100%
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: 0.05em;
        text-shadow: 0 0 60px rgba(125, 216, 125, 0.3);
    }
    
    .subtitle {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1rem;
        color: var(--text-muted);
        text-align: center;
        margin-bottom: 2.5rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        font-weight: 300;
    }
    
    .glass-card {
        background: var(--glass-white);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid var(--glass-border);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 var(--glass-highlight);
        position: relative;
        overflow: hidden;
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--glass-highlight), transparent);
    }
    
    .glass-card h3 {
        color: var(--accent-leaf) !important;
        font-size: 1.1rem;
        margin-bottom: 1.2rem;
        font-weight: 500;
        letter-spacing: 0.05em;
    }
    
    .metric-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.75rem 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.04);
    }
    
    .metric-row:last-child {
        border-bottom: none;
    }
    
    .metric-label {
        font-family: 'Space Grotesk', sans-serif;
        color: var(--text-muted);
        font-size: 0.85rem;
        font-weight: 400;
    }
    
    .metric-value {
        font-family: 'IBM Plex Mono', monospace;
        color: var(--accent-gold);
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    .element-badge {
        display: inline-block;
        padding: 0.35rem 0.9rem;
        border-radius: 24px;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.8rem;
        font-weight: 500;
        margin: 0.2rem;
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
    }
    
    .element-metal {
        background: rgba(192, 192, 192, 0.15);
        color: #e8e8e8;
        border: 1px solid rgba(192, 192, 192, 0.4);
    }
    
    .element-wood {
        background: rgba(125, 216, 125, 0.15);
        color: var(--accent-leaf);
        border: 1px solid rgba(125, 216, 125, 0.4);
    }
    
    .element-water {
        background: rgba(100, 180, 255, 0.15);
        color: #7dc4ff;
        border: 1px solid rgba(100, 180, 255, 0.4);
    }
    
    .element-fire {
        background: rgba(255, 120, 80, 0.15);
        color: #ff9070;
        border: 1px solid rgba(255, 120, 80, 0.4);
    }
    
    .element-earth {
        background: rgba(212, 175, 55, 0.15);
        color: var(--accent-gold);
        border: 1px solid rgba(212, 175, 55, 0.4);
    }
    
    .hash-display {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.7rem;
        color: var(--accent-leaf);
        background: rgba(125, 216, 125, 0.08);
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid rgba(125, 216, 125, 0.2);
        word-break: break-all;
        margin-top: 1rem;
        line-height: 1.6;
    }
    
    .stButton > button {
        background: linear-gradient(
            135deg,
            var(--canopy-deep) 0%,
            var(--canopy-mid) 50%,
            var(--canopy-deep) 100%
        );
        color: var(--text-bright);
        border: 1px solid rgba(125, 216, 125, 0.3);
        padding: 0.9rem 2rem;
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 8px;
        box-shadow: 
            0 4px 20px rgba(77, 139, 77, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        letter-spacing: 0.05em;
    }
    
    .stButton > button:hover {
        background: linear-gradient(
            135deg,
            var(--canopy-mid) 0%,
            var(--canopy-bright) 50%,
            var(--canopy-mid) 100%
        );
        box-shadow: 
            0 6px 30px rgba(125, 216, 125, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.15);
        transform: translateY(-1px);
    }
    
    .talisman-frame {
        background: var(--glass-white);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 
            0 12px 48px rgba(0, 0, 0, 0.5),
            0 0 80px rgba(125, 216, 125, 0.1),
            inset 0 1px 0 var(--glass-highlight);
        margin: 1rem auto;
        max-width: 520px;
    }
    
    .tree-divider {
        height: 2px;
        background: linear-gradient(
            90deg,
            transparent 0%,
            var(--trunk-light) 20%,
            var(--canopy-mid) 50%,
            var(--trunk-light) 80%,
            transparent 100%
        );
        margin: 2.5rem 0;
        opacity: 0.5;
    }
    
    .section-header {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.3rem;
        color: var(--text-mid) !important;
        font-weight: 500;
        margin-bottom: 1rem;
        letter-spacing: 0.03em;
    }
    
    .sidebar-section {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.1rem;
        color: var(--text-mid) !important;
        font-weight: 500;
        margin-bottom: 0.5rem;
        letter-spacing: 0.03em;
    }
    
    .status-indicator {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-excess { background: #ff7050; box-shadow: 0 0 8px #ff7050; }
    .status-balanced { background: var(--accent-leaf); box-shadow: 0 0 8px var(--accent-leaf); }
    .status-deficient { background: #7dc4ff; box-shadow: 0 0 8px #7dc4ff; }
    
    .placeholder-area {
        text-align: center;
        padding: 4rem 2rem;
        color: var(--text-muted);
    }
    
    .placeholder-icon {
        font-size: 3rem;
        margin-bottom: 1.5rem;
        opacity: 0.4;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Hide Streamlit image fullscreen button */
    button[title="View fullscreen"] {
        display: none !important;
    }
    [data-testid="StyledFullScreenButton"] {
        display: none !important;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--roots-deep);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--trunk-mid);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--trunk-light);
    }
    
    /* Input styling */
    .stSelectbox > div > div {
        background: var(--glass-white) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 8px !important;
        color: #ffffff !important;
    }
    
    /* Force white text in all select/dropdown elements */
    .stSelectbox * {
        color: #ffffff !important;
    }
    
    .stSelectbox svg {
        fill: #ffffff !important;
    }
    
    /* Input labels - make them readable */
    .stSelectbox label,
    .stNumberInput label,
    .stTextInput label,
    [data-testid="stWidgetLabel"],
    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] span,
    .stSelectbox [data-testid="stWidgetLabel"] {
        color: #e0f0e0 !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
    }
    
    .stCheckbox label,
    .stCheckbox label span,
    .stCheckbox p {
        color: #e0f0e0 !important;
    }
    
    /* Sidebar text - brighter */
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
        color: #d0e8d0 !important;
    }
    
    [data-testid="stSidebar"] .sidebar-section {
        color: #f0fff0 !important;
    }
    
    /* Selectbox dropdown text - the numbers inside */
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] span,
    [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] > div,
    [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] div[aria-selected],
    .stSelectbox div[data-baseweb="select"] > div > div,
    .stSelectbox [data-baseweb="select"] span,
    [data-baseweb="select"] > div,
    [data-baseweb="select"] span,
    .stSelectbox > div > div > div {
        color: #ffffff !important;
    }
    
    
    /* Dropdown menu items - dark text on light background */
    [data-baseweb="menu"],
    [data-baseweb="menu"] li,
    [data-baseweb="menu"] div,
    [data-baseweb="popover"],
    [data-baseweb="popover"] li,
    [data-baseweb="popover"] div,
    [role="listbox"],
    [role="listbox"] li,
    [role="listbox"] div,
    [role="option"],
    ul[data-testid="stSelectboxVirtualDropdown"] li,
    ul[data-testid="stSelectboxVirtualDropdown"] span {
        color: #1a1a1a !important;
        background-color: #ffffff !important;
    }
    
    /* Dropdown popover styling */
    [data-baseweb="popover"] {
        background: #ffffff !important;
    }
    
    [data-baseweb="popover"] > div {
        background: #ffffff !important;
    }
    
    /* Hover state for dropdown items */
    [data-baseweb="menu"] li:hover,
    [role="option"]:hover,
    [role="listbox"] li:hover {
        background-color: #e0e0e0 !important;
        color: #1a1a1a !important;
    }
    
    /* Selected item in dropdown */
    [aria-selected="true"],
    [data-baseweb="menu"] li[aria-selected="true"] {
        background-color: #4a9f4a !important;
        color: #ffffff !important;
    }
    
    /* ========== MOBILE RESPONSIVE STYLES ========== */
    
    /* Mobile breakpoint: 768px and below */
    @media screen and (max-width: 768px) {
        /* Main container padding */
        .main .block-container {
            padding: 1rem 0.5rem !important;
            max-width: 100% !important;
        }
        
        /* Header adjustments */
        .main-header h1 {
            font-size: 1.8rem !important;
        }
        
        .main-header p {
            font-size: 0.85rem !important;
        }
        
        /* Glass cards - full width on mobile */
        .glass-card {
            padding: 1rem !important;
            margin: 0.5rem 0 !important;
            border-radius: 12px !important;
        }
        
        .glass-card h3 {
            font-size: 1.1rem !important;
        }
        
        /* Metric rows - stack on mobile */
        .metric-row {
            flex-direction: column !important;
            align-items: flex-start !important;
            gap: 0.2rem !important;
            padding: 0.5rem 0 !important;
        }
        
        .metric-label {
            font-size: 0.7rem !important;
        }
        
        .metric-value {
            font-size: 0.9rem !important;
        }
        
        /* Element badges */
        .element-badge {
            padding: 0.2rem 0.5rem !important;
            font-size: 0.75rem !important;
        }
        
        /* Sidebar - better mobile touch targets */
        [data-testid="stSidebar"] {
            min-width: 280px !important;
        }
        
        [data-testid="stSidebar"] .stSelectbox > div > div {
            min-height: 44px !important;
        }
        
        [data-testid="stSidebar"] button {
            min-height: 44px !important;
        }
        
        /* Columns - stack vertically on mobile */
        [data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
        }
        
        /* Image container */
        [data-testid="stImage"] {
            padding: 0 !important;
        }
        
        [data-testid="stImage"] img {
            max-width: 100% !important;
            height: auto !important;
        }
        
        /* Button full width on mobile */
        .stButton > button {
            width: 100% !important;
            min-height: 48px !important;
            font-size: 1rem !important;
        }
        
        /* Download button */
        .stDownloadButton > button {
            width: 100% !important;
            min-height: 48px !important;
        }
        
        /* Hash display - wrap text */
        .hash-display {
            font-size: 0.65rem !important;
            word-break: break-all !important;
        }
        
        /* Reading sections */
        .glass-card > div[style*="grid"] {
            grid-template-columns: 1fr !important;
        }
        
        /* Four pillars - smaller on mobile */
        .metric-value[style*="font-family: var(--font-mono)"] {
            font-size: 0.8rem !important;
            letter-spacing: 0.05em !important;
        }
        
        /* Dividers */
        .tree-divider {
            margin: 1rem 0 !important;
        }
    }
    
    /* Small mobile (iPhone SE, etc) */
    @media screen and (max-width: 375px) {
        .main .block-container {
            padding: 0.5rem 0.25rem !important;
        }
        
        .glass-card {
            padding: 0.8rem !important;
        }
        
        .main-header h1 {
            font-size: 1.5rem !important;
        }
        
        .metric-value {
            font-size: 0.85rem !important;
        }
    }
    
    /* Landscape mobile */
    @media screen and (max-width: 926px) and (orientation: landscape) {
        [data-testid="stSidebar"] {
            max-width: 250px !important;
        }
        
        .glass-card {
            padding: 0.8rem !important;
        }
    }
    
    /* Touch-friendly improvements */
    @media (hover: none) and (pointer: coarse) {
        /* Larger touch targets */
        .stSelectbox > div > div,
        .stCheckbox > label,
        button {
            min-height: 44px !important;
        }
        
        /* Remove hover effects that don't work on touch */
        .glass-card:hover {
            transform: none !important;
        }
    }
    
    </style>
    """, unsafe_allow_html=True)


def render_header():
    """Render the main header."""
    st.markdown('<h1 class="main-title">Qi-Link</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">DePIN Fengshui Node Protocol</p>', unsafe_allow_html=True)
    st.markdown('<div class="tree-divider"></div>', unsafe_allow_html=True)


def get_weather_by_city(city_name: str, location_service):
    """
    Get weather data for a specific city using geocoding.
    Uses Open-Meteo geocoding API (free, no key required).
    """
    import json
    import urllib.request
    import urllib.parse
    
    try:
        # Geocode the city name
        encoded_city = urllib.parse.quote(city_name)
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={encoded_city}&count=1&language=en&format=json"
        
        req = urllib.request.Request(geo_url, headers={"User-Agent": "Qi-Link/1.0"})
        
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            results = data.get("results", [])
            
            if results:
                result = results[0]
                # Create location data from geocoding result
                from qi_link.location_service import LocationData
                location = LocationData(
                    city=result.get("name", city_name),
                    region=result.get("admin1", ""),
                    country=result.get("country", ""),
                    latitude=result.get("latitude", 0.0),
                    longitude=result.get("longitude", 0.0),
                    timezone=result.get("timezone", "UTC"),
                    ip_address="manual",
                )
                
                # Get weather for this location
                weather = location_service.get_weather(location)
                return location, weather
                
    except Exception:
        pass
    
    # Fallback to IP-based location
    env_data = location_service.get_all_environmental_data()
    return env_data["location"], env_data["weather"]


def render_sidebar():
    """Render sidebar with birth data input and node status."""
    with st.sidebar:
        st.markdown('<p class="sidebar-section">Birth Data</p>', unsafe_allow_html=True)
        st.markdown("---")
        
        # Minimal date selector
        current_year = date.today().year
        default_year = current_year - 30  # Assume average user ~30 years old
        
        birth_year = st.selectbox("Year", range(current_year, 1919, -1), index=current_year - default_year)
        birth_month = st.selectbox("Month", range(1, 13), index=0)
        
        # Days based on month
        max_days = 31 if birth_month in [1,3,5,7,8,10,12] else 30 if birth_month in [4,6,9,11] else 29 if (birth_year % 4 == 0 and birth_year % 100 != 0) or (birth_year % 400 == 0) else 28
        birth_day = st.selectbox("Day", range(1, max_days + 1), index=0)
        
        birth_date = date(birth_year, birth_month, birth_day)
        
        # Option for unknown birth time
        time_unknown = st.checkbox("I don't know exact birth time", value=False)
        
        # Chinese double-hour periods (時辰)
        shichen_options = {
            "子時 Zi (23:00-01:00) Water": 0,
            "丑時 Chou (01:00-03:00) Earth": 2,
            "寅時 Yin (03:00-05:00) Wood": 4,
            "卯時 Mao (05:00-07:00) Wood": 6,
            "辰時 Chen (07:00-09:00) Earth": 8,
            "巳時 Si (09:00-11:00) Fire": 10,
            "午時 Wu (11:00-13:00) Fire": 12,
            "未時 Wei (13:00-15:00) Earth": 14,
            "申時 Shen (15:00-17:00) Metal": 16,
            "酉時 You (17:00-19:00) Metal": 18,
            "戌時 Xu (19:00-21:00) Earth": 20,
            "亥時 Hai (21:00-23:00) Water": 22,
        }
        
        if time_unknown:
            # Use noon as default when time is unknown
            birth_hour = 12
            birth_minute = 0
            st.markdown("""
            <div style="background: rgba(212, 175, 55, 0.15); border: 1px solid rgba(212, 175, 55, 0.4); 
                        border-radius: 8px; padding: 0.8rem; margin: 0.5rem 0; font-size: 0.85rem;
                        color: #e8d8a8;">
                <strong style="color: #ffd700;">Note:</strong> Using Wu period (noon) as default. 
                Reading focuses on Year, Month, Day pillars.
            </div>
            """, unsafe_allow_html=True)
        else:
            selected_shichen = st.selectbox(
                "Birth Time Period (時辰)",
                options=list(shichen_options.keys()),
                index=6  # Default to Wu (noon)
            )
            birth_hour = shichen_options[selected_shichen]
            birth_minute = 0
            
            st.markdown("""
            <div style="font-size: 0.75rem; color: #a8c8a8; margin-top: 0.3rem;">
                In Chinese astrology, time is measured in 2-hour periods (時辰), not exact minutes.
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown('<p class="sidebar-section">Settings</p>', unsafe_allow_html=True)
        mock_mode = st.checkbox("Mock Mode", value=True)
        
        st.markdown("---")
        st.markdown('<p class="sidebar-section">Node Status</p>', unsafe_allow_html=True)
        
        sensor = SensorArray()
        metrics = sensor.get_live_metrics()
        
        st.markdown(f"""
        <div class="glass-card">
            <div class="metric-row">
                <span class="metric-label">CPU Usage</span>
                <span class="metric-value">{metrics['cpu_percent']:.1f}%</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Memory</span>
                <span class="metric-value">{metrics['memory_percent']:.1f}%</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Disk</span>
                <span class="metric-value">{metrics['disk_percent']:.1f}%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Real-world environment data
        st.markdown("---")
        st.markdown('<p class="sidebar-section">Real Environment</p>', unsafe_allow_html=True)
        
        # Manual location input for accuracy
        user_city = st.text_input(
            "Your City (for accurate weather)",
            value="",
            placeholder="e.g. Tokyo, London, New York",
            help="IP-based location may be inaccurate. Enter your city for precise weather data."
        )
        
        location_service = LocationService()
        
        # Use manual city if provided, otherwise fall back to IP detection
        if user_city.strip():
            # Try to geocode the city
            location, weather = get_weather_by_city(user_city.strip(), location_service)
        else:
            env_data = location_service.get_all_environmental_data()
            location = env_data["location"]
            weather = env_data["weather"]
        
        # Auto-detect direction from wind direction
        compass = location_service.get_compass_direction(weather.wind_direction_degrees if weather else None)
        
        # Store in session state for use in main content
        st.session_state.real_env = {
            "location": location,
            "weather": weather,
            "compass": compass,
            "temperature": weather.temperature_celsius if weather else 20,
            "weather_condition": weather.weather_condition if weather else "Unknown",
            "wind_direction": compass.cardinal_direction if compass else "North",
        }
        
        location_str = f"{location.city}, {location.country}" if location and location.city != "Unknown" else "Enter city above"
        
        st.markdown(f"""
        <div class="glass-card">
            <div class="metric-row">
                <span class="metric-label">Location</span>
                <span class="metric-value">{location_str}</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Temperature</span>
                <span class="metric-value">{weather.temperature_celsius:.1f}C (feels {weather.feels_like_celsius:.1f}C)</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Humidity</span>
                <span class="metric-value">{weather.humidity_percent}%</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Weather</span>
                <span class="metric-value">{weather.weather_condition}</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Wind</span>
                <span class="metric-value">{weather.wind_speed_kmh:.0f} km/h from {compass.cardinal_direction}</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Qi Flow Direction</span>
                <span class="metric-value">{compass.cardinal_direction} ({compass.chinese_direction}) = {compass.element.title()}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        return datetime(birth_date.year, birth_date.month, birth_date.day, birth_hour, birth_minute), mock_mode, time_unknown


def render_element_badge(element: Element) -> str:
    """Render an element badge with appropriate styling."""
    return f'<span class="element-badge element-{element.value}">{element.chinese} {element.value.title()}</span>'


def render_energy_indicator(state: EnergyState) -> str:
    """Render energy state indicator."""
    css_class = f"status-{state.value}"
    return f'<span class="status-indicator {css_class}"></span>{state.value.title()}'


def render_environment_card(env):
    """Render environment readings card with both machine and real-world data."""
    # Get real environment data from session state if available
    real_env = getattr(st.session_state, 'real_env', None)
    
    # Build HTML rows as a list
    rows = []
    
    # CPU Temperature (machine)
    rows.append(f'<div class="metric-row"><span class="metric-label">CPU Temperature</span><span class="metric-value">{env.cpu_temperature:.1f}C | {render_energy_indicator(env.temperature_state)}</span></div>')
    
    # Real ambient temperature and humidity
    if real_env:
        weather = real_env.get("weather")
        if weather:
            rows.append(f'<div class="metric-row"><span class="metric-label">Ambient Temperature</span><span class="metric-value">{weather.temperature_celsius:.1f}C ({weather.weather_condition})</span></div>')
            rows.append(f'<div class="metric-row"><span class="metric-label">Humidity</span><span class="metric-value">{weather.humidity_percent}%</span></div>')
    
    # Network latency
    rows.append(f'<div class="metric-row"><span class="metric-label">Network Latency</span><span class="metric-value">{env.network_latency_ms:.1f}ms | {render_energy_indicator(env.qi_flow_state)}</span></div>')
    
    # Qi Flow direction (from wind)
    if real_env:
        compass = real_env.get("compass")
        if compass:
            rows.append(f'<div class="metric-row"><span class="metric-label">Qi Flow (Wind)</span><span class="metric-value">{compass.cardinal_direction} ({compass.chinese_direction}) | {compass.element.title()} energy</span></div>')
    
    # Entropy and dominant element
    rows.append(f'<div class="metric-row"><span class="metric-label">Entropy Score</span><span class="metric-value">{env.entropy_score}/100</span></div>')
    rows.append(f'<div class="metric-row"><span class="metric-label">Dominant Element</span><span class="metric-value">{render_element_badge(env.dominant_environment_element)}</span></div>')
    
    # Join all rows
    rows_html = "".join(rows)
    
    st.markdown(f'<div class="glass-card"><h3>Environment Scan</h3>{rows_html}</div>', unsafe_allow_html=True)


def get_palace_english(palace: str) -> str:
    """Get English translation for palace name."""
    translations = {
        "命宮": "Life Palace",
        "兄弟宮": "Siblings Palace",
        "夫妻宮": "Marriage Palace",
        "子女宮": "Children Palace",
        "財帛宮": "Wealth Palace",
        "疾厄宮": "Health Palace",
        "遷移宮": "Travel Palace",
        "交友宮": "Friends Palace",
        "官祿宮": "Career Palace",
        "田宅宮": "Property Palace",
        "福德宮": "Fortune Palace",
        "父母宮": "Parents Palace",
    }
    return translations.get(palace, palace)


# Powerful fate readings - short, emotionally resonant
STAR_FATE_READINGS = {
    "紫微": {
        "core": "You were born to lead, not to follow.",
        "truth": "Others sense your authority before you speak. You carry weight in rooms you enter.",
        "shadow": "Loneliness at the top is your familiar companion.",
        "gift": "Your presence alone can change the energy of any situation.",
    },
    "天機": {
        "core": "Your mind never rests - this is both your power and your curse.",
        "truth": "You see ten moves ahead while others see one. This makes you feel alone.",
        "shadow": "You overthink until paralysis. Learn when to stop analyzing.",
        "gift": "Solutions come to you that others cannot imagine.",
    },
    "太陽": {
        "core": "You give warmth to everyone, but who warms you?",
        "truth": "People are drawn to your light. You make others feel seen.",
        "shadow": "You hide your darkness well. Too well.",
        "gift": "Your generosity will return to you tenfold. But not yet.",
    },
    "武曲": {
        "core": "You measure life in achievements. Stillness feels like failure.",
        "truth": "Money comes to you, but satisfaction always seems one goal away.",
        "shadow": "You've forgotten how to rest without guilt.",
        "gift": "What you build will outlast you. That is your legacy.",
    },
    "天同": {
        "core": "You feel everything deeply - joy and pain alike.",
        "truth": "Conflict exhausts you. You absorb others' emotions like a sponge.",
        "shadow": "Avoiding hard truths keeps you comfortable but stuck.",
        "gift": "Your gentleness heals people who have forgotten softness exists.",
    },
    "廉貞": {
        "core": "You love and hate with equal intensity. There is no middle ground.",
        "truth": "People either adore you or fear you. Rarely anything between.",
        "shadow": "Your fire can burn those closest to you. You know this.",
        "gift": "Your passion transforms everything it touches.",
    },
    "天府": {
        "core": "Security is your deepest need - emotional and material.",
        "truth": "You build walls to protect what you treasure. Sometimes too high.",
        "shadow": "Fear of loss keeps you holding on to what should be released.",
        "gift": "What you protect flourishes. You are a shelter in storms.",
    },
    "太陰": {
        "core": "You see what others hide. This knowing is heavy to carry.",
        "truth": "Your intuition speaks louder than logic. Trust it more.",
        "shadow": "You reveal yourself to few. Perhaps too few.",
        "gift": "In darkness you find treasures others walk past.",
    },
    "貪狼": {
        "core": "You want everything - and why shouldn't you?",
        "truth": "Boredom is your enemy. Routine slowly kills you.",
        "shadow": "Starting is easy. Finishing is where you struggle.",
        "gift": "Your appetite for life is contagious. You make existence exciting.",
    },
    "巨門": {
        "core": "Your words can heal or wound. Choose carefully.",
        "truth": "You question everything - including yourself. Too harshly sometimes.",
        "shadow": "Suspicion protects you but also isolates you.",
        "gift": "You speak truths others are afraid to voice.",
    },
    "天相": {
        "core": "You live for others. But who lives for you?",
        "truth": "You smooth conflicts others cannot resolve. It costs you.",
        "shadow": "You lose yourself in serving. Remember who you were before.",
        "gift": "Without you, things fall apart. You are the bridge.",
    },
    "天梁": {
        "core": "You carry wisdom older than your years.",
        "truth": "People bring you their problems. You cannot refuse.",
        "shadow": "You protect others from growth by solving too much for them.",
        "gift": "Your calm presence alone is medicine for troubled souls.",
    },
    "七殺": {
        "core": "You were not made for gentle paths.",
        "truth": "Obstacles that stop others are fuel for you.",
        "shadow": "Not every wall needs breaking. Some doors just need opening.",
        "gift": "Your courage makes impossible things possible.",
    },
    "破軍": {
        "core": "You destroy to rebuild. This is your nature.",
        "truth": "Change follows you like a shadow. You cannot escape it.",
        "shadow": "What you tear down, you must be willing to reconstruct.",
        "gift": "New worlds are born from your destruction.",
    },
}


# Star name translations (Chinese -> English with Pinyin)
STAR_ENGLISH = {
    "紫微": "Zi Wei (Emperor)",
    "天機": "Tian Ji (Strategist)",
    "太陽": "Tai Yang (Sun)",
    "武曲": "Wu Qu (Warrior)",
    "天同": "Tian Tong (Harmony)",
    "廉貞": "Lian Zhen (Passion)",
    "天府": "Tian Fu (Treasury)",
    "太陰": "Tai Yin (Moon)",
    "貪狼": "Tan Lang (Desire)",
    "巨門": "Ju Men (Gate)",
    "天相": "Tian Xiang (Minister)",
    "天梁": "Tian Liang (Beam)",
    "七殺": "Qi Sha (Killer)",
    "破軍": "Po Jun (Breaker)",
}

# Branch translations
BRANCH_ENGLISH = {
    "子": "Zi (Rat)", "丑": "Chou (Ox)", "寅": "Yin (Tiger)", "卯": "Mao (Rabbit)",
    "辰": "Chen (Dragon)", "巳": "Si (Snake)", "午": "Wu (Horse)", "未": "Wei (Goat)",
    "申": "Shen (Monkey)", "酉": "You (Rooster)", "戌": "Xu (Dog)", "亥": "Hai (Pig)",
}

# Bureau translations
BUREAU_ENGLISH = {
    "水二局": "Water-2 Bureau",
    "木三局": "Wood-3 Bureau",
    "金四局": "Metal-4 Bureau",
    "土五局": "Earth-5 Bureau",
    "火六局": "Fire-6 Bureau",
}

# Si Hua translations
SI_HUA_ENGLISH = {
    "化祿": "Lu (Fortune)",
    "化權": "Quan (Power)",
    "化科": "Ke (Fame)",
    "化忌": "Ji (Obstacle)",
}

def render_fate_card(fate, engine: FateEngine):
    """Render fate profile card with powerful personal reading - English version."""
    extra = getattr(fate, 'extra_data', None) or {}
    
    # Get all stars in life palace - translate to English
    all_stars = extra.get("all_major_stars", [])
    if all_stars:
        stars_en = [STAR_ENGLISH.get(s, s) for s in all_stars]
        stars_display = " + ".join(stars_en)
    else:
        stars_display = STAR_ENGLISH.get(fate.major_star.value, fate.major_star.value)
    
    # Get star info for primary star
    star_info = engine.get_star_description(fate.major_star, extra)
    star_key = all_stars[0] if all_stars else fate.major_star.value
    reading = STAR_FATE_READINGS.get(star_key, STAR_FATE_READINGS["紫微"])
    
    # Translate Wu Xing Ju and positions
    wu_xing_ju = extra.get("wu_xing_ju", "")
    wu_xing_ju_en = BUREAU_ENGLISH.get(wu_xing_ju, wu_xing_ju)
    
    life_palace_branch = extra.get("life_palace_branch", "")
    life_palace_en = BRANCH_ENGLISH.get(life_palace_branch, life_palace_branch)
    
    zi_wei_pos = extra.get("zi_wei_position", "")
    tian_fu_pos = extra.get("tian_fu_position", "")
    zi_wei_en = BRANCH_ENGLISH.get(zi_wei_pos, zi_wei_pos)
    tian_fu_en = BRANCH_ENGLISH.get(tian_fu_pos, tian_fu_pos)
    
    # Si Hua (Four Transformations) - translate to English
    si_hua = extra.get("si_hua", {})
    si_hua_in_life = extra.get("si_hua_in_life", {})
    
    # Build Si Hua display in English
    si_hua_parts = []
    for hua_cn, hua_en in SI_HUA_ENGLISH.items():
        star_name = si_hua.get(hua_cn, "")
        if star_name:
            star_en = STAR_ENGLISH.get(star_name, star_name).split(" (")[0]  # Just pinyin
            if star_name in all_stars:
                color = "#ff6b6b" if hua_cn == "化忌" else "var(--accent-gold)"
                si_hua_parts.append(f'<span style="color: {color}; font-weight: 600;">{star_en} {hua_en}</span>')
            else:
                si_hua_parts.append(f'{star_en} {hua_en}')
    si_hua_display = " | ".join(si_hua_parts) if si_hua_parts else ""
    
    # Check if birth time was unknown
    time_unknown = getattr(st.session_state, 'time_unknown', False)
    hour_pillar_display = fate.hour_stem_branch
    if time_unknown:
        hour_pillar_display = f'<span style="opacity: 0.5;">{fate.hour_stem_branch}*</span>'
    
    uncertainty_note = ""
    if time_unknown:
        uncertainty_note = '<div style="margin-top: 0.8rem; padding: 0.6rem; background: rgba(212, 175, 55, 0.1); border-radius: 6px; font-size: 0.75rem; color: var(--accent-gold);">* Hour pillar estimated (noon default).</div>'
    
    # Si Hua warning/blessing for life palace - English
    si_hua_note = ""
    for hua_cn, star_name in si_hua_in_life.items():
        star_en = STAR_ENGLISH.get(star_name, star_name).split(" (")[0]
        hua_en = SI_HUA_ENGLISH.get(hua_cn, hua_cn)
        if hua_cn == "化忌":
            si_hua_note += f'<div style="margin-top: 0.8rem; padding: 0.6rem; background: rgba(255, 100, 100, 0.1); border-radius: 6px; font-size: 0.8rem; color: #ff8a80;"><strong>{star_en} {hua_en} in Life</strong> - Your karmic lesson. Obstacles here forge your strength.</div>'
        elif hua_cn == "化祿":
            si_hua_note += f'<div style="margin-top: 0.8rem; padding: 0.6rem; background: rgba(100, 200, 100, 0.1); border-radius: 6px; font-size: 0.8rem; color: var(--accent-leaf);"><strong>{star_en} {hua_en} in Life</strong> - Fortune flows to you naturally here.</div>'
    
    # Star positions info (compact)
    positions_note = ""
    if zi_wei_pos and tian_fu_pos:
        positions_note = f'<div style="margin-top: 0.5rem; font-size: 0.75rem; color: var(--text-muted);">Zi Wei in {zi_wei_en} | Tian Fu in {tian_fu_en}</div>'
    
    st.markdown(f'''<div class="glass-card">
<h3>Fate Analysis</h3>
<div class="metric-row">
<span class="metric-label">Major Stars</span>
<span class="metric-value" style="color: var(--accent-gold); font-weight: 600;">{stars_display}</span>
</div>
<div class="metric-row">
<span class="metric-label">Life Palace</span>
<span class="metric-value">{life_palace_en}</span>
</div>
<div class="metric-row">
<span class="metric-label">Bureau</span>
<span class="metric-value">{wu_xing_ju_en}</span>
</div>
<div class="metric-row">
<span class="metric-label">Year Transformations</span>
<span class="metric-value" style="font-size: 0.85rem;">{si_hua_display if si_hua_display else "N/A"}</span>
</div>
<div class="metric-row">
<span class="metric-label">Day Master</span>
<span class="metric-value">{render_element_badge(fate.inherent_element)}</span>
</div>
{positions_note}
<div style="margin-top: 1.5rem; padding: 1.2rem; background: linear-gradient(135deg, rgba(212, 175, 55, 0.1), rgba(124, 179, 66, 0.05)); border-radius: 8px; border-left: 3px solid var(--accent-gold);">
<p style="color: var(--accent-gold); font-size: 1.1rem; font-weight: 600; margin-bottom: 0.8rem; line-height: 1.4;">"{reading['core']}"</p>
<p style="color: var(--text-bright); font-size: 0.9rem; line-height: 1.6; margin-bottom: 0.6rem;">{reading['truth']}</p>
<p style="color: var(--text-muted); font-size: 0.85rem; line-height: 1.5; font-style: italic;">{reading['shadow']}</p>
</div>
<div style="margin-top: 1rem; padding: 0.8rem; background: rgba(124, 179, 66, 0.1); border-radius: 6px;">
<p style="color: var(--accent-leaf); font-size: 0.9rem; line-height: 1.5;"><strong>Your Gift:</strong> {reading['gift']}</p>
</div>
{si_hua_note}
{uncertainty_note}
</div>''', unsafe_allow_html=True)


# Detailed personality descriptions for each Major Star
STAR_PERSONALITIES = {
    "紫微": {
        "title": "The Emperor",
        "summary": "You carry the energy of leadership and authority.",
        "traits": ["Natural leader", "High standards", "Dignified presence", "Protective of loved ones"],
        "strengths": "You command respect without demanding it. People naturally look to you for guidance and direction.",
        "challenges": "You may struggle with delegation and trusting others to handle important matters.",
        "advice": "Learn to share power. Your greatest legacy will be the leaders you nurture, not the battles you win alone."
    },
    "天機": {
        "title": "The Strategist",
        "summary": "Your mind sees patterns others miss.",
        "traits": ["Quick thinking", "Adaptable", "Analytical", "Curious"],
        "strengths": "You excel at solving complex problems and adapting to change. Your mental agility is your greatest asset.",
        "challenges": "Overthinking can lead to anxiety. You may struggle with decisions when logic alone cannot guide you.",
        "advice": "Trust your intuition alongside your intellect. Not everything needs to be figured out before you act."
    },
    "太陽": {
        "title": "The Radiant One",
        "summary": "You shine brightest when lifting others up.",
        "traits": ["Generous", "Optimistic", "Public-facing", "Warm-hearted"],
        "strengths": "Your presence brings warmth and light to any room. You inspire others and give selflessly.",
        "challenges": "You may burn out by giving too much. Learning to receive is as important as giving.",
        "advice": "Even the sun sets. Allow yourself rest and restoration. Your light serves no one if it burns out."
    },
    "武曲": {
        "title": "The Warrior",
        "summary": "Discipline and determination define your path.",
        "traits": ["Disciplined", "Wealth-oriented", "Direct", "Resilient"],
        "strengths": "You have an innate ability to create financial security and achieve material goals through hard work.",
        "challenges": "You may appear cold or overly focused on practical matters. Emotions might feel like obstacles.",
        "advice": "Strength includes vulnerability. The greatest warriors know when to lower their guard with those they trust."
    },
    "天同": {
        "title": "The Harmonizer",
        "summary": "You seek peace and find joy in simple pleasures.",
        "traits": ["Easy-going", "Pleasure-seeking", "Emotionally aware", "Supportive"],
        "strengths": "You bring harmony to chaotic situations and help others feel at ease. Life feels lighter around you.",
        "challenges": "Avoiding conflict at all costs may lead to suppressed needs. Comfort-seeking can become complacency.",
        "advice": "Healthy conflict leads to growth. Your gift for harmony is needed most in difficult conversations, not avoided ones."
    },
    "廉貞": {
        "title": "The Transformer",
        "summary": "Passion and complexity drive your soul.",
        "traits": ["Intense", "Passionate", "Complex", "Magnetic"],
        "strengths": "You feel deeply and live fully. Your intensity draws people in and drives meaningful transformation.",
        "challenges": "Your emotions run deep, which can lead to jealousy or obsession. You may struggle with letting go.",
        "advice": "Channel your fire wisely. Transformation requires both destruction and creation - know when each is needed."
    },
    "天府": {
        "title": "The Treasurer",
        "summary": "Stability and abundance flow naturally to you.",
        "traits": ["Stable", "Resourceful", "Content", "Reliable"],
        "strengths": "You create security wherever you go. Resources, both material and emotional, gather around you.",
        "challenges": "Contentment can become stagnation. You may resist change even when it serves your growth.",
        "advice": "Security is a foundation, not a ceiling. Use your stability as a launch pad, not a hiding place."
    },
    "太陰": {
        "title": "The Mystic",
        "summary": "Your power lies in what remains unseen.",
        "traits": ["Intuitive", "Mysterious", "Emotionally deep", "Receptive"],
        "strengths": "You perceive what others cannot. Your intuition guides you through darkness where logic fails.",
        "challenges": "You may hide your true self or struggle with mood fluctuations. Hidden fears can control you.",
        "advice": "Embrace your depth without drowning in it. The moon reflects light - find your sun to shine with."
    },
    "貪狼": {
        "title": "The Seeker",
        "summary": "Desire drives you toward endless discovery.",
        "traits": ["Charismatic", "Versatile", "Desire-driven", "Artistic"],
        "strengths": "Your hunger for experience makes you dynamic and interesting. You excel in multiple fields.",
        "challenges": "Scattered focus and insatiable desires may prevent deep mastery or lasting satisfaction.",
        "advice": "Depth over breadth. Choose what truly matters and pursue it fully. One mastered skill outweighs ten sampled."
    },
    "巨門": {
        "title": "The Truth-Seeker",
        "summary": "Your words cut through illusion to find reality.",
        "traits": ["Analytical", "Direct communicator", "Skeptical", "Investigative"],
        "strengths": "You see through pretense and speak uncomfortable truths. Your analysis is sharp and thorough.",
        "challenges": "Your directness can wound. Skepticism may prevent you from trusting genuine connections.",
        "advice": "Truth without compassion is cruelty. Deliver your insights with care - the goal is illumination, not destruction."
    },
    "天相": {
        "title": "The Diplomat",
        "summary": "Balance and service guide your purpose.",
        "traits": ["Diplomatic", "Service-oriented", "Fair-minded", "Supportive"],
        "strengths": "You excel at bringing opposing forces together. Your sense of fairness earns universal trust.",
        "challenges": "Serving others may come at the expense of your own needs. You may lose yourself in roles.",
        "advice": "Self-care is not selfish. A depleted diplomat serves no one. Fill your cup before pouring for others."
    },
    "天梁": {
        "title": "The Protector",
        "summary": "Wisdom and shelter radiate from your presence.",
        "traits": ["Wise", "Protective", "Mature", "Long-lived"],
        "strengths": "You naturally shield others from harm. Your wisdom comes from deep observation and experience.",
        "challenges": "You may carry others' burdens too readily. Over-protection can prevent necessary growth.",
        "advice": "Let others struggle sometimes. The best protection includes teaching resilience, not just providing shelter."
    },
    "七殺": {
        "title": "The Conqueror",
        "summary": "Power and courage forge your destiny.",
        "traits": ["Powerful", "Courageous", "Commanding", "Breakthrough-oriented"],
        "strengths": "You break through obstacles that stop others. Your courage inspires and your power transforms.",
        "challenges": "Aggression without wisdom creates enemies. Power without purpose becomes destruction.",
        "advice": "Choose your battles wisely. Not every wall needs breaking - some doors simply need to be opened."
    },
    "破軍": {
        "title": "The Pioneer",
        "summary": "You destroy the old to birth the new.",
        "traits": ["Revolutionary", "Restless", "Pioneering", "Change-agent"],
        "strengths": "You break stagnant patterns and create space for new possibilities. Change flows through you.",
        "challenges": "Constant upheaval exhausts you and others. Destruction without vision leaves only rubble.",
        "advice": "Build as much as you break. The greatest pioneers leave gardens, not battlefields, in their wake."
    },
}

# Lucky numbers associated with elements
ELEMENT_LUCKY_NUMBERS = {
    Element.WATER: [1, 6],
    Element.WOOD: [3, 8],
    Element.FIRE: [2, 7],
    Element.EARTH: [5, 10],
    Element.METAL: [4, 9],
}

ELEMENT_DATA = {
    Element.WATER: {
        "colors": ["Black", "Blue", "Navy", "Dark Gray"],
        "directions": ["North"],
        "activities": ["Meditation", "Swimming", "Reading", "Rest", "Journaling"],
        "items": ["Fountains", "Aquariums", "Mirrors", "Glass items"],
        "foods": ["Soups", "Seafood", "Dark foods", "Salty dishes"],
        "time": "Night (9pm-1am)",
    },
    Element.WOOD: {
        "colors": ["Green", "Teal", "Cyan", "Turquoise"],
        "directions": ["East", "Southeast"],
        "activities": ["Exercise", "Learning", "Gardening", "Walking in nature", "Starting new projects"],
        "items": ["Plants", "Wooden furniture", "Books", "Paper items"],
        "foods": ["Leafy greens", "Sour foods", "Sprouts", "Herbal tea"],
        "time": "Morning (5am-9am)",
    },
    Element.FIRE: {
        "colors": ["Red", "Orange", "Pink", "Purple"],
        "directions": ["South"],
        "activities": ["Socializing", "Sports", "Creative work", "Public speaking", "Networking"],
        "items": ["Candles", "Lights", "Electronics", "Art"],
        "foods": ["Spicy food", "BBQ", "Red foods", "Coffee"],
        "time": "Midday (11am-1pm)",
    },
    Element.EARTH: {
        "colors": ["Yellow", "Brown", "Beige", "Terracotta"],
        "directions": ["Center", "Southwest", "Northeast"],
        "activities": ["Cooking", "Pottery", "Home organizing", "Family time", "Grounding walks"],
        "items": ["Ceramics", "Stones", "Crystals", "Clay pots"],
        "foods": ["Root vegetables", "Grains", "Sweet foods", "Comfort food"],
        "time": "Afternoon transitions (7-9am, 1-3pm, 7-9pm)",
    },
    Element.METAL: {
        "colors": ["White", "Gold", "Silver", "Metallic Gray"],
        "directions": ["West", "Northwest"],
        "activities": ["Organizing", "Planning", "Decluttering", "Financial review", "Precision work"],
        "items": ["Metal objects", "Coins", "Jewelry", "Wind chimes"],
        "foods": ["White foods", "Pungent/spicy", "Rice", "Onions"],
        "time": "Evening (5pm-9pm)",
    },
}


def render_personality_card(fate):
    """Render detailed personality analysis based on Major Star."""
    star_key = fate.major_star.value
    personality = STAR_PERSONALITIES.get(star_key, STAR_PERSONALITIES["紫微"])
    
    traits_html = " ".join([f'<span style="display: inline-block; background: rgba(124, 179, 66, 0.15); color: var(--accent-leaf); padding: 0.25rem 0.6rem; border-radius: 4px; font-size: 0.75rem; margin: 0.15rem;">{t}</span>' for t in personality["traits"]])
    
    st.markdown(f'''<div class="glass-card">
<h3>Your Personality</h3>
<div style="text-align: center; margin: 1rem 0;">
<p style="color: var(--accent-gold); font-size: 1.1rem; font-weight: 600; letter-spacing: 0.05em;">{personality["title"]}</p>
<p style="color: var(--text-bright); font-size: 0.95rem; font-style: italic; margin-top: 0.5rem;">{personality["summary"]}</p>
</div>
<div style="margin: 1rem 0;">{traits_html}</div>
<div style="margin-top: 1.2rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.06);">
<p style="color: var(--text-muted); font-size: 0.85rem; line-height: 1.6; margin-bottom: 0.8rem;"><span style="color: var(--accent-leaf);">Strengths:</span> {personality["strengths"]}</p>
<p style="color: var(--text-muted); font-size: 0.85rem; line-height: 1.6; margin-bottom: 0.8rem;"><span style="color: #ff8a80;">Challenges:</span> {personality["challenges"]}</p>
<p style="color: var(--text-bright); font-size: 0.9rem; line-height: 1.6; background: rgba(212, 175, 55, 0.1); padding: 0.8rem; border-radius: 6px; border-left: 3px solid var(--accent-gold);"><span style="color: var(--accent-gold);">Advice:</span> {personality["advice"]}</p>
</div>
</div>''', unsafe_allow_html=True)


def render_daily_fortune(diagnosis, env_data: dict = None):
    """Render personalized daily fortune message."""
    fate = diagnosis.fate_profile
    
    # Build messages based on environment
    temp_msg = "Moderate temperatures bring balance to your elemental flow."
    weather_msg = ""
    wind_msg = ""
    
    if env_data:
        temp = env_data.get("temperature", 20)
        weather = env_data.get("weather_condition", "")
        wind_dir = env_data.get("wind_direction", "")
        
        if temp is not None:
            if temp < 5:
                temp_msg = "The cold today deepens Water energy - a time for reflection and inner work."
            elif temp > 28:
                temp_msg = "Heat amplifies Fire energy - passion runs high but patience runs thin."
        
        if weather:
            wl = weather.lower()
            if "rain" in wl or "drizzle" in wl:
                weather_msg = "Rain nourishes Wood and strengthens Water - growth emerges from quiet contemplation."
            elif "clear" in wl or "sunny" in wl:
                weather_msg = "Clear skies enhance Metal clarity and Fire visibility - good for decisions."
            elif "cloud" in wl or "overcast" in wl:
                weather_msg = "Clouds soften harsh energies - a gentle day for healing."
            elif "snow" in wl:
                weather_msg = "Snow brings pure Water energy - cleanse old patterns."
        
        if wind_dir:
            wd = wind_dir.lower()
            if "east" in wd:
                wind_msg = "East wind carries Wood energy - new beginnings are favored."
            elif "south" in wd:
                wind_msg = "South wind brings Fire energy - social connections flourish."
            elif "west" in wd:
                wind_msg = "West wind channels Metal energy - completion is supported."
            elif "north" in wd:
                wind_msg = "North wind flows with Water energy - wisdom comes through stillness."
    
    st.markdown(f'''<div class="glass-card">
<h3>Today\'s Insight</h3>
<div style="line-height: 1.8; color: var(--text-muted); font-size: 0.9rem;">
<p style="margin-bottom: 0.8rem;">{temp_msg}</p>
{f'<p style="margin-bottom: 0.8rem;">{weather_msg}</p>' if weather_msg else ''}
{f'<p style="color: var(--text-bright);">{wind_msg}</p>' if wind_msg else ''}
</div>
</div>''', unsafe_allow_html=True)


def render_lucky_section(diagnosis):
    """Render lucky color, number, and direction."""
    fate = diagnosis.fate_profile
    remedy = diagnosis.remedy_elements
    
    primary = remedy[0] if remedy else fate.inherent_element
    
    colors = ELEMENT_DATA.get(primary, ELEMENT_DATA[Element.EARTH])["colors"][:2]
    numbers = ELEMENT_LUCKY_NUMBERS.get(primary, [5, 10])
    directions = ELEMENT_DATA.get(primary, ELEMENT_DATA[Element.EARTH])["directions"]
    
    times = {
        Element.WATER: "9pm - 1am",
        Element.WOOD: "5am - 9am", 
        Element.FIRE: "11am - 1pm",
        Element.EARTH: "1pm - 3pm",
        Element.METAL: "5pm - 7pm",
    }
    lucky_time = times.get(primary, "Anytime")
    
    avoid_map = {
        Element.WATER: "Fire activities, arguments",
        Element.WOOD: "Metal objects, cutting decisions",
        Element.FIRE: "Water activities, cold environments",
        Element.EARTH: "Wood energy, chaotic changes",
        Element.METAL: "Fire situations, impulsive actions",
    }
    avoid = avoid_map.get(fate.inherent_element, "Overexertion")
    
    st.markdown(f'''<div class="glass-card">
<h3>Lucky Guide</h3>
<div class="metric-row">
<span class="metric-label">Lucky Colors</span>
<span class="metric-value">{", ".join(colors)}</span>
</div>
<div class="metric-row">
<span class="metric-label">Lucky Numbers</span>
<span class="metric-value">{", ".join(map(str, numbers))}</span>
</div>
<div class="metric-row">
<span class="metric-label">Lucky Direction</span>
<span class="metric-value">{", ".join(directions)}</span>
</div>
<div class="metric-row">
<span class="metric-label">Optimal Time</span>
<span class="metric-value">{lucky_time}</span>
</div>
<div style="margin-top: 1rem; padding: 0.6rem; background: rgba(255, 100, 100, 0.1); border-radius: 6px;">
<p style="color: #ff8a80; font-size: 0.8rem;"><span style="font-weight: 600;">Avoid today:</span> {avoid}</p>
</div>
</div>''', unsafe_allow_html=True)


def get_personalized_advice(diagnosis, env_data: dict = None) -> dict:
    """Generate personalized advice based on ALL factors."""
    import random
    
    remedy_elements = diagnosis.remedy_elements
    user_element = diagnosis.fate_profile.inherent_element
    
    # Combine advice from all remedy elements with weights
    all_colors = []
    all_directions = []
    all_activities = []
    all_items = []
    all_foods = []
    all_times = []
    
    for elem in remedy_elements:
        data = ELEMENT_DATA.get(elem, ELEMENT_DATA[Element.EARTH])
        all_colors.extend(data["colors"][:2])  # Top 2 from each
        all_directions.extend(data["directions"])
        all_activities.extend(data["activities"][:2])
        all_items.extend(data["items"][:2])
        all_foods.extend(data["foods"][:2])
        all_times.append(data["time"])
    
    # Remove duplicates while preserving order
    def unique(lst):
        seen = set()
        return [x for x in lst if not (x in seen or seen.add(x))]
    
    all_colors = unique(all_colors)
    all_directions = unique(all_directions)
    all_activities = unique(all_activities)
    all_items = unique(all_items)
    all_foods = unique(all_foods)
    
    # Personalize based on environment
    env_note = ""
    if env_data:
        temp = env_data.get("temperature")
        if temp is not None:
            if temp < 10:
                # Cold - prioritize warming elements
                env_note = f"Cold today ({temp:.0f}C) - warming activities recommended"
                all_activities = [a for a in all_activities if "Swimming" not in a] + ["Warm drinks", "Indoor exercise"]
            elif temp > 28:
                # Hot - prioritize cooling elements  
                env_note = f"Hot today ({temp:.0f}C) - cooling activities recommended"
                all_activities = ["Swimming", "Rest in shade"] + [a for a in all_activities if "Sports" not in a]
    
    # Select final recommendations (varied each time based on session)
    # Use all four pillars combined as seed for consistent but personalized results
    pillars = f"{diagnosis.fate_profile.year_stem_branch}{diagnosis.fate_profile.month_stem_branch}{diagnosis.fate_profile.day_stem_branch}{diagnosis.fate_profile.hour_stem_branch}"
    random.seed(hash(pillars))
    
    return {
        "colors": ", ".join(all_colors[:3]),
        "direction": " or ".join(all_directions[:2]),
        "activities": ", ".join(random.sample(all_activities, min(3, len(all_activities)))),
        "items": ", ".join(random.sample(all_items, min(3, len(all_items)))),
        "foods": ", ".join(all_foods[:3]),
        "best_time": all_times[0] if all_times else "Anytime",
        "env_note": env_note,
    }


def render_diagnosis_card(diagnosis, env_data: dict = None):
    """Render diagnosis results card with lucky guide included."""
    remedy_badges = " ".join(render_element_badge(e) for e in diagnosis.remedy_elements)
    
    # Extract just the imbalance type (before the dash)
    imbalance_short = diagnosis.imbalance_description.split(' - ')[0] if ' - ' in diagnosis.imbalance_description else diagnosis.imbalance_description[:50]
    
    # Lucky Guide data
    fate = diagnosis.fate_profile
    remedy = diagnosis.remedy_elements
    primary = remedy[0] if remedy else fate.inherent_element
    
    colors = ELEMENT_DATA.get(primary, ELEMENT_DATA[Element.EARTH])["colors"][:2]
    numbers = ELEMENT_LUCKY_NUMBERS.get(primary, [5, 10])
    directions = ELEMENT_DATA.get(primary, ELEMENT_DATA[Element.EARTH])["directions"]
    
    times = {
        Element.WATER: "9pm - 1am",
        Element.WOOD: "5am - 9am", 
        Element.FIRE: "11am - 1pm",
        Element.EARTH: "1pm - 3pm",
        Element.METAL: "5pm - 7pm",
    }
    lucky_time = times.get(primary, "Anytime")
    
    avoid_map = {
        Element.WATER: "Fire activities, arguments",
        Element.WOOD: "Metal objects, cutting decisions",
        Element.FIRE: "Water activities, cold environments",
        Element.EARTH: "Wood energy, chaotic changes",
        Element.METAL: "Fire situations, impulsive actions",
    }
    avoid = avoid_map.get(fate.inherent_element, "Overexertion")
    
    html = f'''<div class="glass-card">
<h3>Your Reading</h3>
<div style="background: rgba(255,100,100,0.1); border-left: 3px solid #ff6b6b; padding: 0.8rem; margin: 0.8rem 0; border-radius: 0 8px 8px 0;">
<p style="color: #ff6b6b; font-size: 0.75rem; margin-bottom: 0.3rem; text-transform: uppercase;">Current Imbalance</p>
<p style="color: var(--text-bright); font-size: 0.95rem;">{imbalance_short}</p>
</div>
<div style="background: rgba(100,255,150,0.1); border-left: 3px solid var(--accent-leaf); padding: 0.8rem; margin: 0.8rem 0; border-radius: 0 8px 8px 0;">
<p style="color: var(--accent-leaf); font-size: 0.75rem; margin-bottom: 0.5rem; text-transform: uppercase;">Remedy: Add These Elements</p>
<div>{remedy_badges}</div>
</div>
<div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid var(--glass-border);">
<p style="color: var(--accent-gold); font-size: 0.75rem; margin-bottom: 0.8rem; text-transform: uppercase;">Lucky Guide</p>
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; font-size: 0.85rem;">
<div><span style="color: var(--text-muted);">Colors:</span> <span style="color: var(--text-bright);">{", ".join(colors)}</span></div>
<div><span style="color: var(--text-muted);">Numbers:</span> <span style="color: var(--text-bright);">{", ".join(map(str, numbers))}</span></div>
<div><span style="color: var(--text-muted);">Direction:</span> <span style="color: var(--text-bright);">{", ".join(directions)}</span></div>
<div><span style="color: var(--text-muted);">Time:</span> <span style="color: var(--text-bright);">{lucky_time}</span></div>
</div>
</div>
<div style="margin-top: 0.8rem; padding: 0.6rem; background: rgba(255, 100, 100, 0.1); border-radius: 6px;">
<p style="color: #ff8a80; font-size: 0.8rem;"><span style="font-weight: 600;">Avoid today:</span> {avoid}</p>
</div>
</div>'''
    
    st.markdown(html, unsafe_allow_html=True)


def render_blockchain_card(metadata):
    """Render blockchain proof card."""
    st.markdown(f"""
    <div class="glass-card">
        <h3>Blockchain Proof</h3>
        <div class="metric-row">
            <span class="metric-label">Token ID</span>
            <span class="metric-value" style="font-size: 0.75rem;">{metadata.token_id[:24]}...</span>
        </div>
        <div class="metric-row">
            <span class="metric-label">Block Height</span>
            <span class="metric-value">{metadata.block_number:,}</span>
        </div>
        <div class="metric-row">
            <span class="metric-label">Chain</span>
            <span class="metric-value">Ethereum Mainnet</span>
        </div>
        <div class="hash-display">
            <strong>Keccak256 Hash:</strong><br/>
            0x{metadata.metadata_hash}
        </div>
    </div>
    """, unsafe_allow_html=True)


def main():
    """Main application entry point."""
    inject_custom_css()
    render_header()
    
    birth_datetime, mock_mode, time_unknown = render_sidebar()
    
    # Store time_unknown in session state for display purposes
    st.session_state.time_unknown = time_unknown
    
    # Initialize components
    sensor = SensorArray()
    fate_engine = FateEngine()
    alchemist = Alchemist()
    ether_link = EtherLink()
    generator = TalismanGenerator()
    
    # Generate button - full width
    if st.button("Generate Talisman", use_container_width=True):
        with st.spinner(""):
            progress_text = st.empty()
            progress_bar = st.progress(0)
            
            progress_text.markdown("**Step 1/4:** Connecting to DePIN node...")
            env_reading = sensor.read_environment()
            progress_bar.progress(25)
            time.sleep(0.5)
            
            progress_text.markdown("**Step 2/4:** Calculating fate matrix...")
            fate_profile = fate_engine.calculate_fate(birth_datetime)
            progress_bar.progress(50)
            time.sleep(0.5)
            
            progress_text.markdown("**Step 3/4:** Analyzing elemental balance...")
            real_env_data = getattr(st.session_state, 'real_env', None)
            diagnosis = alchemist.diagnose(fate_profile, env_reading, real_env_data)
            progress_bar.progress(75)
            time.sleep(0.5)
            
            progress_text.markdown("**Step 4/4:** Generating cyber talisman...")
            image_url = generator.generate(diagnosis)
            metadata = ether_link.create_talisman_metadata(diagnosis=diagnosis, image_url=image_url)
            progress_bar.progress(100)
            time.sleep(0.3)
            
            progress_text.empty()
            progress_bar.empty()
            
            st.session_state.env_reading = env_reading
            st.session_state.fate_profile = fate_profile
            st.session_state.diagnosis = diagnosis
            st.session_state.metadata = metadata
            st.session_state.image_url = image_url
    
    # Results display
    if hasattr(st.session_state, 'image_url'):
        # Talisman - centered
        col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
        with col_img2:
            st.image(st.session_state.image_url, use_column_width=True)
        
        st.markdown('<div class="tree-divider"></div>', unsafe_allow_html=True)
        
        # Two columns - balanced content
        col_left, col_right = st.columns([1, 1])
        env_data = getattr(st.session_state, 'real_env', None)
        
        with col_left:
            render_fate_card(st.session_state.fate_profile, fate_engine)
        
        with col_right:
            render_diagnosis_card(st.session_state.diagnosis, env_data)
            render_blockchain_card(st.session_state.metadata)
        
        # Download - full width
        st.markdown('<div class="tree-divider"></div>', unsafe_allow_html=True)
        import json
        nft_json = ether_link.generate_nft_json(st.session_state.metadata)
        st.download_button(
            label="Download NFT Metadata",
            data=json.dumps(nft_json, indent=2, ensure_ascii=False),
            file_name=f"qi-link-talisman-{st.session_state.metadata.token_id[:8]}.json",
            mime="application/json",
            use_container_width=True
        )
    else:
        st.markdown('''
        <div class="glass-card" style="text-align: center; padding: 3rem;">
            <p style="font-size: 2rem; opacity: 0.2; margin-bottom: 1rem;">&#9672;</p>
            <p style="color: var(--text-bright); margin-bottom: 0.5rem;">Enter your birth data</p>
            <p style="color: var(--text-muted); font-size: 0.85rem;">Then click Generate to reveal your fate</p>
        </div>
        ''', unsafe_allow_html=True)
    
    # Footer
    st.markdown('<div class="tree-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; color: var(--text-muted); font-size: 0.75rem; padding: 1rem;">
        <p style="letter-spacing: 0.1em;">Qi-Link v1.0.0 | DePIN Fengshui Node Protocol</p>
        <p style="margin-top: 0.5rem; opacity: 0.7;">Destiny + Fortune = Corrective Energy</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
