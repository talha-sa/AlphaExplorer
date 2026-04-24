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

    st.divider()

    st.markdown("#### 📊 Clinical Pipeline Overview")

    phase_counts = (
        df.groupby("Phase").size()
          .reset_index(name="Count")
    )

    # Colour map aligned to phase labels
    PHASE_COLORS = {
        "✅ Approved"    : "#00dce6",
        "🔬 Phase 3"    : "#b9c3ff",
        "🧪 Phase 2"    : "#667eea",
        "🔭 Phase 1"    : "#ffb3b2",
        "💡 Preclinical": "#888888",
        "❌ Discontinued": "#f64f59",
    }
    colors = [
        PHASE_COLORS.get(p, "#aaaaaa")
        for p in phase_counts["Phase"]
    ]

    chart_col1, chart_col2 = st.columns(2)

    # ── Donut: phase distribution ─────────────────────────────
    with chart_col1:
        st.markdown("**Phase Distribution**")
        donut = px.pie(
            phase_counts,
            names="Phase",
            values="Count",
            hole=0.55,
            color="Phase",
            color_discrete_map=PHASE_COLORS,
        )
        donut.update_traces(
            textinfo="percent+label",
            textfont_size=11,
            marker=dict(line=dict(color="#0a0c1a", width=2)),
        )
        donut.update_layout(
            showlegend=False,
            height=300,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e1e1f6", size=11),
        )
        st.plotly_chart(donut, use_container_width=True)

    # ── Horizontal bar: top indications ──────────────────────
    with chart_col2:
        st.markdown("**Top Indications**")
        ind_counts = (
            df[df["Indication"] != "N/A"]
            .groupby("Indication")
            .size()
            .reset_index(name="Count")
            .sort_values("Count", ascending=True)
            .tail(8)
        )
        if not ind_counts.empty:
            hbar = px.bar(
                ind_counts,
                x="Count",
                y="Indication",
                orientation="h",
                color="Count",
                color_continuous_scale=["#667eea", "#00dce6"],
            )
            hbar.update_layout(
                showlegend=False,
                coloraxis_showscale=False,
                height=300,
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(255,255,255,0.03)",
                font=dict(color="#e1e1f6", size=10),
                xaxis=dict(gridcolor="rgba(255,255,255,0.06)", title="Drug Count"),
                yaxis=dict(gridcolor="rgba(0,0,0,0)", title=None),
            )
            st.plotly_chart(hbar, use_container_width=True)
        else:
            st.info("No indication data available.")

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