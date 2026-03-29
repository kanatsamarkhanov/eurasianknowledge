"""
Kulekeyev Intelligence Hub
Цифровая интеллектуальная платформа Жаксыбека Абдрахметовича Кулекеева
Streamlit · Light/Dark · Anthropic AI
"""

import streamlit as st
import anthropic
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Kulekeyev Intelligence Hub",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Session State ────────────────────────────────────────────────────────────
if "dark_mode"     not in st.session_state: st.session_state.dark_mode    = True
if "chat_history"  not in st.session_state: st.session_state.chat_history = []
if "client"        not in st.session_state: st.session_state.client       = None

D = st.session_state.dark_mode

# ─── Theme Tokens ─────────────────────────────────────────────────────────────
if D:
    BG       = "#0b0e16"
    BG2      = "#0f1220"
    CARD     = "rgba(255,255,255,0.04)"
    BORDER   = "rgba(255,255,255,0.08)"
    BORDER_G = "rgba(201,169,110,0.30)"
    TEXT     = "#f0e8d5"
    TEXT2    = "#8fa3b8"
    TEXT3    = "#3f5060"
    PLOT_BG  = "rgba(0,0,0,0)"
    PLOT_F   = "#8fa3b8"
    GRID     = "rgba(255,255,255,0.05)"
    MAPST    = "carto-darkmatter"
    GLAND    = "#161c2e"
    GOCEAN   = "#0b1018"
    GCOAST   = "rgba(255,255,255,0.10)"
    SHADOW   = "rgba(0,0,0,0.45)"
    INP_BG   = "rgba(255,255,255,0.05)"
    HERO_BG  = "linear-gradient(135deg,#0d1225 0%,#141b38 55%,#0b0e16 100%)"
    GOLD_D   = "rgba(201,169,110,0.12)"
else:
    # Sage-green + gold light palette
    BG       = "#f0f7f4"
    BG2      = "#e2ede8"
    CARD     = "#ffffff"
    BORDER   = "rgba(20,80,60,0.08)"
    BORDER_G = "rgba(180,130,55,0.35)"
    TEXT     = "#0f2922"
    TEXT2    = "#3d6e5e"
    TEXT3    = "#7aaa95"
    PLOT_BG  = "rgba(0,0,0,0)"
    PLOT_F   = "#3d6e5e"
    GRID     = "rgba(20,80,60,0.07)"
    MAPST    = "carto-positron"
    GLAND    = "#d4ece3"
    GOCEAN   = "#b8d8e8"
    GCOAST   = "rgba(0,0,0,0.12)"
    SHADOW   = "rgba(15,41,34,0.08)"
    INP_BG   = "rgba(20,80,60,0.04)"
    HERO_BG  = "linear-gradient(135deg,#e2f5ed 0%,#f4fdf8 55%,#dff0e8 100%)"
    GOLD_D   = "rgba(201,169,110,0.13)"

GOLD  = "#c9a96e"
GOLDL = "#e2c99a"
BLUE  = "#7eb8d4"
GREEN = "#4eca8b"
RED   = "#e07070"

CT = dict(
    plot_bgcolor=PLOT_BG, paper_bgcolor=PLOT_BG,
    font=dict(family="DM Sans", color=PLOT_F, size=11),
    xaxis=dict(gridcolor=GRID, linecolor=GRID, tickfont=dict(color=PLOT_F)),
    yaxis=dict(gridcolor=GRID, linecolor=GRID, tickfont=dict(color=PLOT_F)),
    margin=dict(l=10, r=10, t=20, b=10),
)

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400&family=DM+Sans:wght@300;400;500;600&display=swap');
*,html,body{{font-family:'DM Sans',sans-serif;box-sizing:border-box;}}
.stApp,.stApp>div{{background:{BG}!important;color:{TEXT}!important;}}
.main .block-container{{padding-top:1.4rem;padding-bottom:3rem;max-width:1200px;}}
[data-testid="stSidebar"]{{background:{BG2}!important;border-right:1px solid {BORDER};}}
[data-testid="stSidebar"] *{{color:{TEXT2}!important;}}
::-webkit-scrollbar{{width:4px;height:4px;}}
::-webkit-scrollbar-thumb{{background:{GOLD}55;border-radius:99px;}}

/* Cards */
.ek-card{{background:{CARD};border:1px solid {BORDER};border-radius:18px;padding:1.4rem 1.5rem;margin-bottom:1rem;
  box-shadow:0 2px 16px {SHADOW};transition:border-color .25s,box-shadow .25s,transform .2s;}}
.ek-card:hover{{border-color:{BORDER_G};box-shadow:0 6px 28px {SHADOW};transform:translateY(-2px);}}

/* Direction cards */
.dir-card{{background:{CARD};border:1px solid {BORDER};border-radius:16px;padding:1.3rem 1.4rem;height:100%;
  box-shadow:0 1px 10px {SHADOW};transition:all .25s;}}
.dir-card:hover{{border-color:{BORDER_G};transform:translateY(-3px);box-shadow:0 8px 24px {SHADOW};}}
.dir-icon{{font-size:1.8rem;margin-bottom:.6rem;}}
.dir-title{{font-family:'Cormorant Garamond',serif;font-size:1.05rem;font-weight:700;color:{TEXT};margin-bottom:.3rem;}}
.dir-sub{{font-size:.72rem;color:{TEXT3};line-height:1.5;}}

/* KPI */
.kpi-block{{background:{CARD};border:1px solid {BORDER};border-radius:16px;padding:1.1rem 1rem;text-align:center;
  box-shadow:0 1px 8px {SHADOW};transition:transform .2s;}}
.kpi-block:hover{{transform:translateY(-3px);}}
.kpi-value{{font-family:'Cormorant Garamond',serif;font-size:2rem;font-weight:700;color:{TEXT};line-height:1.1;}}
.kpi-label{{font-size:.65rem;text-transform:uppercase;letter-spacing:.1em;color:{TEXT3};margin-top:4px;}}
.kpi-trend{{font-size:.72rem;font-weight:600;color:{GOLD};margin-top:3px;}}

/* Tags */
.ek-tag{{display:inline-flex;align-items:center;gap:5px;padding:3px 12px;border-radius:999px;
  background:{GOLD_D};border:1px solid {BORDER_G};color:{GOLD};font-size:.65rem;font-weight:600;
  letter-spacing:.09em;text-transform:uppercase;}}

/* Hero */
.hero-wrap{{background:{HERO_BG};border-radius:24px;padding:2.8rem 2.5rem;margin-bottom:1.8rem;
  border:1px solid {BORDER_G};position:relative;overflow:hidden;}}
.hero-title{{font-family:'Cormorant Garamond',serif;font-size:clamp(2rem,5vw,3.3rem);font-weight:700;
  color:{TEXT};line-height:1.08;letter-spacing:-.025em;margin-bottom:.7rem;}}
.hero-gold{{color:{GOLD};}}
.hero-sub{{font-size:.96rem;color:{TEXT2};line-height:1.75;max-width:620px;}}
.hero-quote{{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:1.05rem;
  color:{GOLD};margin-top:1.2rem;border-left:3px solid {GOLD};padding-left:1rem;}}

/* Section headers */
.sec-h{{font-family:'Cormorant Garamond',serif;font-size:1.55rem;font-weight:700;color:{TEXT};margin-bottom:.15rem;}}
.sec-s{{font-size:.8rem;color:{TEXT3};margin-bottom:1.1rem;}}

