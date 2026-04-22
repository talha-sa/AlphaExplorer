# AlphaExplorer - Similar Proteins (Session State version)

import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))

from utils.api_utils import search_uniprot

def show():
    st.title("🔗 Similar Proteins")
    st.markdown(
        "Find proteins with similar names, "
        "functions or gene families."
    )
    st.markdown("---")

    uid  = st.session_state.get("uniprot_id")
    info = st.session_state.get("protein_info", {})

    # Auto-suggest based on current protein gene name
    default_query = info.get("gene", "") if uid else ""

    query = st.text_input(
        "🔍 Search Protein Family or Function",
        value=default_query,
        placeholder="kinase, receptor, transferase...",
        key="similar_search"
    )

    organism_filter = st.selectbox(
        "🌍 Filter by Organism",
        ["All", "Human (Homo sapiens)",
         "Mouse (Mus musculus)",
         "E. coli", "Rat (Rattus norvegicus)"]
    )

    if not query.strip():
        st.info(
            "Enter a protein family name or function above "
            "to find related proteins."
        )
        return

    search_q = query.strip()
    if organism_filter == "Human (Homo sapiens)":
        search_q += " AND organism_id:9606"
    elif organism_filter == "Mouse (Mus musculus)":
        search_q += " AND organism_id:10090"
    elif organism_filter == "E. coli":
        search_q += " AND organism_id:83333"
    elif organism_filter == "Rat (Rattus norvegicus)":
        search_q += " AND organism_id:10116"

    with st.spinner("Searching UniProt..."):
        results, err = search_uniprot(search_q, limit=15)

    if err:
        st.error(f"Search failed: {err}")
        return

    if not results:
        st.warning(
            "No proteins found. Try a broader search term."
        )
        return

    st.success(f"✅ Found {len(results)} related proteins")

    proteins = []
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
        try:
            gene = r["genes"][0]["geneName"]["value"]
        except:
            gene = "N/A"
        try:
            length = r["sequence"]["length"]
        except:
            length = "N/A"

        proteins.append({
            "Protein Name": name,
            "UniProt ID"  : acc,
            "Gene"        : gene,
            "Organism"    : org,
            "Length (aa)" : length
        })

    df = pd.DataFrame(proteins)

    st.markdown("### 📋 Related Proteins")
    st.dataframe(df, use_container_width=True)

    # Quick links
    st.markdown("### 🔗 UniProt Links")
    cols = st.columns(3)
    for i, p in enumerate(proteins[:9]):
        with cols[i % 3]:
            st.link_button(
                f"🔬 {p['Gene']} ({p['UniProt ID']})",
                f"https://www.uniprot.org/uniprotkb/{p['UniProt ID']}",
                use_container_width=True
            )

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Table CSV",
        data=csv,
        file_name="similar_proteins.csv",
        mime="text/csv",
        use_container_width=True
    )