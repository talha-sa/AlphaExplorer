# AlphaExplorer - Main Entry Point
# Clean, Colorful, Professional Streamlit App

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

# ── Clean Colorful CSS ─────────────────────────────────────────
st.markdown("""
<style>
    /* Hide Streamlit auto nav */
    section[data-testid="stSidebarNav"],
    div[data-testid="stSidebarNavItems"],
    ul[data-testid="stSidebarNavItems"] { display: none !important; }

    /* Sidebar gradient */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg,
            #6C63FF 0%, #3B82F6 60%, #06B6D4 100%) !important;
    }
    [data-testid="stSidebar"] * { color: white !important; }
    [data-testid="stSidebar"] .stTextInput input,
    [data-testid="stSidebar"] .stTextInput input:focus,
    [data-testid="stSidebar"] .stTextInput input:active,
    [data-testid="stSidebar"] .stTextInput input:hover {
        background: rgba(255,255,255,0.18) !important;
        border: 1px solid rgba(255,255,255,0.5) !important;
        border-radius: 8px !important;
        color: white !important;
        -webkit-text-fill-color: white !important;
        caret-color: white !important;
        box-shadow: none !important;
        outline: none !important;
    }
    [data-testid="stSidebar"] .stTextInput input::placeholder {
        color: rgba(255,255,255,0.6) !important;
    }
    /* Prevent browser autofill white-box override */
    [data-testid="stSidebar"] .stTextInput input:-webkit-autofill,
    [data-testid="stSidebar"] .stTextInput input:-webkit-autofill:hover,
    [data-testid="stSidebar"] .stTextInput input:-webkit-autofill:focus {
        -webkit-text-fill-color: white !important;
        -webkit-box-shadow: 0 0 0px 1000px rgba(80,60,220,0.7) inset !important;
        caret-color: white !important;
    }
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background: rgba(255,255,255,0.15) !important;
        border: 1px solid rgba(255,255,255,0.4) !important;
        border-radius: 8px !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        color: white !important;
        font-size: 14px !important;
        font-weight: 500 !important;
    }

    /* Main area */
    .main .block-container {
        background-color: #F8F9FF !important;
        padding-top: 24px !important;
    }

    /* Metric cards */
    [data-testid="metric-container"] {
        background: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 20px !important;
        box-shadow: 0 2px 12px rgba(108,99,255,0.1) !important;
        border-left: 4px solid #6C63FF !important;
    }
    [data-testid="stMetricValue"] {
        color: #6C63FF !important;
        font-size: 28px !important;
        font-weight: 700 !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #6C63FF, #3B82F6) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 10px 24px !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #3B82F6, #06B6D4) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(108,99,255,0.35) !important;
    }

    /* Text inputs */
    .stTextInput > div > div > input {
        border: 2px solid #E5E7EB !important;
        border-radius: 10px !important;
        font-size: 14px !important;
        transition: border-color 0.2s !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #6C63FF !important;
        box-shadow: 0 0 0 3px rgba(108,99,255,0.1) !important;
    }

    /* Selectbox */
    .stSelectbox > div > div {
        border: 2px solid #E5E7EB !important;
        border-radius: 10px !important;
    }

    /* Headings */
    h1 { color: #1A1A2E !important; font-weight: 700 !important; }
    h2 { color: #6C63FF !important; font-weight: 600 !important; }
    h3 { color: #3B82F6 !important; font-weight: 600 !important; }

    /* Dataframe */
    [data-testid="stDataFrame"] {
        border-radius: 12px !important;
        overflow: hidden !important;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06) !important;
    }

    /* Success / Info / Warning / Error */
    .stSuccess {
        background: #F0FDF4 !important;
        border-left: 4px solid #22C55E !important;
        border-radius: 8px !important;
    }
    .stInfo {
        background: #EFF6FF !important;
        border-left: 4px solid #3B82F6 !important;
        border-radius: 8px !important;
    }
    .stWarning {
        background: #FFFBEB !important;
        border-left: 4px solid #F59E0B !important;
        border-radius: 8px !important;
    }
    .stError {
        background: #FEF2F2 !important;
        border-left: 4px solid #EF4444 !important;
        border-radius: 8px !important;
    }

    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #6C63FF, #06B6D4) !important;
        border-radius: 4px !important;
    }

    /* Divider */
    hr { border-color: #E5E7EB !important; }

    /* Download button */
    [data-testid="stDownloadButton"] > button {
        background: white !important;
        color: #6C63FF !important;
        border: 2px solid #6C63FF !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }
    [data-testid="stDownloadButton"] > button:hover {
        background: #6C63FF !important;
        color: white !important;
    }

    /* Link button */
    [data-testid="stLinkButton"] > a {
        background: white !important;
        color: #6C63FF !important;
        border: 2px solid #6C63FF !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }

    /* Caption */
    .stCaption { color: #6B7280 !important; }
</style>
""", unsafe_allow_html=True)

# Disable browser autocomplete on sidebar inputs (prevents white dropdown over purple sidebar)
st.markdown("""
<script>
(function() {
    function disableAutocomplete() {
        var inputs = document.querySelectorAll(
            '[data-testid="stSidebar"] input[type="text"]'
        );
        inputs.forEach(function(inp) {
            inp.setAttribute('autocomplete', 'off');
            inp.setAttribute('autocorrect', 'off');
            inp.setAttribute('autocapitalize', 'none');
            inp.setAttribute('spellcheck', 'false');
        });
    }
    var observer = new MutationObserver(disableAutocomplete);
    observer.observe(document.body, { childList: true, subtree: true });
    disableAutocomplete();
})();
</script>
""", unsafe_allow_html=True)

