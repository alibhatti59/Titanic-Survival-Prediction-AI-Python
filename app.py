import os
import base64

import pandas as pd
import joblib
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


# ─── PAGE CONFIG ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Titanic Survival Dashboard",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ─── SESSION STATE ─────────────────────────────────────────────────────────────

if "nav" not in st.session_state:
    st.session_state.nav = "Home"


def sync_nav():
    pass


def go_to(page_name):
    st.session_state.nav = page_name


# ─── BACKGROUND ────────────────────────────────────────────────────────────────

def _b64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


_bg = "assets/background.webp"
if os.path.exists(_bg):
    _data = _b64(_bg)
    _bg_css = f"""
    background-image:
        linear-gradient(160deg, rgba(6,12,24,0.91) 0%, rgba(10,14,26,0.96) 100%),
        url("data:image/webp;base64,{_data}");
    """
else:
    _bg_css = (
        "background: radial-gradient("
        "ellipse at 30% 15%, #0d1b2a 0%, #0a0e1a 55%, #060c16 100%);"
    )


# ─── STYLES ────────────────────────────────────────────────────────────────────

st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ══ Design Tokens ══════════════════════════════════════════════════════════ */
:root {{
    --ocean:      #0a0e1a;
    --navy:       #0d1b2a;
    --navy-hi:    #111f35;
    --gold:       #c9a84c;
    --gold-hi:    #e8c96a;
    --green:      #34c97e;
    --red:        #e05252;
    --ice:        #4fb3e8;
    --ivory:      #e8d5a3;
    --text:       #f0e8d5;
    --text-60:    rgba(240,232,213,0.60);
    --text-35:    rgba(240,232,213,0.35);
    --border:     rgba(201,168,76,0.20);
    --border-hi:  rgba(201,168,76,0.40);
}}

/* ══ Base ═══════════════════════════════════════════════════════════════════ */
.stApp {{
    {_bg_css}
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    font-family: 'Inter', sans-serif;
}}
[data-testid="stAppViewContainer"],
[data-testid="stHeader"] {{ background: transparent; }}
.main .block-container {{ padding-top: 1.5rem; padding-bottom: 4rem; max-width: 1280px; }}

/* ══ Typography ══════════════════════════════════════════════════════════════ */
h1, h2, h3, h4, h5, h6 {{
    font-family: 'Playfair Display', serif !important;
    color: var(--text) !important;
}}
p, span, div, label, li {{
    font-family: 'Inter', sans-serif !important;
    color: var(--text) !important;
}}

/* ══ Sidebar ════════════════════════════════════════════════════════════════ */
section[data-testid="stSidebar"] {{
    background: linear-gradient(175deg, #060c18 0%, #08101e 100%) !important;
    border-right: 1px solid var(--border) !important;
}}
/* Gold left accent bar on sidebar */
section[data-testid="stSidebar"]::before {{
    content: '';
    position: fixed;
    top: 0; left: 0;
    width: 2px;
    height: 100vh;
    background: linear-gradient(180deg,
        transparent 0%, var(--gold) 20%,
        var(--gold-hi) 50%, var(--gold) 80%, transparent 100%);
    opacity: 0.45;
    pointer-events: none;
    z-index: 999;
}}
/* Sidebar radio label (the "Navigate" heading) */
section[data-testid="stSidebar"] [data-testid="stRadio"] > label p {{
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.64rem !important;
    letter-spacing: 0.22em !important;
    text-transform: uppercase !important;
    color: var(--gold) !important;
    opacity: 0.85;
}}
/* Sidebar radio options */
section[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] label p {{
    font-family: 'Inter', sans-serif !important;
    font-size: 0.88rem !important;
    color: var(--text-60) !important;
    letter-spacing: 0.02em !important;
    transition: color 0.2s;
}}
section[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] label:hover p {{
    color: var(--ivory) !important;
}}

/* ══ Hero Card ══════════════════════════════════════════════════════════════ */
.hero-card {{
    position: relative;
    background: linear-gradient(145deg, rgba(13,27,42,0.98), rgba(17,31,53,0.98));
    padding: 52px 44px;
    border-radius: 2px;
    border: 1px solid var(--border);
    box-shadow: 0 0 0 1px rgba(201,168,76,0.05), 0 28px 64px rgba(0,0,0,0.55);
    margin-bottom: 28px;
    text-align: center;
    overflow: hidden;
}}
/* Top & bottom gold gradient rules — the Art Deco signature */
.hero-card::before {{
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg,
        transparent 0%, var(--gold) 25%, var(--gold-hi) 50%,
        var(--gold) 75%, transparent 100%);
}}
.hero-card::after {{
    content: '';
    position: absolute; bottom: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg,
        transparent 0%, var(--gold) 25%, var(--gold-hi) 50%,
        var(--gold) 75%, transparent 100%);
}}
/* Art Deco corner brackets */
.deco-tl, .deco-tr, .deco-bl, .deco-br {{
    position: absolute;
    width: 18px; height: 18px;
    border-color: var(--gold);
    border-style: solid;
    opacity: 0.38;
}}
.deco-tl {{ top: 14px; left: 14px;   border-width: 1px 0 0 1px; }}
.deco-tr {{ top: 14px; right: 14px;  border-width: 1px 1px 0 0; }}
.deco-bl {{ bottom: 14px; left: 14px;  border-width: 0 0 1px 1px; }}
.deco-br {{ bottom: 14px; right: 14px; border-width: 0 1px 1px 0; }}

