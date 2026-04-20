# AlphaExplorer - Similar Proteins Page

import streamlit as st
import pandas as pd
import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from utils.api_utils import search_uniprot, get_uniprot_details

def show():
    st.title("🔗 Similar Proteins")
    st.markdown("Find proteins with similar names, functions or gene families.")
    st.markdown("---")

    query = st.text_input(
        "🔍 Search Protein Family or Function",
        placeholder="e.g. kinase, receptor, transferase, hemoglobin...",
        key="similar_search"
    )

    organism_filter = st.selectbox(
        "🌍 Filter by Organism",
        ["All", "Human (Homo sapiens)",
         "Mouse (Mus musculus)",
         "E. coli", "Yeast"]
    )

    if not query:
        st.info("👆 Type a protein family name to explore related proteins.")
        return

    search_query = query
    if organism_filter == "Human (Homo sapiens)":
        search_query += " AND organism_name:human"
    elif organism_filter == "Mouse (Mus musculus)":
        search_query += " AND organism_name:mouse"
    elif organism_filter == "E. coli":
        search_query += " AND organism_name:ecoli"

    with st.spinner("Searching for similar proteins..."):
        results = search_uniprot(search_query, limit=10)

    if not results:
        st.error("No proteins found. Try a broader search term.")
        return

    st.success(f"✅ Found {len(results)} related proteins")

    proteins = []
    for r in results:
        try:
            name = r["proteinDescription"]["recommendedName"]["fullName"]["value"]
        except:
            try:
                name = r["proteinDescription"]["submittedNames"][0]["fullName"]["value"]
            except:
                name = "Unknown"

        acc  = r.get("primaryAccession", "N/A")
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
            "Protein Name" : name,
            "UniProt ID"   : acc,
            "Gene"         : gene,
            "Organism"     : org,
            "Length (aa)"  : length,
            "UniProt Link" : f"https://www.uniprot.org/uniprotkb/{acc}"
        })

    df = pd.DataFrame(proteins)

    st.markdown("### 📋 Related Proteins")
    st.dataframe(
        df[["Protein Name", "UniProt ID", "Gene",
            "Organism", "Length (aa)"]],
        use_container_width=True
    )

    st.markdown("### 🔗 Quick Links")
    for p in proteins[:5]:
        st.markdown(
            f"• [{p['Protein Name']} ({p['UniProt ID']})]"
            f"({p['UniProt Link']})"
        )

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Table as CSV",
        data=csv,
        file_name="similar_proteins.csv",
        mime="text/csv",
        use_container_width=True
    )