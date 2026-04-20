# AlphaExplorer - Plot Utilities

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def plot_confidence_distribution(plddt_scores):
    if not plddt_scores:
        return None

    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=plddt_scores,
        nbinsx=50,
        marker_color=[
            "#0053D6" if s >= 90 else
            "#65CBF3" if s >= 70 else
            "#FFDB13" if s >= 50 else
            "#FF7D45"
            for s in plddt_scores
        ],
        name="pLDDT Score"
    ))

    fig.add_vline(x=90, line_dash="dash",
                  line_color="#0053D6",
                  annotation_text="Very High (90+)")
    fig.add_vline(x=70, line_dash="dash",
                  line_color="#65CBF3",
                  annotation_text="High (70-90)")
    fig.add_vline(x=50, line_dash="dash",
                  line_color="#FFDB13",
                  annotation_text="Low (50-70)")

    fig.update_layout(
        title="Confidence Score Distribution (pLDDT)",
        xaxis_title="pLDDT Score",
        yaxis_title="Number of Residues",
        height=400,
        template="plotly_white"
    )
    return fig

def plot_confidence_per_residue(plddt_scores):
    if not plddt_scores:
        return None

    colors = [
        "#0053D6" if s >= 90 else
        "#65CBF3" if s >= 70 else
        "#FFDB13" if s >= 50 else
        "#FF7D45"
        for s in plddt_scores
    ]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(range(1, len(plddt_scores) + 1)),
        y=plddt_scores,
        mode="lines",
        line=dict(width=1.5),
        marker=dict(color=colors),
        fill="tozeroy",
        fillcolor="rgba(100, 149, 237, 0.2)"
    ))

    fig.add_hrect(y0=90, y1=100,
                  fillcolor="#0053D6",
                  opacity=0.1,
                  annotation_text="Very High")
    fig.add_hrect(y0=70, y1=90,
                  fillcolor="#65CBF3",
                  opacity=0.1,
                  annotation_text="High")
    fig.add_hrect(y0=50, y1=70,
                  fillcolor="#FFDB13",
                  opacity=0.1,
                  annotation_text="Low")
    fig.add_hrect(y0=0, y1=50,
                  fillcolor="#FF7D45",
                  opacity=0.1,
                  annotation_text="Very Low")

    fig.update_layout(
        title="Per-Residue Confidence Score",
        xaxis_title="Residue Position",
        yaxis_title="pLDDT Score",
        height=400,
        template="plotly_white"
    )
    return fig

def plot_disease_bar(diseases):
    if not diseases:
        return None

    df = pd.DataFrame({"Disease": diseases,
                        "Count": [1] * len(diseases)})

    fig = px.bar(
        df, x="Disease", y="Count",
        color="Disease",
        color_discrete_sequence=px.colors.qualitative.Set3,
        title="Associated Diseases"
    )
    fig.update_layout(
        showlegend=False,
        height=350,
        template="plotly_white",
        xaxis_tickangle=-30
    )
    return fig