/* Chat */
.chat-user{{background:{GOLD_D};border:1px solid {BORDER_G};border-radius:16px 16px 4px 16px;
  padding:.75rem 1rem;margin:.4rem 0;color:{TEXT};font-size:.9rem;max-width:85%;margin-left:auto;}}
.chat-ai{{background:{CARD};border:1px solid {BORDER};border-radius:16px 16px 16px 4px;
  padding:.8rem 1rem;margin:.4rem 0;color:{TEXT2};font-size:.9rem;line-height:1.65;max-width:90%;}}

/* Testimonial */
.testimonial{{background:{CARD};border:1px solid {BORDER};border-left:3px solid {GOLD};
  border-radius:0 14px 14px 0;padding:1.1rem 1.4rem;margin-bottom:.8rem;
  color:{TEXT2};font-size:.88rem;line-height:1.7;font-style:italic;}}
.testimonial-author{{font-style:normal;font-weight:600;color:{GOLD};font-size:.78rem;margin-top:.4rem;}}

/* Feature pill */
.feat-pill{{background:{CARD};border:1px solid {BORDER};border-radius:14px;padding:1.2rem;
  text-align:center;transition:all .25s;height:100%;}}
.feat-pill:hover{{border-color:{BORDER_G};transform:translateY(-3px);box-shadow:0 8px 24px {SHADOW};}}
.feat-emoji{{font-size:1.9rem;margin-bottom:.5rem;}}
.feat-title{{font-weight:600;font-size:.88rem;color:{TEXT};margin-bottom:.25rem;}}
.feat-desc{{font-size:.73rem;color:{TEXT3};line-height:1.5;}}

/* Model tag */
.model-tag{{font-size:.68rem;color:{TEXT3};font-style:italic;margin-top:.3rem;}}

/* Buttons */
.stButton>button{{background:linear-gradient(135deg,{GOLD},{GOLDL})!important;color:#0b0e16!important;
  font-weight:600!important;border:none!important;border-radius:10px!important;padding:.45rem 1.4rem!important;
  font-family:'DM Sans',sans-serif!important;transition:opacity .2s,transform .15s!important;
  box-shadow:0 2px 12px rgba(201,169,110,.25)!important;}}
.stButton>button:hover{{opacity:.88!important;transform:translateY(-1px)!important;}}
.theme-btn>button{{background:{CARD}!important;color:{TEXT}!important;
  border:1px solid {BORDER_G}!important;border-radius:10px!important;box-shadow:none!important;}}
.theme-btn>button:hover{{border-color:{GOLD}!important;color:{GOLD}!important;}}

/* Inputs */
.stTextInput>div>input,.stTextArea textarea{{background:{INP_BG}!important;border:1px solid {BORDER}!important;
  border-radius:10px!important;color:{TEXT}!important;}}
.stTextInput>div>input::placeholder,.stTextArea textarea::placeholder{{color:{TEXT3}!important;}}
.stTextInput>div>input:focus,.stTextArea textarea:focus{{border-color:{BORDER_G}!important;
  box-shadow:0 0 0 2px {GOLD_D}!important;}}
.stSelectbox>div>div{{background:{INP_BG}!important;border:1px solid {BORDER}!important;
  border-radius:10px!important;color:{TEXT}!important;}}

/* Tabs */
.stTabs [data-baseweb="tab-list"]{{background:{CARD};border-radius:10px;padding:4px;gap:3px;border:1px solid {BORDER};}}
.stTabs [data-baseweb="tab"]{{background:transparent;color:{TEXT3};border-radius:8px;font-size:.8rem;
  font-weight:600;padding:.4rem .9rem;}}
