import plotly.graph_objects as go
import numpy as np

# Theme colors for consistent branding in charts
THEME_COLORS = {
    "primary": "#FF6B6B",      # Coral Red
    "secondary": "#4ECDC4",    # Turquoise
    "accent": "#45AAF2",       # Cobalt Blue
    "neutral": "#264653"       # Dark Slate Gray
}

SPAIN_COLORS = ["#C60B1E", "#FFC400", "#004D98"]

def create_court_figure():
    """
    Creates a Plotly figure object representing a FIBA basketball court.
    """
    fig = go.Figure()

    # Court dimensions (FIBA standard in meters)
    court_length = 28
    court_width = 15
    basket_to_baseline = 1.575
    three_point_radius = 6.75
    key_width = 4.9
    key_height = 5.8

    # Court outline
    fig.add_shape(type="rect", x0=0, y0=0, x1=court_length, y1=court_width,
                  line=dict(color="black", width=2), fillcolor="#FDF8F0")

    # Half-court line
    fig.add_shape(type="line", x0=court_length/2, y0=0, x1=court_length/2, y1=court_width,
                  line=dict(color="black", width=2))

    # Center circle
    fig.add_shape(type="circle", x0=court_length/2 - 1.8, y0=court_width/2 - 1.8,
                  x1=court_length/2 + 1.8, y1=court_width/2 + 1.8,
                  line=dict(color="black", width=2))

    # Paint area (restricted area)
    fig.add_shape(type="rect", x0=0, y0=(court_width-key_width)/2, x1=key_height,
                  y1=(court_width+key_width)/2, line=dict(color="black", width=2),
                  fillcolor="#EBE0D1", layer="below")
    fig.add_shape(type="rect", x0=court_length-key_height, y0=(court_width-key_width)/2,
                  x1=court_length, y1=(court_width+key_width)/2, line=dict(color="black", width=2),
                  fillcolor="#EBE0D1", layer="below")

    # Three-point lines (arc and straight lines)
    # Right side
    fig.add_shape(type="path",
                  path=f"M {court_length - three_point_radius - basket_to_baseline} {0} L {court_length - key_height} {0} L {court_length - key_height} {(court_width-key_width)/2} M {court_length - key_height} {(court_width+key_width)/2} L {court_length - key_height} {court_width} L {court_length - three_point_radius - basket_to_baseline} {court_width}",
                  line_color="black", width=2)
    angles = np.linspace(np.arcsin((court_width/2)/three_point_radius), -np.arcsin((court_width/2)/three_point_radius), 100)
    three_pt_x_right = court_length - basket_to_baseline - three_point_radius * np.cos(angles)
    three_pt_y_right = court_width/2 + three_point_radius * np.sin(angles)
    fig.add_trace(go.Scatter(x=three_pt_x_right, y=three_pt_y_right, mode='lines',
                             line=dict(color='black', width=2), showlegend=False))


    # Baskets
    fig.add_trace(go.Scatter(x=[basket_to_baseline, court_length - basket_to_baseline],
                             y=[court_width/2, court_width/2], mode='markers',
                             marker=dict(size=12, color='#DE6A39', line=dict(width=2, color='black')),
                             showlegend=False, name='Basket'))

    fig.update_layout(
        xaxis=dict(range=[0, court_length], showgrid=False, zeroline=False, visible=False),
        yaxis=dict(range=[0, court_width], showgrid=False, zeroline=False, visible=False),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=500,
    )
    return fig