# AlphaExplorer - Drug Intelligence (Bento Grid Phase Cards)

import streamlit as st
import pandas as pd
import plotly.express as px
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))

from utils.api_utils import get_chembl_drugs

PHASE_STYLES = {
    4 : {"label":"✅ Approved",   "color":"#00dce6", "bg":"rgba(0,220,230,0.08)"},
    3 : {"label":"🔬 Phase III",  "color":"#b9c3ff", "bg":"rgba(185,195,255,0.08)"},
    2 : {"label":"🧪 Phase II",   "color":"#667eea", "bg":"rgba(102,126,234,0.08)"},
    1 : {"label":"🔭 Phase I",    "color":"#ffb3b2", "bg":"rgba(255,179,178,0.08)"},
    0 : {"label":"💡 Preclinical","color":"#888",    "bg":"rgba(100,100,100,0.08)"},
    -1: {"label":"❌ Discontinued","color":"#f64f59","bg":"rgba(246,79,89,0.08)"},
}

def show():
    uid  = st.session_state.get("uniprot_id")
    info = st.session_state.get("protein_info", {})

    st.markdown("""
    <h1 style="
        font-family:'Space Grotesk',sans-serif;
        font-size:36px; font-weight:600;
        letter-spacing:-0.02em; color:#ffffff; margin:0 0 4px 0;
    ">💊 Drug Intelligence</h1>
    <p style="color:rgba(197,197,213,0.5); font-size:14px; margin:0 0 20px 0;">
        Clinical pipeline data from ChEMBL database.</p>
    <hr style="border:1px solid rgba(255,255,255,0.07); margin-bottom:20px;"/>
    """, unsafe_allow_html=True)

    if not uid:
        st.info("👈 Search for a protein in the sidebar first.")
        return

    st.markdown(f"""
    <p style="
        font-family:'Space Grotesk',sans-serif;
        font-size:12px; color:rgba(197,197,213,0.5);
        margin-bottom:16px;
    ">Target: <span style="color:#b9c3ff; font-weight:600;">
        {info.get('gene','N/A')}</span>
    &nbsp;·&nbsp; UniProt: <span style="
        font-family:'Space Grotesk',monospace;
        color:rgba(197,197,213,0.4);">{uid}</span></p>
    """, unsafe_allow_html=True)

    with st.spinner("🔬 Scanning ChEMBL database..."):
        drugs, err = get_chembl_drugs(uid, limit=25)

    if err and not drugs:
        st.markdown(f"""
        <div style="
            background:rgba(246,79,89,0.08);
            border:1px solid rgba(246,79,89,0.2);
            border-radius:8px; padding:20px;
        ">
            <p style="color:#ffb3b2; margin:0;">⚠️ {err}</p>
        </div>
        """, unsafe_allow_html=True)
        return

    if not drugs:
        st.info("No drug data found in ChEMBL for this protein.")
        return

    df = pd.DataFrame(drugs)

    # ── Summary Metrics ─────────────────────────────────────────
    approved = df[df["Phase Number"] == 4]
    phase3   = df[df["Phase Number"] == 3]
    phase12  = df[df["Phase Number"].isin([1, 2])]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Drugs",    len(df))
    col2.metric("✅ Approved",    len(approved))
    col3.metric("🔬 Phase III",   len(phase3))
    col4.metric("🧪 Phase I/II",  len(phase12))

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Drug Cards ───────────────────────────────────────────────
    st.markdown("**Drug Phase Cards**")

    # Show top 6 drugs as native Streamlit cards
    top_drugs = drugs[:6]
    for i in range(0, len(top_drugs), 3):
        row = top_drugs[i:i+3]
        cols = st.columns(len(row))
        for col, drug in zip(cols, row):
            with col:
                phase_num = drug.get("Phase Number", -1)
                label     = PHASE_STYLES.get(phase_num, PHASE_STYLES[-1])["label"]
                chembl_id = drug.get("ChEMBL ID", "N/A")
                raw_name  = drug.get("Drug Name") or chembl_id
                name      = str(raw_name)[:22]
                raw_ind   = drug.get("Indication", "N/A")
                ind       = str(raw_ind)[:55] if raw_ind and raw_ind != "N/A" else "Indication data not available"
                phase_display = str(phase_num) if phase_num >= 0 else "N/A"
                if phase_num == 4:
                    status = "✅ Approved"
                elif phase_num >= 1:
                    status = "🔬 Ongoing"
                else:
                    status = "💡 Preclinical"

                with st.container(border=True):
                    st.markdown(f"**{label}** &nbsp; `{chembl_id[:12]}`", unsafe_allow_html=True)
                    st.markdown(f"**{name}**")
                    st.caption(ind)
                    c1, c2 = st.columns(2)
                    c1.metric("Phase", phase_display)
                    c2.metric("Status", status)

    st.divider()

    # ── Pipeline Chart ───────────────────────────────────────────
    st.markdown("""
    <p style="
        font-family:'Space Grotesk',sans-serif;
        font-size:9px; letter-spacing:0.2em;
        color:rgba(197,197,213,0.4);
        text-transform:uppercase;
        margin:0 0 12px 0;
    ">Binding Affinity · Phase Distribution</p>
    """, unsafe_allow_html=True)

    phase_counts = (
        df.groupby("Phase").size()
          .reset_index(name="Count")
    )
    fig = px.bar(
        phase_counts, x="Phase", y="Count",
        color="Phase",
        color_discrete_sequence=[
            "#00dce6","#b9c3ff","#667eea","#ffb3b2","#888","#f64f59"
        ],
        title=None
    )
    fig.update_layout(
        showlegend=False,
        height=280,
        paper_bgcolor="rgba(10,12,26,0)",
        plot_bgcolor="rgba(10,12,26,0.4)",
        font=dict(family="Space Grotesk", color="#e1e1f6", size=11),
        xaxis=dict(
            gridcolor="rgba(255,255,255,0.05)",
            title=None
        ),
        yaxis=dict(
            gridcolor="rgba(255,255,255,0.05)",
            title="Count"
        ),
        margin=dict(l=40, r=20, t=10, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Full Table ───────────────────────────────────────────────
    st.markdown("""
    <p style="
        font-family:'Space Grotesk',sans-serif;
        font-size:9px; letter-spacing:0.2em;
        color:rgba(197,197,213,0.4);
        text-transform:uppercase;
        margin:8px 0 12px 0;
    ">Complete Drug List</p>
    """, unsafe_allow_html=True)

    display = df[["Drug Name","ChEMBL ID","Phase","Indication"]].copy()
    st.dataframe(display, use_container_width=True, hide_index=True)

    csv = display.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Export Dataset · CSV",
        data=csv,
        file_name=f"drugs_{uid}.csv",
        mime="text/csv",
        use_container_width=True
    )
    st.markdown("""
    <p style="
        font-family:'Space Grotesk',monospace;
        font-size:9px; letter-spacing:0.1em;
        color:rgba(197,197,213,0.3);
        margin-top:8px;
    ">Data source: ChEMBL — European Bioinformatics Institute
    · Phase 4 = Approved · Phase 0 = Preclinical</p>
    """, unsafe_allow_html=True)