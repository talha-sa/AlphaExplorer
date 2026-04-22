# AlphaExplorer - Cinematic Glassmorphism UI + Bioinformatics Logic
# Stitch: Design System (HTML/Tailwind) + Python API Modules

import streamlit as st
import os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(ROOT))
sys.path.insert(0, ROOT)

st.set_page_config(
    page_title="AlphaExplorer",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Cinematic Design System Injection ─────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>

<style>
/* ── Root & Body ─────────────────────────────────────────── */
* { font-family: 'Inter', sans-serif; box-sizing: border-box; }

body, .stApp {
    background-color: #0a0c1a !important;
    color: #e1e1f6 !important;
}

/* ── Hide Streamlit Chrome ───────────────────────────────── */
section[data-testid="stSidebarNav"],
div[data-testid="stSidebarNavItems"],
ul[data-testid="stSidebarNavItems"],
header[data-testid="stHeader"],
#MainMenu, footer { display: none !important; }

/* ── Grid Background ─────────────────────────────────────── */
.main .block-container {
    background-image:
        linear-gradient(to right, rgba(102,126,234,0.05) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(102,126,234,0.05) 1px, transparent 1px);
    background-size: 40px 40px;
    padding-top: 20px !important;
    max-width: 100% !important;
}

/* ── Sidebar Glassmorphism ───────────────────────────────── */
[data-testid="stSidebar"] {
    background: rgba(10,12,26,0.85) !important;
    backdrop-filter: blur(20px) !important;
    border-right: 1px solid rgba(255,255,255,0.1) !important;
    box-shadow: 10px 0 30px rgba(0,0,0,0.5) !important;
}
[data-testid="stSidebar"] > div:first-child {
    background: transparent !important;
}

/* ── Glass Panel Base Class ──────────────────────────────── */
.glass-panel {
    background: rgba(255,255,255,0.03) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
    padding: 24px !important;
    position: relative !important;
}

/* ── Holographic Border Effect ───────────────────────────── */
.holo-card {
    background: rgba(10,12,26,0.8) !important;
    border-radius: 12px !important;
    padding: 24px !important;
    position: relative !important;
    border: 1px solid rgba(102,126,234,0.2) !important;
    transition: border-color 0.3s ease !important;
}
.holo-card:hover {
    border-color: rgba(102,126,234,0.6) !important;
    box-shadow: 0 0 30px rgba(102,126,234,0.15) !important;
}

/* ── Neon Glows ──────────────────────────────────────────── */
.neon-violet { box-shadow: 0 0 20px rgba(102,126,234,0.3) !important; }
.neon-crimson { box-shadow: 0 0 20px rgba(246,79,89,0.3) !important; }

/* ── Metric Cards → Holographic ─────────────────────────── */
[data-testid="metric-container"] {
    background: rgba(10,12,26,0.8) !important;
    border: 1px solid rgba(102,126,234,0.25) !important;
    border-radius: 8px !important;
    padding: 16px !important;
    transition: all 0.3s ease !important;
}
[data-testid="metric-container"]:hover {
    border-color: rgba(102,126,234,0.6) !important;
    box-shadow: 0 0 20px rgba(102,126,234,0.15) !important;
}
[data-testid="metric-container"] label {
    color: rgba(197,197,213,0.7) !important;
    font-size: 10px !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    font-family: 'Space Grotesk', sans-serif !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #b9c3ff !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 28px !important;
}

/* ── Primary Button ──────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(90deg, #667eea, #f64f59) !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    font-size: 11px !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    filter: brightness(1.15) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 20px rgba(102,126,234,0.4) !important;
}
.stButton > button:active { transform: scale(0.97) !important; }

/* ── Text Inputs ─────────────────────────────────────────── */
.stTextInput > div > div > input {
    background: rgba(10,12,26,0.8) !important;
    border: 1px solid rgba(102,126,234,0.3) !important;
    border-radius: 8px !important;
    color: #e1e1f6 !important;
    font-family: 'Space Grotesk', monospace !important;
    font-size: 13px !important;
    letter-spacing: 0.03em !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(102,126,234,0.7) !important;
    box-shadow: 0 0 15px rgba(102,126,234,0.2) !important;
}
.stTextInput > div > div > input::placeholder {
    color: rgba(197,197,213,0.3) !important;
}

/* ── Selectbox ───────────────────────────────────────────── */
.stSelectbox > div > div {
    background: rgba(10,12,26,0.8) !important;
    border: 1px solid rgba(102,126,234,0.3) !important;
    border-radius: 8px !important;
    color: #e1e1f6 !important;
}

/* ── Radio Buttons ───────────────────────────────────────── */
.stRadio > label {
    color: rgba(197,197,213,0.9) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 13px !important;
}

/* ── Dataframe ───────────────────────────────────────────── */
[data-testid="stDataFrame"] {
    background: rgba(10,12,26,0.6) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 8px !important;
}

/* ── Alerts → Glassmorphism ──────────────────────────────── */
.stSuccess {
    background: rgba(46,213,115,0.08) !important;
    border: 1px solid rgba(46,213,115,0.3) !important;
    border-radius: 8px !important;
    color: #6ff6ff !important;
}
.stInfo {
    background: rgba(102,126,234,0.08) !important;
    border: 1px solid rgba(102,126,234,0.3) !important;
    border-radius: 8px !important;
}
.stWarning {
    background: rgba(255,219,19,0.08) !important;
    border: 1px solid rgba(255,219,19,0.3) !important;
    border-radius: 8px !important;
}
.stError {
    background: rgba(246,79,89,0.08) !important;
    border: 1px solid rgba(246,79,89,0.3) !important;
    border-radius: 8px !important;
}

/* ── Spinner ─────────────────────────────────────────────── */
.stSpinner > div {
    border-color: #667eea transparent transparent !important;
}

/* ── Headings ────────────────────────────────────────────── */
h1, h2 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #ffffff !important;
    letter-spacing: -0.02em !important;
}
h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #b9c3ff !important;
}

