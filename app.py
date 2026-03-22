"""
EurasianKnowledge — Platform
Streamlit app · Light/Dark theme · Anthropic AI
"""

import streamlit as st
import anthropic
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EurasianKnowledge",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Session State ────────────────────────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "client" not in st.session_state:
    st.session_state.client = None

D = st.session_state.dark_mode

# ─── Theme Tokens ─────────────────────────────────────────────────────────────
if D:
    BG         = "#0c0e14"
    BG2        = "#10121a"
    CARD       = "rgba(255,255,255,0.04)"
    BORDER     = "rgba(255,255,255,0.08)"
    BORDER_G   = "rgba(201,169,110,0.3)"
    TEXT       = "#f0e6d3"
    TEXT2      = "#94a3b8"
    TEXT3      = "#4b5563"
    PLOT_BG    = "rgba(0,0,0,0)"
    PLOT_FONT  = "#94a3b8"
    GRID       = "rgba(255,255,255,0.05)"
    MAPSTYLE   = "carto-darkmatter"
    GEO_LAND   = "#1a1e2e"
    GEO_OCEAN  = "#0d1020"
    GEO_COAST  = "rgba(255,255,255,0.1)"
    SHADOW     = "rgba(0,0,0,0.4)"
    INPUT_BG   = "rgba(255,255,255,0.05)"
    HERO_BG    = "linear-gradient(135deg,#0f1120 0%,#1a1e32 50%,#0c0e14 100%)"
    GOLD_DIM   = "rgba(201,169,110,0.12)"
else:
    BG         = "#f5f4f0"
    BG2        = "#ede9e0"
    CARD       = "rgba(255,255,255,0.9)"
    BORDER     = "rgba(0,0,0,0.07)"
    BORDER_G   = "rgba(180,140,70,0.4)"
    TEXT       = "#1a1612"
    TEXT2      = "#5a5248"
    TEXT3      = "#9a9088"
    PLOT_BG    = "rgba(0,0,0,0)"
    PLOT_FONT  = "#5a5248"
    GRID       = "rgba(0,0,0,0.06)"
    MAPSTYLE   = "carto-positron"
    GEO_LAND   = "#e8e4db"
    GEO_OCEAN  = "#c8d8e8"
    GEO_COAST  = "rgba(0,0,0,0.15)"
    SHADOW     = "rgba(0,0,0,0.1)"
    INPUT_BG   = "rgba(0,0,0,0.04)"
    HERO_BG    = "linear-gradient(135deg,#fff8ee 0%,#fef3e2 50%,#f5f0e8 100%)"
    GOLD_DIM   = "rgba(201,169,110,0.1)"

GOLD  = "#c9a96e"
GOLDL = "#e2c99a"
BLUE  = "#7eb8d4"
GREEN = "#4eca8b"

CT = dict(
    plot_bgcolor=PLOT_BG, paper_bgcolor=PLOT_BG,
    font=dict(family="DM Sans", color=PLOT_FONT, size=11),
    xaxis=dict(gridcolor=GRID, linecolor=GRID, tickfont=dict(color=PLOT_FONT)),
    yaxis=dict(gridcolor=GRID, linecolor=GRID, tickfont=dict(color=PLOT_FONT)),
    margin=dict(l=10, r=10, t=20, b=10),
)

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=DM+Sans:wght@300;400;500;600&display=swap');
*,html,body{{font-family:'DM Sans',sans-serif;box-sizing:border-box;}}
.stApp,.stApp>div{{background:{BG}!important;color:{TEXT}!important;}}
.main .block-container{{padding-top:1.5rem;padding-bottom:3rem;}}
[data-testid="stSidebar"]{{background:{BG2}!important;border-right:1px solid {BORDER};}}
[data-testid="stSidebar"] *{{color:{TEXT2}!important;}}
::-webkit-scrollbar{{width:4px;height:4px;}}
::-webkit-scrollbar-thumb{{background:{GOLD}55;border-radius:99px;}}

.ek-card{{background:{CARD};border:1px solid {BORDER};border-radius:18px;padding:1.4rem 1.5rem;margin-bottom:1rem;box-shadow:0 2px 16px {SHADOW};transition:border-color .25s,box-shadow .25s,transform .2s;}}
.ek-card:hover{{border-color:{BORDER_G};box-shadow:0 6px 28px {SHADOW};transform:translateY(-2px);}}

