import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import streamlit.components.v1 as components

# ── Page Config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Sector Rotation Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Premium CSS ──────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ── Global ─────────────────────────────────── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    @keyframes gradient-bg {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .stApp {
        background: linear-gradient(-45deg, #0f172a, #1e1b4b, #2e1065, #1e1b4b, #0f172a) !important;
        background-size: 400% 400% !important;
        animation: gradient-bg 15s ease infinite !important;
    }

    /* ── Sidebar ────────────────────────────────── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(195deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
        border-right: 1px solid rgba(139, 92, 246, 0.15);
    }

    section[data-testid="stSidebar"] .stMarkdown h2 {
        background: linear-gradient(135deg, #a78bfa, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        letter-spacing: -0.5px;
    }

    section[data-testid="stSidebar"] label {
        color: #94a3b8 !important;
        font-weight: 500;
        font-size: 0.85rem;
        letter-spacing: 0.3px;
        text-transform: uppercase;
    }

    section[data-testid="stSidebar"] .stSelectbox > div > div,
    section[data-testid="stSidebar"] .stMultiSelect > div > div {
        background: rgba(30, 27, 75, 0.6) !important;
        border: 1px solid rgba(139, 92, 246, 0.25) !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
    }

    section[data-testid="stSidebar"] .stMultiSelect span[data-baseweb="tag"] {
        background-color: rgba(221, 214, 254, 0.9) !important;
        border: 1px solid rgba(139, 92, 246, 0.6) !important;
    }

    section[data-testid="stSidebar"] .stMultiSelect span[data-baseweb="tag"] span {
        color: #4c1d95 !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px;
    }

    section[data-testid="stSidebar"] hr {
        border-color: rgba(139, 92, 246, 0.12);
    }

    /* ── Main Header ────────────────────────────── */
    @keyframes shine {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .main-header {
        text-align: center;
        font-size: 5.2rem !important;
        font-weight: 900 !important;
        line-height: 1.2 !important;
        padding-top: 20px;
        background: linear-gradient(270deg, #818cf8, #c084fc, #e879f9, #f472b6, #c084fc, #818cf8);
        background-size: 400% 100%;
        animation: shine 5s linear infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
        letter-spacing: -1px;
    }

    .sub-header {
        text-align: center;
        font-size: 1.1rem;
        color: #94a3b8;
        margin-top: 0px;
        margin-bottom: 35px;
        font-weight: 500;
        letter-spacing: 0.5px;
    }

    /* ── Section Titles ─────────────────────────── */
    .section-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #e2e8f0;
        border-left: 4px solid;
        border-image: linear-gradient(to bottom, #818cf8, #a78bfa) 1;
        padding-left: 14px;
        margin: 36px 0 18px 0;
        letter-spacing: -0.3px;
    }

    /* ── Glass Cards ────────────────────────────── */
    .glass-card {
        background: rgba(30, 41, 59, 0.45);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(139, 92, 246, 0.12);
        border-radius: 16px;
        padding: 24px 28px;
        margin-bottom: 20px;
        color: #e2e8f0;
    }

    .overview-box {
        background: linear-gradient(135deg, rgba(30, 27, 75, 0.5), rgba(15, 23, 42, 0.7));
        backdrop-filter: blur(12px);
        border: 1px solid rgba(139, 92, 246, 0.15);
        border-radius: 16px;
        padding: 22px 28px;
        margin-bottom: 24px;
        color: #cbd5e1;
        font-size: 0.92rem;
        line-height: 1.8;
    }

    .overview-box h4 {
        background: linear-gradient(135deg, #a78bfa, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1.1rem;
        margin-bottom: 10px;
        font-weight: 700;
    }

    .overview-box b {
        color: #a78bfa;
    }

    /* ── Insight Box ────────────────────────────── */
    .insight-box {
        background: linear-gradient(145deg, rgba(30, 27, 75, 0.55), rgba(15, 23, 42, 0.75));
        backdrop-filter: blur(12px);
        border: 1px solid rgba(139, 92, 246, 0.18);
        border-radius: 16px;
        padding: 24px 28px;
        margin: 16px 0;
        color: #cbd5e1;
        font-size: 0.92rem;
        line-height: 1.85;
    }

    .insight-box h4 {
        background: linear-gradient(135deg, #fbbf24, #f59e0b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1.1rem;
        margin-bottom: 12px;
        font-weight: 700;
    }

    .insight-box .tag-volatile {
        display: inline-block;
        background: rgba(239, 68, 68, 0.2);
        border: 1px solid rgba(239, 68, 68, 0.4);
        color: #fca5a5;
        padding: 2px 10px;
        border-radius: 6px;
        font-size: 0.82rem;
        font-weight: 600;
    }

    .insight-box .tag-stable {
        display: inline-block;
        background: rgba(52, 211, 153, 0.15);
        border: 1px solid rgba(52, 211, 153, 0.35);
        color: #6ee7b7;
        padding: 2px 10px;
        border-radius: 6px;
        font-size: 0.82rem;
        font-weight: 600;
    }

    .insight-box .tag-gold-up {
        display: inline-block;
        background: rgba(251, 191, 36, 0.15);
        border: 1px solid rgba(251, 191, 36, 0.35);
        color: #fcd34d;
        padding: 2px 10px;
        border-radius: 6px;
        font-size: 0.82rem;
        font-weight: 600;
    }

    .insight-box .tag-gold-down {
        display: inline-block;
        background: rgba(100, 116, 139, 0.2);
        border: 1px solid rgba(100, 116, 139, 0.35);
        color: #94a3b8;
        padding: 2px 10px;
        border-radius: 6px;
        font-size: 0.82rem;
        font-weight: 600;
    }

    /* ── Metrics ────────────────────────────────── */
    div[data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.5);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(139, 92, 246, 0.12);
        border-radius: 14px;
        padding: 18px 20px;
    }

    div[data-testid="stMetric"] label {
        color: #94a3b8 !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #e2e8f0 !important;
        font-weight: 700 !important;
    }

    div[data-testid="stMetric"] div[data-testid="stMetricDelta"] {
        font-weight: 500;
    }

    /* ── Dividers ───────────────────────────────── */
    .stApp hr {
        border-color: rgba(139, 92, 246, 0.1);
        margin: 28px 0;
    }

    /* ── DataFrames ─────────────────────────────── */
    .stDataFrame {
        border-radius: 12px;
    }

    /* ── Footer ─────────────────────────────────── */
    .footer-text {
        text-align: center;
        color: #475569;
        font-size: 0.78rem;
        letter-spacing: 0.5px;
        padding: 16px 0;
    }

    .footer-text span {
        color: #818cf8;
    }

    /* ── Sidebar Brand ──────────────────────────── */
    .sidebar-brand {
        text-align: center;
        padding: 12px 0;
        margin-bottom: 8px;
    }

    .sidebar-brand .logo {
        font-size: 2rem;
        margin-bottom: 4px;
    }

    .sidebar-brand .name {
        font-size: 0.7rem;
        color: white;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# ── Load Data ────────────────────────────────────────────────
@st.cache_data
def load_data():
    base = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(os.path.join(base, "processed/final_dataset.csv"))
    ind = pd.read_csv(os.path.join(base, "processed/master_indicators.csv"))
    df['date'] = pd.to_datetime(df['date'])
    ind['date'] = pd.to_datetime(ind['date'])
    return df, ind

df, ind = load_data()

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="logo">📊</div>
        <div class="name">Sector Rotation Engine</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## ⚙️ Dashboard Controls")
    st.markdown("---")

    all_dates = sorted(df['date'].dt.date.unique(), reverse=True)
    selected_date = st.selectbox("📅 Analysis Date", all_dates, index=0)

    st.markdown("---")

    all_sectors = sorted(df['index_name'].unique())
    default_sectors = ['NIFTY IT', 'NIFTY BANK', 'NIFTY PHARMA', 'NIFTY AUTO', 'NIFTY FMCG']
    valid_defaults = [s for s in default_sectors if s in all_sectors]

    selected_sectors = st.multiselect(
        "🏢 Tracked Sectors",
        all_sectors,
        default=valid_defaults
    )

    st.markdown("---")

    st.markdown("""
    <div style="text-align:center; padding: 20px 0;">
        <p style="color:#64748b; font-size:0.7rem; text-transform:uppercase; letter-spacing:1.5px; margin-bottom:4px;">
            Powered by
        </p>
        <p style="color:#818cf8; font-size:0.85rem; font-weight:600; letter-spacing:0.5px;">
            Python · Pandas · Plotly
        </p>
        <p style="color:#475569; font-size:0.7rem; margin-top:12px;">
            DTU · Data Engineering & Analytics<br>Project 2026
        </p>
    </div>
    """, unsafe_allow_html=True)

# ── Mouse Glow Effect ────────────────────────────────────────
components.html(
    """
    <script>
    const parentDoc = window.parent.document;
    if (!parentDoc.getElementById('custom-mouse-glow')) {
        const glow = parentDoc.createElement('div');
        glow.id = 'custom-mouse-glow';
        glow.style.position = 'fixed';
        glow.style.width = '400px';
        glow.style.height = '400px';
        glow.style.background = 'radial-gradient(circle, rgba(167, 139, 250, 0.15) 0%, rgba(0, 0, 0, 0) 60%)';
        glow.style.borderRadius = '50%';
        glow.style.pointerEvents = 'none';
        glow.style.transform = 'translate(-50%, -50%)';
        glow.style.zIndex = '9999';
        glow.style.transition = 'width 0.1s, height 0.1s';
        parentDoc.body.appendChild(glow);
        
        parentDoc.addEventListener('mousemove', (e) => {
            glow.style.left = e.clientX + 'px';
            glow.style.top = e.clientY + 'px';
        });
    }
    </script>
    """,
    height=0,
    width=0,
)

# ── Header ───────────────────────────────────────────────────
st.markdown('<p class="main-header">Sector Rotation Dashboard</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-header">Tracking capital migration across Indian equity sectors using Relative Strength analytics</p>',
    unsafe_allow_html=True
)

# ── Project Overview ─────────────────────────────────────────
st.markdown("""
<div class="overview-box">
    <h4>📌 Project Overview</h4>
    This dashboard analyzes <b>sector rotation</b> in the Indian stock market using
    <b>Relative Strength (RS)</b>, <b>Simple Moving Averages (SMA-20)</b>, <b>Momentum Signals</b>,
    and <b>Daily Rank Tracking</b>. It reveals which sectors are attracting capital and which are losing ground —
    enabling data-driven investment insight through a scalable ETL pipeline.
</div>
""", unsafe_allow_html=True)

# ── Filter Data ──────────────────────────────────────────────
latest = df[df['date'].dt.date == selected_date].copy()

# ── KPI Cards ────────────────────────────────────────────────
if not latest.empty:
    top_sector = latest.loc[latest['rank_rs'].idxmin()]
    worst_sector = latest.loc[latest['rank_rs'].idxmax()]
    avg_momentum = latest['momentum_20'].mean()
    num_positive = (latest['momentum_20'] > 0).sum()

    k1, k2 = st.columns(2)
    with k1:
        st.metric("📅 Analysis Date", str(selected_date))
        st.metric("📉 Lagging Sector", worst_sector['index_name'], f"RS: {worst_sector['rs']:.4f}")
    with k2:
        st.metric("🏆 Leading Sector", top_sector['index_name'], f"RS: {top_sector['rs']:.4f}")
        st.metric("⚡ Bullish Sectors", f"{num_positive} / {len(latest)}")

st.markdown("---")

# ── Section 1: Sector Leadership ─────────────────────────────
st.markdown('<p class="section-title">🏆 Sector Leadership</p>', unsafe_allow_html=True)

if not latest.empty:
    col1, col2 = st.columns(2)

    with col1:
        top5 = latest.sort_values('rank_rs').head(5)
        fig_top = px.bar(
            top5, x='index_name', y='rs', color='rs',
            color_continuous_scale=[[0, '#065f46'], [0.5, '#10b981'], [1, '#6ee7b7']],
            labels={'rs': 'Relative Strength', 'index_name': ''},
            template='plotly_dark'
        )
        fig_top.update_layout(
            title=dict(text='🟢 Top 5 — Outperformers', font=dict(size=14, color='#e2e8f0')),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=45, b=0), showlegend=False,
            coloraxis_showscale=False,
            xaxis=dict(tickfont=dict(color='#94a3b8')),
            yaxis=dict(tickfont=dict(color='#94a3b8'), gridcolor='rgba(148,163,184,0.08)')
        )
        st.plotly_chart(fig_top, use_container_width=True)

    with col2:
        bottom5 = latest.sort_values('rank_rs', ascending=False).head(5)
        fig_bot = px.bar(
            bottom5, x='index_name', y='rs', color='rs',
            color_continuous_scale=[[0, '#fca5a5'], [0.5, '#ef4444'], [1, '#7f1d1d']],
            labels={'rs': 'Relative Strength', 'index_name': ''},
            template='plotly_dark'
        )
        fig_bot.update_layout(
            title=dict(text='🔴 Bottom 5 — Underperformers', font=dict(size=14, color='#e2e8f0')),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=45, b=0), showlegend=False,
            coloraxis_showscale=False,
            xaxis=dict(tickfont=dict(color='#94a3b8')),
            yaxis=dict(tickfont=dict(color='#94a3b8'), gridcolor='rgba(148,163,184,0.08)')
        )
        st.plotly_chart(fig_bot, use_container_width=True)

st.markdown("---")

# ── Section 2: Sector Rotation Over Time ─────────────────────
st.markdown('<p class="section-title">📈 Sector Rotation Over Time</p>', unsafe_allow_html=True)

if selected_sectors:
    filtered = df[df['index_name'].isin(selected_sectors)]

    fig_rs = px.line(
        filtered, x='date', y='rs', color='index_name',
        labels={'rs': 'Relative Strength', 'date': '', 'index_name': 'Sector'},
        template='plotly_dark'
    )
    fig_rs.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        legend=dict(
            orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5,
            font=dict(color='#94a3b8', size=11),
            bgcolor='rgba(0,0,0,0)'
        ),
        margin=dict(l=0, r=0, t=40, b=0),
        hovermode='x unified',
        xaxis=dict(tickfont=dict(color='#64748b'), gridcolor='rgba(148,163,184,0.06)'),
        yaxis=dict(tickfont=dict(color='#64748b'), gridcolor='rgba(148,163,184,0.06)')
    )
    st.plotly_chart(fig_rs, use_container_width=True)
else:
    st.info("Select at least one sector from the sidebar to view rotation trends.")

st.markdown("---")

# ── Section 3: Momentum Snapshot ──────────────────────────────
st.markdown('<p class="section-title">🔥 Momentum Snapshot</p>', unsafe_allow_html=True)

if not latest.empty:
    momentum_data = latest.dropna(subset=['momentum_20']).sort_values('momentum_20', ascending=True).copy()
    momentum_data['color'] = momentum_data['momentum_20'].apply(
        lambda x: '#34d399' if x > 0 else '#f87171'
    )

    fig_mom = go.Figure()
    fig_mom.add_trace(go.Bar(
        y=momentum_data['index_name'],
        x=momentum_data['momentum_20'],
        orientation='h',
        marker_color=momentum_data['color'],
        text=momentum_data['momentum_20'].apply(lambda x: f'{x:.4f}'),
        textposition='outside',
        textfont=dict(color='#94a3b8', size=10)
    ))
    fig_mom.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(title='Momentum (20-day)', tickfont=dict(color='#64748b'),
                   gridcolor='rgba(148,163,184,0.06)', title_font=dict(color='#94a3b8')),
        yaxis=dict(tickfont=dict(color='#94a3b8')),
        margin=dict(l=0, r=50, t=10, b=0),
        height=450
    )
    st.plotly_chart(fig_mom, use_container_width=True)

