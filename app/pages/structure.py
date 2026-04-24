# AlphaExplorer - Molecule Viewer (Molstar + Cinematic UI)

import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))

from utils.api_utils import get_alphafold_structure, get_pdb_string

def show():
    uid  = st.session_state.get("uniprot_id")
    info = st.session_state.get("protein_info", {})

    # ── Page Header ────────────────────────────────────────────
    st.markdown("""
    <div style="display:flex; justify-content:space-between;
                align-items:flex-end; margin-bottom:8px;">
        <div>
            <p style="
                font-family:'Space Grotesk',sans-serif;
                font-size:10px; letter-spacing:0.25em;
                color:rgba(246,79,89,0.8);
                text-transform:uppercase; margin:0 0 4px 0;
            ">Molecule Viewer</p>
            <h1 style="
                font-family:'Space Grotesk',sans-serif;
                font-size:36px; font-weight:600;
                letter-spacing:-0.02em; color:#ffffff; margin:0;
            ">Structure Viewer</h1>
        </div>
        <div style="text-align:right;">
            <p style="font-size:9px; text-transform:uppercase;
                      letter-spacing:0.15em;
                      color:rgba(197,197,213,0.4); margin:0;">
                Render Mode</p>
            <p style="font-family:'Space Grotesk',monospace;
                      font-size:12px; color:#00dce6; margin:4px 0 0 0;">
                MOLSTAR · EEVEE_HYBRID</p>
        </div>
    </div>
    <hr style="border:1px solid rgba(255,255,255,0.07); margin-bottom:20px;"/>
    """, unsafe_allow_html=True)

    if not uid:
        st.markdown("""
        <div style="
            background:rgba(102,126,234,0.05);
            border:1px solid rgba(102,126,234,0.15);
            border-radius:12px;
            padding:60px; text-align:center;
        ">
            <div style="font-size:48px; margin-bottom:16px;">🏗️</div>
            <h3 style="
                font-family:'Space Grotesk',sans-serif;
                color:#b9c3ff; font-size:18px; margin:0 0 8px 0;
            ">No Sequence Loaded</h3>
            <p style="color:rgba(197,197,213,0.5); font-size:13px;">
                Search for a protein in the sidebar to view its 3D structure.
            </p>
        </div>
        """, unsafe_allow_html=True)
        return

    # ── Structural Specs Bar ────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Gene",     info.get("gene",     "N/A"))
    col2.metric("Organism", info.get("organism", "N/A")[:18])
    col3.metric("Length",   f"{info.get('length','N/A')} aa")
    col4.metric("Location", info.get("location", "N/A")[:18])

    st.markdown("<br/>", unsafe_allow_html=True)

    with st.spinner("🔬 Fetching AlphaFold structure..."):
        af_data, err = get_alphafold_structure(uid)

    if err or not af_data:
        st.markdown(f"""
        <div style="
            background:rgba(246,79,89,0.08);
            border:1px solid rgba(246,79,89,0.25);
            border-radius:8px; padding:20px; text-align:center;
        ">
            <p style="color:#ffb3b2; margin:0;">
                ⚠️ No AlphaFold structure available for <code>{uid}</code>.
                {err or ''}
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.link_button(
            "🔗 Search AlphaFold Manually",
            f"https://alphafold.ebi.ac.uk/entry/{uid}",
            use_container_width=True
        )
        return

    mean_plddt = af_data.get("meanPlddt", 0)
    pdb_url    = af_data.get("pdbUrl", "")

    # ── Confidence Indicator ────────────────────────────────────
    if mean_plddt >= 90:
        conf_color = "#00dce6"; conf_label = "VERY HIGH"
    elif mean_plddt >= 70:
        conf_color = "#667eea"; conf_label = "HIGH"
    elif mean_plddt >= 50:
        conf_color = "#ffdb13"; conf_label = "LOW"
    else:
        conf_color = "#f64f59"; conf_label = "VERY LOW"

    st.markdown(f"""
    <div style="
        background:rgba(10,12,26,0.8);
        border:1px solid rgba(255,255,255,0.08);
        border-radius:8px;
        padding:16px 24px;
        margin-bottom:16px;
        display:flex;
        align-items:center;
        gap:24px;
    ">
        <div>
            <p style="font-size:9px; text-transform:uppercase;
                      letter-spacing:0.15em;
                      color:rgba(197,197,213,0.4); margin:0;">
                pLDDT Confidence</p>
            <p style="font-family:'Space Grotesk',monospace;
                      font-size:28px; font-weight:600;
                      color:{conf_color}; margin:4px 0 0 0;">
                {mean_plddt:.1f}</p>
        </div>
        <div style="flex:1;">
            <div style="
                height:4px;
                background:rgba(255,255,255,0.08);
                border-radius:2px;
                overflow:hidden;
            ">
                <div style="
                    width:{mean_plddt}%;
                    height:100%;
                    background:linear-gradient(90deg,#667eea,{conf_color});
                    border-radius:2px;
                "></div>
            </div>
            <div style="display:flex; justify-content:space-between;
                        margin-top:6px;">
                <span style="font-size:9px;
                             color:rgba(197,197,213,0.3);">
                    0 (Very Low)</span>
                <span style="
                    font-family:'Space Grotesk',sans-serif;
                    font-size:9px; letter-spacing:0.1em;
                    font-weight:700;
                    color:{conf_color};
                ">INTEGRITY: {conf_label}</span>
                <span style="font-size:9px;
                             color:rgba(197,197,213,0.3);">
                    100 (Very High)</span>
            </div>
        </div>
        <div style="
            background:rgba(255,255,255,0.03);
            border:1px solid rgba(255,255,255,0.08);
            border-radius:6px;
            padding:8px 16px;
            text-align:center;
        ">
            <p style="font-size:9px; text-transform:uppercase;
                      letter-spacing:0.15em;
                      color:rgba(197,197,213,0.4); margin:0;">
                Version</p>
            <p style="font-family:'Space Grotesk',monospace;
                      font-size:14px; color:#b9c3ff; margin:4px 0 0 0;">
                v{af_data.get('latestVersion','N/A')}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── 3D Viewer ───────────────────────────────────────────────
    st.markdown("""
    <div style="
        background:rgba(10,12,26,0.8);
        border:1px solid rgba(102,126,234,0.2);
        border-radius:12px;
        padding:4px;
        margin-bottom:16px;
        box-shadow:inset 0 0 20px rgba(102,126,234,0.08),
                   0 0 30px rgba(102,126,234,0.05);
        position:relative;
    ">
        <div style="
            position:absolute; top:12px; left:12px; z-index:10;
            background:rgba(0,0,0,0.5);
            backdrop-filter:blur(10px);
            border:1px solid rgba(255,255,255,0.1);
            border-radius:4px;
            padding:6px 12px;
            font-family:'Space Grotesk',monospace;
            font-size:9px;
            letter-spacing:0.15em;
            color:rgba(197,197,213,0.6);
        ">
            RENDER: MOLSTAR · SAMPLING: EEVEE_HYBRID · ID: """ + uid + """
        </div>
    """, unsafe_allow_html=True)

    if pdb_url:
        try:
            from streamlit_molstar import st_molstar_remote
            st_molstar_remote(pdb_url, height="520px")
        except ImportError:
            # Fallback to py3Dmol
            try:
                pdb_string, perr = get_pdb_string(pdb_url)
                if pdb_string:
                    import py3Dmol
                    import streamlit.components.v1 as components
                    view = py3Dmol.view(width=750, height=500)
                    view.addModel(pdb_string, "pdb")
                    view.setStyle({}, {"cartoon": {
                        "colorscheme": {
                            "prop": "b",
                            "gradient": "roygb",
                            "min": 50, "max": 90
                        }
                    }})
                    view.zoomTo()
                    view.spin(True)
                    components.html(view._make_html(), height=520)
                else:
                    st.error(f"Could not load structure. {perr}")
            except Exception as e:
                st.warning(f"3D viewer unavailable: {e}")
                st.link_button(
                    "🔗 View on AlphaFold DB",
                    f"https://alphafold.ebi.ac.uk/entry/{uid}",
                    use_container_width=True
                )
        except Exception as e:
            st.warning(f"Molstar error: {e}")
    else:
        st.warning("No PDB URL available for this protein.")

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Downloads ────────────────────────────────────────────────
    st.markdown("""
    <p style="
        font-family:'Space Grotesk',sans-serif;
        font-size:9px; letter-spacing:0.2em;
        color:rgba(197,197,213,0.4);
        text-transform:uppercase; margin:0 0 10px 0;
    ">Export Dataset</p>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    if pdb_url:
        with c1:
            st.link_button("⬇️ PDB File",  pdb_url,
                           use_container_width=True)
    cif = af_data.get("cifUrl", "")
    if cif:
        with c2:
            st.link_button("⬇️ CIF File", cif,
                           use_container_width=True)
    with c3:
        st.link_button(
            "🔗 AlphaFold Entry",
            f"https://alphafold.ebi.ac.uk/entry/{uid}",
            use_container_width=True
        )