# ── Session State ───────────────────────────────────────────────
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
    # Logo
    st.markdown("""
    <div style='text-align:center; padding:20px 0 10px 0;'>
        <div style='font-size:44px;'>🧬</div>
        <h1 style='font-size:22px; font-weight:800;
                   color:white; margin:6px 0 2px 0;'>
            AlphaExplorer
        </h1>
        <p style='font-size:11px; color:rgba(255,255,255,0.75);
                  margin:0;'>
            Protein Intelligence Dashboard
        </p>
        <p style='font-size:10px; color:rgba(255,255,255,0.55);
                  margin:4px 0 0 0;'>
            🏆 AlphaFold · Nobel Prize 2024
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Global Search
    st.markdown("""
    <p style='font-size:11px; font-weight:700;
              color:rgba(255,255,255,0.85);
              letter-spacing:1px; margin-bottom:6px;'>
        🔍 SEARCH PROTEIN
    </p>
    """, unsafe_allow_html=True)

    query = st.text_input(
        "Search",
        placeholder="e.g. ACE2, BRCA1, ACHE...",
        label_visibility="collapsed",
        key="global_search"
    )

    if st.button("🔍  Search", use_container_width=True):
        if query.strip():
            from utils.api_utils import (
                search_uniprot,
                get_uniprot_details,
                extract_protein_info
            )
            with st.spinner("Searching UniProt..."):
                results, err = search_uniprot(
                    query.strip(), limit=8
                )

            if err:
                st.error(err)
            elif not results:
                st.warning("No proteins found. Try another name.")
            else:
                options = []
                for r in results:
                    try:
                        name = (
                            r["proteinDescription"]
                             ["recommendedName"]
                             ["fullName"]["value"]
                        )
                    except:
                        try:
                            name = (
                                r["proteinDescription"]
                                 ["submittedNames"][0]
                                 ["fullName"]["value"]
                            )
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

    # Protein selector
    if st.session_state.search_done:
        options = st.session_state.search_options
        results = st.session_state.search_results

        if options:
            selected = st.selectbox(
                "Select protein:",
                options,
                label_visibility="collapsed",
                key="protein_selector"
            )
            idx       = options.index(selected)
            chosen_id = results[idx]["primaryAccession"]

            if chosen_id != st.session_state.uniprot_id:
                st.session_state.uniprot_id = chosen_id
                from utils.api_utils import (
                    get_uniprot_details, extract_protein_info
                )
                with st.spinner("Loading protein..."):
                    data, err = get_uniprot_details(chosen_id)
                    if data:
                        info = extract_protein_info(data)
                        st.session_state.protein_info = info
                        st.session_state.uniprot_raw  = data
                        st.session_state.protein_name = info.get(
                            "name", chosen_id
                        )

    # Loaded protein card
    if st.session_state.uniprot_id:
        info = st.session_state.protein_info or {}
        st.markdown(f"""
        <hr style='border-color:rgba(255,255,255,0.25);'/>
        <div style='background:rgba(255,255,255,0.15);
                    border-radius:10px; padding:12px;
                    margin:8px 0;
                    border:1px solid rgba(255,255,255,0.25);'>
            <p style='font-size:10px; font-weight:700;
                      color:rgba(255,255,255,0.7);
                      letter-spacing:1px; margin:0 0 4px 0;'>
                ✅ LOADED
            </p>
            <p style='font-size:14px; font-weight:700;
                      color:white; margin:0 0 2px 0;'>
                {info.get('gene','N/A')}
            </p>
            <p style='font-size:11px;
                      color:rgba(255,255,255,0.75);
                      margin:0 0 4px 0;'>
                {info.get('name','')[:35]}
            </p>
            <p style='font-size:10px;
                      color:rgba(255,255,255,0.55);
                      margin:0;'>
                📏 {info.get('length','N/A')} aa
                &nbsp;|&nbsp;
                🆔 {st.session_state.uniprot_id}
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Navigation
    st.markdown("---")
    page = st.radio(
        "Navigate",
        [
            "🏠  Home",
            "🏗️  Structure Viewer",
            "⚙️  Function & Disease",
            "💊  Drug Intelligence",
            "🔗  Similar Proteins",
        ],
        label_visibility="collapsed"
    )

    # Data sources + footer
    st.markdown("""
    <hr style='border-color:rgba(255,255,255,0.25);'/>
    <p style='font-size:10px; font-weight:700;
              color:rgba(255,255,255,0.7);
              letter-spacing:1px; margin-bottom:6px;'>
        📡 DATA SOURCES
    </p>
    <p style='font-size:10px; color:rgba(255,255,255,0.65);
              margin:3px 0;'>🔬 AlphaFold Database</p>
    <p style='font-size:10px; color:rgba(255,255,255,0.65);
              margin:3px 0;'>🧬 UniProt Knowledge Base</p>
    <p style='font-size:10px; color:rgba(255,255,255,0.65);
              margin:3px 0;'>💊 ChEMBL Drug Database</p>
    <p style='font-size:10px; color:rgba(255,255,255,0.65);
              margin:3px 0;'>🗄️ Protein Data Bank (PDB)</p>
    <hr style='border-color:rgba(255,255,255,0.25);'/>
    <p style='font-size:10px; color:rgba(255,255,255,0.6);
              margin:3px 0;'>👨‍💻 Developer: <b>Talha Saleem</b></p>
    <p style='font-size:10px; color:rgba(255,255,255,0.6);
              margin:3px 0;'>🎓 University: <b>UAF</b></p>
    <p style='font-size:10px; color:rgba(255,255,255,0.6);
              margin:3px 0;'>📦 Version: <b>1.0</b></p>
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