# AlphaExplorer - Explorer Home (Cinematic Bento Grid)

import streamlit as st

def show():
    uid  = st.session_state.get("uniprot_id")
    info = st.session_state.get("protein_info", {})

    # ── Hero Header ───────────────────────────────────────────
    st.markdown("""
    <div style="padding: 40px 0 20px 0; text-align:left;">
        <h1 style="
            font-family:'Space Grotesk',sans-serif;
            font-size:48px;
            font-weight:600;
            letter-spacing:-0.02em;
            color:#ffffff;
            margin:0;
            line-height:1.1;
        ">Unlocking the
        <span style="
            background:linear-gradient(90deg,#667eea,#f64f59);
            -webkit-background-clip:text;
            -webkit-text-fill-color:transparent;
        "> Proteome</span></h1>
        <p style="
            font-family:'Inter',sans-serif;
            font-size:16px;
            color:rgba(197,197,213,0.6);
            margin:12px 0 0 0;
            max-width:600px;
        ">Real-time structural analysis and drug discovery powered
        by hyper-precision genomic intelligence.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── System Status Bar ─────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🏆 Nobel Prize",  "2024",   "Chemistry")
    col2.metric("🧬 Proteins",     "200M+",  "Predicted")
    col3.metric("🗄️ Databases",    "5",      "Integrated")
    col4.metric("💊 Drug Records", "2M+",    "ChEMBL")

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Active Sequence Panel ─────────────────────────────────
    if uid:
        st.markdown(f"""
        <div style="
            background:rgba(10,12,26,0.8);
            border:1px solid rgba(102,126,234,0.25);
            border-radius:12px;
            padding:28px;
            margin-bottom:24px;
            position:relative;
            overflow:hidden;
        ">
            <div style="
                position:absolute; top:16px; right:16px;
                font-family:'Space Grotesk',monospace;
                font-size:9px; letter-spacing:0.2em;
                color:rgba(102,126,234,0.3);
            ">COORD: {uid[:8]}-N</div>

            <span style="
                font-family:'Space Grotesk',sans-serif;
                font-size:9px; letter-spacing:0.2em;
                color:rgba(246,79,89,0.8);
                text-transform:uppercase;
            ">Nobel Prize Foundation · Active Sequence</span>

            <h2 style="
                font-family:'Space Grotesk',sans-serif;
                font-size:24px; font-weight:500;
                color:#ffffff; margin:8px 0 4px 0;
            ">{info.get('name', 'Unknown Protein')[:60]}</h2>

            <p style="
                font-size:13px;
                color:rgba(197,197,213,0.6);
                margin:0 0 20px 0;
                max-width:500px;
            ">{info.get('function','No function data available.')[:200]}</p>

            <div style="display:flex; gap:32px;">
                <div>
                    <p style="font-size:9px; text-transform:uppercase;
                              color:rgba(197,197,213,0.4);
                              letter-spacing:0.1em; margin:0;">Gene</p>
                    <p style="font-family:'Space Grotesk',monospace;
                              font-size:22px; color:#ffffff;
                              margin:4px 0 0 0;">{info.get('gene','N/A')}</p>
                </div>
                <div>
                    <p style="font-size:9px; text-transform:uppercase;
                              color:rgba(197,197,213,0.4);
                              letter-spacing:0.1em; margin:0;">Length</p>
                    <p style="font-family:'Space Grotesk',monospace;
                              font-size:22px; color:#00dce6;
                              margin:4px 0 0 0;">{info.get('length','N/A')} aa</p>
                </div>
                <div>
                    <p style="font-size:9px; text-transform:uppercase;
                              color:rgba(197,197,213,0.4);
                              letter-spacing:0.1em; margin:0;">Organism</p>
                    <p style="font-family:'Space Grotesk',sans-serif;
                              font-size:14px; color:#b9c3ff;
                              margin:4px 0 0 0;
                              font-style:italic;">{info.get('organism','Unknown')[:30]}</p>
                </div>
                <div>
                    <p style="font-size:9px; text-transform:uppercase;
                              color:rgba(197,197,213,0.4);
                              letter-spacing:0.1em; margin:0;">Diseases</p>
                    <p style="font-family:'Space Grotesk',monospace;
                              font-size:22px; color:#ffb3b2;
                              margin:4px 0 0 0;">{len(info.get('diseases',[]))}</p>
                </div>
            </div>

            <!-- Stability badge -->
            <div style="
                position:absolute; bottom:16px; right:16px;
                display:flex; gap:8px;
            ">
                <span style="
                    background:rgba(102,126,234,0.15);
                    border-left:2px solid #667eea;
                    padding:4px 10px;
                    font-size:9px; font-weight:700;
                    color:#b9c3ff;
                    font-family:'Space Grotesk',sans-serif;
                    letter-spacing:0.1em;
                ">LOADED</span>
                <span style="
                    background:rgba(0,220,230,0.1);
                    border-left:2px solid #00dce6;
                    padding:4px 10px;
                    font-size:9px; font-weight:700;
                    color:#00dce6;
                    font-family:'Space Grotesk',sans-serif;
                    letter-spacing:0.1em;
                ">LIVE</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Disease Discovery Feed ─────────────────────────────
        diseases = info.get("diseases", [])
        if diseases:
            st.markdown("""
            <p style="
                font-family:'Space Grotesk',sans-serif;
                font-size:9px; letter-spacing:0.2em;
                color:rgba(197,197,213,0.4);
                text-transform:uppercase;
                margin:0 0 12px 0;
            ">Disease Associations</p>
            """, unsafe_allow_html=True)

            cols = st.columns(min(3, len(diseases)))
            tags = ["STABILITY_LOW", "TOXICITY_ALERT", "TARGET_FOUND"]
            colors = ["#667eea", "#f64f59", "#00dce6"]

            for i, disease in enumerate(diseases[:3]):
                with cols[i]:
                    tag   = tags[i % 3]
                    color = colors[i % 3]
                    st.markdown(f"""
                    <div style="
                        background:rgba(10,12,26,0.8);
                        border:1px solid rgba(255,255,255,0.08);
                        border-radius:8px;
                        padding:16px;
                        cursor:pointer;
                        transition:border-color 0.3s ease;
                    ">
                        <div style="display:flex;
                                    justify-content:space-between;
                                    margin-bottom:12px;">
                            <span style="
                                background:rgba(255,255,255,0.03);
                                border-left:2px solid {color};
                                padding:3px 8px;
                                font-size:9px; font-weight:700;
                                color:{color};
                                font-family:'Space Grotesk',sans-serif;
                                letter-spacing:0.1em;
                            ">{tag}</span>
                            <span style="
                                font-family:'Space Grotesk',sans-serif;
                                font-size:9px;
                                letter-spacing:0.15em;
                                color:rgba(185,195,255,0.3);
                            ">MOD_{str(i+1).zfill(2)}</span>
                        </div>
                        <p style="
                            font-size:12px;
                            color:rgba(225,225,246,0.8);
                            margin:0;
                            line-height:1.5;
                        ">{disease[:80]}</p>
                    </div>
                    """, unsafe_allow_html=True)

        # ── Live Sequence Stream ───────────────────────────────
        st.markdown("<br/>", unsafe_allow_html=True)
        st.markdown("""
        <div style="
            background:rgba(10,12,26,0.6);
            border:1px solid rgba(255,255,255,0.07);
            border-radius:8px;
            padding:16px;
        ">
            <div style="display:flex; justify-content:space-between;
                        align-items:center; margin-bottom:10px;">
                <span style="
                    font-family:'Space Grotesk',sans-serif;
                    font-size:9px; letter-spacing:0.2em;
                    color:rgba(197,197,213,0.4);
                    text-transform:uppercase;
                ">Live Sequence Stream</span>
                <div style="display:flex; gap:16px; align-items:center;">
                    <div style="display:flex; align-items:center; gap:4px;">
                        <div style="width:6px; height:6px; border-radius:50%;
                                    background:#667eea;
                                    box-shadow:0 0 8px #667eea;"></div>
                        <span style="font-size:9px; color:rgba(197,197,213,0.5);
                                     font-family:'Space Grotesk',monospace;">
                            HYDROPHOBIC</span>
                    </div>
                    <div style="display:flex; align-items:center; gap:4px;">
                        <div style="width:6px; height:6px; border-radius:50%;
                                    background:#f64f59;
                                    box-shadow:0 0 8px #f64f59;"></div>
                        <span style="font-size:9px; color:rgba(197,197,213,0.5);
                                     font-family:'Space Grotesk',monospace;">
                            POLAR</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Render actual amino acid sequence if available
        try:
            seq = st.session_state.uniprot_raw.get(
                "sequence", {}
            ).get("value", "MARTKQTARKSTGGKAPRKQLATKAARKSAPATGGVKKPHRYRPGTVALREIRRYQKSTELLIRKLPFQRLVREIAQDFKTDLRFQSSAVMALQEACEAYLVGLFEDTNLCAIHAKRVTIMPKDIQLARRIRGERA")[:80]

            aa_colors = {
                'A':'#667eea','R':'#f64f59','N':'#00dce6',
                'D':'#f64f59','C':'#00dce6','Q':'#667eea',
                'E':'#f64f59','G':'#b9c3ff','H':'#00dce6',
                'I':'#667eea','L':'#667eea','K':'#f64f59',
                'M':'#00dce6','F':'#b9c3ff','P':'#667eea',
                'S':'#f64f59','T':'#f64f59','W':'#b9c3ff',
                'Y':'#00dce6','V':'#667eea'
            }
            seq_html = "<div style='background:rgba(0,0,0,0.4); border-radius:4px; padding:12px; font-family:Space Grotesk,monospace; font-size:12px; letter-spacing:0.08em; display:flex; flex-wrap:wrap; gap:2px;'>"
            for aa in seq:
                c = aa_colors.get(aa, '#888')
                seq_html += f"<span style='color:{c};'>{aa}</span>"
            seq_html += "</div>"
            st.markdown(seq_html + "</div>", unsafe_allow_html=True)
        except:
            st.markdown("</div>", unsafe_allow_html=True)

    else:
        # ── Landing State ──────────────────────────────────────
        st.markdown("""
        <div style="
            background:rgba(102,126,234,0.05);
            border:1px solid rgba(102,126,234,0.15);
            border-radius:12px;
            padding:48px;
            text-align:center;
            margin:32px 0;
        ">
            <div style="font-size:48px; margin-bottom:16px;">🧬</div>
            <h2 style="
                font-family:'Space Grotesk',sans-serif;
                font-size:24px; font-weight:500;
                color:#b9c3ff; margin:0 0 12px 0;
            ">Query a Protein Sequence</h2>
            <p style="color:rgba(197,197,213,0.5); font-size:14px; margin:0;">
                Use the sidebar search to load a protein and explore
                its structure, function, and clinical data.</p>
            <div style="margin-top:24px; display:flex;
                        justify-content:center; gap:16px; flex-wrap:wrap;">
        """, unsafe_allow_html=True)

        for ex in ["ACE2 — COVID-19 Receptor",
                   "BRCA1 — Breast Cancer Gene",
                   "TP53 — Tumour Suppressor",
                   "ACHE — Alzheimer's Target"]:
            st.markdown(f"""
            <span style="
                background:rgba(102,126,234,0.1);
                border:1px solid rgba(102,126,234,0.3);
                border-radius:4px;
                padding:6px 14px;
                font-family:'Space Grotesk',monospace;
                font-size:11px;
                color:#b9c3ff;
                letter-spacing:0.05em;
            ">{ex}</span>
            """, unsafe_allow_html=True)

        st.markdown("</div></div>", unsafe_allow_html=True)

        # Feature cards
        st.markdown("<br/>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        features = [
            ("🏗️", "Structure Viewer",
             "3D AlphaFold structure with confidence coloring using Molstar renderer",
             "#667eea"),
            ("⚙️", "Function & Disease",
             "GO Terms, subcellular location and disease associations from UniProt",
             "#00dce6"),
            ("💊", "Drug Intelligence",
             "Clinical phase data and drug pipeline from ChEMBL database",
             "#f64f59"),
        ]
        for col, (icon, title, desc, color) in zip([c1,c2,c3], features):
            with col:
                st.markdown(f"""
                <div style="
                    background:rgba(10,12,26,0.8);
                    border:1px solid rgba(255,255,255,0.07);
                    border-radius:8px; padding:24px;
                    border-top:2px solid {color};
                ">
                    <div style="font-size:28px; margin-bottom:12px;">{icon}</div>
                    <h4 style="
                        font-family:'Space Grotesk',sans-serif;
                        font-size:15px; color:#ffffff;
                        margin:0 0 8px 0;
                    ">{title}</h4>
                    <p style="
                        font-size:12px;
                        color:rgba(197,197,213,0.55);
                        margin:0; line-height:1.6;
                    ">{desc}</p>
                </div>
                """, unsafe_allow_html=True)