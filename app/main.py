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

# Custom CSS for professional look
st.markdown("""
<style>
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1A1D26 0%, #0F1117 100%);
        border-right: 1px solid #2E86AB;
    }

    /* Main content */
    .main {
        background-color: #0F1117;
    }

    /* Metric cards */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #1A1D26, #252836);
        border: 1px solid #2E86AB;
        border-radius: 10px;
        padding: 15px;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #2E86AB, #1a5276);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: bold;
    }

    /* Input fields */
    .stTextInput > div > div > input {
        background-color: #1A1D26;
        border: 1px solid #2E86AB;
        color: white;
        border-radius: 8px;
    }

    /* Hide top auto-detected pages */
    section[data-testid="stSidebarNav"] {display: none;}

    /* Selectbox */
    .stSelectbox > div > div {
        background-color: #1A1D26;
        border: 1px solid #2E86AB;
    }

    /* Radio buttons */
    .stRadio > label {
        color: #FFFFFF !important;
    }

    /* Success boxes */
    .stSuccess {
        background-color: #1a3a2a;
        border-left: 4px solid #2ecc71;
    }

    /* Info boxes */
    .stInfo {
        background-color: #1a2a3a;
        border-left: 4px solid #2E86AB;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <h1 style='color: #2E86AB; font-size: 28px;'>🧬 AlphaExplorer</h1>
        <p style='color: #888; font-size: 13px;'>Protein Intelligence Dashboard</p>
        <p style='color: #555; font-size: 11px;'>Powered by AlphaFold Nobel Prize 2024</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    page = st.radio(
        "Navigate",
        ["🏠 Home",
         "🏗️ Structure Viewer",
         "⚙️ Function & Disease",
         "💊 Drug Intelligence",
         "🔗 Similar Proteins"],
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.markdown("""
    <div style='padding: 10px 0;'>
        <p style='color: #2E86AB; font-size: 12px; font-weight: bold;'>DATA SOURCES</p>
        <p style='color: #888; font-size: 11px;'>🔬 AlphaFold Database</p>
        <p style='color: #888; font-size: 11px;'>🧬 UniProt Knowledge Base</p>
        <p style='color: #888; font-size: 11px;'>💊 ChEMBL Drug Database</p>
        <p style='color: #888; font-size: 11px;'>🗄️ Protein Data Bank (PDB)</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    <div style='padding: 5px 0;'>
        <p style='color: #888; font-size: 11px;'>👨‍💻 Developed by: <b style='color:#2E86AB'>Talha</b></p>
        <p style='color: #888; font-size: 11px;'>🎓 University: <b style='color:#2E86AB'>UAF</b></p>
        <p style='color: #888; font-size: 11px;'>📦 Version: <b style='color:#2E86AB'>1.0</b></p>
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