.hero-eyebrow {{
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.70rem !important;
    color: var(--gold) !important;
    letter-spacing: 0.24em;
    text-transform: uppercase;
    display: block;
    margin-bottom: 18px;
    opacity: 0.85;
}}
.hero-title {{
    font-family: 'Playfair Display', serif !important;
    font-size: clamp(2.2rem, 4vw, 3.5rem) !important;
    font-weight: 800 !important;
    color: var(--ivory) !important;
    letter-spacing: 0.03em;
    line-height: 1.15;
    margin: 0 0 4px 0;
}}
.gold-div {{
    width: 100px; height: 1px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
    margin: 18px auto;
}}
.hero-sub {{
    font-family: 'Inter', sans-serif !important;
    font-size: 0.88rem !important;
    color: var(--text-60) !important;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    font-weight: 400;
}}

/* ══ Glass Cards ════════════════════════════════════════════════════════════ */
.glass-card {{
    background: rgba(13,27,42,0.80);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid var(--border);
    border-radius: 2px;
    padding: 28px 32px;
    box-shadow: 0 12px 40px rgba(0,0,0,0.28), inset 0 1px 0 rgba(201,168,76,0.07);
    margin-bottom: 22px;
    transition: border-color 0.3s ease;
}}
.glass-card:hover {{ border-color: var(--border-hi); }}

.section-eyebrow {{
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.65rem !important;
    color: var(--gold) !important;
    letter-spacing: 0.24em;
    text-transform: uppercase;
    display: block;
    margin-bottom: 8px;
    opacity: 0.85;
}}
.section-title {{
    font-family: 'Playfair Display', serif !important;
    font-size: 1.5rem !important;
    font-weight: 700 !important;
    color: var(--ivory) !important;
    letter-spacing: 0.02em;
    margin-bottom: 4px;
}}
.accent-line {{
    width: 44px; height: 2px;
    background: linear-gradient(90deg, var(--gold), var(--gold-hi));
    margin: 12px 0 18px 0;
}}
.section-body {{
    font-size: 0.93rem !important;
    color: var(--text-60) !important;
    line-height: 1.74;
    margin: 0;
}}

/* ══ Sub-headings (within page content) ════════════════════════════════════ */
.sub-heading {{
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 28px 0 16px 0;
}}
.sub-bar {{
    width: 3px; height: 26px; flex-shrink: 0;
    background: linear-gradient(180deg, var(--gold), var(--gold-hi));
}}
.sub-text {{
    font-family: 'Playfair Display', serif !important;
    font-size: 1.18rem !important;
    font-weight: 700 !important;
    color: var(--ivory) !important;
}}

/* ══ Metric Cards ═══════════════════════════════════════════════════════════ */
.metric-card {{
    background: rgba(13,27,42,0.90);
    border: 1px solid var(--border);
    border-radius: 2px;
    padding: 22px 20px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.24);
    transition: border-color 0.25s, box-shadow 0.25s, transform 0.25s;
    position: relative;
    overflow: hidden;
    height: 100%;
}}
.metric-card::before {{
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
    opacity: 0.55;
}}
.metric-card:hover {{
    border-color: var(--border-hi);
    transform: translateY(-2px);
    box-shadow: 0 14px 32px rgba(0,0,0,0.32);
}}
.metric-label {{
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.63rem !important;
    color: var(--gold) !important;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    display: block;
    margin-bottom: 10px;
    opacity: 0.85;
}}
.metric-value {{
    font-family: 'Playfair Display', serif !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
    color: var(--ivory) !important;
    line-height: 1;
}}

