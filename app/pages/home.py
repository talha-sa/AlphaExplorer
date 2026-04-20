# AlphaExplorer - Home Page

import streamlit as st

def show():
    st.title("🧬 AlphaExplorer")
    st.subheader("Protein Structure Intelligence Dashboard")
    st.markdown("*Powered by AlphaFold • UniProt • ChEMBL*")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🏆 Nobel Prize", "2024", "Chemistry")
    col2.metric("🧬 Proteins", "200M+", "Predicted")
    col3.metric("🗄️ Databases", "5", "Integrated")
    col4.metric("💊 Drugs", "Thousands", "Mapped")

    st.markdown("---")

    st.info("""
    **AlphaFold** — developed by Google DeepMind — solved one of 
    biology's greatest challenges: predicting the 3D structure of 
    proteins from their amino acid sequence. It won the **Nobel Prize 
    in Chemistry 2024** and predicted structures for **200+ million proteins**.
    
    **AlphaExplorer** makes this data accessible by combining structural 
    data with disease context, drug information, and functional insights 
    — all in one beautiful dashboard.
    """)

    st.markdown("### 🔬 What Can You Explore?")
    col1, col2 = st.columns(2)
    with col1:
        st.success("**🏗️ 3D Structure Viewer**\nVisualize protein structure with confidence coloring")
        st.success("**🦠 Disease Links**\nDiscover which diseases a protein is associated with")
        st.success("**💊 Drug Intelligence**\nFind known drugs targeting your protein")
    with col2:
        st.success("**⚙️ Protein Function**\nUnderstand what the protein does biologically")
        st.success("**🧪 Structural Stats**\nConfidence scores and structural metrics")
        st.success("**🔗 Similar Proteins**\nFind related proteins across species")

    st.markdown("### 🚀 How to Use")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.info("**Step 1**\nType any protein name or UniProt ID in the search bar")
    with col2:
        st.info("**Step 2**\nSelect your protein from the search results")
    with col3:
        st.info("**Step 3**\nExplore structure, function, diseases and drugs")
    with col4:
        st.info("**Step 4**\nDownload results or share insights")

    st.markdown("### 🎯 Try These Examples")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("**ACE2**")
        st.caption("COVID-19 receptor")
    with col2:
        st.markdown("**BRCA1**")
        st.caption("Breast cancer gene")
    with col3:
        st.markdown("**TP53**")
        st.caption("Tumour suppressor")
    with col4:
        st.markdown("**ACHE**")
        st.caption("Alzheimer's target")

    st.markdown("---")
    st.caption("Data: AlphaFold DB | UniProt | ChEMBL | PDB | KEGG")