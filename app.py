"""
app.py
------
Bitcoin History Dashboard — Futuristic Edition
Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
from pathlib import Path
from filters import load_data, apply_all_filters
from charts import (
    chart_line, chart_bar, chart_histogram, chart_scatter,
    chart_pie, chart_box, chart_heatmap, chart_area,
    chart_count, chart_violin,
)

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="₿ Bitcoin Dashboard",
    page_icon="₿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CUSTOM CSS — Futuristic Bitcoin Theme ─────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    background-color: #030810 !important;
    color: #C8D8E8 !important;
    font-family: 'Share Tech Mono', monospace !important;
}

/* ── Animated grid background ── */
body::before {
    content: '';
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background-image:
        linear-gradient(rgba(247,147,26,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(247,147,26,0.04) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #050D1A 0%, #0A0F1E 100%) !important;
    border-right: 1px solid #F7931A55 !important;
}
section[data-testid="stSidebar"] * { color: #C8D8E8 !important; }

/* ── Headers ── */
h1, h2, h3 {
    font-family: 'Orbitron', sans-serif !important;
    color: #F7931A !important;
}

/* ─── Animated Flipping Bitcoin Coin ─── */
.btc-coin-wrapper {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 80px;
    height: 80px;
    perspective: 400px;
}
.btc-coin {
    width: 70px;
    height: 70px;
    position: relative;
    transform-style: preserve-3d;
    animation: flip3d 2.4s ease-in-out infinite;
    filter: drop-shadow(0 0 16px #F7931A);
}
@keyframes flip3d {
    0%   { transform: rotateY(0deg);   }
    40%  { transform: rotateY(180deg); }
    50%  { transform: rotateY(180deg); }
    90%  { transform: rotateY(360deg); }
    100% { transform: rotateY(360deg); }
}
.btc-coin .face {
    position: absolute;
    width: 70px; height: 70px;
    border-radius: 50%;
    backface-visibility: hidden;
    display: flex; align-items: center; justify-content: center;
    font-size: 34px;
    font-weight: 900;
}
.btc-coin .front {
    background: radial-gradient(circle at 35% 35%, #FFD27A, #F7931A 60%, #B05B00);
    border: 3px solid #FFD27A55;
    color: #fff;
    text-shadow: 0 2px 8px #0008;
}
.btc-coin .back {
    background: radial-gradient(circle at 65% 65%, #B05B00, #F7931A 60%, #FFD27A);
    border: 3px solid #FFD27A55;
    color: #fff;
    transform: rotateY(180deg);
    text-shadow: 0 2px 8px #0008;
}
@keyframes pulseGlow {
    0%, 100% { filter: drop-shadow(0 0 8px #F7931A88); }
    50%       { filter: drop-shadow(0 0 28px #F7931A) drop-shadow(0 0 60px #F7931A44); }
}
.btc-coin {
    animation: flip3d 2.4s ease-in-out infinite, pulseGlow 2s ease-in-out infinite;
}

/* ── Title block ── */
.dashboard-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 2.1rem;
    font-weight: 900;
    background: linear-gradient(90deg, #F7931A, #FFD27A, #F7931A);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 3s linear infinite;
    letter-spacing: 2px;
    margin: 0;
}
@keyframes shimmer {
    0%   { background-position: 0% center; }
    100% { background-position: 200% center; }
}
.dashboard-sub {
    color: #5A7A9A;
    font-size: 0.78rem;
    letter-spacing: 3px;
    margin-top: 4px;
    text-transform: uppercase;
}

/* ── KPI Cards ── */
.kpi-card {
    background: linear-gradient(135deg, #0A1628 0%, #0D1F35 100%);
    border: 1px solid #F7931A44;
    border-top: 2px solid #F7931A;
    border-radius: 8px;
    padding: 18px 16px 14px;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: -30px; right: -30px;
    width: 80px; height: 80px;
    border-radius: 50%;
    background: radial-gradient(circle, #F7931A18 0%, transparent 70%);
}
.kpi-icon  { font-size: 20px; margin-bottom: 6px; }
.kpi-label { font-size: 10px; color: #5A7A9A; letter-spacing: 2px; text-transform: uppercase; }
.kpi-value { font-size: 22px; font-weight: bold; color: #F7931A; font-family: 'Orbitron', sans-serif; margin: 4px 0; }
.kpi-sub   { font-size: 10px; color: #3A5A7A; margin-top: 3px; }

/* ── Section titles ── */
.section-title {
    font-family: 'Orbitron', sans-serif;
    border-left: 3px solid #F7931A;
    padding: 6px 0 6px 14px;
    margin: 28px 0 14px;
    font-size: 15px;
    font-weight: 700;
    color: #F7931A;
    letter-spacing: 2px;
    text-transform: uppercase;
    background: linear-gradient(90deg, #F7931A0D, transparent);
}

/* ── Sidebar filter group ── */
.filter-group {
    background: #0A1628;
    border: 1px solid #F7931A22;
    border-radius: 8px;
    padding: 12px 14px;
    margin-bottom: 12px;
}
.filter-label {
    font-family: 'Orbitron', sans-serif;
    font-size: 10px;
    color: #F7931A;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 6px;
}
.sidebar-header {
    text-align: center;
    padding: 10px 0 16px;
}
.sidebar-header .btc-coin-wrapper {
    margin: 0 auto 12px;
    width: 64px;
    height: 64px;
}
.sidebar-header .btc-coin {
    width: 56px;
    height: 56px;
}
.sidebar-header .btc-coin .face {
    width: 56px;
    height: 56px;
    font-size: 28px;
}

/* ── Streamlit widget overrides ── */
div[data-testid="stSlider"] > div { color: #F7931A !important; }

/* Slider track */
div[data-baseweb="slider"] div[data-testid="stThumbValue"] {
    background: #F7931A !important;
    color: #000 !important;
    font-size: 10px !important;
}

/* Multiselect */
div[data-baseweb="select"] > div {
    background: #0A1628 !important;
    border: 1px solid #F7931A44 !important;
    border-radius: 6px !important;
}
span[data-baseweb="tag"] {
    background: #F7931A22 !important;
    border: 1px solid #F7931A66 !important;
    color: #F7931A !important;
    border-radius: 4px !important;
}

/* Date input */
div[data-testid="stDateInput"] input {
    background: #0A1628 !important;
    border: 1px solid #F7931A44 !important;
    color: #C8D8E8 !important;
    border-radius: 6px !important;
}

/* Text input */
div[data-testid="stTextInput"] input {
    background: #0A1628 !important;
    border: 1px solid #F7931A44 !important;
    color: #C8D8E8 !important;
    border-radius: 6px !important;
    font-family: 'Share Tech Mono', monospace !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #F7931A !important;
    box-shadow: 0 0 0 2px #F7931A22 !important;
}

/* ── Buttons ── */
div.stButton > button {
    background: linear-gradient(135deg, #F7931A, #FFB347) !important;
    color: #030810 !important;
    border: none !important;
    border-radius: 6px !important;
    font-weight: bold !important;
    font-family: 'Orbitron', sans-serif !important;
    letter-spacing: 2px !important;
    font-size: 11px !important;
    padding: 10px 20px !important;
    width: 100% !important;
    text-transform: uppercase !important;
    transition: all 0.2s !important;
    box-shadow: 0 0 12px #F7931A44 !important;
}
div.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 0 24px #F7931A88 !important;
}

/* ── Charts ── */
.stPlotlyChart, iframe { background: transparent !important; }

/* ── Divider ── */
hr { border-color: #F7931A22 !important; }

/* ── Dataframe ── */
div[data-testid="stDataFrame"] { border: 1px solid #F7931A22 !important; border-radius: 8px !important; }

/* ── Filter active badge ── */
.active-filters {
    background: #F7931A22;
    border: 1px solid #F7931A44;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 11px;
    color: #F7931A;
    margin-top: 8px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)


# ── LOAD DATA ─────────────────────────────────────────────────────────────────
@st.cache_data
def get_data():
    base_dir = Path(__file__).resolve().parent
    data_path = base_dir / "data" / "Bitcoin_History.csv"
    return load_data(data_path)


df_full = get_data()


# ── HEADER ────────────────────────────────────────────────────────────────────
col_logo, col_title = st.columns([1, 9])

with col_logo:
    # Animated 3D flipping coin
    st.markdown("""
    <div class="btc-coin-wrapper">
      <div class="btc-coin">
        <div class="face front">₿</div>
        <div class="face back">₿</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

