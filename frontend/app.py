import streamlit as st
import requests
import pandas as pd

# -------------------------------
# Config
# -------------------------------
API_URL = "http://127.0.0.1:8000/predict"

st.set_page_config(
    page_title="SalaryIQ — Predict Your Worth",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -------------------------------
# Custom CSS — Dark Editorial Theme
# -------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --bg:        #0d0f14;
    --surface:   #151820;
    --surface2:  #1c2030;
    --border:    #262c3d;
    --accent:    #4fffb0;
    --accent2:   #38c6f5;
    --danger:    #ff5f6d;
    --muted:     #6b7492;
    --text:      #e8eaf2;
    --text-dim:  #9fa4b8;
}

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2.5rem 1.5rem 4rem !important; max-width: 760px; }

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 3rem 0 2rem;
    position: relative;
}
.hero-eyebrow {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 0.75rem;
}
.hero h1 {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(2.4rem, 5vw, 3.6rem);
    font-weight: 400;
    line-height: 1.1;
    margin: 0 0 1rem;
    background: linear-gradient(135deg, #e8eaf2 30%, var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub {
    color: var(--text-dim);
    font-size: 1rem;
    font-weight: 300;
    letter-spacing: 0.02em;
}
.hero-line {
    width: 60px;
    height: 2px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    margin: 1.5rem auto 0;
    border-radius: 2px;
}

/* ── Section label ── */
.section-label {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--muted);
    margin: 2.2rem 0 1rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ── Card wrapper ── */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s;
}
.card:hover { border-color: #323858; }

/* ── Streamlit widget overrides ── */
div[data-baseweb="select"] > div,
div[data-baseweb="base-input"] > input {
    background: var(--surface2) !important;
    border-color: var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}
div[data-baseweb="select"] > div:focus-within,
div[data-baseweb="base-input"] > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(79,255,176,0.08) !important;
}

/* Select option text */
li[role="option"] {
    background: var(--surface2) !important;
    color: var(--text) !important;
}
li[role="option"]:hover { background: var(--surface) !important; }

/* ── Slider ── */
.stSlider > div > div > div[role="slider"] {
    background: var(--accent) !important;
    border: none !important;
    box-shadow: 0 0 10px rgba(79,255,176,0.4) !important;
}
.stSlider > div > div > div > div {
    background: linear-gradient(90deg, var(--accent), var(--accent2)) !important;
}
.stSlider [data-testid="stTickBarMin"],
.stSlider [data-testid="stTickBarMax"] { color: var(--muted) !important; }

/* ── Labels ── */
.stSelectbox label, .stSlider label {
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    color: var(--text-dim) !important;
    letter-spacing: 0.03em;
    margin-bottom: 0.25rem !important;
}

/* ── Predict button ── */
div[data-testid="stButton"] button {
    width: 100%;
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%) !important;
    color: #0d0f14 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.92rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.9rem 2rem !important;
    cursor: pointer;
    transition: opacity 0.2s, transform 0.15s !important;
    margin-top: 0.5rem;
}
div[data-testid="stButton"] button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}
div[data-testid="stButton"] button:active { transform: translateY(0) !important; }

/* ── Result card ── */
.result-card {
    background: linear-gradient(135deg, rgba(79,255,176,0.07), rgba(56,198,245,0.07));
    border: 1px solid rgba(79,255,176,0.25);
    border-radius: 18px;
    padding: 2rem 2rem 1.75rem;
    text-align: center;
    margin-top: 1.5rem;
    position: relative;
    overflow: hidden;
}
.result-card::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 160px; height: 160px;
    background: radial-gradient(circle, rgba(79,255,176,0.12), transparent 70%);
    pointer-events: none;
}
.result-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 0.5rem;
}
.result-amount {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(2.5rem, 6vw, 3.8rem);
    font-weight: 400;
    line-height: 1;
    color: var(--text);
    margin-bottom: 0.5rem;
}
.result-badge {
    display: inline-block;
    padding: 0.3rem 1rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    margin-top: 0.75rem;
}
.badge-entry  { background: rgba(107,116,146,0.2); color: var(--muted); }
.badge-mid    { background: rgba(56,198,245,0.15); color: var(--accent2); }
.badge-senior { background: rgba(79,255,176,0.15); color: var(--accent); }

/* ── Stats row ── */
.stats-row {
    display: flex;
    gap: 1rem;
    margin-top: 1.25rem;
}
.stat-box {
    flex: 1;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 0.9rem 1rem;
    text-align: center;
}
.stat-val {
    font-family: 'DM Serif Display', serif;
    font-size: 1.3rem;
    color: var(--text);
    line-height: 1;
}
.stat-key {
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--muted);
    margin-top: 0.3rem;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-dim) !important;
    font-size: 0.82rem !important;
}
.streamlit-expanderContent {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
    border-radius: 0 0 10px 10px !important;
}

