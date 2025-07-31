# streamlit_app.py (updated)
import streamlit as st
import pandas as pd
from visualizations import trajectory_plot
from typing import Tuple

# Configuration
st.set_page_config(
    layout="wide",
    page_title="🏀 Basketball Analytics Dashboard",
    page_icon=":basketball:"
)

@st.cache_data(ttl=3600)
def load_data() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Load and cache the data files.
    
    Returns:
        Tuple of (positions, ball, metrics) DataFrames
    """
    try:
        pos = pd.read_csv("data/positions.csv")
        ball = pd.read_csv("data/ball.csv")
        met = pd.read_csv("data/metrics.csv")
        return pos, ball, met
    except FileNotFoundError as e:
        st.error(f"Data loading error: {e}")
        st.stop()

def main():
    """Main application function."""
    st.sidebar.title("Basketball Analytics")
    st.sidebar.markdown("""
        ### Navigation
        Select a player to analyze their movement patterns and physical metrics.
    """)
    
    # Load data
    positions, ball, metrics = load_data()
    
    # Convert player IDs to strings for selectbox compatibility
    player_options = ["All Players"] + [f"Player #{int(p)}" for p in sorted(positions["player_id"].unique())]
    
    # Player selection
    player_opt = st.sidebar.selectbox(
        "Select Player",
        options=player_options,
        index=0  # Default to "All Players"
    )
    
    # Extract player ID if not "All Players"
    pid = None if player_opt == "All Players" else int(player_opt.split("#")[1])
    
    # Main content
    st.title("🏀 Basketball Movement Analysis")
    st.markdown("""
        Analyze player trajectories, position heatmaps, and physical metrics.
        Use the sidebar to select a specific player.
    """)
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["Trajectories", "Heatmaps", "Performance Metrics"])
    
    with tab1:
        st.header("Player Trajectories")
        # In your Streamlit app
        st.plotly_chart(
            trajectory_plot(positions, ball, player_id=pid),
            use_container_width=True,
            theme="streamlit"
        )
        st.markdown("""
            **Instructions:**  
            - Click the play button to animate the play  
            - Hover over points to see player positions  
            - Use the slider to scrub through frames
        """)
    
    with tab2:
        st.header("Position Heatmaps")
        st.plotly_chart(
            heatmap_plot(positions, player_id=pid),
            use_container_width=True,
            theme="streamlit"
        )
        st.markdown("""
            **Interpretation:**  
            - Warmer colors show areas where the player spent more time  
            - Dark red indicates highest concentration of activity
        """)
    
    with tab3:
        st.header("Performance Metrics")
        if pid:
            player_metrics = metrics[metrics["player_id"] == pid]
            if not player_metrics.empty:
                st.metric(
                    label=f"Total Distance Covered (Player #{pid})",
                    value=f"{player_metrics['total_dist_m'].values[0]:.1f} m"
                )
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(
                        "Max Speed",
                        f"{player_metrics['max_speed'].values[0]:.1f} m/s"
                    )
                with col2:
                    st.metric(
                        "Avg Speed",
                        f"{player_metrics['mean_speed'].values[0]:.1f} m/s"
                    )
            else:
                st.warning(f"No metrics found for Player #{pid}")
        else:
            styled_metrics = metrics.style\
                .background_gradient(cmap="Blues", subset=["total_dist_m"])\
                .background_gradient(cmap="Reds", subset=["max_speed"])\
                .background_gradient(cmap="Greens", subset=["mean_speed"])
            st.dataframe(styled_metrics, use_container_width=True)
        st.markdown("""
            **Key Metrics:**  
            - **Total Distance:** Overall movement during play  
            - **Max Speed:** Peak acceleration moment  
            - **Avg Speed:** Consistent movement intensity
        """)

if __name__ == "__main__":
    main()