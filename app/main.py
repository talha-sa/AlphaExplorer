# AlphaExplorer - Main Entry Point

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
    /* Hide auto-detected pages completely */
   section[data-testid="stSidebarNav"] {display: none !important;}
div[data-testid="stSidebarNavItems"] {display: none !important;}
ul[data-testid="stSidebarNavItems"] {display: none !important;}
[data-testid="stSidebarNav"] {display: none !important;}
.st-emotion-cache-pbsa4j {display: none !important;}
    /* Sidebar gradient */
    [data-testid="stSidebar"] {
        background: linear-gradient(160deg,
            #667eea 0%,
            #764ba2 40%,
            #f64f59 100%);
    }

    /* Sidebar text white */
    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Radio buttons in sidebar */
    [data-testid="stSidebar"] .stRadio label {
        color: white !important;
        font-size: 15px;
        font-weight: 500;
    }

    /* Main background */
    .main, .block-container {
        background-color: #FFFFFF;
    }

    /* Metric cards colorful */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 12px;
        padding: 15px;
        color: white !important;
    }
    [data-testid="metric-container"] * {
        color: white !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white !important;
        border: none;
        border-radius: 10px;
        font-weight: bold;
        font-size: 16px;
        padding: 10px 20px;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #764ba2, #f64f59);
        transform: scale(1.02);
    }

    /* Input fields */
    .stTextInput > div > div > input {
        border: 2px solid #667eea;
        border-radius: 10px;
        font-size: 15px;
        padding: 10px;
    }

    /* Selectbox */
    .stSelectbox > div > div {
        border: 2px solid #667eea;
        border-radius: 10px;
    }

    /* Success */
    .stSuccess {
        background: linear-gradient(135deg, #d4edda, #c3e6cb);
        border-left: 4px solid #28a745;
        border-radius: 8px;
    }

    /* Info */
    .stAlert {
        border-radius: 10px;
    }

    /* Dataframe */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
    }

    /* Headers */
    h1 { color: #1A1A2E !important; }
    h2 { color: #667eea !important; }
    h3 { color: #764ba2 !important; }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:25px 10px 15px 10px;'>
        <div style='font-size:48px;'>🧬</div>
        <h1 style='color:white; font-size:26px;
                   margin:5px 0; font-weight:800;'>
            AlphaExplorer
        </h1>
        <p style='color:rgba(255,255,255,0.8);
                  font-size:13px; margin:0;'>
            Protein Intelligence Dashboard
        </p>
        <p style='color:rgba(255,255,255,0.6);
                  font-size:11px; margin:5px 0 0 0;'>
            🏆 Powered by AlphaFold Nobel 2024
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <hr style='border:1px solid rgba(255,255,255,0.3);
               margin: 10px 0;'>
    """, unsafe_allow_html=True)

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
    <hr style='border:1px solid rgba(255,255,255,0.3);
               margin: 10px 0;'>
    <div style='padding:10px 5px;'>
        <p style='color:rgba(255,255,255,0.9);
                  font-size:12px; font-weight:700;
                  letter-spacing:1px;'>
            📡 DATA SOURCES
        </p>
        <p style='color:rgba(255,255,255,0.75);
                  font-size:11px; margin:4px 0;'>
            🔬 AlphaFold Database
        </p>
        <p style='color:rgba(255,255,255,0.75);
                  font-size:11px; margin:4px 0;'>
            🧬 UniProt Knowledge Base
        </p>
        <p style='color:rgba(255,255,255,0.75);
                  font-size:11px; margin:4px 0;'>
            💊 ChEMBL Drug Database
        </p>
        <p style='color:rgba(255,255,255,0.75);
                  font-size:11px; margin:4px 0;'>
            🗄️ Protein Data Bank (PDB)
        </p>
    </div>
    <hr style='border:1px solid rgba(255,255,255,0.3);
               margin: 10px 0;'>
    <div style='padding:5px;'>
        <p style='color:rgba(255,255,255,0.75);
                  font-size:11px; margin:3px 0;'>
            👨‍💻 Developer: <b>Talha</b>
        </p>
        <p style='color:rgba(255,255,255,0.75);
                  font-size:11px; margin:3px 0;'>
            🎓 University: <b>UAF</b>
        </p>
        <p style='color:rgba(255,255,255,0.75);
                  font-size:11px; margin:3px 0;'>
            📦 Version: <b>1.0</b>
        </p>
    </div>
    """, unsafe_allow_html=True)

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