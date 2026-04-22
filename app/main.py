# AlphaExplorer - Main Entry Point
# Session state: single search shared across all pages

import streamlit as st
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(ROOT))
sys.path.insert(0, ROOT)

st.set_page_config(
    page_title="AlphaExplorer",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Hide Streamlit auto-detected pages */
    section[data-testid="stSidebarNav"],
    div[data-testid="stSidebarNavItems"],
    ul[data-testid="stSidebarNavItems"],
    [data-testid="stSidebarNav"],
    header[data-testid="stHeader"] { display: none !important; }

    /* Sidebar gradient — works in both modes */
    [data-testid="stSidebar"] {
        background: linear-gradient(160deg,
            #6C63FF 0%,
            #3B82F6 50%,
            #06B6D4 100%) !important;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Main area */
    .main .block-container {
        padding-top: 20px;
        background-color: transparent;
    }

    /* Metric cards */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg,
            #6C63FF22, #3B82F622);
        border: 1px solid #6C63FF44;
        border-radius: 12px;
        padding: 15px;
    }

    /* Primary button */
    .stButton > button {
        background: linear-gradient(90deg,
            #6C63FF, #3B82F6) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        padding: 10px 24px !important;
        font-size: 15px !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg,
            #3B82F6, #06B6D4) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 15px rgba(108,99,255,0.4) !important;
    }

    /* Search input */
    .stTextInput > div > div > input {
        border: 2px solid #6C63FF !important;
        border-radius: 10px !important;
        font-size: 15px !important;
    }

    /* Selectbox */
    .stSelectbox > div > div {
        border: 2px solid #6C63FF !important;
        border-radius: 10px !important;
    }

    /* Radio */
    .stRadio > div > label {
        font-size: 15px !important;
        padding: 6px 0 !important;
    }

    /* Divider */
    hr { border-color: rgba(255,255,255,0.25) !important; }

    /* Dataframe headers */
    .dataframe th {
        background: linear-gradient(90deg,
            #6C63FF, #3B82F6) !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# ── Session State Initialization ──────────────────────────────
if "uniprot_id"   not in st.session_state:
    st.session_state.uniprot_id   = None
if "protein_info" not in st.session_state:
    st.session_state.protein_info = None
if "search_done"  not in st.session_state:
    st.session_state.search_done  = False

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:20px 0 10px 0;'>
        <span style='font-size:44px;'>🧬</span>
        <h1 style='font-size:24px; font-weight:800;
                   margin:6px 0 2px 0;'>AlphaExplorer</h1>
        <p style='font-size:12px; opacity:0.85;
                  margin:0;'>Protein Intelligence Dashboard</p>
        <p style='font-size:10px; opacity:0.65;
                  margin:4px 0 0 0;'>
            🏆 AlphaFold Nobel Prize 2024
        </p>
    </div>
    <hr/>
    """, unsafe_allow_html=True)

    # ── GLOBAL SEARCH ─────────────────────────────────────────
    st.markdown("""
    <p style='font-size:12px; font-weight:700;
              letter-spacing:1px; opacity:0.9;
              margin-bottom:6px;'>🔍 SEARCH PROTEIN</p>
    """, unsafe_allow_html=True)

    query = st.text_input(
        "Search",
        placeholder="ACE2, BRCA1, TP53, ACHE...",
        label_visibility="collapsed",
        key="global_search"
    )

    if st.button("🔍 Search", use_container_width=True):
        if query.strip():
            from utils.api_utils import (
                search_uniprot, get_uniprot_details,
                extract_protein_info
            )
            with st.spinner("Searching UniProt..."):
                results, err = search_uniprot(query.strip(), limit=8)

            if err:
                st.error(err)
            elif not results:
                st.warning("No proteins found. Try another name.")
            else:
                # Build option list
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
                        f"{name[:30]} | {acc} | {org[:20]}"
                    )

                st.session_state["search_results"] = results
                st.session_state["search_options"]  = options
                st.session_state["search_done"]     = True

    # Show protein selector after search
    if st.session_state.get("search_done"):
        options  = st.session_state.get("search_options", [])
        results  = st.session_state.get("search_results", [])

        if options:
            selected = st.selectbox(
                "Select protein:",
                options,
                key="protein_selector",
                label_visibility="collapsed"
            )
            idx = options.index(selected)
            chosen_id = results[idx]["primaryAccession"]

            if chosen_id != st.session_state.uniprot_id:
                st.session_state.uniprot_id = chosen_id
                from utils.api_utils import (
                    get_uniprot_details, extract_protein_info
                )
                with st.spinner("Loading protein..."):
                    data, err = get_uniprot_details(chosen_id)
                    if data:
                        st.session_state.protein_info = (
                            extract_protein_info(data)
                        )
                        st.session_state.uniprot_raw = data
                    else:
                        st.session_state.protein_info = {}

    # Show selected protein info in sidebar
    if st.session_state.uniprot_id:
        info = st.session_state.protein_info or {}
        st.markdown(f"""
        <hr/>
        <div style='background:rgba(255,255,255,0.12);
                    border-radius:10px; padding:12px;
                    margin:8px 0;'>
            <p style='font-size:13px; font-weight:700;
                      margin:0 0 6px 0;'>
                ✅ {info.get('gene','N/A')}
            </p>
            <p style='font-size:11px; opacity:0.85;
                      margin:2px 0;'>
                {info.get('name','Unknown')[:35]}
            </p>
            <p style='font-size:10px; opacity:0.65;
                      margin:2px 0;'>
                📏 {info.get('length','N/A')} aa
            </p>
            <p style='font-size:10px; opacity:0.65;
                      margin:2px 0;'>
                🔬 {str(info.get('organism',''))[:25]}
            </p>
            <p style='font-size:10px; opacity:0.65;
                      margin:2px 0;'>
                🆔 {st.session_state.uniprot_id}
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Navigation
    st.markdown("<hr/>", unsafe_allow_html=True)
    page = st.radio(
        "Navigate",
        ["🏠 Home",
         "🏗️ Structure Viewer",
         "⚙️ Function & Disease",
         "💊 Drug Intelligence",
         "🔗 Similar Proteins"],
        label_visibility="collapsed"
    )

    st.markdown("""
    <hr/>
    <p style='font-size:11px; opacity:0.7;
              font-weight:700; letter-spacing:1px;'>
        📡 DATA SOURCES
    </p>
    <p style='font-size:10px; opacity:0.65;
              margin:3px 0;'>🔬 AlphaFold Database</p>
    <p style='font-size:10px; opacity:0.65;
              margin:3px 0;'>🧬 UniProt Knowledge Base</p>
    <p style='font-size:10px; opacity:0.65;
              margin:3px 0;'>💊 ChEMBL Drug Database</p>
    <p style='font-size:10px; opacity:0.65;
              margin:3px 0;'>🗄️ Protein Data Bank</p>
    <hr/>
    <p style='font-size:10px; opacity:0.65;
              margin:3px 0;'>👨‍💻 Developer: <b>Talha</b></p>
    <p style='font-size:10px; opacity:0.65;
              margin:3px 0;'>🎓 University: <b>UAF</b></p>
    <p style='font-size:10px; opacity:0.65;
              margin:3px 0;'>📦 Version: <b>1.0</b></p>
    """, unsafe_allow_html=True)

# ── Page Routing ──────────────────────────────────────────────
if page == "🏠 Home":
    from pages.home import show
    show()
elif page == "🏗️ Structure Viewer":
    from pages.structure import show
    show()
elif page == "⚙️ Function & Disease":
    from pages.function import show
    show()
elif page == "💊 Drug Intelligence":
    from pages.drugs import show
    show()
elif page == "🔗 Similar Proteins":
    from pages.similar import show
    show()