/* ── Download Button ─────────────────────────────────────── */
[data-testid="stDownloadButton"] > button {
    background: rgba(102,126,234,0.15) !important;
    border: 1px solid rgba(102,126,234,0.4) !important;
    color: #b9c3ff !important;
    border-radius: 6px !important;
}

/* ── Ambient Background Glows ────────────────────────────── */
.main::before {
    content: '';
    position: fixed;
    top: 10%;
    left: 20%;
    width: 40vw;
    height: 40vw;
    background: radial-gradient(circle, rgba(102,126,234,0.05) 0%, transparent 70%);
    pointer-events: none;
    z-index: -1;
}
.main::after {
    content: '';
    position: fixed;
    bottom: 10%;
    right: 10%;
    width: 30vw;
    height: 30vw;
    background: radial-gradient(circle, rgba(246,79,89,0.05) 0%, transparent 70%);
    pointer-events: none;
    z-index: -1;
}

/* ── Progress Bar ────────────────────────────────────────── */
.stProgress > div > div {
    background: linear-gradient(90deg, #667eea, #f64f59) !important;
}

/* ── Plotly Charts ───────────────────────────────────────── */
.js-plotly-plot .plotly {
    background: transparent !important;
}

/* ── Link Buttons ────────────────────────────────────────── */
[data-testid="stLinkButton"] > a {
    background: rgba(102,126,234,0.1) !important;
    border: 1px solid rgba(102,126,234,0.3) !important;
    color: #b9c3ff !important;
    border-radius: 6px !important;
}

/* ── Caption text ────────────────────────────────────────── */
.stCaption {
    color: rgba(197,197,213,0.5) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 10px !important;
    letter-spacing: 0.05em !important;
}
</style>
""", unsafe_allow_html=True)

# ── Session State Init ─────────────────────────────────────────
for key, val in {
    "uniprot_id"    : None,
    "protein_name"  : None,
    "protein_info"  : None,
    "uniprot_raw"   : None,
    "search_done"   : False,
    "search_results": [],
    "search_options": [],
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ── Sidebar ─────────────────────────────────────────────────────
with st.sidebar:
    # Logo + Branding
    st.markdown("""
    <div style="padding: 24px 0 8px 0;">
        <p style="
            font-family:'Space Grotesk',sans-serif;
            font-size:22px;
            font-weight:700;
            letter-spacing:-0.02em;
            background:linear-gradient(90deg,#667eea,#f64f59);
            -webkit-background-clip:text;
            -webkit-text-fill-color:transparent;
            margin:0;
        ">AlphaExplorer</p>
        <p style="
            font-family:'Space Grotesk',sans-serif;
            font-size:9px;
            letter-spacing:0.25em;
            color:rgba(197,197,213,0.4);
            text-transform:uppercase;
            margin:4px 0 0 0;
        ">Genomic Intelligence</p>
    </div>
    <hr style="border:1px solid rgba(255,255,255,0.07); margin:12px 0;"/>
    """, unsafe_allow_html=True)

    # ── Global Search ──────────────────────────────────────────
    st.markdown("""
    <p style="
        font-family:'Space Grotesk',sans-serif;
        font-size:9px;
        letter-spacing:0.2em;
        color:rgba(197,197,213,0.5);
        text-transform:uppercase;
        margin-bottom:8px;
    ">$ Query Sequence</p>
    """, unsafe_allow_html=True)

    query = st.text_input(
        "Search",
        placeholder="ACE2, BRCA1, TP53, ACHE...",
        label_visibility="collapsed",
        key="global_search_input"
    )

    if st.button("⌘ Execute Query", use_container_width=True):
        if query.strip():
            from utils.api_utils import (
                search_uniprot, get_uniprot_details,
                extract_protein_info
            )
            with st.spinner("Scanning UniProt database..."):
                results, err = search_uniprot(query.strip(), limit=8)

            if err:
                st.error(err)
            elif not results:
                st.warning("No sequences found. Broaden query.")
            else:
                options = []
                for r in results:
                    try:
                        name = (r["proteinDescription"]
                                 ["recommendedName"]
                                 ["fullName"]["value"])
                    except:
                        try:
                            name = (r["proteinDescription"]
                                     ["submittedNames"][0]
                                     ["fullName"]["value"])
                        except:
                            name = "Unknown"
                    acc = r.get("primaryAccession", "N/A")
                    try:
                        org = r["organism"]["scientificName"]
                    except:
                        org = "Unknown"
                    options.append(
                        f"{name[:28]} | {acc} | {org[:18]}"
                    )
                st.session_state.search_results = results
                st.session_state.search_options  = options
                st.session_state.search_done     = True

    # Protein selector after search
    if st.session_state.search_done:
        options = st.session_state.search_options
        results = st.session_state.search_results

        if options:
            selected = st.selectbox(
                "Select sequence:",
                options,
                label_visibility="collapsed",
                key="protein_selector"
            )
            idx = options.index(selected)
            chosen_id = results[idx]["primaryAccession"]

            if chosen_id != st.session_state.uniprot_id:
                st.session_state.uniprot_id = chosen_id
                from utils.api_utils import (
                    get_uniprot_details, extract_protein_info
                )
                with st.spinner("Loading protein data..."):
                    data, err = get_uniprot_details(chosen_id)
                    if data:
                        st.session_state.protein_info = (
                            extract_protein_info(data)
                        )
                        st.session_state.uniprot_raw  = data
                        try:
                            st.session_state.protein_name = (
                                st.session_state.protein_info
                                    .get("name", chosen_id)
                            )
                        except:
                            st.session_state.protein_name = chosen_id

    # Active sequence panel
    if st.session_state.uniprot_id:
        info = st.session_state.protein_info or {}
        uid  = st.session_state.uniprot_id
        st.markdown(f"""
        <hr style="border:1px solid rgba(255,255,255,0.07); margin:12px 0;"/>
        <div style="
            background:rgba(102,126,234,0.08);
            border:1px solid rgba(102,126,234,0.25);
            border-radius:8px;
            padding:14px;
            margin-bottom:12px;
        ">
            <p style="
                font-family:'Space Grotesk',sans-serif;
                font-size:9px;
                letter-spacing:0.2em;
                color:rgba(102,126,234,0.8);
                text-transform:uppercase;
                margin:0 0 6px 0;
            ">Active Sequence</p>
            <p style="
                font-family:'Space Grotesk',sans-serif;
                font-size:13px;
                font-weight:600;
                color:#b9c3ff;
                margin:0 0 4px 0;
            ">{info.get('gene','N/A')}</p>
            <p style="
                font-size:10px;
                color:rgba(197,197,213,0.6);
                margin:2px 0;
            ">{info.get('name','')[:32]}</p>
            <p style="
                font-family:'Space Grotesk',monospace;
                font-size:10px;
                color:rgba(197,197,213,0.4);
                margin:6px 0 0 0;
                letter-spacing:0.1em;
            ">ID: {uid} &nbsp;|&nbsp; {info.get('length','N/A')} aa</p>
        </div>
        """, unsafe_allow_html=True)

    # Navigation
    st.markdown("""
    <hr style="border:1px solid rgba(255,255,255,0.07); margin:8px 0;"/>
    <p style="
        font-family:'Space Grotesk',sans-serif;
        font-size:9px;
        letter-spacing:0.2em;
        color:rgba(197,197,213,0.4);
        text-transform:uppercase;
        margin:0 0 8px 0;
    ">Navigate</p>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigate",
        ["🏠  Explorer Home",
         "🏗️  Molecule Viewer",
         "⚙️  Function & Disease",
         "💊  Drug Intelligence",
         "🔗  Similar Proteins"],
        label_visibility="collapsed"
    )

    # Data sources + branding
    st.markdown("""
    <hr style="border:1px solid rgba(255,255,255,0.07); margin:12px 0;"/>
    <p style="
        font-family:'Space Grotesk',sans-serif;
        font-size:9px;
        letter-spacing:0.2em;
        color:rgba(197,197,213,0.4);
        text-transform:uppercase;
        margin:0 0 8px 0;
    ">Data Sources</p>
    <p style="font-size:10px; color:rgba(197,197,213,0.55); margin:3px 0;">
        🔬 AlphaFold Database</p>
    <p style="font-size:10px; color:rgba(197,197,213,0.55); margin:3px 0;">
        🧬 UniProt Knowledge Base</p>
    <p style="font-size:10px; color:rgba(197,197,213,0.55); margin:3px 0;">
        💊 ChEMBL Drug Database</p>
    <p style="font-size:10px; color:rgba(197,197,213,0.55); margin:3px 0;">
        🗄️ Protein Data Bank (PDB)</p>
    <hr style="border:1px solid rgba(255,255,255,0.07); margin:12px 0;"/>
    <div style="display:flex; align-items:center; gap:10px; padding-bottom:8px;">
        <div style="
            width:36px; height:36px;
            border-radius:50%;
            background:linear-gradient(135deg,#667eea,#f64f59);
            display:flex; align-items:center; justify-content:center;
            font-family:'Space Grotesk',sans-serif;
            font-size:14px; font-weight:700;
            color:white;
            border: 1px solid rgba(255,255,255,0.1);
        ">T</div>
        <div>
            <p style="
                font-family:'Space Grotesk',sans-serif;
                font-size:11px; font-weight:700;
                color:#ffffff; margin:0;
                text-transform:uppercase; letter-spacing:0.05em;
            ">Talha Saleem</p>
            <p style="font-size:9px; color:rgba(197,197,213,0.4);
                      margin:2px 0 0 0;">
                Principal Investigator · UAF</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Page Router ──────────────────────────────────────────────────
if "Explorer Home" in page:
    from pages.home import show
    show()
elif "Molecule Viewer" in page:
    from pages.structure import show
    show()
elif "Function" in page:
    from pages.function import show
    show()
elif "Drug" in page:
    from pages.drugs import show
    show()
elif "Similar" in page:
    from pages.similar import show
    show()