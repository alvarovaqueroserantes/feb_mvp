import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from streamlit_option_menu import option_menu

from utils.styling import inject_custom_css, render_header
from pages import overview, biometrics, heart_rate, tactics, recovery, player_load, team

# --- Page Configuration ---
st.set_page_config(
    layout="wide",
    page_title="Spain Basketball Analytics Pro",
    page_icon="🏀" # Standard emoji is fine for browser tab
)

# --- Load Custom CSS ---
inject_custom_css()

# --- Data Loading and Caching ---
@st.cache_data
def load_data():
    """
    Loads, processes, and enhances the basketball dataset.
    This function is cached to improve performance.
    """
    try:
        df = pd.read_csv('data/integrated_dataset.csv')
    except FileNotFoundError:
        st.error("Error: The data file 'data/integrated_dataset.csv' was not found.")
        st.info("Please make sure the data file is in the 'data' directory.")
        return pd.DataFrame() # Return empty dataframe

    # Enhanced feature engineering (as in original script)
    np.random.seed(42)
    shots = df[df['action'] == 'shot'].copy()
    shot_zones = []
    for _, row in shots.iterrows():
        x, y = row['x'], row['y']
        if x >= 25 and 5 <= y <= 10: shot_zones.append('Paint')
        elif x >= 22 and (y < 5 or y > 10): shot_zones.append('Mid-Range')
        elif x < 22: shot_zones.append('Three-Pointer')
        else: shot_zones.append('Other')
    shots['zone'] = shot_zones
    zone_probs = {'Paint': 0.65, 'Mid-Range': 0.45, 'Three-Pointer': 0.38, 'Other': 0.25}
    shots['success'] = [np.random.binomial(1, zone_probs[z]) for z in shots['zone']]
    df = df.merge(shots[['time', 'player', 'success', 'zone']], on=['time', 'player'], how='left')
    df['success'] = df['success'].fillna(-1)

    df['tactical_situation'] = 'Initial Setup'
    df.loc[df['time'].between(7, 10), 'tactical_situation'] = 'Pick-and-Roll'
    df.loc[df['time'].between(11, 15), 'tactical_situation'] = 'Second Action'
    df.loc[df['time'] >= 15, 'tactical_situation'] = 'Shot Outcome'
    df['role'] = np.where(df['player'].str.startswith('A'), 'Offense', 'Defense')
    df['exertion_index'] = 0.4 * df['heart_rate'] + 0.3 * df['velocity'] + 0.3 * df['acceleration']
    df['recovery_phase'] = np.select(
        [(df['exertion_index'] > df.groupby('player')['exertion_index'].transform('mean') + 15),
         (df['exertion_index'] < df.groupby('player')['exertion_index'].transform('mean') - 10)],
        ['High Exertion', 'Recovery Phase'], default='Normal'
    )
    df['offensive_eff'] = np.where(df['role'] == 'Offense', df['player_load'] / (df['velocity'] + 0.1), np.nan)
    df['defensive_eff'] = np.where(df['role'] == 'Defense', df['player_load'] / (df['acceleration'] + 0.1), np.nan)

    return df

df = load_data()

if df.empty:
    st.stop()

# --- Sidebar for Global Filters ---
with st.sidebar:
    st.markdown("## Global Filters")
    players = sorted(df['player'].unique())
    selected_player = st.selectbox("Select Player", ['All Players'] + players)

    min_time, max_time = int(df['time'].min()), int(df['time'].max())
    time_range = st.slider("Time Range (seconds)", min_time, max_time, (min_time, max_time))

    st.markdown("---")
    st.markdown("## AI Model Selection")
    ai_models = {
        "KMeans Clustering": KMeans(n_clusters=3, random_state=42, n_init=10),
        "DBSCAN": DBSCAN(eps=0.5, min_samples=5),
        "PCA": PCA(n_components=2),
        "t-SNE": TSNE(n_components=2, perplexity=5, random_state=42) # Reduced perplexity for small datasets
    }
    selected_model_name = st.selectbox("Select Clustering/Dimensionality Model", list(ai_models.keys()))

# --- Main Content ---
render_header(
    "Elite Basketball Performance Intelligence",
    "An advanced biometric-tactical integration system for the Spanish National Team."
)

# --- Navigation Menu ---
selected_page = option_menu(
    menu_title=None,
    options=[
        "Overview", "Player Biometrics", "Heart Rate Analysis",
        "Tactical Insights", "Recovery Metrics", "PlayerLoad Insights", "Team Performance"
    ],
    icons=[
        "bar-chart-line", "person-badge", "heart-pulse", "diagram-3",
        "battery-charging", "speedometer2", "people"
    ],
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "transparent"},
        "icon": {"color": "#45AAF2", "font-size": "18px"},
        "nav-link": {
            "font-size": "14px",
            "text-align": "center",
            "margin": "0px 5px",
            "--hover-color": "#F0E5DA"
        },
        "nav-link-selected": {"background-color": "#FF6B6B", "color": "#FFFFFF"},
    }
)

st.markdown("---",)

# --- Filtering Data Based on Sidebar ---
filtered_df = df[(df['time'] >= time_range[0]) & (df['time'] <= time_range[1])]
if selected_player != 'All Players':
    filtered_df = filtered_df[filtered_df['player'] == selected_player]
else:
    # For team-level views that need all players in the time range
    pass

# --- Page Routing ---
if selected_page == "Overview":
    overview.render(filtered_df, ai_models, selected_model_name)
elif selected_page == "Player Biometrics":
    biometrics.render(filtered_df, selected_player)
elif selected_page == "Heart Rate Analysis":
    heart_rate.render(df, time_range) # Pass original df for broader analysis
elif selected_page == "Tactical Insights":
    tactics.render(df, time_range) # Pass original df
elif selected_page == "Recovery Metrics":
    recovery.render(filtered_df)
elif selected_page == "PlayerLoad Insights":
    player_load.render(filtered_df)
elif selected_page == "Team Performance":
    team.render(df, time_range) # Pass original df

# --- Footer ---
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #888;">
        <p>Advanced Basketball Intelligence System v3.0 | Bauhaus Edition</p>
        <p>Developed for the Spanish National Team</p>
    </div>
    """, unsafe_allow_html=True)