with col_title:
    st.markdown('<div class="dashboard-title">BITCOIN HISTORY DASHBOARD</div>', unsafe_allow_html=True)
    st.markdown('<div class="dashboard-sub">⬡ Exploratory Data Analysis &nbsp;•&nbsp; 2010 – 2024 &nbsp;•&nbsp; Course Project ⬡</div>', unsafe_allow_html=True)

st.markdown("---")


# ── SIDEBAR FILTERS ───────────────────────────────────────────────────────────
with st.sidebar:

    # Sidebar header with coin
    st.markdown("""
    <div class="sidebar-header">
      <div class="btc-coin-wrapper">
        <div class="btc-coin">
          <div class="face front">₿</div>
          <div class="face back">₿</div>
        </div>
      </div>
      <div style="font-family:'Orbitron',sans-serif; font-size:13px;
                  color:#F7931A; letter-spacing:3px; text-transform:uppercase;">
        ⬡ FILTERS ⬡
      </div>
      <div style="font-size:10px; color:#3A5A7A; margin-top:4px; letter-spacing:1px;">
        Refine your analysis
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Filter 1: Date Range ──────────────────────────────────────────────────
    st.markdown("""<div class="filter-group">
    <div class="filter-label">📅 Date Range</div>""", unsafe_allow_html=True)

    min_date = df_full["Date"].min().date()
    max_date = df_full["Date"].max().date()
    start_date, end_date = st.date_input(
        "date_range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        label_visibility="collapsed",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Filter 2: Year Quick-Select ───────────────────────────────────────────
    st.markdown("""<div class="filter-group">
    <div class="filter-label">📆 Year Selection</div>""", unsafe_allow_html=True)

    all_years = sorted(df_full["Year"].unique())
    selected_years = st.multiselect(
        "years",
        options=all_years,
        default=all_years,
        label_visibility="collapsed",
        placeholder="All years selected",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Filter 3: Price Range ─────────────────────────────────────────────────
    st.markdown("""<div class="filter-group">
    <div class="filter-label">💵 Price Range (USD)</div>""", unsafe_allow_html=True)

    price_min_val = float(df_full["Price"].min())
    price_max_val = float(df_full["Price"].max())
    price_range = st.slider(
        "price",
        min_value=price_min_val,
        max_value=price_max_val,
        value=(price_min_val, price_max_val),
        format="$%.0f",
        label_visibility="collapsed",
    )
    # Show selected range nicely
    st.markdown(
        f"<div style='font-size:10px; color:#5A7A9A; text-align:center; margin-top:4px;'>"
        f"${price_range[0]:,.0f} &nbsp;→&nbsp; ${price_range[1]:,.0f}"
        f"</div>",
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Filter 4: Market Direction ─────────────────────────────────────────────
    st.markdown("""<div class="filter-group">
    <div class="filter-label">📊 Market Direction</div>""", unsafe_allow_html=True)

    # Use checkboxes for clearer UX
    col_bull, col_bear = st.columns(2)
    with col_bull:
        show_bullish = st.checkbox("🟢 Bullish", value=True)
    with col_bear:
        show_bearish = st.checkbox("🔴 Bearish", value=True)

    selected_dirs = []
    if show_bullish:
        selected_dirs.append("Bullish")
    if show_bearish:
        selected_dirs.append("Bearish")

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Filter 5: Keyword Search ──────────────────────────────────────────────
    st.markdown("""<div class="filter-group">
    <div class="filter-label">🔍 Search by Date</div>""", unsafe_allow_html=True)

    keyword = st.text_input(
        "keyword",
        value="",
        placeholder="e.g.  2021  or  Jan  or  2020-03",
        label_visibility="collapsed",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Active filter summary ──────────────────────────────────────────────────
    active_count = sum([
        start_date != min_date or end_date != max_date,
        len(selected_years) != len(all_years),
        price_range != (price_min_val, price_max_val),
        len(selected_dirs) != 2,
        bool(keyword.strip()),
    ])

    if active_count > 0:
        st.markdown(
            f'<div class="active-filters">⚡ {active_count} active filter{"s" if active_count > 1 else ""}</div>',
            unsafe_allow_html=True
        )

    st.markdown("---")

    if st.button("⟳  RESET ALL FILTERS"):
        st.rerun()

    st.markdown(
        "<div style='font-size:10px; color:#2A3A4A; text-align:center; margin-top:12px;'>"
        "Data: Bitcoin_History.csv<br>Charts: Matplotlib + Seaborn"
        "</div>",
        unsafe_allow_html=True,
    )


# ── APPLY ALL FILTERS ─────────────────────────────────────────────────────────
df = apply_all_filters(
    df_full,
    start_date, end_date,
    price_range[0], price_range[1],
    selected_dirs,
    selected_years,
    keyword,
)


# ── KPI CARDS ─────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">⬡ Key Statistics</div>', unsafe_allow_html=True)

k1, k2, k3, k4, k5 = st.columns(5)

def kpi(col, icon, label, value, sub=""):
    col.markdown(
        f'<div class="kpi-card">'
        f'<div class="kpi-icon">{icon}</div>'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div>'
        f'<div class="kpi-sub">{sub}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

kpi(k1, "📋", "TOTAL RECORDS",    f"{len(df):,}",                        "filtered rows")
kpi(k2, "₿",  "LATEST PRICE",     f"${df['Price'].iloc[-1]:,.1f}" if len(df) else "—",  "last closing price")
kpi(k3, "🚀", "ALL-TIME HIGH",    f"${df['Price'].max():,.1f}" if len(df) else "—",     "in filtered range")
kpi(k4, "📈", "AVG DAILY RETURN", f"{df['Change %'].mean():.2f}%" if len(df) else "—", "mean daily change")
kpi(k5, "🟢", "BULLISH DAYS",
    f"{(df['Direction'] == 'Bullish').sum():,}" if len(df) else "—",
    f"of {len(df):,} total")


# ── GUARD ─────────────────────────────────────────────────────────────────────
if df.empty:
    st.warning("⚠️ No data matches your filters. Try adjusting the sidebar.")
    st.stop()


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — Price Trends
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">📈 Price Trends</div>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 2])
with col1:
    st.markdown("**Line Chart — Closing Price Over Time**")
    st.pyplot(chart_line(df), use_container_width=True)
with col2:
    st.markdown("**Area Chart — Price vs All-Time High**")
    st.pyplot(chart_area(df), use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — Distribution & Returns
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">📉 Distribution & Returns</div>', unsafe_allow_html=True)

col3, col4, col5 = st.columns([2, 2, 1.5])
with col3:
    st.markdown("**Histogram — Daily % Change**")
    st.pyplot(chart_histogram(df), use_container_width=True)
with col4:
    st.markdown("**Scatter — Volume vs Price**")
    st.pyplot(chart_scatter(df), use_container_width=True)
with col5:
    st.markdown("**Pie — Bullish vs Bearish**")
    st.pyplot(chart_pie(df), use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — Yearly Analysis
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">📆 Yearly Analysis</div>', unsafe_allow_html=True)

col6, col7 = st.columns(2)
with col6:
    st.markdown("**Bar Chart — Average Price by Year**")
    st.pyplot(chart_bar(df), use_container_width=True)
with col7:
    st.markdown("**Count Plot — Bullish/Bearish per Year**")
    st.pyplot(chart_count(df), use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — Statistical Depth
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">🔬 Statistical Depth</div>', unsafe_allow_html=True)

col8, col9, col10 = st.columns([2, 2, 2])
with col8:
    st.markdown("**Box Plot — Price by Year**")
    st.pyplot(chart_box(df), use_container_width=True)
with col9:
    st.markdown("**Violin Plot — % Change by Year**")
    st.pyplot(chart_violin(df), use_container_width=True)
with col10:
    st.markdown("**Heatmap — Feature Correlations**")
    st.pyplot(chart_heatmap(df), use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 5 — Raw Data Preview
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">🗃 Raw Data Preview</div>', unsafe_allow_html=True)
st.dataframe(
    df[["Date", "Price", "Open", "High", "Low", "Vol.", "Change %", "Direction"]]
      .sort_values("Date", ascending=False)
      .head(50),
    use_container_width=True,
    hide_index=True,
)

st.markdown("---")
st.markdown(
    "<center><small style='color:#2A3A4A; font-size:10px; letter-spacing:2px;'>"
    "₿ BITCOIN HISTORY DASHBOARD &nbsp;•&nbsp; EDA COURSE PROJECT &nbsp;•&nbsp; "
    "STREAMLIT + PANDAS + MATPLOTLIB + SEABORN"
    "</small></center>",
    unsafe_allow_html=True,
)