.stTabs [aria-selected="true"]{{background:linear-gradient(135deg,{GOLD},{GOLDL})!important;color:#0b0e16!important;}}

/* Progress */
.stProgress>div>div{{background:linear-gradient(90deg,{GOLD},{GOLDL})!important;border-radius:99px!important;}}
.stProgress>div{{background:{BORDER}!important;border-radius:99px!important;}}

/* Metrics */
[data-testid="metric-container"]{{background:{CARD};border:1px solid {BORDER};border-radius:14px;padding:.9rem 1.1rem;}}
[data-testid="stMetricLabel"]{{color:{TEXT3}!important;font-size:.65rem!important;text-transform:uppercase!important;letter-spacing:.08em!important;}}
[data-testid="stMetricValue"]{{color:{TEXT}!important;font-family:'Cormorant Garamond',serif!important;font-size:1.85rem!important;}}
[data-testid="stMetricDelta"]{{color:{GOLD}!important;}}

hr{{border-color:{BORDER}!important;margin:1.4rem 0!important;}}
.stAlert{{border-radius:12px!important;}}
#MainMenu,footer{{visibility:hidden;}}
header[data-testid="stHeader"]{{background:transparent!important;}}
</style>
""", unsafe_allow_html=True)

# ─── Data ─────────────────────────────────────────────────────────────────────
@st.cache_data
def get_df():
    months = ["Янв","Фев","Мар","Апр","Май","Июн","Июл","Авг","Сен","Окт","Ноя","Дек"]
    return pd.DataFrame({"month": months,
        "publications": [2,1,3,2,4,3,2,5,3,4,3,5],
        "users":        [480,620,580,740,810,990,1100,1450,1620,1890,2240,2780],
        "views":        [1200,1800,1550,2100,2400,3200,2900,4100,3800,4600,5200,6400]})

@st.cache_data
def get_geo():
    return pd.DataFrame({
        "country": ["Казахстан","Россия","Китай","Узбекистан","Кыргызстан","Германия","США","Азербайджан"],
        "users":   [8400,3200,1100,880,440,320,290,560],
        "share":   [52,20,7,5,3,2,2,4],
        "lat": [48.0,61.5,35.9,41.4,41.2,51.2,37.1,40.4],
        "lon": [68.0,105.3,104.2,64.6,74.7,10.4,-95.7,49.9],
    })

@st.cache_data
def get_caspian():
    np.random.seed(7)
    return pd.DataFrame({
        "station":     ["Актау","Баку","Астрахань","Туркменбаши","Энзели"],
        "water_level": [round(np.random.uniform(-28.5,-27.8),2) for _ in range(5)],
        "salinity":    [round(np.random.uniform(12.5,13.5),1)   for _ in range(5)],
        "temp":        [round(np.random.uniform(10,24),1)        for _ in range(5)],
        "oil_index":   [round(np.random.uniform(0.02,0.18),3)    for _ in range(5)],
        "lat": [43.65,40.41,46.35,40.02,37.47],
        "lon": [51.17,49.87,48.03,53.00,49.47],
    })

# ─── Charts ───────────────────────────────────────────────────────────────────
def fig_users(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["month"], y=df["users"], fill="tozeroy",
        fillcolor=f"rgba(201,169,110,{0.08 if D else 0.12})",
        line=dict(color=GOLD, width=2.5), mode="lines+markers",
        marker=dict(color=GOLD, size=6, line=dict(color=BG, width=2)),
        hovertemplate="<b>%{x}</b><br>%{y:,} посетителей<extra></extra>"))
    fig.update_layout(**CT, height=230, showlegend=False)
    return fig

def fig_pubs(df):
    fig = go.Figure(go.Bar(x=df["month"], y=df["publications"],
        marker=dict(color=BLUE, opacity=.8, line=dict(width=0)),
        hovertemplate="<b>%{x}</b><br>%{y} публикаций<extra></extra>"))
    fig.update_layout(**CT, height=230, showlegend=False)
    return fig

def fig_views(df):
    fig = go.Figure(go.Bar(x=df["month"], y=df["views"],
        marker=dict(color=GREEN, opacity=.75, line=dict(width=0)),
        hovertemplate="<b>%{x}</b><br>%{y:,} просмотров<extra></extra>"))
    fig.update_layout(**CT, height=230, showlegend=False)
    return fig

def fig_geo(df):
    fig = px.scatter_geo(df, lat="lat", lon="lon", size="users", color="share",
        color_continuous_scale=[[0,GLAND],[.5,"#6b4e20"],[1,GOLD]],
        hover_name="country",
        hover_data={"users":True,"share":True,"lat":False,"lon":False},
        size_max=38)
    fig.update_layout(
        geo=dict(bgcolor=PLOT_BG, showland=True, landcolor=GLAND, showocean=True,
                 oceancolor=GOCEAN, showcoastlines=True, coastlinecolor=GCOAST,
                 showframe=False, projection_type="natural earth",
                 center=dict(lat=45,lon=65), projection_scale=2.2),
        paper_bgcolor=PLOT_BG, coloraxis_showscale=False,
        margin=dict(l=0,r=0,t=0,b=0), height=310)
    return fig

def fig_caspian(df):
    fig = px.scatter_mapbox(df, lat="lat", lon="lon", size="oil_index", color="temp",
        color_continuous_scale=[[0,BLUE],[.5,GOLD],[1,RED]],
        hover_name="station",
        hover_data={"water_level":":.2f","salinity":":.1f","temp":":.1f",
                    "oil_index":":.3f","lat":False,"lon":False},
        size_max=35, zoom=3.8, center={"lat":42,"lon":51})
    fig.update_layout(mapbox_style=MAPST, paper_bgcolor=PLOT_BG,
                      coloraxis_showscale=False,
                      margin=dict(l=0,r=0,t=0,b=0), height=350)
    return fig

def fig_radar():
    cats = ["Экономика","Энергетика","Каспий","Геополитика","История","Образование"]
    vals = [92, 85, 96, 78, 72, 80]
    fig = go.Figure(go.Scatterpolar(
        r=vals + [vals[0]], theta=cats + [cats[0]],
        fill="toself",
        fillcolor=f"rgba(201,169,110,{0.15 if D else 0.12})",
        line=dict(color=GOLD, width=2),
        marker=dict(color=GOLD, size=6)))
    fig.update_layout(
        polar=dict(
            bgcolor=PLOT_BG,
            radialaxis=dict(visible=True, range=[0,100],
                            gridcolor=GRID, tickfont=dict(color=TEXT3, size=9)),
            angularaxis=dict(tickfont=dict(color=TEXT2, size=10), gridcolor=GRID)),
        paper_bgcolor=PLOT_BG, showlegend=False,
        margin=dict(l=30,r=30,t=30,b=30), height=290)
    return fig

# ─── AI ───────────────────────────────────────────────────────────────────────
SYS = """Ты — интеллектуальный ассистент платформы Kulekeyev Intelligence Hub.

Платформа создана на основе научного и аналитического наследия
Жаксыбека Абдрахметовича Кулекеева — экономиста, исследователя Каспийского
региона, автора книг и аналитических работ. Концепция разработана Гульбазар Акыловной Медиевой.

Шесть ключевых направлений:
1. Economic Intelligence — макро/микроэкономика, госфинансы, инвестиции, национальная экономика Казахстана
2. Energy & Resource Intelligence — нефтегазовый сектор, энергетические системы, ресурсная экономика
3. Caspian Intelligence — Каспийский регион как стратегическое пространство: экология, ресурсы, геополитика
4. Governance & Policy Analysis — государственные процессы, трансформации, стратегические решения
5. Civilization & History — история, происхождение народов, цивилизационные модели, культура
6. Education & Knowledge — передача знаний, детские книги, развитие научного мышления

Также охватываешь тему ESG Kazakhstan Initiative — адаптация ESG-стандартов к экономике Казахстана.

Аналогии для контекста: Ray Dalio (система принципов), Yuval Noah Harari (Big History),
Nassim Taleb (риск и неопределённость), Klaus Schwab (институциональная повестка).

Отвечай профессионально, по-русски, структурировано. Умей:
- объяснять экономические концепции просто
- анализировать темы Каспийского региона
- рассказывать об истории и цивилизации Центральной Азии
- генерировать аннотации и резюме к работам автора
- формировать аналитические обзоры по запросу"""

MODELS = [
    "claude-opus-4-5",
    "claude-sonnet-4-5",
    "claude-3-5-sonnet-20241022",
    "claude-3-5-haiku-20241022",
]

def call_ai(client, messages):
    last_err = None
    for model in MODELS:
        try:
            resp = client.messages.create(
                model=model, max_tokens=1400,
                system=SYS, messages=messages)
            return resp.content[0].text, model
        except anthropic.BadRequestError:
            raise
        except Exception as e:
            last_err = e
            continue
    raise last_err

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="font-family:'Cormorant Garamond',serif;font-size:1.25rem;font-weight:700;
         color:{TEXT};line-height:1.2;margin-bottom:4px;">
      🧠 Kulekeyev<br><span style="color:{GOLD};">Intelligence Hub</span>
    </div>""", unsafe_allow_html=True)
    st.markdown(f'<span class="ek-tag">Интеллектуальная платформа</span>', unsafe_allow_html=True)

    # ── Theme ──────────────────────────────────────────────────────────────
    st.markdown(f'<div style="font-size:.62rem;text-transform:uppercase;letter-spacing:.1em;color:{TEXT3};margin:1rem 0 .35rem;">Оформление</div>', unsafe_allow_html=True)
    cd, cl = st.columns(2)
    with cd:
        st.markdown('<div class="theme-btn">', unsafe_allow_html=True)
        if st.button("🌙 Тёмная", use_container_width=True, key="t_dark"):
            st.session_state.dark_mode = True;  st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with cl:
        st.markdown('<div class="theme-btn">', unsafe_allow_html=True)
        if st.button("☀️ Светлая", use_container_width=True, key="t_light"):
            st.session_state.dark_mode = False; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:.68rem;color:{GOLD};text-align:center;margin:.25rem 0 .5rem;">{"🌙 Тёмная" if D else "☀️ Светлая"} активна</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ── Navigation ─────────────────────────────────────────────────────────
    st.markdown(f'<div style="font-size:.62rem;text-transform:uppercase;letter-spacing:.1em;color:{TEXT3};margin-bottom:.35rem;">Разделы</div>', unsafe_allow_html=True)
    section = st.radio("nav", [
        "🏠 О Хабе",
        "👤 О Кулекееве",
        "🧭 Направления",
        "🗺️ Каспий GIS",
        "📚 Библиотека",
        "🤖 AI Ассистент",
        "📊 Аналитика",
    ], label_visibility="collapsed")

    st.markdown("---")

    # ── API Key ─────────────────────────────────────────────────────────────
    st.markdown(f'<div style="font-size:.62rem;text-transform:uppercase;letter-spacing:.1em;color:{TEXT3};margin-bottom:.35rem;">AI — Anthropic API</div>', unsafe_allow_html=True)
    api_key = st.text_input("key", type="password", placeholder="sk-ant-...", label_visibility="collapsed")
    st.markdown(f'<a href="https://console.anthropic.com/settings/keys" target="_blank" style="font-size:.74rem;color:{GOLD};text-decoration:none;font-weight:500;">🔑 Получить ключ бесплатно →</a>', unsafe_allow_html=True)
    if api_key:
        try:
            st.session_state.client = anthropic.Anthropic(api_key=api_key)
            st.markdown(f'<div style="color:{GREEN};font-size:.74rem;margin-top:4px;">✓ AI подключён</div>', unsafe_allow_html=True)
        except Exception:
            st.markdown('<div style="color:#ef4444;font-size:.74rem;margin-top:4px;">✗ Неверный ключ</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.selectbox("Язык", ["🇷🇺 RU", "🇰🇿 KZ", "🇬🇧 EN"], label_visibility="collapsed")
    st.markdown(f'<div style="font-size:.62rem;color:{TEXT3};margin-top:1.4rem;line-height:1.65;">© 2025 Kulekeyev Intelligence Hub<br></div>', unsafe_allow_html=True)

# ─── Data load ────────────────────────────────────────────────────────────────
df      = get_df()
geo_df  = get_geo()
cas_df  = get_caspian()

# ══════════════════════════════════════════════════════════════════════════════
if section == "🏠 О Хабе":
# ══════════════════════════════════════════════════════════════════════════════

    # Hero
    st.markdown(f"""
    <div class="hero-wrap">
      <span class="ek-tag" style="margin-bottom:1rem;display:inline-block;">🧠 Интеллектуальная платформа · Казахстан</span>
      <div class="hero-title">Kulekeyev<br><span class="hero-gold">Intelligence Hub</span></div>
      <div class="hero-sub">
        Цифровая платформа систематизации научного, аналитического и образовательного
        наследия <b>Жаксыбека Абдрахметовича Кулекеева</b> — экономиста, исследователя
        Каспийского региона, автора книг и концепций развития Казахстана.
      </div>
      <div class="hero-quote">
        «От отдельных работ — к системе знаний.<br>
         От анализа — к формированию повестки.<br>
         От накопления — к масштабированию.»
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Mission block
    st.markdown(f'<div class="sec-h">Миссия</div><div class="sec-s">Зачем создан Hub</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="ek-card" style="border-color:{BORDER_G};">
      <div style="font-family:'Cormorant Garamond',serif;font-size:1.1rem;font-weight:600;color:{TEXT};margin-bottom:.8rem;">
        Формирование интеллектуальной среды, объединяющей экономику, ресурсы, геополитику,
        историю и образование в единую систему мышления
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:.8rem;margin-top:.5rem;">
        {"".join(f'<div style="font-size:.82rem;color:{TEXT2};padding:.5rem .7rem;background:rgba(201,169,110,0.06);border-radius:10px;">✦ {m}</div>' for m in [
          "Развитие культуры системного мышления",
          "Формирование национальной интеллектуальной повестки",
          "Интеграция науки, государства и бизнеса",
          "Поддержка устойчивого развития и ESG",
          "Передача знаний новым поколениям",
          "Вывод на международный уровень"
        ])}
      </div>
    </div>
    """, unsafe_allow_html=True)



    st.markdown("---")

    # Audience
    st.markdown(f'<div class="sec-h">Для кого</div>', unsafe_allow_html=True)
    a1, a2, a3 = st.columns(3)
    for col, emoji, title, items, clr in [
        (a1, "🎓", "Студентам и учёным", ["AI-помощник по экономике Казахстана", "Аналитические материалы и статьи", "Библиотека авторских работ", "Детские энциклопедии на KZ/RU"], BLUE),
        (a2, "🏛️", "Государству и бизнесу", ["Стратегические аналитические обзоры", "ESG Kazakhstan Initiative", "Каспийский мониторинг", "Экспертные заключения"], GOLD),
        (a3, "🌍", "Международной аудитории", ["Исследования Центральной Азии", "GIS Каспийского бассейна", "Цивилизационная история региона", "Публикации на 3 языках"], GREEN),
    ]:
        with col:
            items_html = "".join(f'<li style="font-size:.8rem;color:{TEXT2};margin-bottom:5px;list-style:none;">✓ {it}</li>' for it in items)
            st.markdown(f'<div class="ek-card"><div style="font-size:1.8rem;margin-bottom:.5rem;">{emoji}</div><div style="font-family:\'Cormorant Garamond\',serif;font-size:1.1rem;font-weight:700;color:{TEXT};margin-bottom:.7rem;">{title}</div><ul style="padding:0;margin:0;">{items_html}</ul></div>', unsafe_allow_html=True)

    st.markdown("---")

    # ESG block
    st.markdown(f'<div class="sec-h">ESG Kazakhstan Initiative</div><div class="sec-s">Флагманское направление устойчивого развития</div>', unsafe_allow_html=True)
    e1, e2 = st.columns([2, 1])
    with e1:
        st.markdown(f"""
        <div class="ek-card">
          <div style="font-size:.9rem;color:{TEXT2};line-height:1.75;">
            В рамках Hub создаётся специальное направление — <span style="color:{GOLD};font-weight:600;">ESG Kazakhstan Initiative</span> —
            разработка прикладной системы ESG-подходов, адаптированной к экономике Казахстана.
          </div>
          <div style="margin-top:1rem;display:grid;grid-template-columns:1fr 1fr;gap:.6rem;">
            {"".join(f'<div style="font-size:.78rem;color:{TEXT2};padding:.45rem .7rem;background:rgba(78,202,139,0.07);border-radius:8px;border:1px solid rgba(78,202,139,0.15);">◆ {t}</div>' for t in [
              "Анализ ESG-вызовов по отраслям",
              "Адаптация международных стандартов",
              "Отраслевые рекомендации для RK",
              "Система оценки устойчивости бизнеса"
            ])}
          </div>
        </div>
        """, unsafe_allow_html=True)
    with e2:
        st.markdown(f"""
        <div class="ek-card" style="text-align:center;border-color:rgba(78,202,139,0.3);">
          <div style="font-size:2.5rem;margin-bottom:.5rem;">🌱</div>
          <div style="font-family:'Cormorant Garamond',serif;font-size:1rem;font-weight:700;color:{TEXT};margin-bottom:.4rem;">Флагманский продукт</div>
          <div style="font-size:.78rem;color:{TEXT2};line-height:1.6;">Национальная рамка ESG-практик для предприятий Казахстана</div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
elif section == "👤 О Кулекееве":
# ══════════════════════════════════════════════════════════════════════════════

    # Biography hero — inspired by raydalio.com / principles.com style
    st.markdown(f"""
    <div class="hero-wrap" style="padding:3rem 2.5rem;">
      <span class="ek-tag" style="margin-bottom:1.2rem;display:inline-block;">👤 Об авторе</span>
      <div style="display:flex;gap:2.5rem;align-items:flex-start;flex-wrap:wrap;">
        <div style="flex:1;min-width:260px;">
          <div class="hero-title" style="font-size:clamp(1.8rem,4vw,2.8rem);">
            Жаксыбек<br><span class="hero-gold">Абдрахметович<br>Кулекеев</span>
          </div>
          <div style="font-size:.9rem;color:{TEXT2};line-height:1.8;margin-top:1rem;max-width:520px;">
            Казахстанский экономист, учёный и государственный деятель. На протяжении десятилетий
            формирует уникальную систему знаний, охватывающую экономику, энергетику, Каспийский
            регион, геополитику, историю цивилизаций и образование.
          </div>
        </div>
        <div style="display:flex;flex-direction:column;gap:.6rem;min-width:200px;">
          {"".join(f'<div style="display:flex;align-items:center;gap:.7rem;"><div style="width:36px;height:36px;border-radius:10px;background:{c}22;border:1px solid {c}44;display:flex;align-items:center;justify-content:center;font-size:1rem;">{ic}</div><div><div style="font-size:.75rem;font-weight:600;color:{TEXT};">{t}</div><div style="font-size:.68rem;color:{TEXT3};">{s}</div></div></div>' for ic,t,s,c in [
            ("🎓","Доктор экономических наук","Профессор","#c9a96e"),
            ("🏛️","Государственный деятель","Казахстан","#7eb8d4"),
            ("📚","Автор книг и монографий","6+ изданий","#4eca8b"),
            ("🌊","Исследователь Каспия","Ведущий эксперт региона","#a78bfa"),
            ("🌱","Эксперт по ESG","Устойчивое развитие","#e2c99a"),
          ])}
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Main biography card
    st.markdown(f'<div class="sec-h">Биография</div>', unsafe_allow_html=True)
    b1, b2 = st.columns([3, 2])
    with b1:
        st.markdown(f"""
        <div class="ek-card">
          <div style="font-family:'Cormorant Garamond',serif;font-size:1.05rem;font-weight:600;
               color:{TEXT};line-height:1.5;margin-bottom:1rem;">
            Жаксыбек Абдрахметович Кулекеев — экономист, учёный и исследователь,
            чья деятельность охватывает ключевые вопросы развития Казахстана
            и Центральноазиатского региона.
          </div>
          <div style="font-size:.87rem;color:{TEXT2};line-height:1.8;">
            На протяжении многих лет он формирует уникальный массив знаний — от
            глубокого анализа макроэкономики и нефтегазового сектора до исследований
            Каспийского бассейна, геополитических процессов и цивилизационной
            истории народов Казахстана.<br><br>
            Его научные работы, аналитические статьи и книги образуют целостную
            систему мышления, способную влиять на стратегические решения, формировать
            повестку устойчивого развития и передавать знания будущим поколениям.<br><br>
            Kulekeyev Intelligence Hub создан для того, чтобы структурировать,
            сохранить и развить это интеллектуальное наследие — превратив его
            в живую цифровую платформу национального и международного уровня.
          </div>
        </div>
        """, unsafe_allow_html=True)
    with b2:
        # Timeline
        st.markdown(f'<div class="sec-h" style="font-size:1.1rem;">Ключевые вехи</div>', unsafe_allow_html=True)
        for yr, ev, clr in [
            ("1990-е","Начало научной и государственной деятельности в области экономики", GOLD),
            ("2000-е","Формирование экспертизы по нефтегазовому сектору и Каспию", BLUE),
            ("2010-е","Исследования цивилизационной истории, детские книги на KZ", GREEN),
            ("2020-е","ESG Kazakhstan Initiative, цифровая трансформация ЦА", GOLDL),
            ("2025","Запуск Kulekeyev Intelligence Hub", GOLD),
        ]:
            st.markdown(f"""
            <div style="display:flex;gap:.8rem;align-items:flex-start;margin-bottom:.8rem;">
              <div style="min-width:52px;padding:3px 8px;border-radius:6px;background:{clr}22;
                   border:1px solid {clr}44;font-size:.65rem;font-weight:700;color:{clr};
                   text-align:center;white-space:nowrap;">{yr}</div>
              <div style="font-size:.8rem;color:{TEXT2};line-height:1.5;padding-top:2px;">{ev}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Key achievements
    st.markdown(f'<div class="sec-h">Области экспертизы</div><div class="sec-s">Шесть направлений интеллектуальной системы</div>', unsafe_allow_html=True)
    ex_cols = st.columns(3)
    for i, (icon, area, desc) in enumerate([
        ("📈","Экономика Казахстана","Макро- и микроэкономика, государственные финансы, инвестиционная политика"),
        ("⚡","Энергетика и ресурсы","Нефтегазовый сектор, ресурсная экономика, энергетическая безопасность"),
        ("🌊","Каспийский регион","Ведущий исследователь: экология, ресурсы, геополитика бассейна"),
        ("🏛️","Государство и политика","Анализ трансформаций, стратегические решения, политические процессы"),
        ("🗿","История и цивилизация","Происхождение народов, казахская цивилизация, культурная идентичность"),
        ("📖","Образование","Детские книги на казахском, научное мышление, языковая культура"),
    ]):
        with ex_cols[i % 3]:
            st.markdown(f"""
            <div class="feat-pill" style="margin-bottom:.6rem;">
              <div class="feat-emoji">{icon}</div>
              <div class="feat-title">{area}</div>
              <div class="feat-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Philosophy / principles block
    st.markdown(f'<div class="sec-h">Система мышления</div><div class="sec-s">Принципы интеллектуального подхода Кулекеева</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="ek-card" style="border-color:{BORDER_G};">
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;">
        {"".join(f'<div style="padding:.8rem 1rem;background:rgba(201,169,110,0.05);border-radius:12px;border-left:3px solid {GOLD};"><div style="font-size:.8rem;font-weight:600;color:{TEXT};margin-bottom:.3rem;">{t}</div><div style="font-size:.75rem;color:{TEXT2};line-height:1.55;">{d}</div></div>' for t,d in [
          ("Системный подход","Любая проблема рассматривается в контексте экономики, ресурсов, истории и геополитики одновременно"),
          ("Национальный контекст","Международные концепции адаптируются к реалиям Казахстана и Центральной Азии"),
          ("Передача знаний","Сложные идеи формулируются доступно — от академических работ до детских книг"),
          ("Долгосрочное мышление","Анализ строится на понимании цивилизационных циклов, а не только текущей конъюнктуры"),
        ])}
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Contact / connect
    st.markdown("---")
    st.markdown(f'<div class="sec-h">Связаться</div>', unsafe_allow_html=True)
    cc1, cc2, cc3 = st.columns(3)
    for col, icon, title, detail in [
        (cc1, "📧", "Email", "hub@kulekeyev.kz"),
        (cc2, "🌐", "Платформа", "kulekeyev-hub.kz"),
        (cc3, "📍", "Алматы, Казахстан", "Центральная Азия"),
    ]:
        with col:
            st.markdown(f'<div class="kpi-block" style="padding:.9rem;"><div style="font-size:1.4rem;margin-bottom:.3rem;">{icon}</div><div class="kpi-label">{title}</div><div style="font-size:.8rem;color:{TEXT2};margin-top:.3rem;">{detail}</div></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
elif section == "🧭 Направления":
# ══════════════════════════════════════════════════════════════════════════════

    st.markdown(f'<span class="ek-tag">6 Ключевых направлений</span>', unsafe_allow_html=True)
    st.markdown(f'<div class="sec-h" style="margin-top:.5rem;">Концептуальная модель Hub</div><div class="sec-s">Четыре уровня · Шесть направлений · Единая система мышления</div>', unsafe_allow_html=True)

    # Radar chart + description
    rc, rd = st.columns([2, 3])
    with rc:
        st.plotly_chart(fig_radar(), use_container_width=True, config={"displayModeBar": False})
    with rd:
        st.markdown(f"""
        <div class="ek-card" style="height:100%;">
          <div style="font-family:'Cormorant Garamond',serif;font-size:1.2rem;font-weight:700;color:{TEXT};margin-bottom:.8rem;">
            Четыре уровня системы знаний
          </div>
          {"".join(f'''<div style="display:flex;gap:.8rem;align-items:flex-start;margin-bottom:.7rem;">
            <div style="min-width:28px;height:28px;border-radius:8px;background:{c};display:flex;align-items:center;justify-content:center;font-size:.75rem;font-weight:700;color:#0b0e16;">{n}</div>
            <div><div style="font-size:.85rem;font-weight:600;color:{TEXT};">{t}</div><div style="font-size:.75rem;color:{TEXT2};margin-top:2px;">{d}</div></div>
          </div>''' for n,t,d,c in [
            ("1","Аналитический","Экономика, макро/микро, госфинансы, энергетика, Каспий","#c9a96e"),
            ("2","Системный","Геоэкономика, стратегическое моделирование, гострансформации","#7eb8d4"),
            ("3","Цивилизационный","История, культурные процессы, идентичность, происхождение народов","#4eca8b"),
            ("4","Образовательный","Передача знаний, детские книги, научное мышление, языковая культура","#a78bfa"),
          ])}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # 6 Directions grid
    st.markdown(f'<div class="sec-h">6 Ключевых направлений</div>', unsafe_allow_html=True)

    DIRECTIONS = [
        ("📈", "Economic Intelligence", "#c9a96e",
         "Макро- и микроэкономика, государственные финансы, инвестиционные процессы, экономическая политика и развитие национальной экономики Казахстана.",
         ["Государственные финансы RK", "Инвестиционные институты", "Национальная экономическая модель", "Макроэкономический анализ"]),
        ("⚡", "Energy & Resource Intelligence", "#7eb8d4",
         "Нефтегазовый сектор, энергетические системы, ресурсная экономика и их роль в устойчивом развитии и геоэкономике.",
         ["Нефтегазовый сектор Казахстана", "Ресурсная экономика", "Энергетическая политика", "ESG и декарбонизация"]),
        ("🌊", "Caspian Intelligence", "#4eca8b",
         "Каспийский регион как стратегическое пространство: экономика, ресурсы, экология, геополитика и международные отношения.",
         ["Экологический мониторинг", "Ресурсы бассейна", "Геополитика Каспия", "Правовой статус"]),
        ("🏛️", "Governance & Policy Analysis", "#e2c99a",
         "Анализ государственных процессов, политических трансформаций, стратегических решений и современных вызовов развития.",
         ["Государственные трансформации", "Политический анализ", "Стратегические решения", "Январские события 2022"]),
        ("🗿", "Civilization & History", "#d4907e",
         "История Центральной Азии, происхождение народов, культурные процессы, цивилизационные модели и связь с экономическим развитием.",
         ["Древняя история Казахстана", "Происхождение казахского народа", "Цивилизационные модели", "Культурная идентичность"]),
        ("📖", "Education & Knowledge", "#a78bfa",
         "Развитие образовательных инициатив, передача знаний, детские книги на казахском языке, формирование научного мышления.",
         ["Детские энциклопедии (KZ)", "Развитие языковой культуры", "Научное мышление", "Образовательный контент"]),
    ]

    cols = st.columns(3)
    for i, (icon, title, color, desc, tags) in enumerate(DIRECTIONS):
        with cols[i % 3]:
            tags_html = "".join(f'<span style="font-size:.63rem;padding:2px 8px;border-radius:999px;background:{color}20;border:1px solid {color}40;color:{color};margin-right:4px;margin-bottom:4px;display:inline-block;">{t}</span>' for t in tags)
            st.markdown(f"""
            <div class="dir-card" style="border-color:{color}30;margin-bottom:.8rem;">
              <div style="display:flex;align-items:center;gap:.6rem;margin-bottom:.6rem;">
                <div style="font-size:1.5rem;">{icon}</div>
                <div style="font-family:'Cormorant Garamond',serif;font-size:1rem;font-weight:700;color:{color};">{title}</div>
              </div>
              <div style="font-size:.78rem;color:{TEXT2};line-height:1.55;margin-bottom:.8rem;">{desc}</div>
              <div style="flex-wrap:wrap;">{tags_html}</div>
            </div>
            """, unsafe_allow_html=True)

    # AI analysis for directions
    if st.session_state.client:
        st.markdown("---")
        sel_dir = st.selectbox("Выберите направление для AI-анализа", [d[1] for d in DIRECTIONS])
        if st.button("🤖 Сгенерировать аналитический обзор"):
            with st.spinner("Формирую обзор..."):
                try:
                    prompt = f"Напиши краткий аналитический обзор (250–300 слов) направления '{sel_dir}' применительно к Казахстану и работам Кулекеева. Структурируй по разделам."
                    full, used = call_ai(st.session_state.client, [{"role":"user","content":prompt}])
                    st.markdown(f'<div class="chat-ai">{full}</div>', unsafe_allow_html=True)
                    st.download_button("⬇️ Скачать", data=full, file_name=f"analysis_{sel_dir}.txt", mime="text/plain")
                    st.markdown(f'<div class="model-tag">Модель: {used}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Ошибка AI: {e}")
    else:
        st.info(f"🔑 [Получить API Key](https://console.anthropic.com/settings/keys) — для AI-анализа по направлениям")

# ══════════════════════════════════════════════════════════════════════════════
elif section == "🗺️ Каспий GIS":
# ══════════════════════════════════════════════════════════════════════════════

    st.markdown(f'<span class="ek-tag">🛰️ Caspian Intelligence · Live GIS</span>', unsafe_allow_html=True)
    st.markdown(f'<div class="sec-h" style="margin-top:.5rem;">Каспийский бассейн</div><div class="sec-s">Экологический мониторинг · спутниковые данные · анализ месторождений · геополитика</div>', unsafe_allow_html=True)

    cols = st.columns(5)
    for i, (_, row) in enumerate(cas_df.iterrows()):
        with cols[i]:
            oc = RED if row["oil_index"] > .12 else GREEN
            st.markdown(f'<div class="kpi-block"><div class="kpi-label">{row["station"]}</div><div class="kpi-value" style="font-size:1.25rem;">{row["temp"]:.1f}°C</div><div style="font-size:.62rem;color:{oc};margin-top:3px;">Нефть: {row["oil_index"]:.3f}</div><div style="font-size:.62rem;color:{TEXT3};">Ур.: {row["water_level"]:.2f} м</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.plotly_chart(fig_caspian(cas_df), use_container_width=True, config={"displayModeBar": False})

    st.markdown("---")
    cl, cr = st.columns(2)
    with cl:
        st.markdown(f'<div class="sec-h" style="font-size:1.1rem;">📋 Данные станций</div>', unsafe_allow_html=True)
        disp = cas_df[["station","temp","salinity","water_level","oil_index"]].copy()
        disp.columns = ["Станция","°C","Солёность ‰","Уровень м","Нефть-индекс"]
        st.dataframe(disp, use_container_width=True, hide_index=True)
    with cr:
        st.markdown(f'<div class="sec-h" style="font-size:1.1rem;">📊 Температура воды</div>', unsafe_allow_html=True)
        fig = go.Figure(go.Bar(x=cas_df["station"], y=cas_df["temp"],
            marker=dict(color=cas_df["temp"].tolist(), colorscale=[[0,BLUE],[1,GOLD]], line=dict(width=0)),
            hovertemplate="<b>%{x}</b><br>%{y:.1f}°C<extra></extra>"))
        fig.update_layout(**CT, height=210, showlegend=False)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # Key research themes
    st.markdown("---")
    st.markdown(f'<div class="sec-h" style="font-size:1.1rem;">🔬 Ключевые исследовательские темы</div>', unsafe_allow_html=True)
    tc = st.columns(4)
    for col, icon, title, desc in [
        (tc[0], "🛢️", "Ресурсная экономика", "Нефтегазовые месторождения, добыча и распределение доходов"),
        (tc[1], "🌿", "Экология Каспия", "Изменение уровня воды, загрязнение, флора и фауна"),
        (tc[2], "🤝", "Геополитика", "Правовой статус, интересы 5 прибрежных государств"),
        (tc[3], "📡", "Мониторинг", "Спутниковые данные, экологические индексы"),
    ]:
        with col:
            st.markdown(f'<div class="feat-pill"><div class="feat-emoji">{icon}</div><div class="feat-title">{title}</div><div class="feat-desc">{desc}</div></div>', unsafe_allow_html=True)

    if st.session_state.client:
        st.markdown("---")
        if st.button("🤖 AI-отчёт по экологической обстановке Каспия"):
            with st.spinner("Формирую отчёт..."):
                try:
                    prompt = f"Напиши краткий экспертный отчёт об экологической обстановке Каспийского моря на основе данных: {cas_df.to_dict('records')}. Включи интерпретацию нефть-индекса, уровня воды и температуры."
                    full, used = call_ai(st.session_state.client, [{"role":"user","content":prompt}])
                    st.markdown(f'<div class="chat-ai">{full}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="model-tag">Модель: {used}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Ошибка AI: {e}")
    else:
        st.info(f"🔑 [Получить API Key](https://console.anthropic.com/settings/keys) — для AI-анализа Каспия")

# ══════════════════════════════════════════════════════════════════════════════
elif section == "📚 Библиотека":
# ══════════════════════════════════════════════════════════════════════════════

    st.markdown(f'<div class="sec-h">Библиотека работ</div><div class="sec-s">Книги, аналитические статьи и исследования · AI-генерация контента</div>', unsafe_allow_html=True)

    BOOKS = [
        {"title":"Қаңтар: политологический анализ","sub":"События января 2022: причины, хронология, последствия","emoji":"📕","tag":"Governance","progress":100,"color":"#d4907e","lang":"RU/KZ","level":"Продвинутый","direction":"Governance & Policy Analysis"},
        {"title":"Жануарлар","sub":"Детская энциклопедия животных Казахстана на казахском языке","emoji":"🦁","tag":"Education","progress":68,"color":GREEN,"lang":"KZ","level":"Дети 6+","direction":"Education & Knowledge"},
        {"title":"Каспий: экология и ресурсы","sub":"Исследование бассейна: экология, месторождения, геополитика","emoji":"🌊","tag":"Caspian","progress":85,"color":BLUE,"lang":"RU/EN","level":"Средний","direction":"Caspian Intelligence"},
        {"title":"Экономика Шёлкового пути","sub":"Торговые маршруты и геоэкономика XXI века","emoji":"🗺️","tag":"Economic","progress":90,"color":GOLD,"lang":"RU","level":"Продвинутый","direction":"Economic Intelligence"},
        {"title":"Цифровая трансформация ЦА","sub":"IT-экосистема и цифровая экономика Центральной Азии","emoji":"💻","tag":"Economic","progress":75,"color":"#a78bfa","lang":"RU/EN","level":"Средний","direction":"Economic Intelligence"},
        {"title":"Нефтегазовый сектор Казахстана","sub":"Ресурсная база, политика, устойчивое развитие","emoji":"⚡","tag":"Energy","progress":60,"color":"#7eb8d4","lang":"RU","level":"Экспертный","direction":"Energy & Resource Intelligence"},
    ]

    bcols = st.columns(3)
    for i, b in enumerate(BOOKS):
        with bcols[i % 3]:
            st.markdown(f'<div class="ek-card"><div style="display:flex;justify-content:space-between;align-items:flex-start;"><span style="font-size:1.9rem;">{b["emoji"]}</span><span class="ek-tag" style="font-size:.58rem;">{b["tag"]}</span></div><div style="font-family:\'Cormorant Garamond\',serif;font-size:1.15rem;font-weight:700;color:{TEXT};margin:.45rem 0 .2rem;line-height:1.2;">{b["title"]}</div><div style="font-size:.75rem;color:{TEXT3};margin-bottom:.7rem;">{b["sub"]}</div><div style="font-size:.68rem;color:{TEXT3};margin-bottom:.3rem;">🌐 {b["lang"]} &nbsp;·&nbsp; 🎯 {b["level"]}</div><div style="font-size:.68rem;color:{TEXT3};margin-bottom:.5rem;">↗ {b["direction"]}</div><div style="display:flex;justify-content:space-between;font-size:.68rem;color:{TEXT3};margin-bottom:4px;"><span>Готовность</span><span style="color:{b["color"]};">{b["progress"]}%</span></div></div>', unsafe_allow_html=True)
            st.progress(b["progress"] / 100)

    st.markdown("---")
    st.markdown(f'<div class="sec-h" style="font-size:1.2rem;">✨ AI-генератор контента</div><div class="sec-s">Аннотации, резюме, маркетинговые тексты на основе работ автора</div>', unsafe_allow_html=True)

    cl, cr = st.columns(2)
    with cl:
        sel  = st.selectbox("Книга / работа", [b["title"] for b in BOOKS])
        ctype = st.selectbox("Тип контента", [
            "Аннотация (200 слов)",
            "Executive Summary для аудитории государственных органов",
            "Краткое резюме для академической среды",
            "Маркетинговое описание для широкой аудитории",
            "Список ключевых тезисов",
            "Вопросы для обсуждения / дискуссии",
            "Цитаты и тезисы для соцсетей",
        ])
    with cr:
        extra = st.text_area("Дополнительный контекст", height=110,
            placeholder="Для кого: студенты, государственные органы, инвесторы...\nАкцент: ESG, геополитика, история...")

    if st.button("✨ Сгенерировать"):
        if not st.session_state.client:
            st.warning(f"🔑 [Получить API Key →](https://console.anthropic.com/settings/keys) — вставьте в боковой панели")
        else:
            with st.spinner("Генерирую контент..."):
                try:
                    prompt = f"Напиши '{ctype}' для работы «{sel}» из библиотеки Kulekeyev Intelligence Hub. {extra}"
                    full, used = call_ai(st.session_state.client, [{"role":"user","content":prompt}])
                    st.markdown(f'<div class="chat-ai">{full}</div>', unsafe_allow_html=True)
                    st.download_button("⬇️ Скачать текст", data=full, file_name=f"{sel[:30]}_{ctype[:20]}.txt", mime="text/plain")
                    st.markdown(f'<div class="model-tag">Модель: {used}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Ошибка AI: {e}")


    # Book purchase buttons
    st.markdown("---")
    st.markdown(f'<div class="sec-h" style="font-size:1.2rem;">🛒 Купить книги</div><div class="sec-s">Доступны на ведущих платформах</div>', unsafe_allow_html=True)

    STORES = [
        ("🟠", "Kaspi",      "https://kaspi.kz/shop/search/?text=Kulekeyev",      "#f05a28"),
        ("🔵", "Ozon",       "https://www.ozon.ru/search/?text=Kulekeyev",         "#005bff"),
        ("🍓", "Wildberries","https://www.wildberries.ru/catalog/0/search.aspx?search=Kulekeyev","#cb11ab"),
        ("🍎", "Apple Books","https://books.apple.com/search?term=Kulekeyev",      "#fc3c44"),
        ("📦", "Amazon",     "https://www.amazon.com/s?k=Kulekeyev",               "#ff9900"),
        ("🛒", "eBay",       "https://www.ebay.com/sch/i.html?_nkw=Kulekeyev+book","#e53238"),
    ]

    store_cols = st.columns(len(STORES))
    for col, (emoji, name, url, color) in zip(store_cols, STORES):
        with col:
            st.markdown(f"""
            <a href="{url}" target="_blank" style="text-decoration:none;">
              <div style="background:{CARD};border:1px solid {BORDER};border-radius:14px;
                   padding:.9rem .6rem;text-align:center;transition:all .2s;cursor:pointer;
                   box-shadow:0 1px 8px {SHADOW};"
                   onmouseover="this.style.borderColor='{color}';this.style.transform='translateY(-3px)'"
                   onmouseout="this.style.borderColor='{BORDER}';this.style.transform='translateY(0)'">
                <div style="font-size:1.5rem;margin-bottom:.3rem;">{emoji}</div>
                <div style="font-size:.72rem;font-weight:600;color:{TEXT};">{name}</div>
                <div style="font-size:.6rem;color:{color};margin-top:2px;">Купить →</div>
              </div>
            </a>
            """, unsafe_allow_html=True)

    st.markdown(f'<div style="font-size:.7rem;color:{TEXT3};margin-top:.5rem;text-align:center;">Книги доступны в печатном и электронном форматах</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
elif section == "🤖 AI Ассистент":
# ══════════════════════════════════════════════════════════════════════════════

    st.markdown(f'<span class="ek-tag">🤖 Kulekeyev AI · на базе Anthropic Claude</span>', unsafe_allow_html=True)
    st.markdown(f'<div class="sec-h" style="margin-top:.5rem;">Интеллектуальный Ассистент</div><div class="sec-s">Обучен на концепции Hub · 6 направлений · экономика, Каспий, история, ESG</div>', unsafe_allow_html=True)

    if not st.session_state.client:
        st.markdown(f"""
        <div class="ek-card" style="border-color:{BORDER_G};text-align:center;padding:2.2rem;">
          <div style="font-size:2.4rem;margin-bottom:.8rem;">🔑</div>
          <div style="font-family:'Cormorant Garamond',serif;font-size:1.4rem;color:{TEXT};margin-bottom:.5rem;">Активируйте AI-ассистента</div>
          <div style="color:{TEXT2};font-size:.87rem;margin-bottom:1.2rem;max-width:380px;margin-left:auto;margin-right:auto;">
            Для работы нужен бесплатный API-ключ Anthropic. Регистрация занимает 2 минуты.
          </div>
          <a href="https://console.anthropic.com/settings/keys" target="_blank"
             style="display:inline-block;padding:.6rem 1.8rem;border-radius:10px;
             background:linear-gradient(135deg,{GOLD},{GOLDL});color:#0b0e16;
             font-weight:600;text-decoration:none;font-size:.9rem;">
            Получить ключ бесплатно →
          </a>
          <div style="font-size:.72rem;color:{TEXT3};margin-top:.8rem;">Затем вставьте ключ в боковой панели слева</div>
        </div>
        """, unsafe_allow_html=True)

    # Quick prompts by direction
    st.markdown(f'<div style="font-size:.65rem;text-transform:uppercase;letter-spacing:.1em;color:{TEXT3};margin-bottom:.5rem;">Быстрые запросы по направлениям</div>', unsafe_allow_html=True)

    QUICK = [
        ("📈", "Макроэкономика Казахстана 2024"),
        ("⚡", "Нефтяной сектор: вызовы и перспективы"),
        ("🌊", "Экологический статус Каспийского моря"),
        ("🏛️", "Анализ событий Қаңтар 2022"),
        ("🗿", "История казахской цивилизации"),
        ("🌱", "ESG Kazakhstan: с чего начать?"),
        ("📖", "Зачем детские книги на казахском?"),
        ("🌍", "Шёлковый путь в XXI веке"),
        ("💡", "Что такое Kulekeyev Intelligence Hub?"),
    ]

    quick_input = None
    qc = st.columns(3)
    for i, (icon, label) in enumerate(QUICK):
        with qc[i % 3]:
            if st.button(f"{icon} {label}", key=f"q{i}", use_container_width=True):
                quick_input = label

    st.markdown("---")

    # Chat history
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div style="display:flex;justify-content:flex-end;"><div class="chat-user">{msg["content"]}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-ai">🤖 {msg["content"]}</div>', unsafe_allow_html=True)

    final = st.chat_input("Задайте вопрос по экономике, истории, Каспию, ESG...") or quick_input
    if final:
        if not st.session_state.client:
            st.warning("🔑 Введите API Key в боковой панели")
        else:
            st.session_state.chat_history.append({"role": "user", "content": final})
            st.markdown(f'<div style="display:flex;justify-content:flex-end;"><div class="chat-user">{final}</div></div>', unsafe_allow_html=True)
            with st.spinner("AI анализирует..."):
                try:
                    msgs = [{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_history]
                    full, used = call_ai(st.session_state.client, msgs)
                    st.markdown(f'<div class="chat-ai">🤖 {full}</div>', unsafe_allow_html=True)
                    st.session_state.chat_history.append({"role": "assistant", "content": full})
                    st.markdown(f'<div class="model-tag">Модель: {used}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.session_state.chat_history.pop()
                    st.error(f"Ошибка AI: {e}")

    if st.session_state.chat_history:
        if st.button("🗑️ Очистить историю"):
            st.session_state.chat_history = []; st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
elif section == "📊 Аналитика":
# ══════════════════════════════════════════════════════════════════════════════

    st.markdown(f'<div class="sec-h">Аналитика платформы</div><div class="sec-s">Активность Hub · география · публикации</div>', unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    with k1: st.metric("Посетителей (год)", "15.7 K", "+127% к пред. году")
    with k2: st.metric("Публикаций", "38", "+12 в работе")
    with k3: st.metric("Направлений", "6", "+ ESG Initiative")
    with k4: st.metric("Языков", "3", "KZ · RU · EN")

    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["👥 Посетители", "📄 Публикации", "👁️ Просмотры"])
    with tab1:
        ca, cb = st.columns([3, 1])
        with ca: st.plotly_chart(fig_users(df), use_container_width=True, config={"displayModeBar": False})
        with cb:
            for lbl, val in [("Стран", "12"), ("Ср. сессия", "7.8 мин"), ("Возвратов", "62%"), ("Рейтинг", "4.8 ★")]:
                st.markdown(f'<div class="kpi-block" style="padding:.75rem;text-align:left;margin-bottom:.45rem;"><div class="kpi-label">{lbl}</div><div class="kpi-value" style="font-size:1.3rem;color:{GOLD};">{val}</div></div>', unsafe_allow_html=True)
    with tab2: st.plotly_chart(fig_pubs(df), use_container_width=True, config={"displayModeBar": False})
    with tab3: st.plotly_chart(fig_views(df), use_container_width=True, config={"displayModeBar": False})

    st.markdown("---")
    st.markdown(f'<div class="sec-h" style="font-size:1.15rem;">🌍 География аудитории</div>', unsafe_allow_html=True)
    st.plotly_chart(fig_geo(geo_df), use_container_width=True, config={"displayModeBar": False})

    # Direction breakdown
    st.markdown("---")
    st.markdown(f'<div class="sec-h" style="font-size:1.15rem;">📊 Интерес по направлениям</div>', unsafe_allow_html=True)
    dir_data = pd.DataFrame({
        "Направление": ["Economic","Energy & Resource","Caspian","Governance","Civilization","Education"],
        "Запросов": [34, 28, 42, 31, 18, 22],
    })
    fig_dir = go.Figure(go.Bar(
        x=dir_data["Запросов"], y=dir_data["Направление"],
        orientation="h",
        marker=dict(color=[GOLD, BLUE, GREEN, GOLDL, RED, "#a78bfa"], line=dict(width=0)),
        hovertemplate="<b>%{y}</b><br>%{x} запросов<extra></extra>",
    ))
    fig_dir.update_layout(**CT, height=260, showlegend=False)
    st.plotly_chart(fig_dir, use_container_width=True, config={"displayModeBar": False})
