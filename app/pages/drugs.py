# AlphaExplorer - Drug Intelligence Page

import streamlit as st
import pandas as pd
import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from utils.api_utils import (
    search_uniprot,
    get_chembl_drugs
)

def show():
    st.title("💊 Drug Intelligence")
    st.markdown("Discover drugs and compounds targeting your protein of interest.")
    st.markdown("---")

    query = st.text_input(
        "🔍 Search Protein",
        placeholder="e.g. ACE2, BRCA1, ACHE, TP53...",
        key="drug_search"
    )

    if not query:
        st.info("👆 Type a protein name to find associated drugs.")
        return

    with st.spinner("Searching..."):
        results = search_uniprot(query, limit=5)

    if not results:
        st.error("No proteins found.")
        return

    options = []
    for r in results:
        try:
            name = r["proteinDescription"]["recommendedName"]["fullName"]["value"]
        except:
            name = "Unknown"
        acc = r.get("primaryAccession", "Unknown")
        options.append(f"{name} | {acc}")

    selected = st.selectbox("Select protein:", options, key="drug_select")
    selected_idx = options.index(selected)
    uniprot_id = results[selected_idx]["primaryAccession"]

    with st.spinner("Fetching drug data from ChEMBL..."):
        drugs = get_chembl_drugs(uniprot_id, limit=20)

    st.markdown("---")

    if not drugs:
        st.warning("No drug data found in ChEMBL for this protein.")
        st.markdown(f"""
        **Try searching manually:**
        - [ChEMBL Target Search](https://www.ebi.ac.uk/chembl/target_report_card/{uniprot_id})
        - [UniProt Drug Cross-references](https://www.uniprot.org/uniprotkb/{uniprot_id})
        """)
        return

    st.success(f"✅ Found {len(drugs)} drug records")

    drug_data = []
    for d in drugs:
        drug_data.append({
            "Drug Name"   : d.get("molecule_name", "Unknown"),
            "ChEMBL ID"   : d.get("molecule_chembl_id", "N/A"),
            "Max Phase"   : d.get("max_phase_for_ind", "N/A"),
            "Indication"  : d.get("efo_term", "N/A"),
        })

    df = pd.DataFrame(drug_data)

    # Phase distribution
    st.markdown("### 📊 Drug Pipeline Overview")
    phase_counts = df["Max Phase"].value_counts()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Drugs", len(df))
    col2.metric("Phase 3/4", int(phase_counts.get(4, 0)) + int(phase_counts.get(3, 0)))
    col3.metric("Phase 1/2", int(phase_counts.get(1, 0)) + int(phase_counts.get(2, 0)))
    col4.metric("Approved", int(phase_counts.get(4, 0)))

    # Drug table
    st.markdown("### 📋 Drug List")
    st.dataframe(df, use_container_width=True)

    # Download
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Drug List CSV",
        data=csv,
        file_name=f"drugs_{uniprot_id}.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.markdown("---")
    st.caption("Drug data sourced from ChEMBL — European Bioinformatics Institute")