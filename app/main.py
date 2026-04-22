import streamlit as st
import sys
from pathlib import Path

# ── 1. Pathing & Imports ───────────────────────────────────────
ROOT = Path(__file__).parent.resolve()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from utils.api_utils import search_uniprot, get_uniprot_details, extract_protein_info
except ImportError:
    st.error("Critical Error: utils/api_utils.py missing. Please check your files.")

st.set_page_config(
    page_title="AlphaExplorer",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── 2. Cinematic CSS Injection ───────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet"/>
<style>
    /* Hide default Streamlit elements */
    [data-testid="stSidebarNav"] {display: none !important;}
    header, footer {visibility: hidden;}

    /* Force Body Theme */
    .stApp {
        background-color: #0a0c1a !important;
        background-image: radial-gradient(circle at 20% 20%, rgba(102,126,234,0.05) 0%, transparent 50%),
                          radial-gradient(circle at 80% 80%, rgba(246,79,89,0.05) 0%, transparent 50%) !important;
    }

    /* THE SIDEBAR FIX: Proper visibility and styling */
    [data-testid="stSidebar"] {
        background-color: rgba(10, 12, 26, 0.95) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
        min-width: 300px !important;
    }

    /* Custom Navigation Styling */
    .stRadio > label {display: none;} /* Hide the 'Nav' label */
    .stRadio div[role="radiogroup"] {
        padding: 10px 0;
        gap: 5px;
    }
    
    /* Metrics Styling */
    [data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(102, 126, 234, 0.2) !important;
        border-radius: 12px !important;
        padding: 15px !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #667eea, #f64f59) !important;
        border: none !important;
        color: white !important;
        font-weight: bold !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
    }
</style>
""", unsafe_allow_html=True)

# ── 3. Session State Initialization ──────────────────────────
if "uniprot_id" not in st.session_state:
    st.session_state.update({
        "uniprot_id": None, "protein_name": None,
        "search_done": False, "search_options": [], "search_results": []
    })

# ── 4. Sidebar Content ────────────────────────────────────────
with st.sidebar:
    # Branding
    st.markdown("""
        <h1 style='background:linear-gradient(90deg,#667eea,#f64f59); -webkit-background-clip:text; -webkit-text-fill-color:transparent; font-family:Space Grotesk; font-size:26px; margin-bottom:0;'>AlphaExplorer</h1>
        <p style='color:rgba(255,255,255,0.4); font-size:10px; letter-spacing:0.3em; margin-top:0;'>GENOMIC INTELLIGENCE</p>
        <hr style='border: 0.5px solid rgba(255,255,255,0.1); margin: 20px 0;'>
    """, unsafe_allow_html=True)

    # Global Search
    st.markdown("<p style='font-size:11px; color:#667eea; font-family:Space Grotesk;'>$ QUERY_SEQUENCE</p>", unsafe_allow_html=True)
    query = st.text_input("Search", placeholder="e.g., ACE2, BRCA1...", label_visibility="collapsed")
    
    if st.button("EXECUTE SCAN", use_container_width=True):
        if query:
            with st.spinner("Fetching data..."):
                results, err = search_uniprot(query, limit=5)
                if results:
                    st.session_state.search_results = results
                    st.session_state.search_options = [f"{r.get('primaryAccession')} | {r.get('organism', {}).get('scientificName', 'Unknown')}" for r in results]
                    st.session_state.search_done = True
                else:
                    st.error("No results.")

    if st.session_state.search_done:
        selected = st.selectbox("Select Result", st.session_state.search_options, label_visibility="collapsed")
        idx = st.session_state.search_options.index(selected)
        st.session_state.uniprot_id = st.session_state.search_results[idx]["primaryAccession"]

    # Navigation Menu
    st.markdown("<br><p style='font-size:11px; color:rgba(255,255,255,0.3);'>NAVIGATE</p>", unsafe_allow_html=True)
    page = st.radio("Menu", ["🏠 Home", "🏗️ Structure", "⚙️ Function", "💊 Drugs", "🔗 Similar"], label_visibility="collapsed")

    # Developer Signature (Fixed at bottom)
    st.markdown(f"""
        <div style='margin-top: 50px; padding: 15px; border-top: 1px solid rgba(255,255,255,0.1); display:flex; align-items:center; gap:12px;'>
            <div style='width:35px; height:35px; border-radius:50%; background:linear-gradient(45deg,#667eea,#f64f59); display:flex; align-items:center; justify-content:center; font-weight:bold; color:white;'>T</div>
            <div>
                <p style='font-size:12px; font-weight:700; color:white; margin:0;'>TALHA SALEEM</p>
                <p style='font-size:9px; color:rgba(255,255,255,0.4); margin:0;'>Principal Investigator · UAF</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ── 5. Page Routing ──────────────────────────────────────────
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