st.markdown("---")

# ── Section 4: Rank Tracker Over Time ────────────────────────
st.markdown('<p class="section-title">📊 Rank Tracker Over Time</p>', unsafe_allow_html=True)

if selected_sectors:
    rank_data = df[df['index_name'].isin(selected_sectors)]

    fig_rank = px.line(
        rank_data, x='date', y='rank_rs', color='index_name',
        labels={'rank_rs': 'RS Rank', 'date': '', 'index_name': 'Sector'},
        template='plotly_dark'
    )
    fig_rank.update_yaxes(autorange='reversed')
    fig_rank.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        legend=dict(
            orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5,
            font=dict(color='#94a3b8', size=11),
            bgcolor='rgba(0,0,0,0)'
        ),
        margin=dict(l=0, r=0, t=40, b=0),
        hovermode='x unified',
        xaxis=dict(tickfont=dict(color='#64748b'), gridcolor='rgba(148,163,184,0.06)'),
        yaxis=dict(tickfont=dict(color='#64748b'), gridcolor='rgba(148,163,184,0.06)',
                   title=dict(text='Rank (1 = strongest)', font=dict(color='#94a3b8')))
    )
    st.plotly_chart(fig_rank, use_container_width=True)

st.markdown("---")

# ── Section 5: Macro Indicators ──────────────────────────────
st.markdown('<p class="section-title">🌍 Macro Indicators</p>', unsafe_allow_html=True)

