# AlphaExplorer - Home Page with Central Search Bar

import streamlit as st


def show():
    uid  = st.session_state.get("uniprot_id")
    info = st.session_state.get("protein_info", {})

    # ── Hero Header ──────────────────────────────────────────────
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

    # ── Stats Row ─────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🏆 Nobel Prize",  "2024",  "Chemistry")
    col2.metric("🧬 Proteins",     "200M+", "AlphaFold DB")
    col3.metric("🗄️ Databases",    "5",     "Integrated")
    col4.metric("💊 Drug Records", "2M+",   "ChEMBL")

    st.markdown("---")

    # ── Central Search Bar ────────────────────────────────────────
    st.markdown("""
<div style='text-align:center; margin:8px 0 24px 0;'>
    <h2 style='font-size:26px; font-weight:700;
               color:#1A1A2E; margin:0 0 6px 0;'>
        🔍 Search Any Protein
    </h2>
    <p style='font-size:14px; color:#6B7280; margin:0 0 20px 0;'>
        Enter a gene name, protein name, or UniProt ID
    </p>
</div>
""", unsafe_allow_html=True)

    # Central search input — uses same session state as sidebar
    _, col_search, _ = st.columns([1, 3, 1])
    with col_search:
        st.markdown("""
<style>
/* Style only the central search box */
div[data-testid="stHorizontalBlock"] .stTextInput input {
    background: white !important;
    border: 2px solid #6C63FF !important;
    border-radius: 50px !important;
    padding: 12px 24px !important;
    font-size: 16px !important;
    color: #1A1A2E !important;
    box-shadow: 0 4px 20px rgba(108,99,255,0.15) !important;
}
div[data-testid="stHorizontalBlock"] .stTextInput input:focus {
    box-shadow: 0 4px 24px rgba(108,99,255,0.3) !important;
    border-color: #3B82F6 !important;
}
div[data-testid="stHorizontalBlock"] .stTextInput input::placeholder {
    color: #9CA3AF !important;
}
</style>
""", unsafe_allow_html=True)

        central_query = st.text_input(
            "Central Search",
            placeholder="🔬 e.g. ACE2, BRCA1, TP53, ACHE, insulin...",
            label_visibility="collapsed",
            key="central_search_input"
        )

        if st.button(
            "🔍  Search Protein",
            use_container_width=True,
            key="central_search_btn"
        ):
            if central_query.strip():
                from utils.api_utils import (
                    search_uniprot,
                    get_uniprot_details,
                    extract_protein_info
                )
                with st.spinner("Searching UniProt database..."):
                    results, err = search_uniprot(
                        central_query.strip(), limit=8
                    )

                if err:
                    st.error(f"Search error: {err}")
                elif not results:
                    st.warning(
                        "No proteins found. Try a different name."
                    )
                else:
                    options = []
                    for r in results:
                        try:
                            name = (
                                r["proteinDescription"]
                                 ["recommendedName"]
                                 ["fullName"]["value"]
                            )
                        except Exception:
                            try:
                                name = (
                                    r["proteinDescription"]
                                     ["submittedNames"][0]
                                     ["fullName"]["value"]
                                )
                            except Exception:
                                name = "Unknown"
                        acc = r.get("primaryAccession", "N/A")
                        try:
                            org = r["organism"]["scientificName"]
                        except Exception:
                            org = "Unknown"
                        options.append(
                            f"{name[:28]} | {acc} | {org[:18]}"
                        )
                    st.session_state.search_results = results
                    st.session_state.search_options  = options
                    st.session_state.search_done     = True
                    st.rerun()

    # Show protein selector after central search
    if (st.session_state.search_done and
            not st.session_state.uniprot_id):
        _, col_sel, _ = st.columns([1, 3, 1])
        with col_sel:
            options = st.session_state.search_options
            results = st.session_state.search_results

            if options:
                selected = st.selectbox(
                    "Select protein from results:",
                    options,
                    key="central_protein_selector"
                )
                idx       = options.index(selected)
                chosen_id = results[idx]["primaryAccession"]

                if st.button(
                    "✅  Load This Protein",
                    use_container_width=True,
                    key="central_load_btn"
                ):
                    from utils.api_utils import (
                        get_uniprot_details, extract_protein_info
                    )
                    with st.spinner("Loading protein data..."):
                        data, err = get_uniprot_details(chosen_id)
                        if data:
                            info_new = extract_protein_info(data)
                            st.session_state.uniprot_id   = chosen_id
                            st.session_state.protein_info = info_new
                            st.session_state.uniprot_raw  = data
                            st.session_state.protein_name = info_new.get(
                                "name", chosen_id
                            )
                            st.rerun()

    # ── Quick Example Chips ───────────────────────────────────────
    if not uid:
        st.markdown("""
<div style='text-align:center; margin:16px 0 8px 0;'>
    <p style='font-size:12px; color:#9CA3AF;
              font-weight:600; letter-spacing:1px;'>
        TRY THESE EXAMPLES
    </p>
</div>
""", unsafe_allow_html=True)

        _, chip_col, _ = st.columns([1, 4, 1])
        with chip_col:
            chips = st.columns(6)
            examples = ["ACE2","BRCA1","TP53","ACHE","INS","HBB"]
            descs    = [
                "COVID-19","Breast Cancer",
                "Tumour Suppressor","Alzheimer's",
                "Insulin","Haemoglobin"
            ]
            for i, (chip, (gene, desc)) in enumerate(
                zip(chips, zip(examples, descs))
            ):
                with chip:
                    st.markdown(f"""
<div style='background:white;
            border:2px solid #6C63FF20;
            border-radius:8px;
            padding:8px 6px;
            text-align:center;
            box-shadow:0 2px 8px rgba(0,0,0,0.05);'>
    <p style='font-size:13px; font-weight:700;
              color:#6C63FF; margin:0;'>
        {gene}
    </p>
    <p style='font-size:9px; color:#9CA3AF;
              margin:2px 0 0 0;'>
        {desc}
    </p>
</div>
""", unsafe_allow_html=True)

    st.markdown("---")

    # ── Active Protein Card ───────────────────────────────────────
    if uid:
        protein_name = info.get('name', 'Unknown')[:55]
        organism     = info.get('organism', 'Unknown')
        gene         = info.get('gene', 'N/A')
        length       = info.get('length', 'N/A')
        num_diseases = len(info.get('diseases', []))
        location     = info.get('location', 'Unknown')[:30]

        st.markdown(f"""
<div style='background:linear-gradient(135deg,#6C63FF15,#3B82F615);
            border:2px solid #6C63FF30;
            border-radius:16px; padding:28px;
            margin-bottom:24px;'>
    <div style='display:flex;
                justify-content:space-between;
                align-items:flex-start; flex-wrap:wrap;
                gap:16px;'>
        <div>
            <span style='background:#6C63FF; color:white;
                         font-size:11px; font-weight:700;
                         padding:4px 14px;
                         border-radius:20px;
                         letter-spacing:1px;'>
                ✅ PROTEIN LOADED
            </span>
            <h2 style='font-size:24px; font-weight:800;
                       color:#1A1A2E;
                       margin:12px 0 4px 0;'>
                {protein_name}
            </h2>
            <p style='font-size:14px; color:#6B7280;
                      margin:0; font-style:italic;'>
                {organism}
            </p>
        </div>
        <div style='text-align:right;'>
            <p style='font-size:11px; color:#9CA3AF; margin:0;'>
                UniProt ID
            </p>
            <p style='font-size:20px; font-weight:700;
                      color:#6C63FF; margin:4px 0 0 0;
                      font-family:monospace;'>
                {uid}
            </p>
        </div>
    </div>
    <div style='display:flex; gap:40px;
                flex-wrap:wrap; margin-top:20px;'>
        <div>
            <p style='font-size:10px; color:#9CA3AF;
                      margin:0; font-weight:700;
                      text-transform:uppercase;
                      letter-spacing:1px;'>Gene</p>
            <p style='font-size:24px; font-weight:700;
                      color:#1A1A2E; margin:4px 0 0 0;'>
                {gene}
            </p>
        </div>
        <div>
            <p style='font-size:10px; color:#9CA3AF;
                      margin:0; font-weight:700;
                      text-transform:uppercase;
                      letter-spacing:1px;'>Length</p>
            <p style='font-size:24px; font-weight:700;
                      color:#3B82F6; margin:4px 0 0 0;'>
                {length} aa
            </p>
        </div>
        <div>
            <p style='font-size:10px; color:#9CA3AF;
                      margin:0; font-weight:700;
                      text-transform:uppercase;
                      letter-spacing:1px;'>Diseases</p>
            <p style='font-size:24px; font-weight:700;
                      color:#EF4444; margin:4px 0 0 0;'>
                {num_diseases}
            </p>
        </div>
        <div>
            <p style='font-size:10px; color:#9CA3AF;
                      margin:0; font-weight:700;
                      text-transform:uppercase;
                      letter-spacing:1px;'>Location</p>
            <p style='font-size:14px; font-weight:600;
                      color:#06B6D4; margin:8px 0 0 0;'>
                {location}
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
            st.info("Function data not available for this protein.")

        # Disease associations
        diseases = info.get("diseases", [])
        if diseases:
            st.markdown("### 🦠 Disease Associations")
            c1, c2, c3 = st.columns(3)
            colors  = ["#EF444415","#F59E0B15","#8B5CF615"]
            borders = ["#EF4444","#F59E0B","#8B5CF6"]
            for i, disease in enumerate(diseases[:6]):
                with [c1, c2, c3][i % 3]:
                    st.markdown(f"""
<div style='background:{colors[i%3]};
            border-left:3px solid {borders[i%3]};
            border-radius:8px;
            padding:10px 14px;
            margin-bottom:8px;'>
    <p style='font-size:12px; font-weight:600;
              color:#1A1A2E; margin:0;'>
        {disease[:55]}
    </p>
</div>
""", unsafe_allow_html=True)

        # Quick navigation
        st.markdown("---")
        st.markdown("### 🚀 Explore This Protein")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown("""
<div style='background:white; border-radius:12px;
            padding:20px; text-align:center;
            box-shadow:0 2px 12px rgba(108,99,255,0.1);
            border-top:3px solid #6C63FF;'>
    <div style='font-size:28px;'>🏗️</div>
    <p style='font-weight:700; color:#1A1A2E;
              margin:8px 0 4px 0;'>Structure</p>
    <p style='font-size:11px; color:#9CA3AF; margin:0;'>
        3D AlphaFold Viewer</p>
</div>
""", unsafe_allow_html=True)
        with c2:
            st.markdown("""
<div style='background:white; border-radius:12px;
            padding:20px; text-align:center;
            box-shadow:0 2px 12px rgba(59,130,246,0.1);
            border-top:3px solid #3B82F6;'>
    <div style='font-size:28px;'>⚙️</div>
    <p style='font-weight:700; color:#1A1A2E;
              margin:8px 0 4px 0;'>Function</p>
    <p style='font-size:11px; color:#9CA3AF; margin:0;'>
        GO Terms · Disease Links</p>
</div>
""", unsafe_allow_html=True)
        with c3:
            st.markdown("""
<div style='background:white; border-radius:12px;
            padding:20px; text-align:center;
            box-shadow:0 2px 12px rgba(6,182,212,0.1);
            border-top:3px solid #06B6D4;'>
    <div style='font-size:28px;'>💊</div>
    <p style='font-weight:700; color:#1A1A2E;
              margin:8px 0 4px 0;'>Drugs</p>
    <p style='font-size:11px; color:#9CA3AF; margin:0;'>
        Clinical Pipeline</p>
</div>
""", unsafe_allow_html=True)
        with c4:
            st.markdown("""
<div style='background:white; border-radius:12px;
            padding:20px; text-align:center;
            box-shadow:0 2px 12px rgba(139,92,246,0.1);
            border-top:3px solid #8B5CF6;'>
    <div style='font-size:28px;'>🔗</div>
    <p style='font-weight:700; color:#1A1A2E;
              margin:8px 0 4px 0;'>Similar</p>
    <p style='font-size:11px; color:#9CA3AF; margin:0;'>
        Related Proteins</p>
</div>
""", unsafe_allow_html=True)

        st.markdown("""
<p style='font-size:12px; color:#9CA3AF;
          text-align:center; margin-top:12px;'>
    👈 Use the sidebar navigation to switch between pages
</p>
""", unsafe_allow_html=True)

    else:
        # Feature overview when no protein loaded
        st.markdown("### 🎯 What AlphaExplorer Can Do")
        features = [
            ("🏗️", "Structure Viewer",
             "View AlphaFold 3D predicted structure with pLDDT confidence coloring. Download PDB and CIF files.",
             "#6C63FF"),
            ("⚙️", "Function & Disease",
             "Explore biological function, GO terms, disease links, and subcellular location from UniProt.",
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
            box-shadow:0 2px 12px rgba(0,0,0,0.05);
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

    # ── Footer ────────────────────────────────────────────────────
    st.markdown("---")
    st.caption(
        "Data: AlphaFold DB · UniProt · ChEMBL · PDB | "
        "Built by Talha Saleem · UAF · 2026"
    )