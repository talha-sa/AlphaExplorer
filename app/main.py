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

st.sidebar.title("🧬 AlphaExplorer")
st.sidebar.markdown("*Protein Intelligence Dashboard*")
st.sidebar.markdown("*Powered by AlphaFold Nobel Prize 2024*")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    ["🏠 Home",
     "🏗️ Structure Viewer",
     "⚙️ Function & Disease",
     "💊 Drug Intelligence",
     "🔗 Similar Proteins"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Data Sources:**")
st.sidebar.caption("🔬 AlphaFold Database")
st.sidebar.caption("🧬 UniProt")
st.sidebar.caption("💊 ChEMBL")
st.sidebar.caption("🗄️ PDB")
st.sidebar.markdown("---")
st.sidebar.markdown("**Developed by:** Talha")
st.sidebar.markdown("**University:** UAF")
st.sidebar.markdown("**Version:** 1.0")

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