macro = ind[ind['indicator_name'].isin(['Gold price INR', 'VIX_History'])]

if not macro.empty:
    m1, m2 = st.columns(2)

    with m1:
        gold = macro[macro['indicator_name'] == 'Gold price INR']
        fig_gold = px.area(
            gold, x='date', y='value',
            labels={'value': 'Gold Price (INR)', 'date': ''},
            template='plotly_dark'
        )
        fig_gold.update_traces(line_color='#fbbf24', fillcolor='rgba(251,191,36,0.08)')
        fig_gold.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=45, b=0),
            title=dict(text='Gold Price (INR)', font=dict(size=14, color='#fbbf24')),
            xaxis=dict(tickfont=dict(color='#64748b'), gridcolor='rgba(148,163,184,0.06)'),
            yaxis=dict(tickfont=dict(color='#64748b'), gridcolor='rgba(148,163,184,0.06)')
        )
        st.plotly_chart(fig_gold, use_container_width=True)

    with m2:
        vix = macro[macro['indicator_name'] == 'VIX_History']
        fig_vix = px.area(
            vix, x='date', y='value',
            labels={'value': 'VIX', 'date': ''},
            template='plotly_dark'
        )
        fig_vix.update_traces(line_color='#f87171', fillcolor='rgba(248,113,113,0.08)')
        fig_vix.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=45, b=0),
            title=dict(text='VIX (Volatility Index)', font=dict(size=14, color='#f87171')),
            xaxis=dict(tickfont=dict(color='#64748b'), gridcolor='rgba(148,163,184,0.06)'),
            yaxis=dict(tickfont=dict(color='#64748b'), gridcolor='rgba(148,163,184,0.06)')
        )
        st.plotly_chart(fig_vix, use_container_width=True)

