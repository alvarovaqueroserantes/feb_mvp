# visualizations.py (improved)
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from court_utils import get_plotly_court
from typing import Optional

def trajectory_plot(players_df: pd.DataFrame, 
                   ball_df: pd.DataFrame, 
                   *, 
                   player_id: Optional[int] = None) -> go.Figure:
    """
    Creates an advanced interactive trajectory visualization with:
    - Smooth player animations
    - Enhanced court visualization
    - Professional styling
    - Intuitive controls
    """
    # Data preparation
    df = players_df.copy()
    if player_id is not None:
        df = df[df["player_id"] == player_id]
    
    # Enhanced ball visualization
    ball = ball_df.copy()
    ball["player_id"] = "Ball"
    ball["size"] = 12  # Larger ball size
    ball["symbol"] = "circle"  # Special symbol
    
    # Player styling
    df["size"] = 8  # Player size
    df["symbol"] = "circle"  # Player symbol
    
    # Combine data
    df_all = pd.concat([df, ball], ignore_index=True)
    
    # Professional color scheme
    color_discrete_map = {
        "1": "#1F77B4",  # PG - Blue
        "2": "#FF7F0E",  # SG - Orange
        "3": "#2CA02C",  # SF - Green
        "4": "#D62728",  # PF - Red
        "5": "#9467BD",  # C - Purple
        "Ball": "#000000" # Ball - Black
    }
    
    # Create base court
    fig = get_plotly_court()
    
    # Add animated trajectories
    anim_fig = px.scatter(
        df_all,
        x="x_m",
        y="y_m",
        animation_frame="frame",
        color="player_id",
        color_discrete_map=color_discrete_map,
        size="size",
        size_max=15,
        opacity=0.9,
        symbol="symbol",
        symbol_sequence=["circle"],
        range_x=[0, 14],
        range_y=[0, 15],
        hover_name="player_id",
        hover_data={
            "x_m": ":.1f",
            "y_m": ":.1f", 
            "frame": True,
            "size": False,
            "symbol": False
        },
        render_mode="svg"
    )
    
    # Merge with court
    for trace in anim_fig.data:
        fig.add_trace(trace)
    
    # Enhanced animation controls
    fig.update_layout(
        updatemenus=[{
            "type": "buttons",
            "showactive": False,
            "buttons": [{
                "label": "▶️ Play",
                "method": "animate",
                "args": [
                    None, 
                    {
                        "frame": {"duration": 100, "redraw": True},
                        "fromcurrent": True,
                        "transition": {"duration": 50}
                    }
                ]
            }]
        }],
        title={
            "text": f"<b>Player #{player_id} Trajectory</b>" if player_id else "<b>All Players Trajectories</b>",
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 24, "family": "Arial"}
        },
        annotations=[{
            "text": "Frame:",
            "x": 0.1,
            "y": 0.05,
            "showarrow": False,
            "font": {"size": 12}
        }]
    )
    
    # Smooth animation settings
    fig.update_traces(
        marker=dict(
            line=dict(width=1, color="DarkSlateGrey")
        ),
        selector=dict(mode="markers")
    )
    
    # Professional hover effects
    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial"
        )
    )
    
    return fig