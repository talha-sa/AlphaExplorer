# AlphaExplorer - Drug Intelligence (Session State version)

import streamlit as st
import pandas as pd
import plotly.express as px
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))

from utils.api_utils import get_chembl_drugs

def show():
    st.title("💊 Drug Intelligence")
    st.markdown(
        "Drugs and clinical candidates targeting this protein "
        "from ChEMBL."
    )
    st.markdown("---")

    uid  = st.session_state.get("uniprot_id")
    info = st.session_state.get("protein_info", {})

    if not uid:
        st.info(
            "👈 Search for a protein in the sidebar first."
        )
        return

    st.markdown(f"### 💊 Drugs for {info.get('gene','N/A')} `{uid}`")
    st.markdown("---")

    with st.spinner("Fetching drug data from ChEMBL..."):
        drugs, err = get_chembl_drugs(uid, limit=25)

    if err:
        st.warning(f"⚠️ {err}")
        st.markdown(
            f"[Search ChEMBL manually]"
            f"(https://www.ebi.ac.uk/chembl/)"
        )
        return

    if not drugs:
        st.info("No drug data found in ChEMBL for this protein.")
        return

    df = pd.DataFrame(drugs)

    # Summary metrics
    approved   = df[df["Phase Number"] == 4]
    phase3     = df[df["Phase Number"] == 3]
    phase1_2   = df[df["Phase Number"].isin([1, 2])]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Drugs",    len(df))
    col2.metric("✅ Approved",    len(approved))
    col3.metric("🔬 Phase 3",     len(phase3))
    col4.metric("🧪 Phase 1/2",   len(phase1_2))

    # Phase distribution chart
    st.markdown("### 📊 Drug Pipeline by Phase")
    phase_counts = (
        df.groupby("Phase")
          .size()
          .reset_index(name="Count")
    )
    fig = px.bar(
        phase_counts,
        x="Phase", y="Count",
        color="Phase",
        color_discrete_sequence=px.colors.qualitative.Set2,
        title="Drug Count by Clinical Phase"
    )
    fig.update_layout(
        showlegend=False, height=350,
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Drug table
    st.markdown("### 📋 Drug List")
    display_df = df[[
        "Drug Name", "ChEMBL ID",
        "Phase", "Indication"
    ]].copy()
    st.dataframe(display_df, use_container_width=True)

    # Download
    csv = display_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Drug List CSV",
        data=csv,
        file_name=f"drugs_{uid}.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.markdown("---")
    st.caption(
        "Drug data from ChEMBL — European Bioinformatics Institute. "
        "Phase 4 = Approved, Phase 3/2/1 = Clinical trials, "
        "Phase 0 = Preclinical."
    )