/* ── Spinner ── */
.stSpinner > div { border-top-color: var(--accent) !important; }

/* ── Alert overrides ── */
.stAlert { border-radius: 12px !important; border-left-width: 3px !important; }

/* ── Columns gap ── */
div[data-testid="column"] { padding: 0 0.4rem !important; }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Load Dataset
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/salary_data.csv")
    return df

df = load_data()

def get_unique(col):
    return sorted(df[col].dropna().unique().tolist())

# -------------------------------
# Hero
# -------------------------------
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">AI-Powered Compensation Intelligence</div>
    <h1>Know Your Worth</h1>
    <p class="hero-sub">Fill in your profile below and get an instant, data-driven salary estimate.</p>
    <div class="hero-line"></div>
</div>
""", unsafe_allow_html=True)

# -------------------------------
# Form — Role & Experience
# -------------------------------
st.markdown('<div class="section-label">Role & Experience</div>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 2])
with col1:
    job_title = st.selectbox("Job Title", get_unique("job_title"))
with col2:
    industry = st.selectbox("Industry", get_unique("industry"))

col3, col4 = st.columns(2)
with col3:
    experience_years = st.slider(
        "Years of Experience",
        int(df["experience_years"].min()),
        int(df["experience_years"].max()),
        2
    )
with col4:
    skills_count = st.slider(
        "Number of Skills",
        int(df["skills_count"].min()),
        int(df["skills_count"].max()),
        5
    )

# -------------------------------
# Form — Education & Credentials
# -------------------------------
st.markdown('<div class="section-label">Education & Credentials</div>', unsafe_allow_html=True)

col5, col6 = st.columns(2)
with col5:
    education_level = st.selectbox("Education Level", get_unique("education_level"))
with col6:
    certifications = st.slider(
        "Certifications",
        int(df["certifications"].min()),
        int(df["certifications"].max()),
        1
    )

# -------------------------------
# Form — Work Environment
# -------------------------------
st.markdown('<div class="section-label">Work Environment</div>', unsafe_allow_html=True)

col7, col8, col9 = st.columns(3)
with col7:
    company_size = st.selectbox("Company Size", get_unique("company_size"))
with col8:
    location = st.selectbox("Location", get_unique("location"))
with col9:
    remote_work = st.selectbox("Remote Work", get_unique("remote_work"))

# -------------------------------
# Predict
# -------------------------------
st.markdown("<br>", unsafe_allow_html=True)

if st.button("⚡  Predict My Salary"):

    payload = {
        "job_title": job_title,
        "experience_years": experience_years,
        "education_level": education_level,
        "skills_count": skills_count,
        "industry": industry,
        "company_size": company_size,
        "location": location,
        "remote_work": remote_work,
        "certifications": certifications
    }

    with st.spinner("Crunching the numbers…"):
        try:
            response = requests.post(API_URL, json=payload)

            if response.status_code == 200:
                result = response.json()
                salary = result.get("predicted_salary")

                if salary:
                    # Level badge
                    if salary < 60000:
                        badge_class, badge_text, tier = "badge-entry", "Entry-Level Range", "Entry"
                    elif salary < 120000:
                        badge_class, badge_text, tier = "badge-mid", "Mid-Level Range", "Mid"
                    else:
                        badge_class, badge_text, tier = "badge-senior", "Senior-Level Range", "Senior"

                    # Rough monthly & daily
                    monthly = salary / 12
                    daily   = salary / 250

                    st.markdown(f"""
                    <div class="result-card">
                        <div class="result-label">Predicted Annual Salary</div>
                        <div class="result-amount">₹ {salary:,.0f}</div>
                        <span class="result-badge {badge_class}">{badge_text}</span>
                        <div class="stats-row">
                            <div class="stat-box">
                                <div class="stat-val">₹ {monthly:,.0f}</div>
                                <div class="stat-key">Per Month</div>
                            </div>
                            <div class="stat-box">
                                <div class="stat-val">₹ {daily:,.0f}</div>
                                <div class="stat-key">Per Day</div>
                            </div>
                            <div class="stat-box">
                                <div class="stat-val">{tier}</div>
                                <div class="stat-key">Career Tier</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                else:
                    st.error("The model returned an empty prediction. Please try again.")

            else:
                st.error(f"API Error {response.status_code} — please check that the backend is running.")

        except Exception as e:
            st.error(f"Could not reach the API: {e}")
