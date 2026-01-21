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
    .stSelectbox > div > div,
    .stDateInput > div > div {
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
    .stDateInput label,
    .stNumberInput label,
    .stTextInput label,
    [data-testid="stWidgetLabel"],
    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] span,
    .stSelectbox [data-testid="stWidgetLabel"],
    .stDateInput [data-testid="stWidgetLabel"] {
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
    
    /* Date input text - dark on white background */
    [data-testid="stSidebar"] .stDateInput input,
    .stDateInput input {
        color: #1a1a1a !important;
        background-color: #ffffff !important;
    }
    
    /* Dropdown menu items - dark text on light background */
    [data-baseweb="menu"],
    [data-baseweb="menu"] li,
    [data-baseweb="menu"] div,
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
    </style>
    """, unsafe_allow_html=True)


def render_header():
    """Render the main header."""
    st.markdown('<h1 class="main-title">Qi-Link</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">DePIN Fengshui Node Protocol</p>', unsafe_allow_html=True)
    st.markdown('<div class="tree-divider"></div>', unsafe_allow_html=True)


def render_sidebar():
    """Render sidebar with birth data input and node status."""
    with st.sidebar:
        st.markdown('<p class="sidebar-section">Birth Data</p>', unsafe_allow_html=True)
        st.markdown("---")
        
        birth_date = st.date_input(
            "Date of Birth",
            value=date(1990, 1, 1),
            min_value=date(1900, 1, 1),
            max_value=date.today()
        )
        
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
        
        location_service = LocationService()
        env_data = location_service.get_all_environmental_data()
        
        location = env_data["location"]
        weather = env_data["weather"]
        # Auto-detect direction from wind direction
        compass = location_service.get_compass_direction(None)
        
        # Store in session state for use in main content
        st.session_state.real_env = {
            "location": location,
            "weather": weather,
            "compass": compass,
        }
        
        location_str = f"{location.city}, {location.country}" if location.city != "Unknown" else "Detecting..."
        
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


def render_fate_card(fate, engine: FateEngine):
    """Render fate profile card."""
    star_info = engine.get_star_description(fate.major_star)
    palace_en = get_palace_english(fate.life_palace)
    
    # Check if birth time was unknown
    time_unknown = getattr(st.session_state, 'time_unknown', False)
    
    # Build hour pillar display with uncertainty note if needed
    hour_pillar_display = fate.hour_stem_branch
    if time_unknown:
        hour_pillar_display = f'<span style="opacity: 0.5;">{fate.hour_stem_branch}*</span>'
    
    # Uncertainty note
    uncertainty_note = ""
    if time_unknown:
        uncertainty_note = """
        <div style="margin-top: 0.8rem; padding: 0.6rem; background: rgba(212, 175, 55, 0.1); 
                    border-radius: 6px; font-size: 0.75rem; color: var(--accent-gold);">
            * Hour pillar estimated (noon default). Year/Month/Day pillars are accurate.
        </div>
        """
    
    st.markdown(f"""
    <div class="glass-card">
        <h3>Fate Analysis</h3>
        <div class="metric-row">
            <span class="metric-label">Major Star</span>
            <span class="metric-value">{fate.major_star.value} ({star_info['english']})</span>
        </div>
        <div class="metric-row">
            <span class="metric-label">Life Palace</span>
            <span class="metric-value">{fate.life_palace} ({palace_en})</span>
        </div>
        <div class="metric-row">
            <span class="metric-label">Inherent Element</span>
            <span class="metric-value">{render_element_badge(fate.inherent_element)}</span>
        </div>
        <div class="metric-row">
            <span class="metric-label">Four Pillars</span>
            <span class="metric-value">{fate.year_stem_branch} {fate.month_stem_branch} {fate.day_stem_branch} {hour_pillar_display}</span>
        </div>
        <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.06);">
            <p style="color: var(--text-muted); font-size: 0.85rem; line-height: 1.5;">
                <strong style="color: var(--accent-gold);">{star_info['english']}</strong>: {star_info['nature']}
            </p>
        </div>
        {uncertainty_note}
    </div>
    """, unsafe_allow_html=True)


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
    """Render diagnosis results card with clear, actionable advice."""
    advice = get_personalized_advice(diagnosis, env_data)
    
    remedy_badges = " ".join(render_element_badge(e) for e in diagnosis.remedy_elements)
    
    # Extract just the imbalance type (before the dash)
    imbalance_short = diagnosis.imbalance_description.split(' - ')[0] if ' - ' in diagnosis.imbalance_description else diagnosis.imbalance_description[:50]
    
    # Environment note if available
    env_note_html = ""
    if advice.get("env_note"):
        env_note_html = f'<p style="color: var(--accent-gold); font-size: 0.8rem; font-style: italic; margin-top: 0.5rem;">{advice["env_note"]}</p>'
    
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
<div style="background: rgba(212,175,55,0.1); border-left: 3px solid var(--accent-gold); padding: 0.8rem; margin: 0.8rem 0; border-radius: 0 8px 8px 0;">
<p style="color: var(--accent-gold); font-size: 0.75rem; margin-bottom: 0.5rem; text-transform: uppercase;">What To Do Today</p>
<div style="display: grid; gap: 0.4rem; font-size: 0.85rem;">
<div style="color: var(--text-mid);"><span style="color: var(--text-bright);">Wear:</span> {advice['colors']}</div>
<div style="color: var(--text-mid);"><span style="color: var(--text-bright);">Face:</span> {advice['direction']}</div>
<div style="color: var(--text-mid);"><span style="color: var(--text-bright);">Do:</span> {advice['activities']}</div>
<div style="color: var(--text-mid);"><span style="color: var(--text-bright);">Add:</span> {advice['items']}</div>
<div style="color: var(--text-mid);"><span style="color: var(--text-bright);">Eat:</span> {advice['foods']}</div>
<div style="color: var(--text-mid);"><span style="color: var(--text-bright);">Best Time:</span> {advice['best_time']}</div>
</div>
{env_note_html}
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
    
    # Main content columns
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.markdown('<p class="section-header">System Analysis</p>', unsafe_allow_html=True)
        
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
                
                progress_text.markdown("**Step 3/4:** Analyzing elemental balance with Feng Shui...")
                # Get real environment data for enhanced Feng Shui calculation
                real_env_data = getattr(st.session_state, 'real_env', None)
                diagnosis = alchemist.diagnose(fate_profile, env_reading, real_env_data)
                progress_bar.progress(75)
                time.sleep(0.5)
                
                progress_text.markdown("**Step 4/4:** Generating cyber talisman...")
                image_url = generator.generate(diagnosis)
                metadata = ether_link.create_talisman_metadata(
                    diagnosis=diagnosis,
                    image_url=image_url
                )
                progress_bar.progress(100)
                time.sleep(0.3)
                
                progress_text.empty()
                progress_bar.empty()
                
                # Store in session state
                st.session_state.env_reading = env_reading
                st.session_state.fate_profile = fate_profile
                st.session_state.diagnosis = diagnosis
                st.session_state.metadata = metadata
                st.session_state.image_url = image_url
                
                st.success("Talisman generation complete.")
        
        # Display analysis results
        if hasattr(st.session_state, 'env_reading'):
            render_environment_card(st.session_state.env_reading)
        
        if hasattr(st.session_state, 'fate_profile'):
            render_fate_card(st.session_state.fate_profile, fate_engine)
    
    with col_right:
        st.markdown('<p class="section-header">Cyber Talisman</p>', unsafe_allow_html=True)
        
        if hasattr(st.session_state, 'image_url'):
            st.markdown('<div class="talisman-frame">', unsafe_allow_html=True)
            st.image(st.session_state.image_url, use_column_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Pass environment data for personalized advice
            env_data = getattr(st.session_state, 'real_env', None)
            render_diagnosis_card(st.session_state.diagnosis, env_data)
            render_blockchain_card(st.session_state.metadata)
            
            # Download button
            import json
            nft_json = ether_link.generate_nft_json(st.session_state.metadata)
            st.download_button(
                label="Download NFT Metadata",
                data=json.dumps(nft_json, indent=2, ensure_ascii=False),
                file_name=f"qi-link-talisman-{st.session_state.metadata.token_id[:8]}.json",
                mime="application/json"
            )
        else:
            st.markdown("""
            <div class="glass-card placeholder-area">
                <div class="placeholder-icon">&#9672;</div>
                <p style="font-size: 1.1rem; margin-bottom: 0.5rem;">Awaiting Generation</p>
                <p style="font-size: 0.85rem;">Enter birth data and click generate to create your cyber talisman</p>
            </div>
            """, unsafe_allow_html=True)
    
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
