import streamlit as st
import sys
from pathlib import Path

# ── 1. Modern Pathing & Utility Imports ────────────────────────
ROOT = Path(__file__).parent.resolve()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from utils.api_utils import (
        search_uniprot, get_uniprot_details, 
        extract_protein_info
    )
except ImportError:
    st.error("Missing Logic: Ensure utils/api_utils.py is in your project folder.")

st.set_page_config(
    page_title="AlphaExplorer",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── 2. Cinematic Glassmorphism UI Injection ───────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>

<style>
    /* Global Background and Typography */
    .stApp {
        background-color: #0a0c1a !important;
        background-image: 
            radial-gradient(circle at 20% 20%, rgba(102,126,234,0.05) 0%, transparent 40%),
            radial-gradient(circle at 80% 80%, rgba(246,79,89,0.05) 0%, transparent 40%) !important;
    }

    /* Surgical Sidebar Fix: Hides default nav but keeps container visible */
    [data-testid="stSidebarNav"] { display: none !important; }
    [data-testid="stSidebar"] {
        background-color: rgba(10, 12, 26, 0.9) !important;
        backdrop-filter: blur(25px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
        min-width: 320px !important;
    }

    /* Glass Panel Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }

    /* Neon Gradient Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #667eea, #f64f59) !important;
        color: white !important;
        border: none !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: 0.1em !important;
        text-transform: uppercase !important;
    }

    /* Hide standard Header/Footer */
    header, footer { visibility: hidden !important; }
</style>
""", unsafe_allow_html=True)

# ── 3. Session State Initialization ──────────────────────────
if "uniprot_id" not in st.session_state:
    st.session_state.update({
        "uniprot_id": None,
        "protein_name": "No Target Selected",
        "search_done": False,
        "search_results": [],
        "search_options": []
    })

# ── 4. Side Navigation & Search ──────────────────────────────
with st.sidebar:
    # Branding Header
    st.markdown("""
        <div style="padding-bottom: 20px;">
            <h1 style="background: linear-gradient(90deg,#667eea,#f64f59); -webkit-background-clip:text; -webkit-text-fill-color:transparent; font-family:'Space Grotesk'; font-size:24px; font-weight:700; margin:0;">AlphaExplorer</h1>
            <p style="color:rgba(255,255,255,0.4); font-size:10px; letter-spacing:0.3em; margin:0;">GENOMIC INTELLIGENCE</p>
        </div>
        <hr style="border: 0.1px solid rgba(255,255,255,0.1); margin-bottom: 20px;">
    """, unsafe_allow_html=True)

    # Global Search Input
    st.markdown("<p style='font-size:10px; color:#667eea; letter-spacing:0.2em;'>$ QUERY_SEQUENCE</p>", unsafe_allow_html=True)
    query = st.text_input("Search", placeholder="e.g. INS, ACE2...", label_visibility="collapsed")
    
    if st.button("EXECUTE SCAN", use_container_width=True):
        if query:
            with st.spinner("Accessing Repositories..."):
                results, err = search_uniprot(query.strip(), limit=5)
                if not err and results:
                    st.session_state.search_results = results
                    st.session_state.search_options = [
                        f"{r.get('primaryAccession')} | {r.get('organism', {}).get('scientificName', 'Unknown')[:15]}" 
                        for r in results
                    ]
                    st.session_state.search_done = True
                else:
                    st.error("No matches in database.")

    # Selection Box (Appears after search)
    if st.session_state.search_done:
        selected = st.selectbox("Select Result", st.session_state.search_options, label_visibility="collapsed")
        idx = st.session_state.search_options.index(selected)
        chosen_id = st.session_state.search_results[idx]["primaryAccession"]
        
        if chosen_id != st.session_state.uniprot_id:
            st.session_state.uniprot_id = chosen_id
            st.session_state.protein_name = chosen_id  # Update logic to pull full name if needed

    # Page Routing Menu
    st.markdown("<br><p style='font-size:10px; color:rgba(255,255,255,0.3); letter-spacing:0.2em;'>NAVIGATE</p>", unsafe_allow_html=True)
    page = st.radio("Menu", ["🏠 Home", "🏗️ Structure", "⚙️ Function", "💊 Drugs", "🔗 Similar"], label_visibility="collapsed")

    # Fixed Profile Footer
    st.markdown(f"""
        <div style="margin-top: 60px; padding: 15px; border-top: 1px solid rgba(255,255,255,0.1); display:flex; align-items:center; gap:12px;">
            <div style="width:36px; height:36px; border-radius:50%; background:linear-gradient(45deg,#667eea,#f64f59); display:flex; align-items:center; justify-content:center; font-weight:700; color:white;">T</div>
            <div>
                <p style="font-size:12px; font-weight:700; color:white; margin:0; text-transform:uppercase;">Talha Saleem</p>
                <p style="font-size:9px; color:rgba(255,255,255,0.4); margin:0;">Principal Investigator · UAF</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ── 5. Page Routing Logic ────────────────────────────────────
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