# AlphaExplorer - Function & Disease Page

import streamlit as st
import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from utils.api_utils import (
    search_uniprot,
    get_uniprot_details,
    extract_protein_info
)
from utils.plot_utils import plot_disease_bar

def show():
    st.title("⚙️ Function & Disease")
    st.markdown("Explore protein function, biological pathways and disease associations.")
    st.markdown("---")

    query = st.text_input(
        "🔍 Search Protein",
        placeholder="e.g. ACE2, BRCA1, TP53, ACHE...",
        key="function_search"
    )

    if not query:
        st.info("👆 Type a protein name above to get started.")
        return

    with st.spinner("Searching..."):
        results, error = search_uniprot(query, limit=5)

    if error:
        st.error(error)
        return

    if not results:
        st.error("No proteins found. Try a different search term.")
        return

    options = []
    for r in results:
        try:
            name = r["proteinDescription"]["recommendedName"]["fullName"]["value"]
        except:
            name = "Unknown"
        acc = r.get("primaryAccession", "Unknown")
        try:
            org = r["organism"]["scientificName"]
        except:
            org = "Unknown"
        options.append(f"{name} | {acc} | {org}")

    selected = st.selectbox("Select protein:", options, key="function_select")
    selected_idx = options.index(selected)
    uniprot_id = results[selected_idx]["primaryAccession"]

    with st.spinner("Loading protein details..."):
        data, error = get_uniprot_details(uniprot_id)
        if error:
            st.error(error)
            return
        info = extract_protein_info(data)

    if not info:
        st.error("Could not load protein details.")
        return

    st.markdown("---")

    # Basic info
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Gene", info.get("gene", "N/A"))
    col2.metric("Length", f"{info.get('length', 'N/A')} aa")
    col3.metric("Organism", info.get("organism", "N/A")[:20])
    col4.metric("Diseases", len(info.get("diseases", [])))

    # Function
    st.markdown("### 🔬 Biological Function")
    func = info.get("function", "Not available")
    if func != "Not available":
        st.success(func)
    else:
        st.info("Function information not available for this protein.")

    # Location
    st.markdown("### 📍 Subcellular Location")
    loc = info.get("location", "Unknown")
    st.info(f"📍 {loc}")

    # Diseases
    st.markdown("### 🦠 Associated Diseases")
    diseases = info.get("diseases", [])
    if diseases:
        fig = plot_disease_bar(diseases)
        if fig:
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("**Disease List:**")
        for i, d in enumerate(diseases, 1):
            st.markdown(f"{i}. {d}")
    else:
        st.info("No disease associations found for this protein.")

    # GO Terms
    st.markdown("### 🧬 Gene Ontology (GO) Terms")
    if data:
        go_terms = []
        for ref in data.get("uniProtKBCrossReferences", []):
            if ref.get("database") == "GO":
                try:
                    props = ref.get("properties", [])
                    for prop in props:
                        if prop.get("key") == "GoTerm":
                            go_terms.append(prop.get("value", ""))
                except:
                    pass

        if go_terms:
            bio = [t for t in go_terms if t.startswith("P:")]
            mol = [t for t in go_terms if t.startswith("F:")]
            cel = [t for t in go_terms if t.startswith("C:")]

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("**Biological Process**")
                for t in bio[:5]:
                    st.caption(f"• {t[2:]}")
            with col2:
                st.markdown("**Molecular Function**")
                for t in mol[:5]:
                    st.caption(f"• {t[2:]}")
            with col3:
                st.markdown("**Cellular Component**")
                for t in cel[:5]:
                    st.caption(f"• {t[2:]}")
        else:
            st.info("No GO terms available.")

    # UniProt link
    st.markdown("---")
    st.link_button(
        f"🔗 View full entry on UniProt",
        f"https://www.uniprot.org/uniprotkb/{uniprot_id}",
        use_container_width=True
    )