/* ══ Buttons ════════════════════════════════════════════════════════════════ */
.stButton > button {{
    border-radius: 2px !important;
    border: 1px solid rgba(201,168,76,0.42) !important;
    padding: 0.72rem 1.6rem !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.80rem !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    background: rgba(201,168,76,0.08) !important;
    color: var(--gold-hi) !important;
    transition: all 0.22s ease !important;
    box-shadow: 0 4px 14px rgba(0,0,0,0.22) !important;
}}
.stButton > button:hover {{
    background: rgba(201,168,76,0.16) !important;
    border-color: rgba(201,168,76,0.68) !important;
    box-shadow: 0 6px 20px rgba(201,168,76,0.14) !important;
    transform: translateY(-1px) !important;
    color: #f0d87a !important;
}}

/* ══ Form Inputs ════════════════════════════════════════════════════════════ */
[data-testid="stSelectbox"] label p,
[data-testid="stNumberInput"] label p {{
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    color: var(--gold) !important;
}}

/* ══ Status Messages ════════════════════════════════════════════════════════ */
[data-testid="stSuccess"] {{
    background: rgba(52,201,126,0.07) !important;
    border: 1px solid rgba(52,201,126,0.26) !important;
    border-radius: 2px !important;
}}
[data-testid="stError"] {{
    background: rgba(224,82,82,0.07) !important;
    border: 1px solid rgba(224,82,82,0.26) !important;
    border-radius: 2px !important;
}}
[data-testid="stWarning"] {{
    background: rgba(201,168,76,0.07) !important;
    border: 1px solid rgba(201,168,76,0.26) !important;
    border-radius: 2px !important;
}}

/* ══ Charts & DataFrames ════════════════════════════════════════════════════ */
.stPlotlyChart > div {{ border-radius: 2px !important; }}
[data-testid="stDataFrame"] {{
    border: 1px solid var(--border) !important;
    border-radius: 2px !important;
}}

/* ══ Scrollbar ══════════════════════════════════════════════════════════════ */
::-webkit-scrollbar {{ width: 5px; height: 5px; }}
::-webkit-scrollbar-track {{ background: rgba(8,12,22,0.50); }}
::-webkit-scrollbar-thumb {{ background: rgba(201,168,76,0.28); border-radius: 2px; }}
::-webkit-scrollbar-thumb:hover {{ background: rgba(201,168,76,0.48); }}

/* ══ Animations ══════════════════════════════════════════════════════════════ */
.fade-in  {{ animation: fadeIn  0.6s ease-out both; }}
.slide-up {{ animation: slideUp 0.5s ease-out both; }}