# ── Section 6: Indicator Analysis ────────────────────────────
st.markdown('<p class="section-title">🧠 Macro Indicator Analysis</p>', unsafe_allow_html=True)

# VIX Analysis
vix_filtered = vix[vix['date'].dt.date <= selected_date].copy() if not macro.empty else pd.DataFrame()
vix_data = vix_filtered.sort_values('date') if not vix_filtered.empty else pd.DataFrame()
latest_vix = vix_data['value'].iloc[-1] if not vix_data.empty else None

if latest_vix is not None:
    if latest_vix > 15:
        vix_tag = '<span class="tag-volatile">⚠️ VOLATILE</span>'
        vix_message = (
            f"The current VIX is at <b>{latest_vix:.2f}</b>, which is above the critical threshold of 15. "
            "This indicates <b>heightened market volatility</b> — expect sharp, unpredictable moves in either direction. "
            "During high-VIX regimes, defensive sectors like <b>FMCG and Pharma</b> tend to outperform, "
            "while high-beta sectors like <b>Metals and IT</b> face increased selling pressure. "
            "Portfolio hedging and position sizing become critical in this environment."
        )
    else:
        vix_tag = '<span class="tag-stable">✅ STABLE</span>'
        vix_message = (
            f"The current VIX is at <b>{latest_vix:.2f}</b>, well below the 15 threshold. "
            "This signals a <b>calm and stable market environment</b> — ideal for trend-following strategies. "
            "In low-volatility periods, <b>cyclical sectors</b> like Banking, Auto, and Infrastructure "
            "typically see steady capital inflows, and momentum-based rotation strategies tend to perform well."
        )
