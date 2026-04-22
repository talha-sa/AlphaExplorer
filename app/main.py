import streamlit as st
import os, sys
from pathlib import Path

# Modern Pathing - No more os.chdir (which causes server crashes)
ROOT = Path(__file__).parent.resolve()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Import your utils at the top for better performance
try:
    from utils.api_utils import (
        search_uniprot, get_uniprot_details,
        extract_protein_info
    )
except ImportError:
    st.error("Error: utils/api_utils.py not found. Check your file structure.")

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
/* Root & Body */
* { font-family: 'Inter', sans-serif; box-sizing: border-box; }

body, .stApp {
    background-color: #0a0c1a !important;
    color: #e1e1f6 !important;
}

/* ── THE FIX: HIDE NAVIGATION BUT NOT THE SIDEBAR ── */
/* This hides the default links without collapsing the sidebar width */
[data-testid="stSidebarNav"] {
    display: none !important;
}

/* Hide Header and Footer */
header[data-testid="stHeader"], 
#MainMenu, footer { 
    display: none !important; 
}

/* Sidebar Glassmorphism */
[data-testid="stSidebar"] {
    background: rgba(10,12,26,0.95) !important;
    backdrop-filter: blur(25px) !important;
    border-right: 1px solid rgba(255,255,255,0.1) !important;
    box-shadow: 10px 0 30px rgba(0,0,0,0.5) !important;
    min-width: 320px !important; /* Force a consistent width */
}

/* Grid Background */
.main .block-container {
    background-image: 
        linear-gradient(to right, rgba(102,126,234,0.05) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(102,126,234,0.05) 1px, transparent 1px);
    background-size: 40px 40px;
    padding-top: 40px !important;
}

/* Metric Cards → Holographic */
[data-testid="metric-container"] {
    background: rgba(10,12,26,0.8) !important;
    border: 1px solid rgba(102,126,234,0.25) !important;
    border-radius: 12px !important;
    padding: 16px !important;
}

/* Primary Button Styling */
.stButton > button {
    background: linear-gradient(90deg, #667eea, #f64f59) !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
}

/* Radio Buttons inside Sidebar */
.stRadio > div {
    gap: 10px;
}
</style>
""", unsafe_allow_html=True)

# ── Session State Init ─────────────────────────────────────────
if "uniprot_id" not in st.session_state:
    st.session_state.update({
        "uniprot_id": None,
        "protein_name": None,
        "protein_info": None,
        "uniprot_raw": None,
        "search_done": False,
        "search_results": [],
        "search_options": [],
    })

# ── Sidebar Content ─────────────────────────────────────────────
with st.sidebar:
    # Branding
    st.markdown("""
    <div style="padding: 10px 0 20px 0;">
        <h1 style="background:linear-gradient(90deg,#667eea,#f64f59); -webkit-background-clip:text; -webkit-text-fill-color:transparent; font-size:24px; margin:0;">AlphaExplorer</h1>
        <p style="font-size:10px; color:rgba(197,197,213,0.4); letter-spacing:0.3em; margin:0;">GENOMIC INTELLIGENCE</p>
    </div>
    """, unsafe_allow_html=True)

    # Search Section
    st.markdown("<p style='font-size:11px; color:#667eea;'>$ QUERY_SEQUENCE</p>", unsafe_allow_html=True)
    query = st.text_input("Search", placeholder="e.g., ACE2, BRCA1...", label_visibility="collapsed")
    
    if st.button("EXECUTE SCAN", use_container_width=True):
        if query:
            with st.spinner("Accessing UniProt..."):
                results, err = search_uniprot(query.strip(), limit=5)
                if not err and results:
                    options = []
                    for r in results:
                        acc = r.get("primaryAccession", "N/A")
                        name = r.get("proteinDescription", {}).get("recommendedName", {}).get("fullName", {}).get("value", "Unknown")
                        options.append(f"{name[:20]}... | {acc}")
                    st.session_state.search_results = results
                    st.session_state.search_options = options
                    st.session_state.search_done = True
                else:
                    st.error("Target not found.")

    # Selector
    if st.session_state.search_done:
        selected = st.selectbox("Select Result", st.session_state.search_options, label_visibility="collapsed")
        idx = st.session_state.search_options.index(selected)
        chosen_id = st.session_state.search_results[idx]["primaryAccession"]
        
        if chosen_id != st.session_state.uniprot_id:
            st.session_state.uniprot_id = chosen_id
            data, _ = get_uniprot_details(chosen_id)
            if data:
                st.session_state.protein_info = extract_protein_info(data)
                st.session_state.uniprot_raw = data
                st.session_state.protein_name = st.session_state.protein_info.get("name", chosen_id)

    # Active Profile
    if st.session_state.uniprot_id:
        st.markdown(f"""
        <div class="glass-panel" style="padding:15px; margin-top:20px; border:1px solid #667eea44;">
            <p style="font-size:10px; color:#667eea; margin:0;">ACTIVE TARGET</p>
            <p style="font-size:14px; font-weight:700; color:#b9c3ff; margin:5px 0;">{st.session_state.protein_name[:25]}</p>
            <p style="font-size:10px; color:rgba(255,255,255,0.4);">ID: {st.session_state.uniprot_id}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><p style='font-size:11px; color:rgba(255,255,255,0.3);'>NAVIGATE</p>", unsafe_allow_html=True)
    page = st.radio("Nav", ["🏠 Home", "🏗️ Structure", "⚙️ Function", "💊 Drugs", "🔗 Similar"], label_visibility="collapsed")

    # Developer Signature
    st.markdown(f"""
    <div style="position:fixed; bottom:20px; left:20px; display:flex; align-items:center; gap:10px;">
        <div style="width:30px; height:30px; border-radius:50%; background:linear-gradient(45deg,#667eea,#f64f59); display:flex; align-items:center; justify-content:center; font-weight:bold; font-size:12px;">T</div>
        <div>
            <p style="font-size:11px; font-weight:700; margin:0;">TALHA SALEEM</p>
            <p style="font-size:9px; color:rgba(255,255,255,0.4); margin:0;">Principal Investigator</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Page Router ──────────────────────────────────────────────────
if "Home" in page:
    from pages.home import show
    show()
elif "Structure" in page:
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