.kpi-block{{background:{CARD};border:1px solid {BORDER};border-radius:16px;padding:1.2rem 1rem;text-align:center;box-shadow:0 1px 8px {SHADOW};transition:transform .2s,box-shadow .2s;}}
.kpi-block:hover{{transform:translateY(-3px);box-shadow:0 8px 24px {SHADOW};}}
.kpi-value{{font-family:'Cormorant Garamond',serif;font-size:2.1rem;font-weight:700;color:{TEXT};line-height:1.1;}}
.kpi-label{{font-size:.68rem;text-transform:uppercase;letter-spacing:.1em;color:{TEXT3};margin-top:4px;}}
.kpi-trend{{font-size:.75rem;font-weight:600;color:{GOLD};margin-top:3px;}}

.ek-tag{{display:inline-flex;align-items:center;gap:5px;padding:3px 12px;border-radius:999px;background:{GOLD_DIM};border:1px solid {BORDER_G};color:{GOLD};font-size:.68rem;font-weight:600;letter-spacing:.08em;text-transform:uppercase;}}

.hero-wrap{{background:{HERO_BG};border-radius:24px;padding:3rem 2.5rem;margin-bottom:2rem;border:1px solid {BORDER_G};position:relative;overflow:hidden;}}
.hero-title{{font-family:'Cormorant Garamond',serif;font-size:clamp(2rem,5vw,3.2rem);font-weight:700;color:{TEXT};line-height:1.1;letter-spacing:-.02em;margin-bottom:.8rem;}}
.hero-gold{{color:{GOLD};}}
.hero-sub{{font-size:1rem;color:{TEXT2};line-height:1.7;max-width:600px;}}

.section-header{{font-family:'Cormorant Garamond',serif;font-size:1.5rem;font-weight:700;color:{TEXT};margin-bottom:.2rem;}}
.section-sub{{font-size:.82rem;color:{TEXT3};margin-bottom:1.2rem;}}

.chat-user{{background:{GOLD_DIM};border:1px solid {BORDER_G};border-radius:16px 16px 4px 16px;padding:.8rem 1rem;margin:.4rem 0;color:{TEXT};font-size:.9rem;max-width:85%;margin-left:auto;}}
.chat-ai{{background:{CARD};border:1px solid {BORDER};border-radius:16px 16px 16px 4px;padding:.8rem 1rem;margin:.4rem 0;color:{TEXT2};font-size:.9rem;line-height:1.65;max-width:90%;}}

.feature-pill{{background:{CARD};border:1px solid {BORDER};border-radius:14px;padding:1.3rem;text-align:center;transition:all .25s;height:100%;}}
.feature-pill:hover{{border-color:{BORDER_G};transform:translateY(-3px);box-shadow:0 8px 24px {SHADOW};}}
.feature-emoji{{font-size:2rem;margin-bottom:.5rem;}}
.feature-title{{font-weight:600;font-size:.9rem;color:{TEXT};margin-bottom:.3rem;}}
.feature-desc{{font-size:.75rem;color:{TEXT3};line-height:1.5;}}

.testimonial{{background:{CARD};border:1px solid {BORDER};border-left:3px solid {GOLD};border-radius:0 14px 14px 0;padding:1.2rem 1.5rem;margin-bottom:1rem;color:{TEXT2};font-size:.9rem;line-height:1.7;font-style:italic;}}
.testimonial-author{{font-style:normal;font-weight:600;color:{GOLD};font-size:.8rem;margin-top:.5rem;}}