@keyframes fadeIn  {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
@keyframes slideUp {{
    from {{ opacity: 0; transform: translateY(16px); }}
    to   {{ opacity: 1; transform: translateY(0);    }}
}}
</style>
""",
    unsafe_allow_html=True,
)


# ─── DATA / MODEL ──────────────────────────────────────────────────────────────

@st.cache_data
def load_data():
    return pd.read_csv("data/train.csv")


@st.cache_data
def load_results():
    p = "data/model_results.csv"
    return pd.read_csv(p) if os.path.exists(p) else None


@st.cache_resource
def load_model():
    return joblib.load("models/best_model.pkl")


df = load_data()
results_df = load_results()
model = load_model()
train_columns = pd.read_csv("data/X_train.csv").columns


# ─── HELPERS ───────────────────────────────────────────────────────────────────

# Consistent Plotly color palettes
_SURV_COLORS  = ["#e05252", "#34c97e"]   # 0 = red, 1 = green
_SEX_COLORS   = ["#4fb3e8", "#c9a84c"]
_MULTI_COLORS = ["#c9a84c", "#4fb3e8", "#34c97e", "#e05252", "#a78bfa"]


def chart_style(fig: go.Figure) -> go.Figure:
    """Apply the Art Deco / deep-navy theme to any Plotly figure."""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(8,14,24,0.50)",
        font=dict(color="#e8d5a3", family="Inter, sans-serif", size=12),
        margin=dict(t=54, b=20, l=20, r=20),
        legend=dict(
            font=dict(color="#e8d5a3", size=11),
            bgcolor="rgba(10,14,26,0.85)",
            bordercolor="rgba(201,168,76,0.22)",
            borderwidth=1,
        ),
        xaxis=dict(
            gridcolor="rgba(201,168,76,0.07)",
            linecolor="rgba(201,168,76,0.18)",
            tickfont=dict(
                color="rgba(232,213,163,0.52)",
                size=10,
                family="JetBrains Mono, monospace",
            ),
            zerolinecolor="rgba(201,168,76,0.12)",
        ),
        yaxis=dict(
            gridcolor="rgba(201,168,76,0.07)",
            linecolor="rgba(201,168,76,0.18)",
            tickfont=dict(
                color="rgba(232,213,163,0.52)",
                size=10,
                family="JetBrains Mono, monospace",
            ),
            zerolinecolor="rgba(201,168,76,0.12)",
        ),
        title=dict(
            font=dict(
                color="#e8d5a3",
                size=14,
                family="Playfair Display, serif",
            ),
            pad=dict(b=8),
        ),
    )
    return fig


def show_metric_card(label: str, value) -> None:
    st.markdown(
        f"""
<div class="metric-card slide-up">
    <span class="metric-label">{label}</span>
    <div class="metric-value">{value}</div>
</div>""",
        unsafe_allow_html=True,
    )


def sub_heading(text: str) -> None:
    st.markdown(
        f"""
<div class="sub-heading">
    <div class="sub-bar"></div>
    <span class="sub-text">{text}</span>
</div>""",
        unsafe_allow_html=True,
    )


def section_header(eyebrow: str, title: str, body: str = "") -> None:
    body_html = f'<p class="section-body">{body}</p>' if body else ""
    st.markdown(
        f"""
<div class="glass-card fade-in">
    <span class="section-eyebrow">{eyebrow}</span>
    <div class="section-title">{title}</div>
    <div class="accent-line"></div>
    {body_html}
</div>""",
        unsafe_allow_html=True,
    )


def create_input_data(pclass, sex, age, sibsp, parch, fare, title, deck):
    family_size = sibsp + parch + 1
    is_alone    = 1 if family_size == 1 else 0

    input_data = pd.DataFrame([[0] * len(train_columns)], columns=train_columns)
    input_data["Pclass"]     = pclass
    input_data["Age"]        = age
    input_data["SibSp"]      = sibsp
    input_data["Parch"]      = parch
    input_data["Fare"]       = fare
    input_data["FamilySize"] = family_size
    input_data["IsAlone"]    = is_alone

    if "Sex_male" in input_data.columns:
        input_data["Sex_male"] = 1 if sex == "Male" else 0

    for col in input_data.columns:
        if col.startswith("Title_"):
            input_data[col] = 0
    title_col = f"Title_{title}"
    if title_col in input_data.columns:
        input_data[title_col] = 1

    for col in input_data.columns:
        if col.startswith("Deck_"):
            input_data[col] = 0
    deck_col = f"Deck_{deck}"
    if deck_col in input_data.columns:
        input_data[deck_col] = 1

    return input_data


# ─── SIDEBAR ───────────────────────────────────────────────────────────────────

st.sidebar.markdown(
    """
<div style="padding:4px 0 22px 0;">
    <div style="font-family:'Playfair Display',serif;font-size:1.22rem;font-weight:700;
                color:#e8d5a3;letter-spacing:0.04em;">🚢 Titanic</div>
    <div style="font-family:'JetBrains Mono',monospace;font-size:0.63rem;
                color:#c9a84c !important;letter-spacing:0.20em;
                text-transform:uppercase;margin-top:3px;">Survival Dashboard</div>
    <div style="font-size:0.75rem;color:rgba(240,232,213,0.38) !important;
                margin-top:8px;font-family:'Inter',sans-serif;">
        by Ali Hassnain Bhatti
    </div>
</div>
<div style="border-top:1px solid rgba(201,168,76,0.16);margin:0 0 18px 0;"></div>
""",
    unsafe_allow_html=True,
)

pages = ["Home", "Data Insights", "Predict Survival", "Model Comparison", "About"]
page = st.sidebar.radio(
    "Navigate",
    pages,
    key="nav"
)

# Project flow steps
_STEPS = [
    "Explore data",
    "Preprocess data",
    "Train models",
    "Compare results",
    "Predict survival",
]
_steps_html = "".join(
    f"""<div style="display:flex;align-items:center;gap:10px;padding:5px 0;">
    <span style="font-family:'JetBrains Mono',monospace;font-size:0.60rem;
                 color:#c9a84c !important;background:rgba(201,168,76,0.10);
                 border:1px solid rgba(201,168,76,0.22);border-radius:2px;
                 min-width:20px;height:20px;display:inline-flex;
                 align-items:center;justify-content:center;flex-shrink:0;">{i + 1}</span>
    <span style="font-family:'Inter',sans-serif;font-size:0.82rem;
                 color:rgba(240,232,213,0.50) !important;">{s}</span>
</div>"""
    for i, s in enumerate(_STEPS)
)

st.sidebar.markdown(
    f"""
<div style="border-top:1px solid rgba(201,168,76,0.16);margin:16px 0 14px 0;"></div>
<div style="font-family:'JetBrains Mono',monospace;font-size:0.60rem;
            color:#c9a84c !important;letter-spacing:0.20em;
            text-transform:uppercase;margin-bottom:10px;opacity:0.85;">
    Project Flow
</div>
{_steps_html}
""",
    unsafe_allow_html=True,
)

if results_df is not None:
    best_row = results_df.loc[results_df["F1 Score"].idxmax()]
    st.sidebar.markdown(
        f"""
<div style="border-top:1px solid rgba(201,168,76,0.16);margin:16px 0 12px 0;"></div>
<div style="background:rgba(52,201,126,0.07);border:1px solid rgba(52,201,126,0.22);
            border-radius:2px;padding:11px 14px;">
    <div style="font-family:'JetBrains Mono',monospace;font-size:0.58rem;
                color:#34c97e !important;letter-spacing:0.16em;
                text-transform:uppercase;margin-bottom:4px;">Best Model</div>
    <div style="font-family:'Playfair Display',serif;font-size:0.95rem;
                color:#e8d5a3;font-weight:600;">{best_row['Model']}</div>
</div>
""",
        unsafe_allow_html=True,
    )



# ─── HERO ──────────────────────────────────────────────────────────────────────

st.markdown(
    """
<div class="hero-card fade-in">
    <div class="deco-tl"></div><div class="deco-tr"></div>
    <div class="deco-bl"></div><div class="deco-br"></div>
    <span class="hero-eyebrow">
        RMS Titanic &nbsp;·&nbsp; 1912 &nbsp;·&nbsp; Machine Learning Analysis
    </span>
    <h1 class="hero-title">Titanic Survival Dashboard</h1>
    <div class="gold-div"></div>
    <p class="hero-sub">
        Predictive Modelling &nbsp;·&nbsp; Data Insights &nbsp;·&nbsp; Passenger Analysis
    </p>
</div>
""",
    unsafe_allow_html=True,
)


# ═══════════════════════════════════════════════════════════════════════════════
# HOME
# ═══════════════════════════════════════════════════════════════════════════════

if page == "Home":
    section_header(
        "Overview",
        "Project Summary",
        "This dashboard predicts whether a Titanic passenger survived. "
        "Explore visual insights, compare machine learning models, and run live predictions.",
    )

    total_passengers = len(df)
    survived         = int(df["Survived"].sum())
    survival_rate    = df["Survived"].mean() * 100
    avg_fare         = df["Fare"].mean()

    col_btn, _ = st.columns([1, 3])
    with col_btn:
        def goto_prediction():
            st.session_state.nav = "Predict Survival"
        st.button(
            "Predict Survival →",
            on_click=goto_prediction
            )

    sub_heading("Quick Summary")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        show_metric_card("Total Passengers", total_passengers)
    with c2:
        show_metric_card("Survived", survived)
    with c3:
        show_metric_card("Survival Rate", f"{survival_rate:.1f}%")
    with c4:
        show_metric_card("Avg. Fare", f"£{avg_fare:.2f}")

    sub_heading("Visual Insights")
    v1, v2 = st.columns(2)

    with v1:
        fig = px.pie(
            df,
            names="Survived",
            title="Survival Distribution",
            color_discrete_sequence=_SURV_COLORS,
        )
        st.plotly_chart(chart_style(fig), use_container_width=True)

    with v2:
        fig = px.histogram(
            df,
            x="Age",
            nbins=30,
            title="Age Distribution",
            color_discrete_sequence=["#4fb3e8"],
        )
        st.plotly_chart(chart_style(fig), use_container_width=True)

    v3, v4 = st.columns(2)

    with v3:
        fig = px.histogram(
            df,
            x="Pclass",
            color="Survived",
            barmode="group",
            title="Survival by Passenger Class",
            color_discrete_sequence=_SURV_COLORS,
        )
        st.plotly_chart(chart_style(fig), use_container_width=True)

    with v4:
        fig = px.histogram(
            df,
            x="Sex",
            color="Survived",
            barmode="group",
            title="Survival by Sex",
            color_discrete_sequence=_SEX_COLORS,
        )
        st.plotly_chart(chart_style(fig), use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# DATA INSIGHTS
# ═══════════════════════════════════════════════════════════════════════════════

elif page == "Data Insights":
    section_header(
        "Analysis",
        "Exploratory Data Analysis",
        "Key patterns and distributions within the Titanic passenger dataset.",
    )

    c1, c2 = st.columns(2)

    with c1:
        fig = px.histogram(
            df,
            x="Survived",
            color="Survived",
            title="Survival Count",
            color_discrete_sequence=_SURV_COLORS,
        )
        st.plotly_chart(chart_style(fig), use_container_width=True)

        fig = px.histogram(
            df,
            x="Sex",
            color="Survived",
            barmode="group",
            title="Survival by Sex",
            color_discrete_sequence=_SEX_COLORS,
        )
        st.plotly_chart(chart_style(fig), use_container_width=True)

    with c2:
        fig = px.histogram(
            df,
            x="Pclass",
            color="Survived",
            barmode="group",
            title="Survival by Passenger Class",
            color_discrete_sequence=_SURV_COLORS,
        )
        st.plotly_chart(chart_style(fig), use_container_width=True)

        fig = px.histogram(
            df,
            x="Fare",
            nbins=30,
            title="Fare Distribution",
            color_discrete_sequence=["#a78bfa"],
        )
        st.plotly_chart(chart_style(fig), use_container_width=True)

    sub_heading("Correlation Heatmap")
    numeric_df = df.select_dtypes(include=["int64", "float64"])
    corr       = numeric_df.corr()

    heatmap = go.Figure(
        go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.columns,
            colorscale="RdBu",
            zmin=-1,
            zmax=1,
        )
    )
    heatmap.update_layout(
        height=600,
        title="Feature Correlation Heatmap",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(8,14,24,0.50)",
        font=dict(color="#e8d5a3", family="Inter, sans-serif"),
        title_font=dict(family="Playfair Display, serif", size=14, color="#e8d5a3"),
        margin=dict(t=54, b=20, l=20, r=20),
    )
    st.plotly_chart(heatmap, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PREDICT SURVIVAL
# ═══════════════════════════════════════════════════════════════════════════════

elif page == "Predict Survival":
    section_header(
        "Prediction Engine",
        "Passenger Survival Prediction",
        "Enter passenger details below — the model will estimate survival probability instantly.",
    )

    with st.form("prediction_form"):
        a, b, c = st.columns(3)

        with a:
            pclass = st.selectbox("Passenger Class", [1, 2, 3], key="pclass")
            sex    = st.selectbox("Sex", ["Male", "Female"], key="sex")
            age    = st.number_input("Age", min_value=0, max_value=100, value=25, key="age")

        with b:
            sibsp  = st.number_input("Siblings / Spouse Aboard", min_value=0, max_value=10, value=0, key="sibsp")
            parch  = st.number_input("Parents / Children Aboard", min_value=0, max_value=10, value=0, key="parch")
            fare   = st.number_input("Fare (£)", min_value=0.0, value=32.0, key="fare")

        with c:
            title_options = ["Mr", "Master", "Rare"] if sex == "Male" else ["Mrs", "Miss", "Rare"]
            title = st.selectbox("Title", title_options, key=f"title_{sex}")
            deck  = st.selectbox(
                "Deck", ["Unknown", "B", "C", "D", "E", "F", "G", "T"], key="deck"
            )

        submitted = st.form_submit_button("Run Prediction")

    if submitted:
        if (sex == "Male" and title in ["Mrs", "Miss"]) or (
            sex == "Female" and title == "Mr"
        ):
            st.error("Title does not match selected sex — please choose a valid title.")
            st.stop()

        input_df    = create_input_data(pclass, sex, age, sibsp, parch, fare, title, deck)
        prediction  = model.predict(input_df)[0]
        probability = (
            model.predict_proba(input_df)[0][1]
            if hasattr(model, "predict_proba")
            else None
        )

        sub_heading("Prediction Result")
        left, right = st.columns(2)

        with left:
            if prediction == 1:
                st.markdown(
                    """
<div style="background:rgba(52,201,126,0.07);border:1px solid rgba(52,201,126,0.28);
            border-radius:2px;padding:28px;text-align:center;">
    <div style="font-family:'Playfair Display',serif;font-size:1.45rem;font-weight:700;
                color:#34c97e !important;margin-bottom:7px;">✦ Likely to Survive</div>
    <div style="font-family:'Inter',sans-serif;font-size:0.84rem;
                color:rgba(52,201,126,0.65) !important;letter-spacing:0.05em;">
        Profile indicates favourable survival odds
    </div>
</div>""",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    """
<div style="background:rgba(224,82,82,0.07);border:1px solid rgba(224,82,82,0.28);
            border-radius:2px;padding:28px;text-align:center;">
    <div style="font-family:'Playfair Display',serif;font-size:1.45rem;font-weight:700;
                color:#e05252 !important;margin-bottom:7px;">✦ Likely Not to Survive</div>
    <div style="font-family:'Inter',sans-serif;font-size:0.84rem;
                color:rgba(224,82,82,0.65) !important;letter-spacing:0.05em;">
        Profile indicates low survival probability
    </div>
</div>""",
                    unsafe_allow_html=True,
                )

        with right:
            if probability is not None:
                st.markdown(
                    f"""
<div class="metric-card" style="text-align:center;padding:28px 20px;">
    <span class="metric-label">Survival Probability</span>
    <div class="metric-value" style="font-size:2.9rem !important;margin-top:8px;">
        {probability:.0%}
    </div>
</div>""",
                    unsafe_allow_html=True,
                )

        if probability is not None:
            gauge = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=probability * 100,
                    title={
                        "text": "Survival Probability (%)",
                        "font": {
                            "color": "#e8d5a3",
                            "family": "Playfair Display, serif",
                            "size": 15,
                        },
                    },
                    number={
                        "font": {
                            "color": "#e8d5a3",
                            "family": "Playfair Display, serif",
                            "size": 38,
                        },
                        "suffix": "%",
                    },
                    gauge={
                        "axis": {
                            "range": [0, 100],
                            "tickcolor": "#c9a84c",
                            "tickfont": {
                                "color": "#c9a84c",
                                "size": 10,
                                "family": "JetBrains Mono, monospace",
                            },
                        },
                        "bar": {"color": "#c9a84c"},
                        "bgcolor": "rgba(13,27,42,0.50)",
                        "borderwidth": 1,
                        "bordercolor": "rgba(201,168,76,0.28)",
                        "steps": [
                            {"range": [0, 40],   "color": "rgba(224,82,82,0.18)"},
                            {"range": [40, 70],  "color": "rgba(201,168,76,0.12)"},
                            {"range": [70, 100], "color": "rgba(52,201,126,0.18)"},
                        ],
                    },
                )
            )
            gauge.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#e8d5a3"),
                margin=dict(t=44, b=20, l=30, r=30),
                height=280,
            )
            st.plotly_chart(gauge, use_container_width=True)

        sub_heading("Input Used for Prediction")
        st.dataframe(input_df, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# MODEL COMPARISON
# ═══════════════════════════════════════════════════════════════════════════════

elif page == "Model Comparison":
    section_header(
        "Evaluation",
        "Model Performance",
        "Comparison of Logistic Regression, Decision Tree, and K-Nearest Neighbours.",
    )

    if results_df is not None:
        best_row = results_df.loc[results_df["F1 Score"].idxmax()]

        c1, c2, c3 = st.columns(3)
        with c1:
            show_metric_card("Best Model",    best_row["Model"])
        with c2:
            show_metric_card("Best F1 Score", f'{best_row["F1 Score"]:.3f}')
        with c3:
            show_metric_card("Best ROC-AUC",  f'{best_row["ROC-AUC"]:.3f}')

        sub_heading("Detailed Results")
        st.dataframe(results_df, use_container_width=True)

        fig = px.bar(
            results_df,
            x="Model",
            y=["Accuracy", "Precision", "Recall", "F1 Score", "ROC-AUC"],
            barmode="group",
            title="Model Comparison",
            color_discrete_sequence=_MULTI_COLORS,
        )
        st.plotly_chart(chart_style(fig), use_container_width=True)

        sub_heading("Metric Heatmap")
        metrics_df = results_df.set_index("Model")[
            ["Accuracy", "Precision", "Recall", "F1 Score", "ROC-AUC"]
        ]
        heatmap = go.Figure(
            go.Heatmap(
                z=metrics_df.values,
                x=metrics_df.columns,
                y=metrics_df.index,
                colorscale="Viridis",
                text=metrics_df.round(3).values,
                texttemplate="%{text}",
                hoverongaps=False,
            )
        )
        heatmap.update_layout(
            height=400,
            title="Model Performance Heatmap",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(8,14,24,0.50)",
            font=dict(color="#e8d5a3", family="Inter, sans-serif"),
            title_font=dict(family="Playfair Display, serif", size=14, color="#e8d5a3"),
            margin=dict(t=54, b=20, l=20, r=20),
        )
        st.plotly_chart(heatmap, use_container_width=True)

        st.markdown(
            f"""
<div style="background:rgba(52,201,126,0.07);border:1px solid rgba(52,201,126,0.26);
            border-radius:2px;padding:14px 20px;margin-top:8px;">
    <div style="font-family:'JetBrains Mono',monospace;font-size:0.62rem;
                color:#34c97e !important;letter-spacing:0.16em;
                text-transform:uppercase;margin-bottom:4px;">Best Model by F1 Score</div>
    <div style="font-family:'Playfair Display',serif;font-size:1.05rem;
                color:#e8d5a3;font-weight:600;">{best_row['Model']}</div>
</div>""",
            unsafe_allow_html=True,
        )

    else:
        st.markdown(
            """
<div style="background:rgba(201,168,76,0.07);border:1px solid rgba(201,168,76,0.26);
            border-radius:2px;padding:16px 20px;">
    <span style="font-family:'Inter',sans-serif;font-size:0.88rem;
                 color:#c9a84c !important;">
        model_results.csv not found — run train_model.py first.
    </span>
</div>""",
            unsafe_allow_html=True,
        )


# ═══════════════════════════════════════════════════════════════════════════════
# ABOUT
# ═══════════════════════════════════════════════════════════════════════════════

elif page == "About":
    section_header("Credits", "About This Project")

    tech_stack = [
        ("Python",       "Core language"),
        ("Pandas",       "Data manipulation"),
        ("Scikit-learn", "Machine learning"),
        ("Streamlit",    "Dashboard framework"),
        ("Plotly",       "Interactive charts"),
    ]
    tech_rows = "".join(
        f"""<div style="display:flex;align-items:center;justify-content:space-between;
                        padding:11px 0;border-bottom:1px solid rgba(201,168,76,0.10);">
    <span style="font-family:'Playfair Display',serif;font-size:0.98rem;
                 font-weight:600;color:#e8d5a3;">{name}</span>
    <span style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;
                 color:#c9a84c !important;letter-spacing:0.10em;">{desc}</span>
</div>"""
        for name, desc in tech_stack
    )

    demonstrates = [
        "Data preprocessing & feature engineering",
        "Classification model training & tuning",
        "Model evaluation & cross-validation",
        "Interactive dashboard design",
    ]
    demo_rows = "".join(
        f"""<div style="display:flex;align-items:flex-start;gap:10px;padding:7px 0;">
    <span style="color:#c9a84c !important;flex-shrink:0;font-size:0.8rem;margin-top:1px;">✦</span>
    <span style="font-family:'Inter',sans-serif;font-size:0.88rem;
                 color:rgba(240,232,213,0.60) !important;">{item}</span>
</div>"""
        for item in demonstrates
    )

    a1, a2 = st.columns(2)
    with a1:
        st.markdown(
            f"""
<div class="glass-card fade-in">
    <span class="section-eyebrow">Technology Stack</span>
    <div class="section-title">Built With</div>
    <div class="accent-line"></div>
    {tech_rows}
</div>""",
            unsafe_allow_html=True,
        )
    with a2:
        st.markdown(
            f"""
<div class="glass-card fade-in">
    <span class="section-eyebrow">Capabilities</span>
    <div class="section-title">What It Demonstrates</div>
    <div class="accent-line"></div>
    {demo_rows}
</div>""",
            unsafe_allow_html=True,
        )