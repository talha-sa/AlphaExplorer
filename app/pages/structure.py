# AlphaExplorer - Structure Viewer Page

import streamlit as st
import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from utils.api_utils import (
    get_alphafold_structure,
    get_pdb_string,
    get_uniprot_details,
    extract_protein_info,
    search_uniprot
)
from utils.plot_utils import (
    plot_confidence_distribution,
    plot_confidence_per_residue
)

def show():
    st.title("🏗️ Structure Viewer")
    st.markdown("Search any protein to view its AlphaFold predicted structure.")
    st.markdown("---")

    query = st.text_input(
        "🔍 Search Protein",
        placeholder="e.g. ACE2, BRCA1, TP53, ACHE, insulin...",
        help="Enter protein name, gene name, or UniProt ID"
    )

    if not query:
        st.info("👆 Type a protein name above to get started.")
        st.markdown("**Quick examples:** ACE2 · BRCA1 · TP53 · ACHE · Insulin · Hemoglobin")
        return

    with st.spinner(f"Searching UniProt for '{query}'..."):
        results = search_uniprot(query, limit=5)

    if not results:
        st.error(f"No proteins found for '{query}'. Try a different name.")
        return

    st.markdown("### 🔎 Search Results")
    options = []
    for r in results:
        try:
            name = r["proteinDescription"]["recommendedName"]["fullName"]["value"]
        except:
            name = "Unknown protein"
        try:
            acc = r["primaryAccession"]
        except:
            acc = "Unknown"
        try:
            org = r["organism"]["scientificName"]
        except:
            org = "Unknown"
        options.append(f"{name} | {acc} | {org}")

    selected = st.selectbox("Select a protein:", options)
    selected_idx = options.index(selected)
    uniprot_id = results[selected_idx]["primaryAccession"]

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with st.spinner("Fetching AlphaFold structure..."):
        af_data = get_alphafold_structure(uniprot_id)
        uniprot_data = get_uniprot_details(uniprot_id)
        protein_info = extract_protein_info(uniprot_data)

    if not af_data:
        st.warning(f"No AlphaFold structure found for {uniprot_id}.")
        st.markdown("**Available info from UniProt:**")
        if protein_info:
            st.json(protein_info)
        return

    # Metrics
    col1.metric("🧬 Protein", protein_info.get("gene", "N/A"))
    col2.metric("📏 Length", f"{protein_info.get('length', 'N/A')} aa")
    col3.metric("🏆 AlphaFold Version", af_data.get("latestVersion", "N/A"))

    # 3D Structure viewer
    st.markdown("### 🔬 3D Structure")
    st.markdown("*Colored by confidence: 🔵 Very High | 🩵 High | 🟡 Low | 🟠 Very Low*")

    pdb_url = af_data.get("pdbUrl", "")
    if pdb_url:
        pdb_string = get_pdb_string(pdb_url)
        if pdb_string:
            try:
                import py3Dmol
                view = py3Dmol.view(width=700, height=500)
                view.addModel(pdb_string, "pdb")
                view.setStyle({}, {"cartoon": {
                    "colorscheme": {
                        "prop": "b",
                        "gradient": "roygb",
                        "min": 50,
                        "max": 90
                    }
                }})
                view.zoomTo()
                view.spin(True)

                import streamlit.components.v1 as components
                components.html(
                    view._make_html(),
                    height=520
                )
            except Exception as e:
                st.warning(f"3D viewer error: {e}")
                st.markdown(f"[View structure on AlphaFold DB]({af_data.get('cifUrl', '')})")
        else:
            st.error("Could not fetch structure file.")
    else:
        st.warning("No PDB URL available for this protein.")

    # Confidence scores
    st.markdown("### 📊 Confidence Analysis (pLDDT)")
    st.markdown("""
    pLDDT (predicted Local Distance Difference Test) measures 
    AlphaFold's confidence in each residue position:
    - **90-100** 🔵 Very high confidence
    - **70-90** 🩵 High confidence  
    - **50-70** 🟡 Low confidence
    - **0-50** 🟠 Very low confidence
    """)

    mean_plddt = af_data.get("meanPlddt", 0)
    st.metric("Average pLDDT Score", f"{mean_plddt:.1f}/100")

    if mean_plddt >= 90:
        st.success("✅ Very high confidence structure prediction")
    elif mean_plddt >= 70:
        st.info("ℹ️ High confidence structure prediction")
    elif mean_plddt >= 50:
        st.warning("⚠️ Low confidence — interpret with caution")
    else:
        st.error("❌ Very low confidence — structure may be unreliable")

    # Download button
    if pdb_url:
        st.markdown("---")
        st.markdown("### ⬇️ Downloads")
        col1, col2 = st.columns(2)
        with col1:
            st.link_button(
                "⬇️ Download PDB File",
                pdb_url,
                use_container_width=True
            )
        with col2:
            cif_url = af_data.get("cifUrl", "")
            if cif_url:
                st.link_button(
                    "⬇️ Download CIF File",
                    cif_url,
                    use_container_width=True
                )