/* Buttons */
.stButton>button{{background:linear-gradient(135deg,{GOLD},{GOLDL})!important;color:#0c0e14!important;font-weight:600!important;border:none!important;border-radius:10px!important;padding:.45rem 1.4rem!important;font-family:'DM Sans',sans-serif!important;transition:opacity .2s,transform .15s!important;box-shadow:0 2px 12px rgba(201,169,110,.25)!important;}}
.stButton>button:hover{{opacity:.88!important;transform:translateY(-1px)!important;}}
.theme-btn>button{{background:{CARD}!important;color:{TEXT}!important;border:1px solid {BORDER_G}!important;border-radius:10px!important;width:100%;box-shadow:none!important;}}
.theme-btn>button:hover{{border-color:{GOLD}!important;color:{GOLD}!important;}}

/* Inputs */
.stTextInput>div>input,.stTextArea textarea{{background:{INPUT_BG}!important;border:1px solid {BORDER}!important;border-radius:10px!important;color:{TEXT}!important;}}
.stTextInput>div>input::placeholder,.stTextArea textarea::placeholder{{color:{TEXT3}!important;}}
.stTextInput>div>input:focus,.stTextArea textarea:focus{{border-color:{BORDER_G}!important;box-shadow:0 0 0 2px {GOLD_DIM}!important;}}
.stSelectbox>div>div{{background:{INPUT_BG}!important;border:1px solid {BORDER}!important;border-radius:10px!important;color:{TEXT}!important;}}

/* Tabs */
.stTabs [data-baseweb="tab-list"]{{background:{CARD};border-radius:10px;padding:4px;gap:3px;border:1px solid {BORDER};}}
.stTabs [data-baseweb="tab"]{{background:transparent;color:{TEXT3};border-radius:8px;font-size:.82rem;font-weight:600;padding:.4rem 1rem;}}
.stTabs [aria-selected="true"]{{background:linear-gradient(135deg,{GOLD},{GOLDL})!important;color:#0c0e14!important;}}

/* Progress */
.stProgress>div>div{{background:linear-gradient(90deg,{GOLD},{GOLDL})!important;border-radius:99px!important;}}
.stProgress>div{{background:{BORDER}!important;border-radius:99px!important;}}

/* Metrics */
[data-testid="metric-container"]{{background:{CARD};border:1px solid {BORDER};border-radius:14px;padding:1rem 1.2rem;}}
[data-testid="stMetricLabel"]{{color:{TEXT3}!important;font-size:.68rem!important;text-transform:uppercase!important;letter-spacing:.08em!important;}}
[data-testid="stMetricValue"]{{color:{TEXT}!important;font-family:'Cormorant Garamond',serif!important;font-size:2rem!important;}}
[data-testid="stMetricDelta"]{{color:{GOLD}!important;}}

.stAlert{{border-radius:12px!important;}}
hr{{border-color:{BORDER}!important;margin:1.5rem 0!important;}}
#MainMenu,footer{{visibility:hidden;}}
header[data-testid="stHeader"]{{background:transparent!important;}}
</style>
""", unsafe_allow_html=True)

# ─── Data ─────────────────────────────────────────────────────────────────────
@st.cache_data
def get_df():
    months = ["Янв","Фев","Мар","Апр","Май","Июн","Июл","Авг","Сен","Окт","Ноя","Дек"]
    return pd.DataFrame({"month":months,
        "revenue":[42,59,53,77,67,101,91,129,118,145,162,190],
        "users":  [2800,3400,3100,4200,4900,6300,7100,9200,10400,12100,14500,17800],
        "books":  [38,52,46,71,88,110,104,138,151,172,198,230]})

@st.cache_data
def get_geo():
    return pd.DataFrame({"country":["Казахстан","Россия","Китай","Узбекистан","Кыргызстан","Германия","США"],
        "users":[18400,9200,4100,2800,1300,980,720],"revenue_share":[48,24,11,7,4,3,3],
        "lat":[48.0,61.5,35.9,41.4,41.2,51.2,37.1],"lon":[68.0,105.3,104.2,64.6,74.7,10.4,-95.7]})

@st.cache_data
def get_caspian():
    np.random.seed(42)
    return pd.DataFrame({"station":["Актау","Баку","Астрахань","Туркменбаши","Энзели"],
        "water_level":[round(np.random.uniform(-28.5,-27.8),2) for _ in range(5)],
        "salinity":   [round(np.random.uniform(12.5,13.5),1)  for _ in range(5)],
        "temp":       [round(np.random.uniform(10,24),1)       for _ in range(5)],
        "oil_index":  [round(np.random.uniform(0.02,0.18),3)   for _ in range(5)],
        "lat":[43.65,40.41,46.35,40.02,37.47],"lon":[51.17,49.87,48.03,53.00,49.47]})

# ─── Charts ───────────────────────────────────────────────────────────────────
def fig_revenue(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["month"],y=df["revenue"],fill="tozeroy",
        fillcolor=f"rgba(201,169,110,{0.08 if D else 0.12})",
        line=dict(color=GOLD,width=2.5),mode="lines+markers",
        marker=dict(color=GOLD,size=6,line=dict(color=BG,width=2)),
        hovertemplate="<b>%{x}</b><br>$%{y}K<extra></extra>"))
    fig.update_layout(**CT,height=240,showlegend=False)
    return fig

def fig_users(df):
    fig = go.Figure(go.Bar(x=df["month"],y=df["users"],
        marker=dict(color=df["users"].tolist(),colorscale=[[0,f"rgba(126,184,212,.3)"],[1,BLUE]],line=dict(width=0)),
        hovertemplate="<b>%{x}</b><br>%{y:,}<extra></extra>"))
    fig.update_layout(**CT,height=240,showlegend=False)
    return fig

def fig_books(df):
    fig = go.Figure(go.Bar(x=df["month"],y=df["books"],
        marker=dict(color=GREEN,opacity=.75,line=dict(width=0)),
        hovertemplate="<b>%{x}</b><br>%{y}<extra></extra>"))
    fig.update_layout(**CT,height=240,showlegend=False)
    return fig

def fig_geo(df):
    fig = px.scatter_geo(df,lat="lat",lon="lon",size="users",color="revenue_share",
        color_continuous_scale=[[0,GEO_LAND],[.5,"#6b4e20"],[1,GOLD]],
        hover_name="country",hover_data={"users":True,"revenue_share":True,"lat":False,"lon":False},size_max=40)
    fig.update_layout(geo=dict(bgcolor=PLOT_BG,showland=True,landcolor=GEO_LAND,showocean=True,oceancolor=GEO_OCEAN,
        showcoastlines=True,coastlinecolor=GEO_COAST,showframe=False,projection_type="natural earth",
        center=dict(lat=45,lon=65),projection_scale=2.2),
        paper_bgcolor=PLOT_BG,coloraxis_showscale=False,margin=dict(l=0,r=0,t=0,b=0),height=320)
    return fig

def fig_caspian(df):
    fig = px.scatter_mapbox(df,lat="lat",lon="lon",size="oil_index",color="temp",
        color_continuous_scale=[[0,BLUE],[.5,GOLD],[1,"#ef4444"]],hover_name="station",
        hover_data={"water_level":":.2f","salinity":":.1f","temp":":.1f","oil_index":":.3f","lat":False,"lon":False},
        size_max=35,zoom=3.8,center={"lat":42,"lon":51})
    fig.update_layout(mapbox_style=MAPSTYLE,paper_bgcolor=PLOT_BG,coloraxis_showscale=False,margin=dict(l=0,r=0,t=0,b=0),height=360)
    return fig



# ─── AI ───────────────────────────────────────────────────────────────────────
SYS = """Ты — помощник платформы EurasianKnowledge. Эксперт по экономике Евразии и Каспийскому региону.
Помогаешь студентам, предпринимателям и исследователям. Отвечай дружелюбно и структурированно.
Книги: «Қаңтар» (политология), «Жануарлар» (детская KZ), «Каспий: экология»,
«Экономика Шёлкового пути», «Цифровая трансформация ЦА»."""

MODELS = [
    "claude-opus-4-5",
    "claude-sonnet-4-5",
    "claude-3-5-sonnet-20241022",
    "claude-3-5-haiku-20241022",
]

def call_ai(client, messages):
    """Try models in order until one works, return (text, model_used)."""
    last_err = None
    for model in MODELS:
        try:
            resp = client.messages.create(
                model=model, max_tokens=1200,
                system=SYS, messages=messages,
            )
            return resp.content[0].text, model
        except anthropic.BadRequestError:
            raise   # bad input — don't retry other models
        except Exception as e:
            last_err = e
            continue
    raise last_err

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f'<div style="font-family:\'Cormorant Garamond\',serif;font-size:1.4rem;font-weight:700;color:{TEXT};margin-bottom:4px;">🌐 EurasianKnowledge</div>', unsafe_allow_html=True)
    st.markdown(f'<span class="ek-tag">Цифровая экосистема знаний</span>', unsafe_allow_html=True)

    st.markdown(f'<div style="font-size:.65rem;text-transform:uppercase;letter-spacing:.1em;color:{TEXT3};margin:1rem 0 .4rem;">Оформление</div>', unsafe_allow_html=True)
    cd, cl = st.columns(2)
    with cd:
        st.markdown('<div class="theme-btn">', unsafe_allow_html=True)
        if st.button("🌙 Тёмная", use_container_width=True, key="t_dark"):
            st.session_state.dark_mode = True; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with cl:
        st.markdown('<div class="theme-btn">', unsafe_allow_html=True)
        if st.button("☀️ Светлая", use_container_width=True, key="t_light"):
            st.session_state.dark_mode = False; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:.7rem;color:{GOLD};text-align:center;margin:.3rem 0 .5rem;">Активна: {"🌙 Тёмная" if D else "☀️ Светлая"}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f'<div style="font-size:.65rem;text-transform:uppercase;letter-spacing:.1em;color:{TEXT3};margin-bottom:.4rem;">Разделы</div>', unsafe_allow_html=True)
    section = st.radio("nav", ["🏠 Главная","📊 Аналитика","🗺️ GIS Каспий","📚 Библиотека","🤖 AI Ассистент"],
        label_visibility="collapsed")

    st.markdown("---")
    st.markdown(f'<div style="font-size:.65rem;text-transform:uppercase;letter-spacing:.1em;color:{TEXT3};margin-bottom:.4rem;">AI — Anthropic API</div>', unsafe_allow_html=True)
    api_key = st.text_input("key", type="password", placeholder="sk-ant-...", label_visibility="collapsed")
    st.markdown(f'<a href="https://console.anthropic.com/settings/keys" target="_blank" style="font-size:.75rem;color:{GOLD};text-decoration:none;font-weight:500;">🔑 Получить бесплатный ключ →</a>', unsafe_allow_html=True)
    if api_key:
        try:
            st.session_state.client = anthropic.Anthropic(api_key=api_key)
            st.markdown(f'<div style="color:{GREEN};font-size:.75rem;margin-top:4px;">✓ AI подключён</div>', unsafe_allow_html=True)
        except Exception:
            st.markdown('<div style="color:#ef4444;font-size:.75rem;margin-top:4px;">✗ Неверный ключ</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.selectbox("Язык", ["🇷🇺 RU","🇰🇿 KZ","🇬🇧 EN"], label_visibility="collapsed")
    st.markdown(f'<div style="font-size:.65rem;color:{TEXT3};margin-top:1.5rem;line-height:1.6;">© 2025 EurasianKnowledge<br>Цифровая платформа знаний</div>', unsafe_allow_html=True)

# ─── Load data ────────────────────────────────────────────────────────────────
df = get_df(); geo_df = get_geo(); cas_df = get_caspian()

# ══════════════════════════════════════════════════════════════════════════════
if section == "🏠 Главная":
# ══════════════════════════════════════════════════════════════════════════════
    st.markdown(f"""
    <div class="hero-wrap">
        <span class="ek-tag" style="margin-bottom:1rem;display:inline-block;">🌐 Евразийская платформа знаний</span>
        <div class="hero-title">Знания Евразии —<br><span class="hero-gold">в одном месте</span></div>
        <div class="hero-sub">Исследуйте экономику Каспийского региона, читайте книги на казахском и русском,
        задавайте вопросы AI-ассистенту. Для студентов, предпринимателей и исследователей.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="section-header">Что вы получаете</div><div class="section-sub">Всё необходимое для изучения Евразии в одном приложении</div>', unsafe_allow_html=True)
    fcols = st.columns(3)
    for i,(emoji,title,desc) in enumerate([
        ("🤖","AI-Ассистент","Задайте любой вопрос про экономику, историю, книги. Мгновенный ответ."),
        ("🗺️","Карта Каспия","GIS-мониторинг с экологическими и ресурсными данными в реальном времени."),
        ("📚","Библиотека книг","5 авторских книг с AI-озвучкой на казахском, русском и английском."),
        ("📊","Аналитика рынков","Данные по СНГ, Китаю, нефтяным рынкам и торговым маршрутам."),
        ("🌍","3 языка","Контент на казахском, русском и английском — для всех пользователей."),
        ("🎓","Edu-модуль","Образовательные курсы и энциклопедии для детей и студентов."),
    ]):
        with fcols[i%3]:
            st.markdown(f'<div class="feature-pill"><div class="feature-emoji">{emoji}</div><div class="feature-title">{title}</div><div class="feature-desc">{desc}</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f'<div class="section-header">Для кого эта платформа?</div>', unsafe_allow_html=True)
    a1,a2,a3 = st.columns(3)
    for col,emoji,title,items,color in [
        (a1,"🎓","Студентам",["Конспекты и AI-помощник","Книги с озвучкой","Аналитика для курсовых"],BLUE),
        (a2,"💼","Предпринимателям",["Рыночная аналитика СНГ","Данные по торговым маршрутам","Экспортные отчёты"],GOLD),
        (a3,"🔬","Исследователям",["GIS Каспийского бассейна","38+ аналитических статей","Экспорт данных"],GREEN),
    ]:
        with col:
            items_html = "".join(f'<li style="font-size:.82rem;color:{TEXT2};margin-bottom:6px;list-style:none;">✓ {it}</li>' for it in items)
            st.markdown(f'<div class="ek-card"><div style="font-size:2rem;margin-bottom:.5rem;">{emoji}</div><div style="font-family:\'Cormorant Garamond\',serif;font-size:1.2rem;font-weight:700;color:{TEXT};margin-bottom:.8rem;">{title}</div><ul style="padding:0;margin:0;">{items_html}</ul></div>', unsafe_allow_html=True)



    st.markdown("---")
    st.markdown(f'<div class="section-header">Отзывы пользователей</div>', unsafe_allow_html=True)
    t1c,t2c = st.columns(2)
    for col,text,author in [
        (t1c,"Отличный инструмент для написания дипломной — AI помог структурировать аналитику по экономике Казахстана за 20 минут.","Айгерим С., студентка КазНУ"),
        (t2c,"Наконец-то одна платформа для всего: карта Каспия, экспортные данные и переводчик. Использую каждую неделю.","Данияр М., торговый аналитик"),
    ]:
        with col:
            st.markdown(f'<div class="testimonial">{text}<div class="testimonial-author">— {author}</div></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
elif section == "📊 Аналитика":
# ══════════════════════════════════════════════════════════════════════════════
    st.markdown(f'<div class="section-header">Аналитический дашборд</div><div class="section-sub">Рынки СНГ · Китай · Нефть · Торговля</div>', unsafe_allow_html=True)
    k1,k2,k3,k4 = st.columns(4)
    with k1: st.metric("Активных читателей","38 K","+127% за год")
    with k2: st.metric("Книг в библиотеке","5","+2 в разработке")
    with k3: st.metric("Статей & отчётов","38","Новые каждый месяц")
    with k4: st.metric("Языков","3","KZ · RU · EN")
    st.markdown("---")
    tab1,tab2,tab3 = st.tabs(["💰 Выручка","👥 Пользователи","📚 Книги"])
    with tab1:
        ca,cb = st.columns([3,1])
        with ca: st.plotly_chart(fig_revenue(df),use_container_width=True,config={"displayModeBar":False})
        with cb:
            for lbl,val in [("Стран охвата","12"),("Ср. сессия","8.4 мин"),("Повторных визитов","64%"),("Рейтинг","4.8 ★")]:
                st.markdown(f'<div class="kpi-block" style="padding:.8rem;text-align:left;margin-bottom:.5rem;"><div class="kpi-label">{lbl}</div><div class="kpi-value" style="font-size:1.4rem;color:{GOLD};">{val}</div></div>', unsafe_allow_html=True)
    with tab2: st.plotly_chart(fig_users(df),use_container_width=True,config={"displayModeBar":False})
    with tab3: st.plotly_chart(fig_books(df),use_container_width=True,config={"displayModeBar":False})
    st.markdown("---")
    st.markdown(f'<div class="section-header" style="font-size:1.1rem;">🌍 География аудитории</div>', unsafe_allow_html=True)
    st.plotly_chart(fig_geo(geo_df),use_container_width=True,config={"displayModeBar":False})

# ══════════════════════════════════════════════════════════════════════════════
elif section == "🗺️ GIS Каспий":
# ══════════════════════════════════════════════════════════════════════════════
    st.markdown(f'<span class="ek-tag">🛰️ Live GIS</span>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-header">Каспийский бассейн</div><div class="section-sub">Экологический мониторинг · спутниковые данные · анализ месторождений</div>', unsafe_allow_html=True)
    cols = st.columns(5)
    for i,(_,row) in enumerate(cas_df.iterrows()):
        with cols[i]:
            oc = "#ef4444" if row["oil_index"]>.12 else GREEN
            st.markdown(f'<div class="kpi-block"><div class="kpi-label">{row["station"]}</div><div class="kpi-value" style="font-size:1.3rem;">{row["temp"]:.1f}°C</div><div style="font-size:.65rem;color:{oc};margin-top:3px;">Нефть: {row["oil_index"]:.3f}</div><div style="font-size:.65rem;color:{TEXT3};">Ур.: {row["water_level"]:.2f} м</div></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.plotly_chart(fig_caspian(cas_df),use_container_width=True,config={"displayModeBar":False})
    st.markdown("---")
    cl,cr = st.columns(2)
    with cl:
        st.markdown(f'<div class="section-header" style="font-size:1.1rem;">📋 Данные</div>', unsafe_allow_html=True)
        disp = cas_df[["station","temp","salinity","water_level","oil_index"]].copy()
        disp.columns = ["Станция","°C","Солёность ‰","Уровень м","Нефть"]
        st.dataframe(disp,use_container_width=True,hide_index=True)
    with cr:
        st.markdown(f'<div class="section-header" style="font-size:1.1rem;">📊 Температура</div>', unsafe_allow_html=True)
        fig = go.Figure(go.Bar(x=cas_df["station"],y=cas_df["temp"],
            marker=dict(color=cas_df["temp"].tolist(),colorscale=[[0,BLUE],[1,GOLD]],line=dict(width=0)),
            hovertemplate="<b>%{x}</b><br>%{y:.1f}°C<extra></extra>"))
        fig.update_layout(**CT,height=220,showlegend=False)
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    if st.session_state.client:
        st.markdown("---")
        if st.button("🤖 AI-отчёт по экологии"):
            prompt = f"Краткий экологический отчёт по данным Каспия: {cas_df.to_dict('records')}"
            with st.spinner("Генерирую отчёт..."):
                try:
                    full, used = call_ai(st.session_state.client, [{"role":"user","content":prompt}])
                    st.markdown(f'<div class="chat-ai">{full}</div>', unsafe_allow_html=True)
                    st.caption(f"Модель: {used}")
                except Exception as e:
                    st.error(f"Ошибка AI: {e}")
    else:
        st.info(f"🔑 [Получить API Key](https://console.anthropic.com/settings/keys) и вставьте в боковой панели для AI-анализа.")

# ══════════════════════════════════════════════════════════════════════════════
elif section == "📚 Библиотека":
# ══════════════════════════════════════════════════════════════════════════════
    st.markdown(f'<div class="section-header">Библиотека книг</div><div class="section-sub">Авторский контент на трёх языках · AI-озвучка · Образование</div>', unsafe_allow_html=True)
    BOOKS = [
        {"title":"Қаңтар","sub":"Политологический анализ событий","emoji":"📕","tag":"Политология","progress":100,"sales":312,"color":"#d4907e","level":"Продвинутый","lang":"RU/KZ","pages":280},
        {"title":"Жануарлар","sub":"Детская энциклопедия животных","emoji":"🦁","tag":"Дети 6+","progress":68,"sales":284,"color":GREEN,"level":"Дети 6+","lang":"KZ","pages":96},
        {"title":"Каспий: экология","sub":"Ресурсы и экомониторинг","emoji":"🌊","tag":"Наука","progress":85,"sales":98,"color":BLUE,"level":"Средний","lang":"RU/EN","pages":196},
        {"title":"Экономика Шёлкового пути","sub":"Торговые маршруты XXI века","emoji":"🗺️","tag":"Аналитика","progress":90,"sales":104,"color":GOLD,"level":"Продвинутый","lang":"RU","pages":224},
        {"title":"Цифровая трансформация ЦА","sub":"IT-экосистема Центральной Азии","emoji":"💻","tag":"Tech","progress":75,"sales":44,"color":"#a78bfa","level":"Средний","lang":"RU/EN","pages":160},
    ]
    bcols = st.columns(3)
    for i,b in enumerate(BOOKS):
        with bcols[i%3]:
            st.markdown(f'<div class="ek-card"><div style="display:flex;justify-content:space-between;align-items:flex-start;"><span style="font-size:2rem;">{b["emoji"]}</span><span class="ek-tag" style="font-size:.6rem;">{b["tag"]}</span></div><div style="font-family:\'Cormorant Garamond\',serif;font-size:1.25rem;font-weight:700;color:{TEXT};margin:.5rem 0 .2rem;">{b["title"]}</div><div style="font-size:.78rem;color:{TEXT3};margin-bottom:.8rem;">{b["sub"]}</div><div style="display:flex;gap:1rem;font-size:.7rem;color:{TEXT3};margin-bottom:.7rem;"><span>📖 {b["pages"]} стр</span><span>🌐 {b["lang"]}</span><span>🎯 {b["level"]}</span></div><div style="display:flex;justify-content:space-between;font-size:.7rem;color:{TEXT3};margin-bottom:4px;"><span>Готовность</span><span style="color:{b["color"]}">{b["progress"]}%</span></div></div>', unsafe_allow_html=True)
            st.progress(b["progress"]/100)
            st.markdown(f'<div style="font-size:.72rem;color:{TEXT3};margin-bottom:.3rem;">📦 Продаж: <b style="color:{b["color"]}">{b["sales"]}</b></div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(f'<div class="section-header" style="font-size:1.2rem;">✨ AI-генератор контента</div>', unsafe_allow_html=True)
    cl,cr = st.columns(2)
    with cl:
        sel = st.selectbox("Книга",[b["title"] for b in BOOKS])
        ctype = st.selectbox("Тип",["Аннотация (200 слов)","Executive Summary","Маркетинговый текст","Вопросы для обсуждения","Цитаты для соцсетей"])
    with cr:
        extra = st.text_area("Дополнительный контекст",height=100,placeholder="Для кого: студент, инвестор...")
    if st.button("✨ Сгенерировать"):
        if not st.session_state.client:
            st.warning(f"🔑 [Получить API Key →](https://console.anthropic.com/settings/keys) и вставьте в боковой панели.")
        else:
            with st.spinner("Генерирую контент..."):
                try:
                    full, used = call_ai(st.session_state.client, [{"role":"user","content":f"Напиши '{ctype}' для книги '{sel}'. {extra}"}])
                    st.markdown(f'<div class="chat-ai">{full}</div>', unsafe_allow_html=True)
                    st.download_button("⬇️ Скачать", data=full, file_name=f"{sel}.txt", mime="text/plain")
                    st.caption(f"Модель: {used}")
                except Exception as e:
                    st.error(f"Ошибка AI: {e}")

# ══════════════════════════════════════════════════════════════════════════════
elif section == "🤖 AI Ассистент":
# ══════════════════════════════════════════════════════════════════════════════
    st.markdown(f'<span class="ek-tag">🤖 Author AI · v2.0</span>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-header">AI-Ассистент</div><div class="section-sub">Задайте любой вопрос — обучен на книгах и статьях платформы</div>', unsafe_allow_html=True)
    if not st.session_state.client:
        st.markdown(f'<div class="ek-card" style="border-color:{BORDER_G};text-align:center;padding:2rem;"><div style="font-size:2.5rem;margin-bottom:1rem;">🔑</div><div style="font-family:\'Cormorant Garamond\',serif;font-size:1.4rem;color:{TEXT};margin-bottom:.5rem;">Активируйте AI-ассистента</div><div style="color:{TEXT2};font-size:.88rem;margin-bottom:1.2rem;">Для работы нужен бесплатный API-ключ Anthropic</div><a href="https://console.anthropic.com/settings/keys" target="_blank" style="display:inline-block;padding:.6rem 1.8rem;border-radius:10px;background:linear-gradient(135deg,{GOLD},{GOLDL});color:#0c0e14;font-weight:600;text-decoration:none;font-size:.9rem;">Получить ключ бесплатно →</a><div style="font-size:.75rem;color:{TEXT3};margin-top:.8rem;">Затем вставьте в боковой панели слева</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:.7rem;text-transform:uppercase;letter-spacing:.1em;color:{TEXT3};margin-bottom:.5rem;">Быстрые запросы</div>', unsafe_allow_html=True)
    quick_input = None
    qcols = st.columns(3)
    for i,(icon,label) in enumerate([("📊","Аналитика ВВП Казахстана"),("📝","Аннотация к «Қаңтар»"),("🛢️","Обзор нефтяного рынка СНГ"),("🌊","Экологический статус Каспия"),("💡","Топ-5 фактов о Шёлковом пути"),("🎓","Объясни простыми словами")]):
        with qcols[i%3]:
            if st.button(f"{icon} {label}",key=f"q{i}",use_container_width=True):
                quick_input = label
    st.markdown("---")
    for msg in st.session_state.chat_history:
        if msg["role"]=="user":
            st.markdown(f'<div style="display:flex;justify-content:flex-end;"><div class="chat-user">{msg["content"]}</div></div>',unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-ai">🤖 {msg["content"]}</div>',unsafe_allow_html=True)
    final = st.chat_input("Напишите запрос...") or quick_input
    if final:
        if not st.session_state.client:
            st.warning("🔑 Введите API Key в боковой панели")
        else:
            st.session_state.chat_history.append({"role":"user","content":final})
            st.markdown(f'<div style="display:flex;justify-content:flex-end;"><div class="chat-user">{final}</div></div>',unsafe_allow_html=True)
            with st.spinner("AI думает..."):
                try:
                    msgs = [{"role":m["role"],"content":m["content"]} for m in st.session_state.chat_history]
                    full, used = call_ai(st.session_state.client, msgs)
                    st.markdown(f'<div class="chat-ai">🤖 {full}</div>', unsafe_allow_html=True)
                    st.session_state.chat_history.append({"role":"assistant","content":full})
                    st.caption(f"Модель: {used}")
                except Exception as e:
                    st.session_state.chat_history.pop()  # remove failed user msg
                    st.error(f"Ошибка AI: {e}")
    if st.session_state.chat_history:
        if st.button("🗑️ Очистить историю"):
            st.session_state.chat_history=[]; st.rerun()
