# AlphaExplorer - Structure Viewer (Session State version)

import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))

from utils.api_utils import get_alphafold_structure, get_pdb_string
from utils.plot_utils import (
    plot_confidence_distribution,
    plot_confidence_per_residue
)

def show():
    st.title("🏗️ Structure Viewer")
    st.markdown(
        "3D structure powered by AlphaFold — "
        "confidence colored by pLDDT score."
    )
    st.markdown("---")

    uid  = st.session_state.get("uniprot_id")
    info = st.session_state.get("protein_info", {})

    if not uid:
        st.info(
            "👈 Search for a protein in the sidebar to "
            "view its structure."
        )
        st.markdown("**Try:** ACE2 · BRCA1 · TP53 · ACHE · Insulin")
        return

    st.markdown(f"### 🧬 {info.get('name','Unknown')} `{uid}`")

    col1, col2, col3 = st.columns(3)
    col1.metric("Gene",     info.get("gene",     "N/A"))
    col2.metric("Organism", info.get("organism", "N/A")[:20])
    col3.metric("Length",   f"{info.get('length','N/A')} aa")

    st.markdown("---")

    with st.spinner("Fetching AlphaFold structure..."):
        af_data, err = get_alphafold_structure(uid)

    if err or not af_data:
        st.warning(
            f"⚠️ No AlphaFold structure for `{uid}`. "
            f"{err or ''}"
        )
        st.markdown(
            f"[Search AlphaFold manually]"
            f"(https://alphafold.ebi.ac.uk/entry/{uid})"
        )
        return

    mean_plddt = af_data.get("meanPlddt", 0)
    version    = af_data.get("latestVersion", "N/A")

    col1, col2, col3 = st.columns(3)
    col1.metric("AlphaFold Version", version)
    col2.metric("Mean pLDDT",        f"{mean_plddt:.1f}/100")
    if mean_plddt >= 90:
        col3.success("✅ Very High Confidence")
    elif mean_plddt >= 70:
        col3.info("ℹ️ High Confidence")
    elif mean_plddt >= 50:
        col3.warning("⚠️ Low Confidence")
    else:
        col3.error("❌ Very Low Confidence")

    # 3D Viewer
    st.markdown("### 🔬 3D Structure")
    st.caption(
        "🔵 Very High (90+)  |  "
        "🩵 High (70–90)  |  "
        "🟡 Low (50–70)  |  "
        "🟠 Very Low (<50)"
    )

    pdb_url = af_data.get("pdbUrl", "")
    if pdb_url:
        with st.spinner("Loading 3D structure..."):
            pdb_string, perr = get_pdb_string(pdb_url)

        if pdb_string:
            try:
                import py3Dmol
                import streamlit.components.v1 as components
                view = py3Dmol.view(width=750, height=500)
                view.addModel(pdb_string, "pdb")
                view.setStyle({}, {"cartoon": {
                    "colorscheme": {
                        "prop"    : "b",
                        "gradient": "roygb",
                        "min"     : 50,
                        "max"     : 90
                    }
                }})
                view.zoomTo()
                view.spin(True)
                components.html(
                    view._make_html(), height=520
                )
            except Exception as e:
                st.warning(f"3D viewer unavailable: {e}")
                st.markdown(
                    f"[View on AlphaFold DB]"
                    f"(https://alphafold.ebi.ac.uk/entry/{uid})"
                )
        else:
            st.error(f"Could not load structure. {perr}")
    else:
        st.warning("No PDB URL available.")

    # Downloads
    st.markdown("---")
    st.markdown("### ⬇️ Downloads")
    col1, col2, col3 = st.columns(3)
    with col1:
        if pdb_url:
            st.link_button(
                "⬇️ PDB File", pdb_url,
                use_container_width=True
            )
    with col2:
        cif = af_data.get("cifUrl", "")
        if cif:
            st.link_button(
                "⬇️ CIF File", cif,
                use_container_width=True
            )
    with col3:
        st.link_button(
            "🔗 AlphaFold Entry",
            f"https://alphafold.ebi.ac.uk/entry/{uid}",
            use_container_width=True
        )