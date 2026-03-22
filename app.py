"""
EurasianKnowledge — Investor Platform
Streamlit app with Anthropic AI assistant
"""

import streamlit as st
import anthropic
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import json
import time
from datetime import datetime, timedelta

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EurasianKnowledge — Investor Platform",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Global CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}
.stApp {
    background: #0c0e14;
    color: #d4c5a9;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #10121a !important;
    border-right: 1px solid rgba(201,169,110,0.1);
}
[data-testid="stSidebar"] * { color: #94a3b8 !important; }
[data-testid="stSidebar"] .sidebar-title {
    color: #f0e6d3 !important;
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.4rem;
    font-weight: 700;
}

/* ── Cards ── */
.ek-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: border-color 0.3s;
}
.ek-card:hover { border-color: rgba(201,169,110,0.25); }

/* ── KPI ── */
.kpi-block {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    text-align: center;
}
.kpi-value {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: #f0e6d3;
    line-height: 1.1;
}
.kpi-label { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; color: #6b7280; margin-top: 4px; }
.kpi-trend { font-size: 0.75rem; font-weight: 600; color: #c9a96e; margin-top: 2px; }

/* ── Section Header ── */
.section-header {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: #f0e6d3;
    margin-bottom: 0.3rem;
}
.section-sub { font-size: 0.85rem; color: #6b7280; margin-bottom: 1.5rem; }

/* ── Tag ── */
.ek-tag {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 999px;
    background: rgba(201,169,110,0.12);
    border: 1px solid rgba(201,169,110,0.25);
    color: #c9a96e;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* ── Chat ── */
.chat-user {
    background: rgba(201,169,110,0.1);
    border: 1px solid rgba(201,169,110,0.2);
    border-radius: 14px 14px 4px 14px;
    padding: 0.8rem 1rem;
    margin: 0.5rem 0;
    color: #f0e6d3;
    font-size: 0.9rem;
}
.chat-ai {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 14px 14px 14px 4px;
    padding: 0.8rem 1rem;
    margin: 0.5rem 0;
    color: #d4c5a9;
    font-size: 0.9rem;
    line-height: 1.6;
}

/* ── Hero ── */
.hero-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(2rem, 5vw, 3.5rem);
    font-weight: 700;
    color: #f0e6d3;
    line-height: 1.1;
    letter-spacing: -0.02em;
}
.hero-gold { color: #c9a96e; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #c9a96e, #e2c99a) !important;
    color: #0c0e14 !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.5rem 1.5rem !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.88 !important; }

/* secondary button override via class */
.btn-secondary > button {
    background: rgba(255,255,255,0.04) !important;
    color: #94a3b8 !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
}
.btn-secondary > button:hover {
    border-color: rgba(201,169,110,0.4) !important;
    color: #c9a96e !important;
}

/* ── Inputs ── */
.stTextInput > div > input, .stTextArea textarea, .stSelectbox div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #f0e6d3 !important;
}
.stTextInput > div > input::placeholder { color: #4b5563 !important; }
.stTextInput > div > input:focus, .stTextArea textarea:focus {
    border-color: rgba(201,169,110,0.5) !important;
    box-shadow: 0 0 0 2px rgba(201,169,110,0.1) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03);
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
    border: 1px solid rgba(255,255,255,0.07);
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #6b7280;
    border-radius: 8px;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.82rem;
    font-weight: 600;
    padding: 0.4rem 1rem;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #c9a96e, #e2c99a) !important;
    color: #0c0e14 !important;
}

/* ── Progress bars ── */
.stProgress > div > div { background: linear-gradient(90deg, #c9a96e, #e2c99a) !important; border-radius: 99px !important; }
.stProgress > div { background: rgba(255,255,255,0.06) !important; border-radius: 99px !important; }

/* ── Divider ── */
hr { border-color: rgba(255,255,255,0.07) !important; }

/* ── Metrics ── */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 1rem 1.2rem;
}
[data-testid="stMetricLabel"] { color: #6b7280 !important; font-size: 0.7rem !important; text-transform: uppercase !important; letter-spacing: 0.08em !important; }
[data-testid="stMetricValue"] { color: #f0e6d3 !important; font-family: 'Cormorant Garamond', serif !important; font-size: 2rem !important; }
[data-testid="stMetricDelta"] { color: #c9a96e !important; }

/* ── Alerts ── */
.stAlert { border-radius: 12px !important; }

/* ── Plotly charts background fix ── */
.js-plotly-plot { border-radius: 14px; overflow: hidden; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(201,169,110,0.3); border-radius: 99px; }

/* hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─── Colour palette for charts ────────────────────────────────────────────────
CHART_THEME = dict(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="#94a3b8", size=11),
    xaxis=dict(gridcolor="rgba(255,255,255,0.05)", linecolor="rgba(255,255,255,0.07)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.05)", linecolor="rgba(255,255,255,0.07)"),
    margin=dict(l=10, r=10, t=20, b=10),
)
GOLD = "#c9a96e"
GOLD_LIGHT = "#e2c99a"
BLUE = "#7eb8d4"
GREEN = "#88c9a0"

# ─── Session State Init ───────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "active_section" not in st.session_state:
    st.session_state.active_section = "dashboard"
if "client" not in st.session_state:
    st.session_state.client = None

# ─── Mock Data ────────────────────────────────────────────────────────────────
@st.cache_data
def get_revenue_data():
    months = ["Янв", "Фев", "Мар", "Апр", "Май", "Июн", "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек"]
    revenue = [42, 59, 53, 77, 67, 101, 91, 129, 118, 145, 162, 190]
    users = [2800, 3400, 3100, 4200, 4900, 6300, 7100, 9200, 10400, 12100, 14500, 17800]
    books = [38, 52, 46, 71, 88, 110, 104, 138, 151, 172, 198, 230]
    return pd.DataFrame({"month": months, "revenue": revenue, "users": users, "books": books})

@st.cache_data
def get_geo_data():
    return pd.DataFrame({
        "country": ["Казахстан", "Россия", "Китай", "Узбекистан", "Кыргызстан", "Германия", "США"],
        "users": [18400, 9200, 4100, 2800, 1300, 980, 720],
        "revenue_share": [48, 24, 11, 7, 4, 3, 3],
        "lat": [48.0, 61.5, 35.9, 41.4, 41.2, 51.2, 37.1],
        "lon": [68.0, 105.3, 104.2, 64.6, 74.7, 10.4, -95.7],
    })

@st.cache_data
def get_caspian_data():
    """Mock environmental sensor data for Caspian region"""
    np.random.seed(42)
    return pd.DataFrame({
        "station": ["Актау", "Баку", "Астрахань", "Туркменбаши", "Энзели"],
        "water_level": [np.random.uniform(-28.5, -27.8) for _ in range(5)],
        "salinity": [np.random.uniform(12.5, 13.5) for _ in range(5)],
        "temp": [np.random.uniform(10, 24) for _ in range(5)],
        "oil_index": [np.random.uniform(0.02, 0.18) for _ in range(5)],
        "lat": [43.65, 40.41, 46.35, 40.02, 37.47],
        "lon": [51.17, 49.87, 48.03, 53.00, 49.47],
    })

# ─── Chart helpers ────────────────────────────────────────────────────────────
def revenue_chart(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["month"], y=df["revenue"],
        fill="tozeroy",
        fillcolor="rgba(201,169,110,0.08)",
        line=dict(color=GOLD, width=2.5),
        mode="lines+markers",
        marker=dict(color=GOLD, size=6, line=dict(color="#0c0e14", width=2)),
        name="Выручка $K",
        hovertemplate="<b>%{x}</b><br>$%{y}K<extra></extra>",
    ))
    fig.update_layout(**CHART_THEME, height=260, showlegend=False)
    return fig

def users_chart(df):
    fig = go.Figure(go.Bar(
        x=df["month"], y=df["users"],
        marker=dict(
            color=df["users"],
            colorscale=[[0, "rgba(126,184,212,0.3)"], [1, BLUE]],
            line=dict(width=0),
        ),
        hovertemplate="<b>%{x}</b><br>%{y:,} пользователей<extra></extra>",
    ))
    fig.update_layout(**CHART_THEME, height=260, showlegend=False)
    return fig

def books_chart(df):
    fig = go.Figure(go.Bar(
        x=df["month"], y=df["books"],
        marker=dict(color=GREEN, opacity=0.75, line=dict(width=0)),
        hovertemplate="<b>%{x}</b><br>%{y} продаж<extra></extra>",
    ))
    fig.update_layout(**CHART_THEME, height=260, showlegend=False)
    return fig

def geo_map(df):
    fig = px.scatter_geo(
        df, lat="lat", lon="lon", size="users",
        color="revenue_share", color_continuous_scale=[[0, "#1e2030"], [0.5, "#4a3820"], [1, GOLD]],
        hover_name="country",
        hover_data={"users": True, "revenue_share": True, "lat": False, "lon": False},
        size_max=45,
    )
    fig.update_layout(
        geo=dict(
            bgcolor="rgba(0,0,0,0)",
            showland=True, landcolor="#1a1e2e",
            showocean=True, oceancolor="#0d1020",
            showcoastlines=True, coastlinecolor="rgba(255,255,255,0.1)",
            showframe=False, projection_type="natural earth",
            center=dict(lat=45, lon=65), projection_scale=2.2,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False,
        margin=dict(l=0, r=0, t=0, b=0),
        height=340,
    )
    return fig

def caspian_scatter(df):
    fig = px.scatter_mapbox(
        df, lat="lat", lon="lon", size="oil_index",
        color="temp", color_continuous_scale=[[0, BLUE], [0.5, GOLD], [1, "#ef4444"]],
        hover_name="station",
        hover_data={"water_level": ":.2f", "salinity": ":.1f", "temp": ":.1f", "oil_index": ":.3f", "lat": False, "lon": False},
        size_max=35, zoom=3.8,
        center={"lat": 42, "lon": 51},
    )
    fig.update_layout(
        mapbox_style="carto-darkmatter",
        paper_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False,
        margin=dict(l=0, r=0, t=0, b=0),
        height=380,
    )
    return fig

def funnel_chart():
    fig = go.Figure(go.Funnel(
        y=["TAM · $4.2B", "SAM · $620M", "SOM · $38M", "Текущий ARR · $820K"],
        x=[4200, 620, 38, 0.82],
        textinfo="label+percent initial",
        marker=dict(color=[
            "rgba(201,169,110,0.25)", "rgba(201,169,110,0.45)",
            "rgba(201,169,110,0.7)", GOLD
        ], line=dict(width=0)),
        connector=dict(line=dict(color="rgba(255,255,255,0.05)")),
        hovertemplate="<b>%{label}</b><br>$%{x}M<extra></extra>",
    ))
    fig.update_layout(**CHART_THEME, height=280, showlegend=False)
    return fig

def pie_funds():
    fig = go.Figure(go.Pie(
        labels=["Продукт & AI", "Маркетинг & GTM", "Команда", "Операции"],
        values=[40, 30, 20, 10],
        hole=0.65,
        marker=dict(colors=[GOLD, BLUE, GREEN, "#d4907e"], line=dict(color="#0c0e14", width=2)),
        textinfo="none",
        hovertemplate="<b>%{label}</b><br>%{value}%<extra></extra>",
    ))
    fig.add_annotation(text="$1.5M", x=0.5, y=0.5, font=dict(size=22, color="#f0e6d3", family="Cormorant Garamond"), showarrow=False)
    fig.update_layout(**CHART_THEME, height=260, showlegend=True,
        legend=dict(font=dict(color="#6b7280", size=10), bgcolor="rgba(0,0,0,0)"))
    return fig

# ─── AI Client ────────────────────────────────────────────────────────────────
def get_client(api_key: str):
    return anthropic.Anthropic(api_key=api_key)

SYSTEM_PROMPT = """Ты — Author AI-Ассистент платформы EurasianKnowledge. 
Ты эксперт по:
- Экономике Каспийского региона, СНГ, Китая и Центральной Азии
- Нефтяным рынкам, экспортной аналитике, геополитике Евразии
- 5 авторским книгам платформы: «Қаңтар» (политология), «Жануарлар» (детская энциклопедия на казахском), 
  «Каспий: экология и ресурсы», «Экономика Шёлкового пути», «Цифровая трансформация ЦА»
- KPI и инвестиционной аналитике платформы (ARR $820K, MAU 38K, Seed Round $1.5M)

Отвечай профессионально, по делу. Умей:
1. Писать аннотации к книгам
2. Составлять executive summary по экономическим темам
3. Анализировать рыночные возможности
4. Отвечать на вопросы инвесторов
5. Генерировать контент для презентаций

Формат ответа: чёткий, структурированный. Используй заголовки и списки где уместно."""

def stream_ai_response(client, messages):
    with client.messages.stream(
        model="claude-sonnet-4-20250514",
        max_tokens=1200,
        system=SYSTEM_PROMPT,
        messages=messages,
    ) as stream:
        for text in stream.text_stream:
            yield text

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-title">🌐 EurasianKnowledge</div>', unsafe_allow_html=True)
    st.markdown('<span class="ek-tag">Investor Platform · Seed</span>', unsafe_allow_html=True)
    st.markdown("---")

    section = st.radio(
        "Навигация",
        ["📊 Dashboard", "🗺️ GIS Каспий", "📚 Edu Module", "🤖 AI Ассистент", "💼 Инвесторам"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown('<div style="font-size:0.7rem;color:#4b5563;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px;">API Key</div>', unsafe_allow_html=True)
    api_key = st.text_input("Anthropic API Key", type="password", placeholder="sk-ant-...", label_visibility="collapsed")
    if api_key:
        try:
            st.session_state.client = get_client(api_key)
            st.markdown('<div style="color:#88c9a0;font-size:0.75rem;">✓ Подключено</div>', unsafe_allow_html=True)
        except Exception:
            st.markdown('<div style="color:#ef4444;font-size:0.75rem;">✗ Неверный ключ</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="color:#4b5563;font-size:0.72rem;">Введите ключ для AI-функций</div>', unsafe_allow_html=True)

    st.markdown("---")
    lang = st.selectbox("Язык", ["RU", "KZ", "EN"], label_visibility="collapsed")
    
    st.markdown('<div style="margin-top:2rem;font-size:0.68rem;color:#374151;line-height:1.6;">© 2025 EurasianKnowledge<br>Seed Round closes Mar 31</div>', unsafe_allow_html=True)

# ─── Route sections ───────────────────────────────────────────────────────────
df = get_revenue_data()
geo_df = get_geo_data()
caspian_df = get_caspian_data()

# ════════════════════════════════════════════════════════════════════════
if section == "📊 Dashboard":
# ════════════════════════════════════════════════════════════════════════

    st.markdown("""
    <div style="margin-bottom:0.5rem;">
        <span class="ek-tag">Seed Round · Q1 2025</span>
    </div>
    <div class="hero-title">Цифровая Экосистема<br><span class="hero-gold">Евразийских Знаний</span></div>
    <div class="section-sub" style="font-size:0.95rem;margin-top:0.5rem;">
        Аналитическая платформа для инвесторов — данные в реальном времени.
    </div>
    """, unsafe_allow_html=True)

    # KPI row
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("TAM 2025", "$4.2B", "СНГ + Китай + Индия")
    with k2:
        st.metric("MAU", "38 K", "+127% г/г")
    with k3:
        st.metric("ARR", "$820 K", "+34% MRR")
    with k4:
        st.metric("Раунд", "Seed", "Seeking $1.5M")

    st.markdown("---")

    # Charts
    tab1, tab2, tab3 = st.tabs(["💰 Выручка", "👥 Пользователи", "📚 Продажи книг"])
    with tab1:
        col_a, col_b = st.columns([3, 1])
        with col_a:
            st.plotly_chart(revenue_chart(df), use_container_width=True, config={"displayModeBar": False})
        with col_b:
            st.markdown('<div class="section-header" style="font-size:1.2rem;">Метрики</div>', unsafe_allow_html=True)
            for label, val, trend in [("MRR Growth", "+34%", ""), ("Churn Rate", "2.1%", ""), ("LTV/CAC", "4.7×", ""), ("Gross Margin", "72%", "")]:
                st.markdown(f"""<div class="kpi-block" style="text-align:left;padding:0.8rem;">
                    <div class="kpi-label">{label}</div>
                    <div class="kpi-value" style="font-size:1.6rem;color:#c9a96e;">{val}</div>
                </div>""", unsafe_allow_html=True)
    with tab2:
        st.plotly_chart(users_chart(df), use_container_width=True, config={"displayModeBar": False})
    with tab3:
        st.plotly_chart(books_chart(df), use_container_width=True, config={"displayModeBar": False})

    st.markdown("---")

    # Geo + Funds
    col_map, col_pie = st.columns([3, 2])
    with col_map:
        st.markdown('<div class="section-header" style="font-size:1.2rem;">🌍 География аудитории</div>', unsafe_allow_html=True)
        st.plotly_chart(geo_map(geo_df), use_container_width=True, config={"displayModeBar": False})
    with col_pie:
        st.markdown('<div class="section-header" style="font-size:1.2rem;">💼 Use of Funds</div>', unsafe_allow_html=True)
        st.plotly_chart(pie_funds(), use_container_width=True, config={"displayModeBar": False})
        for item, pct in [("Продукт & AI", 40), ("Маркетинг & GTM", 30), ("Команда", 20), ("Операции", 10)]:
            c1, c2 = st.columns([3, 1])
            with c1:
                st.progress(pct / 100)
            with c2:
                st.markdown(f'<div style="color:#c9a96e;font-size:0.8rem;font-weight:600;margin-top:2px;">{item} {pct}%</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════
elif section == "🗺️ GIS Каспий":
# ════════════════════════════════════════════════════════════════════════

    st.markdown("""
    <span class="ek-tag">Live GIS · Мониторинг</span>
    <div class="hero-title" style="font-size:2.2rem;margin-top:0.5rem;">Каспийский бассейн</div>
    <div class="section-sub">Экологический мониторинг, спутниковые данные и анализ месторождений.</div>
    """, unsafe_allow_html=True)

    # Station metrics
    cols = st.columns(5)
    for i, (_, row) in enumerate(caspian_df.iterrows()):
        with cols[i]:
            oil_color = "#ef4444" if row["oil_index"] > 0.12 else "#88c9a0"
            st.markdown(f"""<div class="kpi-block">
                <div class="kpi-label">{row["station"]}</div>
                <div class="kpi-value" style="font-size:1.3rem;">{row["temp"]:.1f}°C</div>
                <div style="font-size:0.65rem;color:{oil_color};margin-top:3px;">Нефть: {row["oil_index"]:.3f}</div>
                <div style="font-size:0.65rem;color:#6b7280;margin-top:1px;">Ур. воды: {row["water_level"]:.2f} м</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.plotly_chart(caspian_scatter(caspian_df), use_container_width=True, config={"displayModeBar": False})

    st.markdown("---")
    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown('<div class="section-header" style="font-size:1.1rem;">📋 Данные станций</div>', unsafe_allow_html=True)
        display_df = caspian_df[["station", "temp", "salinity", "water_level", "oil_index"]].copy()
        display_df.columns = ["Станция", "Темп °C", "Солёность ‰", "Уровень м", "Нефть-индекс"]
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    with col_r:
        st.markdown('<div class="section-header" style="font-size:1.1rem;">📊 Температура по станциям</div>', unsafe_allow_html=True)
        fig = go.Figure(go.Bar(
            x=caspian_df["station"], y=caspian_df["temp"],
            marker=dict(color=caspian_df["temp"], colorscale=[[0, BLUE], [1, GOLD]], line=dict(width=0)),
            hovertemplate="<b>%{x}</b><br>%{y:.1f}°C<extra></extra>",
        ))
        fig.update_layout(**CHART_THEME, height=240, showlegend=False)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    if st.session_state.client:
        st.markdown("---")
        if st.button("🤖 AI-анализ экологической обстановки"):
            prompt = f"Сделай краткий экологический отчёт по данным мониторинга Каспия: {caspian_df.to_dict('records')}"
            with st.spinner("Генерирую отчёт..."):
                full = ""
                placeholder = st.empty()
                for chunk in stream_ai_response(st.session_state.client, [{"role": "user", "content": prompt}]):
                    full += chunk
                    placeholder.markdown(f'<div class="chat-ai">{full}▌</div>', unsafe_allow_html=True)
                placeholder.markdown(f'<div class="chat-ai">{full}</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════
elif section == "📚 Edu Module":
# ════════════════════════════════════════════════════════════════════════

    st.markdown("""
    <span class="ek-tag">Edu Module · Казахский контент</span>
    <div class="hero-title" style="font-size:2.2rem;margin-top:0.5rem;">Книги & Энциклопедии</div>
    <div class="section-sub">Мультиязычный образовательный контент с AI-озвучкой.</div>
    """, unsafe_allow_html=True)

    BOOKS = [
        {"title": "Қаңтар", "sub": "Политологический анализ", "emoji": "📕", "tag": "Политология", "progress": 100, "sales": 312, "color": "#d4907e"},
        {"title": "Жануарлар", "sub": "Детская энциклопедия на казахском", "emoji": "🦁", "tag": "Edu · KZ", "progress": 68, "sales": 284, "color": "#88c9a0"},
        {"title": "Каспий: экология", "sub": "Ресурсы и мониторинг", "emoji": "🌊", "tag": "Наука", "progress": 85, "sales": 98, "color": "#7eb8d4"},
        {"title": "Экономика Шёлкового пути", "sub": "Торговые маршруты XXI века", "emoji": "🗺️", "tag": "Аналитика", "progress": 90, "sales": 104, "color": GOLD},
        {"title": "Цифровая трансформация ЦА", "sub": "IT-экосистема Центральной Азии", "emoji": "💻", "tag": "Tech", "progress": 75, "sales": 44, "color": "#a78bfa"},
    ]

    cols = st.columns(3)
    for i, book in enumerate(BOOKS):
        with cols[i % 3]:
            st.markdown(f"""<div class="ek-card" style="border-color:rgba({','.join(str(int(book['color'].lstrip('#')[j:j+2], 16)) for j in (0,2,4))},0.3);">
                <div style="font-size:2.2rem;margin-bottom:0.5rem;">{book['emoji']}</div>
                <span class="ek-tag" style="font-size:0.6rem;">{book['tag']}</span>
                <div style="font-family:'Cormorant Garamond',serif;font-size:1.3rem;font-weight:700;color:#f0e6d3;margin:0.5rem 0 0.2rem;">{book['title']}</div>
                <div style="font-size:0.78rem;color:#6b7280;margin-bottom:0.8rem;">{book['sub']}</div>
                <div style="display:flex;justify-content:space-between;font-size:0.7rem;color:#6b7280;margin-bottom:4px;">
                    <span>Готовность</span><span style="color:{book['color']}">{book['progress']}%</span>
                </div>
            </div>""", unsafe_allow_html=True)
            st.progress(book["progress"] / 100)
            st.markdown(f'<div style="font-size:0.72rem;color:#6b7280;margin-bottom:0.5rem;">Продажи: <span style="color:{book["color"]}">{book["sales"]}</span></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-header" style="font-size:1.2rem;">🤖 AI-генератор контента</div>', unsafe_allow_html=True)

    col_l, col_r = st.columns(2)
    with col_l:
        selected_book = st.selectbox("Выберите книгу", [b["title"] for b in BOOKS])
        content_type = st.selectbox("Тип контента", ["Аннотация (200 слов)", "Executive Summary", "Маркетинговое описание", "Оглавление", "Вопросы для интервью"])
    with col_r:
        extra = st.text_area("Дополнительный контекст (необязательно)", height=108, placeholder="Например: для LinkedIn-поста, для инвесторов...")

    if st.button("✨ Сгенерировать"):
        if not st.session_state.client:
            st.warning("Введите Anthropic API Key в боковой панели.")
        else:
            prompt = f"Напиши '{content_type}' для книги '{selected_book}'. {extra}"
            full = ""
            placeholder = st.empty()
            for chunk in stream_ai_response(st.session_state.client, [{"role": "user", "content": prompt}]):
                full += chunk
                placeholder.markdown(f'<div class="chat-ai">{full}▌</div>', unsafe_allow_html=True)
            placeholder.markdown(f'<div class="chat-ai">{full}</div>', unsafe_allow_html=True)
            st.download_button("⬇️ Скачать текст", data=full, file_name=f"{selected_book}_{content_type}.txt", mime="text/plain")

# ════════════════════════════════════════════════════════════════════════
elif section == "🤖 AI Ассистент":
# ════════════════════════════════════════════════════════════════════════

    st.markdown("""
    <span class="ek-tag">Author AI · v2.0</span>
    <div class="hero-title" style="font-size:2.2rem;margin-top:0.5rem;">AI-Ассистент</div>
    <div class="section-sub">Обучен на 5 книгах и 38 аналитических статьях автора.</div>
    """, unsafe_allow_html=True)

    if not st.session_state.client:
        st.info("🔑 Введите Anthropic API Key в боковой панели, чтобы активировать AI-ассистента.")

    # Quick prompts
    st.markdown('<div style="margin-bottom:0.8rem;font-size:0.72rem;color:#4b5563;text-transform:uppercase;letter-spacing:0.1em;">Быстрые запросы</div>', unsafe_allow_html=True)
    quick_prompts = [
        "📊 Аналитика ВВП Казахстана 2024",
        "📝 Аннотация к книге «Қаңтар»",
        "🛢️ Обзор нефтяного рынка СНГ",
        "💡 Почему инвестировать в EurasianKnowledge?",
        "🌊 Экологический статус Каспия",
        "📈 Executive summary платформы",
    ]
    cols = st.columns(3)
    quick_input = None
    for i, qp in enumerate(quick_prompts):
        with cols[i % 3]:
            if st.button(qp, key=f"qp_{i}"):
                quick_input = qp

    st.markdown("---")

    # Chat history
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-user">🧑 {msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-ai">🤖 {msg["content"]}</div>', unsafe_allow_html=True)

    # Input
    user_input = st.chat_input("Задайте вопрос или запросите аналитику...")
    final_input = user_input or quick_input

    if final_input and st.session_state.client:
        st.session_state.chat_history.append({"role": "user", "content": final_input})
        st.markdown(f'<div class="chat-user">🧑 {final_input}</div>', unsafe_allow_html=True)

        messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_history]
        full = ""
        placeholder = st.empty()
        for chunk in stream_ai_response(st.session_state.client, messages):
            full += chunk
            placeholder.markdown(f'<div class="chat-ai">🤖 {full}▌</div>', unsafe_allow_html=True)
        placeholder.markdown(f'<div class="chat-ai">🤖 {full}</div>', unsafe_allow_html=True)

        st.session_state.chat_history.append({"role": "assistant", "content": full})

    elif final_input and not st.session_state.client:
        st.warning("Введите API Key в боковой панели.")

    if st.session_state.chat_history:
        if st.button("🗑️ Очистить чат"):
            st.session_state.chat_history = []
            st.rerun()

# ════════════════════════════════════════════════════════════════════════
elif section == "💼 Инвесторам":
# ════════════════════════════════════════════════════════════════════════

    st.markdown("""
    <span class="ek-tag">Investor Relations</span>
    <div class="hero-title" style="font-size:2.2rem;margin-top:0.5rem;">Инвестиционный кейс</div>
    <div class="section-sub">Seed Round · $1.5M · Закрытие 31 марта 2025</div>
    """, unsafe_allow_html=True)

    # Market funnel
    col_f, col_t = st.columns([3, 2])
    with col_f:
        st.markdown('<div class="section-header" style="font-size:1.1rem;">📐 Рыночная возможность</div>', unsafe_allow_html=True)
        st.plotly_chart(funnel_chart(), use_container_width=True, config={"displayModeBar": False})
    with col_t:
        st.markdown('<div class="section-header" style="font-size:1.1rem;">🏆 Конкурентные преимущества</div>', unsafe_allow_html=True)
        advantages = [
            ("🌐", "Единственная мультиязычная (KZ/RU/EN/ZH) B2B+B2C платформа в регионе"),
            ("🤖", "AI-ассистент обученный на авторском контенте"),
            ("🗺️", "Эксклюзивная GIS-база по Каспийскому бассейну"),
            ("📚", "5 авторских книг + 38 статей как IP-актив"),
            ("💰", "3 revenue streams: SaaS, книги, API-доступ"),
        ]
        for icon, text in advantages:
            st.markdown(f'<div class="ek-card" style="padding:0.8rem 1rem;"><span style="font-size:1.1rem;">{icon}</span> <span style="font-size:0.85rem;color:#d4c5a9;">{text}</span></div>', unsafe_allow_html=True)

    st.markdown("---")

    # Traction
    st.markdown('<div class="section-header" style="font-size:1.1rem;">📈 Traction</div>', unsafe_allow_html=True)
    t1, t2, t3, t4, t5 = st.columns(5)
    for col, label, val, trend in zip(
        [t1, t2, t3, t4, t5],
        ["ARR", "MAU", "NPS", "Retention (M1)", "Книг продано"],
        ["$820K", "38 K", "71", "64%", "842"],
        ["+34%", "+127%", "↑ отлично", "↑ выше рынка", "+89%"],
    ):
        with col:
            st.markdown(f"""<div class="kpi-block">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value" style="font-size:1.5rem;">{val}</div>
                <div class="kpi-trend">{trend}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # AI-generated pitch
    st.markdown('<div class="section-header" style="font-size:1.1rem;">🤖 AI-генератор питча</div>', unsafe_allow_html=True)
    col_in, col_btn = st.columns([3, 1])
    with col_in:
        investor_type = st.selectbox("Профиль инвестора", [
            "Венчурный фонд (ЦА/СНГ)", "Стратегический инвестор (медиа/EdTech)",
            "Семейный офис", "Государственный фонд (Казахстан)", "Международный фонд (США/Европа)"
        ])
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        gen_pitch = st.button("✨ Сгенерировать питч")

    if gen_pitch:
        if not st.session_state.client:
            st.warning("Введите API Key в боковой панели.")
        else:
            prompt = f"""Напиши инвестиционный питч (300-400 слов) для EurasianKnowledge, 
адаптированный под: {investor_type}. 
Используй данные: ARR $820K (+34% MRR), MAU 38K (+127% г/г), Seed Round $1.5M, 
TAM $4.2B (СНГ+Китай+Индия), продукт: B2B/B2C платформа знаний с AI-ассистентом."""
            full = ""
            placeholder = st.empty()
            for chunk in stream_ai_response(st.session_state.client, [{"role": "user", "content": prompt}]):
                full += chunk
                placeholder.markdown(f'<div class="chat-ai">{full}▌</div>', unsafe_allow_html=True)
            placeholder.markdown(f'<div class="chat-ai">{full}</div>', unsafe_allow_html=True)
            st.download_button("⬇️ Скачать питч", data=full, file_name=f"EK_pitch_{investor_type}.txt", mime="text/plain")

    st.markdown("---")
    st.markdown("""<div class="ek-card" style="text-align:center;padding:2.5rem;background:linear-gradient(135deg,rgba(201,169,110,0.08),transparent);border-color:rgba(201,169,110,0.25);">
        <div style="font-family:'Cormorant Garamond',serif;font-size:2rem;font-weight:700;color:#f0e6d3;margin-bottom:0.5rem;">Присоединитесь к раунду</div>
        <div style="color:#6b7280;margin-bottom:1.5rem;font-size:0.9rem;">Минимальный чек $50K · Закрытие 31 марта 2025 · Прогресс раунда: 60%</div>
    </div>""", unsafe_allow_html=True)
    st.progress(0.6)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="section-sub" style="text-align:center;">$900K собрано из $1.5M</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="section-sub" style="text-align:center;">3 инвестора подтверждены</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="section-sub" style="text-align:center;">9 дней до закрытия</div>', unsafe_allow_html=True)
