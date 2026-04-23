# AlphaExplorer - Home Page

import streamlit as st

def show():
    uid  = st.session_state.get("uniprot_id")
    info = st.session_state.get("protein_info", {})

    # ── Hero ────────────────────────────────────────────────────
    st.markdown("""
    <div style='padding:10px 0 24px 0;'>
        <h1 style='font-size:42px; font-weight:800;
                   color:#1A1A2E; margin:0; line-height:1.2;'>
            🧬 AlphaExplorer
        </h1>
        <p style='font-size:18px; color:#6B7280;
                  margin:8px 0 0 0; font-weight:400;'>
            Protein Structure Intelligence Dashboard
            &nbsp;·&nbsp;
            <span style='color:#6C63FF; font-weight:600;'>
                Powered by AlphaFold Nobel Prize 2024
            </span>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Stats Row ────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🏆 Nobel Prize",  "2024",   "Chemistry")
    col2.metric("🧬 Proteins",     "200M+",  "AlphaFold DB")
    col3.metric("🗄️ Databases",    "5",      "Integrated")
    col4.metric("💊 Drug Records", "2M+",    "ChEMBL")

    st.markdown("---")

    # ── Active Protein Card ──────────────────────────────────────
    if uid:
        st.markdown(f"""
        <div style='background:linear-gradient(135deg,#6C63FF15,#3B82F615);
                    border:2px solid #6C63FF30;
                    border-radius:16px; padding:28px;
                    margin-bottom:24px;'>
            <div style='display:flex;
                        justify-content:space-between;
                        align-items:flex-start;'>
                <div>
                    <span style='background:#6C63FF;
                                 color:white;
                                 font-size:11px; font-weight:700;
                                 padding:4px 12px;
                                 border-radius:20px;
                                 letter-spacing:1px;'>
                        ✅ PROTEIN LOADED
                    </span>
                    <h2 style='font-size:26px; font-weight:800;
                               color:#1A1A2E; margin:12px 0 4px 0;'>
                        {info.get('name','Unknown Protein')[:55]}
                    </h2>
                    <p style='font-size:15px; color:#6B7280;
                              margin:0 0 16px 0;
                              font-style:italic;'>
                        {info.get('organism','Unknown organism')}
                    </p>
                </div>
                <div style='text-align:right;'>
                    <p style='font-size:11px; color:#9CA3AF;
                              margin:0;'>UniProt ID</p>
                    <p style='font-size:20px; font-weight:700;
                              color:#6C63FF; margin:4px 0 0 0;
                              font-family:monospace;'>
                        {uid}
                    </p>
                </div>
            </div>
            <div style='display:flex; gap:32px; flex-wrap:wrap;'>
                <div>
                    <p style='font-size:11px; color:#9CA3AF;
                              margin:0; font-weight:600;
                              text-transform:uppercase;
                              letter-spacing:1px;'>Gene</p>
                    <p style='font-size:22px; font-weight:700;
                              color:#1A1A2E; margin:4px 0 0 0;'>
                        {info.get('gene','N/A')}
                    </p>
                </div>
                <div>
                    <p style='font-size:11px; color:#9CA3AF;
                              margin:0; font-weight:600;
                              text-transform:uppercase;
                              letter-spacing:1px;'>Length</p>
                    <p style='font-size:22px; font-weight:700;
                              color:#3B82F6; margin:4px 0 0 0;'>
                        {info.get('length','N/A')} aa
                    </p>
                </div>
                <div>
                    <p style='font-size:11px; color:#9CA3AF;
                              margin:0; font-weight:600;
                              text-transform:uppercase;
                              letter-spacing:1px;'>Diseases</p>
                    <p style='font-size:22px; font-weight:700;
                              color:#EF4444; margin:4px 0 0 0;'>
                        {len(info.get('diseases',[]))}
                    </p>
                </div>
                <div>
                    <p style='font-size:11px; color:#9CA3AF;
                              margin:0; font-weight:600;
                              text-transform:uppercase;
                              letter-spacing:1px;'>Location</p>
                    <p style='font-size:14px; font-weight:600;
                              color:#06B6D4; margin:8px 0 0 0;'>
                        {info.get('location','Unknown')[:25]}
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Biological Function
        st.markdown("### 🔬 Biological Function")
        func = info.get("function", "Not available")
        if func != "Not available":
            st.success(func[:400])
        else:
            st.info("Function information not available for this protein.")

        # Disease associations
        diseases = info.get("diseases", [])
        if diseases:
            st.markdown("### 🦠 Disease Associations")
            cols = st.columns(3)
            colors = ["#EF444415","#F59E0B15","#8B5CF615"]
            borders = ["#EF4444","#F59E0B","#8B5CF6"]
            for i, disease in enumerate(diseases[:6]):
                with cols[i % 3]:
                    st.markdown(f"""
                    <div style='background:{colors[i%3]};
                                border-left:3px solid {borders[i%3]};
                                border-radius:8px;
                                padding:10px 14px;
                                margin-bottom:8px;'>
                        <p style='font-size:12px; font-weight:600;
                                  color:#1A1A2E; margin:0;'>
                            {disease[:50]}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

        # Navigate buttons
        st.markdown("---")
        st.markdown("### 🚀 Explore This Protein")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            if st.button("🏗️ View Structure",
                         use_container_width=True):
                st.session_state["_nav"] = "structure"
        with c2:
            if st.button("⚙️ Function & Disease",
                         use_container_width=True):
                st.session_state["_nav"] = "function"
        with c3:
            if st.button("💊 Drug Intelligence",
                         use_container_width=True):
                st.session_state["_nav"] = "drugs"
        with c4:
            if st.button("🔗 Similar Proteins",
                         use_container_width=True):
                st.session_state["_nav"] = "similar"

    else:
        # ── Landing State ────────────────────────────────────────
        st.markdown("""
        <div style='background:linear-gradient(135deg,#6C63FF08,#3B82F608);
                    border:2px dashed #6C63FF30;
                    border-radius:16px; padding:48px;
                    text-align:center; margin:16px 0 32px 0;'>
            <div style='font-size:56px; margin-bottom:16px;'>🔬</div>
            <h2 style='font-size:24px; font-weight:700;
                       color:#1A1A2E; margin:0 0 12px 0;'>
                Search for a Protein to Begin
            </h2>
            <p style='font-size:15px; color:#6B7280;
                      margin:0 0 24px 0; max-width:480px;
                      margin-left:auto; margin-right:auto;'>
                Use the search box in the sidebar to find any protein.
                Try typing a gene name, protein name, or UniProt ID.
            </p>
            <div style='display:flex; flex-wrap:wrap;
                        gap:10px; justify-content:center;'>
        """, unsafe_allow_html=True)

        examples = [
            ("ACE2",  "COVID-19 Receptor"),
            ("BRCA1", "Breast Cancer Gene"),
            ("TP53",  "Tumour Suppressor"),
            ("ACHE",  "Alzheimer's Target"),
            ("INS",   "Insulin"),
            ("HBB",   "Haemoglobin Beta"),
        ]
        for gene, desc in examples:
            st.markdown(f"""
            <span style='background:white;
                         border:2px solid #6C63FF30;
                         border-radius:8px;
                         padding:8px 16px;
                         font-size:13px; font-weight:600;
                         color:#6C63FF;'>
                {gene}
                <span style='color:#9CA3AF;
                             font-weight:400;
                             font-size:11px;'>
                    — {desc}
                </span>
            </span>
            """, unsafe_allow_html=True)

        st.markdown("</div></div>", unsafe_allow_html=True)

        # Feature overview cards
        st.markdown("### 🎯 What AlphaExplorer Can Do")
        features = [
            ("🏗️", "Structure Viewer",
             "View AlphaFold 3D predicted structure with pLDDT confidence coloring. Download PDB and CIF files.",
             "#6C63FF"),
            ("⚙️", "Function & Disease",
             "Explore biological function, GO terms across 3 categories, disease links, and subcellular location.",
             "#3B82F6"),
            ("💊", "Drug Intelligence",
             "Find FDA-approved drugs and clinical candidates targeting your protein from ChEMBL database.",
             "#06B6D4"),
            ("🔗", "Similar Proteins",
             "Discover related proteins and gene families across species using UniProt search expansion.",
             "#8B5CF6"),
        ]
        c1, c2 = st.columns(2)
        for i, (icon, title, desc, color) in enumerate(features):
            with (c1 if i % 2 == 0 else c2):
                st.markdown(f"""
                <div style='background:white;
                            border-radius:12px;
                            padding:24px;
                            margin-bottom:16px;
                            box-shadow:0 2px 12px rgba(0,0,0,0.06);
                            border-top:3px solid {color};'>
                    <div style='font-size:32px;
                                margin-bottom:10px;'>{icon}</div>
                    <h4 style='font-size:16px; font-weight:700;
                               color:#1A1A2E; margin:0 0 8px 0;'>
                        {title}
                    </h4>
                    <p style='font-size:13px; color:#6B7280;
                              margin:0; line-height:1.6;'>
                        {desc}
                    </p>
                </div>
                """, unsafe_allow_html=True)

    # ── Footer ───────────────────────────────────────────────────
    st.markdown("---")
    st.caption(
        "Data: AlphaFold DB · UniProt · ChEMBL · PDB | "
        "Built by Talha Saleem · UAF · 2026"
    )