else:
    vix_tag = ''
    vix_message = 'VIX data not available.'

# Gold Analysis
gold_filtered = gold[gold['date'].dt.date <= selected_date].copy() if not macro.empty else pd.DataFrame()
gold_data = gold_filtered.sort_values('date') if not gold_filtered.empty else pd.DataFrame()
if not gold_data.empty and len(gold_data) >= 22:
    gold_latest = gold_data['value'].iloc[-1]
    gold_1m_ago = gold_data['value'].iloc[-22]   # ~1 month of trading days
    gold_change_pct = ((gold_latest - gold_1m_ago) / gold_1m_ago) * 100

    if gold_change_pct > 3:
        gold_tag = '<span class="tag-gold-up">🔺 RISING SHARPLY</span>'
        gold_message = (
            f"Gold has surged by <b>{gold_change_pct:.1f}%</b> in the last month "
            f"(₹{gold_1m_ago:,.0f} → ₹{gold_latest:,.0f}). "
            "A sharp rise in gold prices typically signals <b>risk-off sentiment</b> — investors are moving capital "
            "from equities into safe-haven assets. This often coincides with weakness in equity markets, "
            "especially in <b>Banking and Real Estate</b> sectors. "
            "Historically, rising gold correlates with <b>INR depreciation</b> and global uncertainty."
        )
    elif gold_change_pct < -3:
        gold_tag = '<span class="tag-gold-down">🔻 FALLING</span>'
        gold_message = (
            f"Gold has declined by <b>{abs(gold_change_pct):.1f}%</b> in the last month "
            f"(₹{gold_1m_ago:,.0f} → ₹{gold_latest:,.0f}). "
            "Falling gold prices indicate <b>risk-on sentiment</b> — investors are confident and moving capital "
            "into equities for higher returns. This is typically bullish for <b>cyclical and growth sectors</b> "
            "like IT, Auto, and Banking. Market breadth tends to expand in such environments."
        )
    else:
        gold_tag = '<span class="tag-stable">➡️ FLAT</span>'
        gold_message = (
            f"Gold has moved only <b>{gold_change_pct:+.1f}%</b> in the last month "
            f"(₹{gold_1m_ago:,.0f} → ₹{gold_latest:,.0f}). "
            "Stable gold prices suggest <b>neutral macro sentiment</b> — neither fear nor greed is dominating. "
            "In such environments, sector rotation is driven more by <b>earnings and fundamentals</b> "
            "rather than macro flows. Stock-picking and relative strength analysis become more valuable."
        )
else:
    gold_tag = ''
    gold_message = 'Insufficient gold data for 1-month comparison.'

# Render Analysis Box
html_parts = []
html_parts.append('<div class="insight-box">')
html_parts.append('<h4>🔮 Market Intelligence Report</h4>')
html_parts.append('<p style="margin-bottom:6px;"><b style="color:#f87171;">VIX Analysis</b> ' + vix_tag + '</p>')
html_parts.append('<p style="margin-bottom:20px;">' + vix_message + '</p>')
html_parts.append('<p style="margin-bottom:6px;"><b style="color:#fbbf24;">Gold Analysis</b> ' + gold_tag + '</p>')
html_parts.append('<p>' + gold_message + '</p>')
html_parts.append('</div>')
analysis_html = '\n'.join(html_parts)
st.markdown(analysis_html, unsafe_allow_html=True)

# ── Footer ───────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<p class="footer-text">'
    '<span>Yash Kalra (23/IT/178) | Sumay Mittal (23/IT/163)</span> · Data Engineering & Analytics Project · DTU 2026'
    '</p>',
    unsafe_allow_html=True
)
