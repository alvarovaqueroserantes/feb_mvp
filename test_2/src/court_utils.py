# court_utils.py
import plotly.graph_objects as go

def get_plotly_court() -> go.Figure:
    """
    Generate a Plotly figure with a simplified FIBA half-court (14x15m)
    without using sportypy to avoid compatibility issues.
    
    Returns:
        go.Figure: Plotly figure with court lines
    """
    fig = go.Figure()
    
    # Court outline (half court)
    fig.add_shape(
        type="rect",
        x0=0, y0=0, x1=14, y1=15,
        line=dict(color="#000000", width=2),
        fillcolor="#f0f0f0"
    )
    
    # Center circle
    fig.add_shape(
        type="circle",
        xref="x", yref="y",
        x0=5.8, y0=6.7, x1=8.2, y1=9.3,
        line=dict(color="#000000", width=2)
    )
    
    # Free throw line
    fig.add_shape(
        type="line",
        x0=4, y0=5.8, x1=10, y1=5.8,
        line=dict(color="#000000", width=2)
    )
    
    # Restricted area arc
    fig.add_shape(
        type="circle",
        xref="x", yref="y",
        x0=5.3, y0=5.3, x1=8.7, y1=8.7,
        line=dict(color="#000000", width=2)
    )
    
    # Three-point line (simplified)
    three_pt_line = [
        (0.9, 14), (1.5, 13.5), (2.5, 12.5), 
        (3.5, 11), (4, 9.5), (4, 5.8)
    ]
    fig.add_trace(go.Scatter(
        x=[x for x, y in three_pt_line],
        y=[y for x, y in three_pt_line],
        mode="lines",
        line=dict(color="#000000", width=2),
        hoverinfo="none",
        showlegend=False
    ))
    
    # Add mirrored three-point line
    mirrored_line = [(14-x, y) for x, y in three_pt_line]
    fig.add_trace(go.Scatter(
        x=[x for x, y in mirrored_line],
        y=[y for x, y in mirrored_line],
        mode="lines",
        line=dict(color="#000000", width=2),
        hoverinfo="none",
        showlegend=False
    ))
    
    # Layout configuration
    fig.update_layout(
        xaxis=dict(
            range=[0, 14],
            showgrid=False,
            zeroline=False,
            visible=False
        ),
        yaxis=dict(
            range=[0, 15],
            showgrid=False,
            zeroline=False,
            visible=False,
            scaleanchor="x",
            scaleratio=1
        ),
        plot_bgcolor="#f8f9fa",
        paper_bgcolor="#f8f9fa",
        width=800,
        height=700,
        margin=dict(l=20, r=20, t=60, b=20),
        title={
            "text": "FIBA Basketball Court",
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 20}
        }
    )
    
    return fig