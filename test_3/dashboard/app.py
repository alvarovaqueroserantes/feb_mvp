import streamlit as st 
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from PIL import Image
import os
import seaborn as sns
from scipy import stats
from scipy.spatial import distance
from scipy.stats import pearsonr
from scipy.signal import savgol_filter

# Configuration - Professional Dark Theme
st.set_page_config(
    layout="wide", 
    page_title="Spain Basketball Analytics Pro",
    page_icon="🏀",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme with electric yellow accents
st.markdown("""
    <style>
    :root {
        --primary: #FFEA00;
        --secondary: #0E1117;
        --accent: #FF4B4B;
        --background: #12151F;
        --card: #1A1E2C;
        --text: #FFFFFF;
        --border: #2A3045;
    }
    
    body {
        background-color: var(--background);
        color: var(--text);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .stApp {
        background-color: var(--background);
    }
    
    .stButton>button {
        background-color: var(--primary) !important;
        color: var(--secondary) !important;
        border-radius: 4px;
        font-weight: bold;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #FFD700 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    .stSelectbox>div>div {
        background-color: var(--card);
        color: var(--text);
        border-color: var(--border);
    }
    
    .stSlider>div>div>div>div {
        background-color: var(--primary);
    }
    
    .stMetric {
        background-color: var(--card);
        border-radius: 8px;
        padding: 15px;
        border-left: 4px solid var(--primary);
        transition: transform 0.3s ease;
    }
    
    .stMetric:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    .stMetric label {
        color: #A0AEC0 !important;
        font-size: 0.9rem;
    }
    
    .stMetric div[data-testid="stMetricValue"] {
        color: var(--primary) !important;
        font-size: 1.8rem !important;
        font-weight: bold;
    }
    
    .stMetric div[data-testid="stMetricDelta"] {
        font-size: 1rem !important;
    }
    
    .stTabs [aria-selected="true"] {
        color: var(--primary) !important;
        font-weight: bold;
        border-bottom: 3px solid var(--primary);
    }
    
    .stDataFrame {
        background-color: var(--card) !important;
        border-radius: 8px;
        overflow: hidden;
    }
    
    .stHeader {
        color: var(--primary) !important;
        border-bottom: 2px solid var(--primary);
        padding-bottom: 0.5rem;
        margin-top: 1.5rem;
    }
    
    .sidebar .sidebar-content {
        background-color: var(--card) !important;
        box-shadow: 0 0 15px rgba(0,0,0,0.3);
    }
    
    .plot-container {
        border-radius: 10px;
        background-color: var(--card);
        padding: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        margin-bottom: 20px;
    }
    
    .plot-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    
    .footer {
        text-align: center;
        padding: 20px;
        margin-top: 30px;
        color: #A0AEC0;
        font-size: 0.9rem;
        border-top: 1px solid var(--border);
    }
    
    .kpi-card {
        background-color: var(--card);
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        border-left: 4px solid var(--primary);
        transition: all 0.3s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    .kpi-title {
        font-size: 1rem;
        color: #A0AEC0;
        margin-bottom: 5px;
        font-weight: 600;
    }
    
    .kpi-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: var(--primary);
        margin-bottom: 5px;
    }
    
    .kpi-delta {
        font-size: 0.9rem;
        color: #4ADE80;
        font-weight: 600;
    }
    
    .kpi-target {
        font-size: 0.85rem;
        color: #A0AEC0;
        font-style: italic;
    }
    
    .insight-card {
        background-color: var(--card);
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
        border-left: 3px solid var(--accent);
    }
    
    .tactical-card {
        background: linear-gradient(135deg, #1A1E2C 0%, #2A3045 100%);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid var(--border);
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    
    .player-card {
        background-color: var(--card);
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        border-top: 3px solid var(--primary);
    }
    
    .section-title {
        color: var(--primary);
        font-size: 1.5rem;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 2px solid var(--border);
    }
    </style>
    """, unsafe_allow_html=True)

# Color Scheme
PRIMARY_COLOR = "#FFEA00"  # Electric Yellow
SECONDARY_COLOR = "#FF4B4B"  # Vibrant Red
BACKGROUND_COLOR = "#12151F"  # Dark Blue-Black
CARD_COLOR = "#1A1E2C"  # Card Background
TEXT_COLOR = "#FFFFFF"  # White
ACCENT_COLOR = "#00D4FF"  # Electric Blue

SPAIN_COLORS = [PRIMARY_COLOR, ACCENT_COLOR, SECONDARY_COLOR]

# Load data with enhanced features
@st.cache_data
def load_data():
    # Simulate dataset with advanced metrics
    np.random.seed(42)
    times = np.linspace(0, 24, 240)
    players = ['A1', 'A2', 'A3', 'A4', 'A5', 'D1', 'D2', 'D3', 'D4', 'D5']
    positions = {
        'A1': 'Guard', 'A2': 'Guard', 'A3': 'Forward', 'A4': 'Forward', 'A5': 'Center',
        'D1': 'Guard', 'D2': 'Guard', 'D3': 'Forward', 'D4': 'Forward', 'D5': 'Center'
    }
    body_weights = {
        'Guard': 85, 'Forward': 100, 'Center': 110  # kg
    }
    actions = ['run', 'pass', 'shot', 'dribble', 'defend', 'rebound', 'steal', 'block']
    
    data = []
    for t in times:
        for p in players:
            pos = positions[p]
            heart_rate = np.random.normal(160, 15)
            velocity = np.random.uniform(0.5, 8)
            acceleration = np.random.uniform(0, 7)
            player_load = np.random.uniform(1, 10)
            action = np.random.choice(actions, p=[0.3, 0.15, 0.1, 0.15, 0.15, 0.05, 0.05, 0.05])
            
            # Position based on player and time
            if p.startswith('A'):
                x = np.random.uniform(0, 28)
                y = np.random.uniform(0, 15)
                dist_to_basket = np.sqrt((x - 0)**2 + (y - 7.5)**2)
            else:
                # Defenders stay closer to their own basket
                x = np.random.uniform(20, 28)
                y = np.random.uniform(0, 15)
                dist_to_basket = np.sqrt((x - 28)**2 + (y - 7.5)**2)
                
            # Calculate advanced metrics
            metabolic_power = (velocity * acceleration) / body_weights[pos]
            high_intensity_burst = 1 if acceleration > 3 else 0
            
            # Add fatigue effect - heart rate increases over time
            if t > 20:
                heart_rate = min(heart_rate * (1 + (t-20)*0.01), 200)
            
            data.append({
                'time': t,
                'player': p,
                'position': pos,
                'heart_rate': heart_rate,
                'velocity': velocity,
                'acceleration': acceleration,
                'player_load': player_load,
                'action': action,
                'x': x,
                'y': y,
                'dist_to_basket': dist_to_basket,
                'metabolic_power': metabolic_power,
                'high_intensity_burst': high_intensity_burst
            })
            
    df = pd.DataFrame(data)
    
    # Enhanced shot simulation with court zones
    shots = df[df['action'] == 'shot'].copy()
    shot_zones = []
    for idx, row in shots.iterrows():
        x, y = row['x'], row['y']
        if x >= 25 and 5 <= y <= 10:
            shot_zones.append('Paint')
        elif x >= 22 and (y < 5 or y > 10):
            shot_zones.append('Mid-Range')
        elif x < 22:
            shot_zones.append('Three-Pointer')
        else:
            shot_zones.append('Other')
    shots['zone'] = shot_zones
    
    # Zone-based success probabilities
    zone_probs = {'Paint': 0.65, 'Mid-Range': 0.45, 'Three-Pointer': 0.38, 'Other': 0.25}
    shots['success'] = [np.random.binomial(1, zone_probs[z]) for z in shots['zone']]
    
    df = df.merge(shots[['time', 'player', 'success', 'zone']], 
                 on=['time', 'player'], how='left', suffixes=('', '_shot'))
    df['success'] = df['success'].fillna(-1)  # -1 = not a shot
    
    # Enhanced tactical situations with player roles
    df['tactical_situation'] = 'Initial Setup'
    df.loc[df['time'].between(7, 10), 'tactical_situation'] = 'Pick-and-Roll'
    df.loc[df['time'].between(11, 15), 'tactical_situation'] = 'Second Action'
    df.loc[df['time'] >= 15, 'tactical_situation'] = 'Shot Outcome'
    
    # Offensive/defensive roles
    df['role'] = np.where(df['player'].str.startswith('A'), 'Offense', 'Defense')
    
    # Enhanced recovery metrics with exertion index
    df['exertion_index'] = 0.4 * df['heart_rate'] + 0.3 * df['velocity'] + 0.3 * df['acceleration']
    df['recovery_phase'] = np.select(
        [
            (df['exertion_index'] > df.groupby('player')['exertion_index'].transform('mean') + 15),
            (df['exertion_index'] < df.groupby('player')['exertion_index'].transform('mean') - 10),
        ],
        ['High Exertion', 'Recovery Phase'],
        default='Normal'
    )
    
    # PlayerLoad efficiency metrics
    df['offensive_eff'] = np.where(df['role'] == 'Offense', df['player_load'] / (df['velocity'] + 0.1), np.nan)
    df['defensive_eff'] = np.where(df['role'] == 'Defense', df['player_load'] / (df['acceleration'] + 0.1), np.nan)
    
    # Ball possession simulation
    df['ball_handler'] = False
    ball_handler = 'A1'
    for t in sorted(df['time'].unique()):
        time_df = df[df['time'] == t]
        actions = time_df[time_df['action'].isin(['pass', 'shot', 'dribble'])]['player'].values
        if len(actions) > 0:
            ball_handler = actions[0]
        df.loc[(df['time'] == t) & (df['player'] == ball_handler), 'ball_handler'] = True
    
    # Calculate advanced metrics
    # Physical Load Metrics
    df['hr_stress_index'] = df.groupby('player')['heart_rate'].transform(lambda x: (x.max() - x.min()) / len(x))
    
    # Movement Efficiency Metrics
    df['effective_distance'] = np.where(
        (df['x'] >= 25) & (df['y'] >= 5) & (df['y'] <= 10), 
        df['velocity'], 
        0
    )
    
    # Tactical Metrics
    offensive_players = df[df['role'] == 'Offense']
    spacing_index = offensive_players.groupby('time')['dist_to_basket'].std().reset_index()
    spacing_index.columns = ['time', 'spacing_index']
    df = df.merge(spacing_index, on='time', how='left')
    
    # Rebound positioning score
    shot_times = df[df['action'] == 'shot']['time'].unique()
    for t in shot_times:
        shot_df = df[df['time'] == t]
        for _, row in shot_df.iterrows():
            player = row['player']
            x, y = row['x'], row['y']
            # Calculate distance to nearest opponent
            opponents = df[(df['time'] == t) & (df['role'] != row['role'])][['x', 'y']]
            if not opponents.empty:
                dist_to_opponent = distance.cdist([(x, y)], opponents).min()
                df.loc[(df['time'] == t) & (df['player'] == player), 'rebound_score'] = 1 / (row['dist_to_basket'] + dist_to_opponent + 0.1)
    
    # Time-Derived Features
    df['fatigue_slope'] = df.groupby('player')['heart_rate'].diff() / df.groupby('player')['time'].diff()
    
    # Add fatigue index (cumulative fatigue)
    df['fatigue_index'] = df.groupby('player')['player_load'].cumsum() / 100
    
    # Add recovery metrics
    df['recovery_rate'] = df.groupby('player')['heart_rate'].transform(
        lambda x: x.diff().rolling(5, min_periods=1).mean()
    )
    
    # Add PlayerLoad metrics
    df['player_load_per_min'] = df['player_load'] / (df['time'] / 60)
    
    return df

df = load_data()

# Sidebar - Professional Design
with st.sidebar:
    st.title("Spanish Basketball Analytics Pro")
    st.markdown("### Advanced Filters")
    st.divider()
    
    # Player selection
    players = df['player'].unique()
    selected_player = st.selectbox("Select Player", ['All Players'] + list(players))
    
    # Time range selection
    min_time, max_time = df['time'].min(), df['time'].max()
    time_range = st.slider("Time Range (seconds)", min_time, max_time, (min_time, max_time))
    
    # Analysis focus
    analysis_options = [
        "Overview", 
        "Player Biometrics", 
        "Heart Rate Analysis", 
        "Tactical Insights",
        "Recovery Metrics", 
        "PlayerLoad Insights",
        "Team Performance"
    ]
    analysis_focus = st.selectbox("Analysis Focus", analysis_options)
    
    # AI Model Selection
    st.divider()
    st.markdown("### AI Models")
    ai_models = {
        "KMeans Clustering": KMeans(n_clusters=3, random_state=42),
        "DBSCAN": DBSCAN(eps=0.5, min_samples=5),
        "PCA": PCA(n_components=2),
        "t-SNE": TSNE(n_components=2, perplexity=30)
    }
    selected_model = st.selectbox("Select AI Model", list(ai_models.keys()))
    
    st.divider()
    st.markdown("### Performance Indicators")
    
    # KPI Cards in Sidebar
    kpi_data = [
        {"title": "Offensive Efficiency", "value": "1.12 PPP", "delta": "↑ 0.08 vs Avg", "target": "Target: >0.85"},
        {"title": "Defensive Reactivity", "value": "0.9s", "delta": "↓ 0.3s vs Avg", "target": "Target: <1.2s"},
        {"title": "Screen Impact Score", "value": "2.8 m/s", "delta": "↑ 0.3 vs Avg", "target": "Target: >2.5 m/s"}
    ]
    
    for kpi in kpi_data:
        st.markdown(f"""
            <div class='kpi-card'>
                <div class='kpi-title'>{kpi['title']}</div>
                <div class='kpi-value'>{kpi['value']}</div>
                <div class='kpi-delta'>{kpi['delta']}</div>
                <div class='kpi-target'>{kpi['target']}</div>
            </div>
        """, unsafe_allow_html=True)

# Filter data based on selections
filtered_df = df[(df['time'] >= time_range[0]) & (df['time'] <= time_range[1])]
if selected_player != 'All Players':
    filtered_df = filtered_df[filtered_df['player'] == selected_player]

# Main Content - Professional Layout
st.title("Elite Basketball Performance Intelligence")
st.markdown("""
    **Advanced Biometric-Tactical Integration System**  
    *Spanish National Team - Next Generation Performance Analytics*
""")
st.divider()

# Enhanced Overview Tab
if analysis_focus == "Overview":
    # Performance Summary Cards
    st.subheader("Game Performance Summary")
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculate KPIs
    if not filtered_df.empty:
        total_pl = filtered_df['player_load'].sum()
        avg_mp = filtered_df['metabolic_power'].mean()
        bursts = filtered_df['high_intensity_burst'].sum()
        hr_stress = filtered_df['hr_stress_index'].mean()
        
        with col1:
            st.metric("Player Load", f"{total_pl:.0f}", 
                     "High" if total_pl > 500 else "Moderate")
            
        with col2:
            st.metric("Metabolic Power", f"{avg_mp:.1f} W/kg", 
                     "High" if avg_mp > 0.8 else "Moderate")
            
        with col3:
            st.metric("High-Intensity Bursts", f"{bursts}", 
                     "Intense" if bursts > 15 else "Moderate")
            
        with col4:
            st.metric("HR Stress Index", f"{hr_stress:.2f}", 
                     "High Stress" if hr_stress > 1.5 else "Optimal")
    
    # Main analysis columns
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Player Efficiency Comparison
        st.subheader("Player Efficiency Analysis")
        eff_df = filtered_df.groupby('player').agg({
            'offensive_eff': 'mean',
            'defensive_eff': 'mean',
            'metabolic_power': 'mean'
        }).reset_index().melt(id_vars='player', var_name='efficiency_type', value_name='efficiency')
        
        if not eff_df.empty:
            fig_eff = px.bar(
                eff_df.dropna(),
                x='player',
                y='efficiency',
                color='efficiency_type',
                barmode='group',
                color_discrete_map={'offensive_eff': PRIMARY_COLOR, 'defensive_eff': ACCENT_COLOR, 'metabolic_power': SECONDARY_COLOR},
                title="Player Efficiency Comparison",
                labels={'efficiency': 'Efficiency Score', 'efficiency_type': 'Efficiency Type'},
                template='plotly_dark'
            )
            fig_eff.update_layout(
                plot_bgcolor=CARD_COLOR,
                paper_bgcolor=CARD_COLOR,
                font=dict(color=TEXT_COLOR)
            )
            st.plotly_chart(fig_eff, use_container_width=True)
        
        # Tactical Insights
        st.subheader("Tactical Performance Insights")
        insights = [
            "Pick-and-Roll Execution: A1's acceleration increased by 40% during drive phase",
            "Defensive Coordination: D4-D5 communication gap (1.2s) exploited in 3 possessions",
            "Shooting Efficiency: Corner 3PT% 48% vs Wing 3PT% 35%",
            "PlayerLoad Distribution: Guards carry 55% of offensive load vs 45% for bigs",
            "Recovery Patterns: Backcourt recovers 25% faster after high-intensity sprints"
        ]
        for insight in insights:
            st.markdown(f"<div class='insight-card'>{insight}</div>", unsafe_allow_html=True)
    
    with col2:
        # Player Load Distribution
        st.subheader("Player Load Distribution")
        pl_df = filtered_df.groupby('player')['player_load'].sum().reset_index()
        fig_pl = px.pie(
            pl_df,
            names='player',
            values='player_load',
            color='player',
            color_discrete_sequence=SPAIN_COLORS,
            hole=0.4
        )
        fig_pl.update_layout(
            template='plotly_dark',
            plot_bgcolor=CARD_COLOR,
            paper_bgcolor=CARD_COLOR,
            font=dict(color=TEXT_COLOR)
        )
        st.plotly_chart(fig_pl, use_container_width=True)
        
        # Recovery Status
        st.subheader("Recovery Status")
        recovery_df = filtered_df[filtered_df['recovery_phase'] != 'Normal']
        if not recovery_df.empty:
            recovery_stats = recovery_df['recovery_phase'].value_counts(normalize=True).reset_index()
            recovery_stats.columns = ['Phase', 'Percentage']
            
            fig_recovery = px.bar(
                recovery_stats,
                x='Phase',
                y='Percentage',
                color='Phase',
                color_discrete_map={'High Exertion': SECONDARY_COLOR, 'Recovery Phase': ACCENT_COLOR},
                title="Recovery Phase Distribution",
                template='plotly_dark'
            )
            fig_recovery.update_layout(
                plot_bgcolor=CARD_COLOR,
                paper_bgcolor=CARD_COLOR,
                font=dict(color=TEXT_COLOR))
            st.plotly_chart(fig_recovery, use_container_width=True)
        else:
            st.warning("No recovery data in selected range")
    
    # AI Cluster Analysis
    st.subheader("AI Player Clustering")
    cluster_df = filtered_df.groupby('player').agg({
        'heart_rate': 'mean',
        'velocity': 'mean',
        'acceleration': 'max',
        'player_load': 'sum',
        'offensive_eff': 'mean',
        'defensive_eff': 'mean',
        'metabolic_power': 'mean'
    }).reset_index().dropna()
    
    if len(cluster_df) > 2:
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(cluster_df.select_dtypes(include=np.number))
        
        model = ai_models[selected_model]
        
        if selected_model in ["PCA", "t-SNE"]:
            if selected_model == "t-SNE":
                transformed = model.fit_transform(scaled_data)
            else:
                transformed = model.fit_transform(scaled_data)
                
            cluster_df['dim1'] = transformed[:, 0]
            cluster_df['dim2'] = transformed[:, 1]
            
            fig_cluster = px.scatter(
                cluster_df, 
                x='dim1', 
                y='dim2', 
                text='player',
                color='player',
                title=f"{selected_model} Player Clustering",
                color_discrete_sequence=SPAIN_COLORS,
                template='plotly_dark'
            )
        else:
            clusters = model.fit_predict(scaled_data)
            cluster_df['cluster'] = clusters
            
            fig_cluster = px.scatter(
                cluster_df,
                x='heart_rate',
                y='player_load',
                color='cluster',
                size='velocity',
                hover_name='player',
                title=f"{selected_model} Player Clustering",
                color_discrete_sequence=SPAIN_COLORS,
                template='plotly_dark'
            )
        
        fig_cluster.update_layout(
            plot_bgcolor=CARD_COLOR,
            paper_bgcolor=CARD_COLOR,
            font=dict(color=TEXT_COLOR))
        st.plotly_chart(fig_cluster, use_container_width=True)
    else:
        st.warning("Insufficient data for clustering")

# Enhanced Player Biometrics Tab
elif analysis_focus == "Player Biometrics":
    st.subheader("Advanced Physiological Metrics")
    
    if selected_player == 'All Players':
        st.warning("Please select a specific player to view biometric details")
    else:
        player_df = filtered_df[filtered_df['player'] == selected_player]
        
        # Create tabs for different metrics
        tab1, tab2, tab3, tab4 = st.tabs(["Heart Rate", "Velocity", "Acceleration", "PlayerLoad"])
        
        with tab1:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # Enhanced HR visualization with game situations
                fig_hr = px.line(
                    player_df, 
                    x='time', 
                    y='heart_rate',
                    title=f"{selected_player} Heart Rate with Game Context",
                    markers=True,
                    hover_data=['action', 'tactical_situation', 'zone'],
                    template='plotly_dark',
                    color_discrete_sequence=[PRIMARY_COLOR]
                )
                
                # Add game situation annotations
                for situation in player_df['tactical_situation'].unique():
                    sit_df = player_df[player_df['tactical_situation'] == situation]
                    if not sit_df.empty:
                        fig_hr.add_vrect(
                            x0=sit_df['time'].min(), x1=sit_df['time'].max(),
                            fillcolor=PRIMARY_COLOR if situation == "Pick-and-Roll" else ACCENT_COLOR,
                            opacity=0.2,
                            line_width=0,
                            annotation_text=situation,
                            annotation_position="top left"
                        )
                
                fig_hr.update_layout(
                    xaxis_title="Time (seconds)",
                    yaxis_title="Heart Rate (bpm)",
                    hovermode="x unified",
                    plot_bgcolor=CARD_COLOR,
                    paper_bgcolor=CARD_COLOR,
                    font=dict(color=TEXT_COLOR))
                st.plotly_chart(fig_hr, use_container_width=True)
                
                # Additional HR graph: HR by tactical situation
                st.subheader("HR by Tactical Situation")
                fig_hr_box = px.box(
                    player_df,
                    x='tactical_situation',
                    y='heart_rate',
                    color='tactical_situation',
                    points="all",
                    template='plotly_dark',
                    color_discrete_sequence=SPAIN_COLORS
                )
                fig_hr_box.update_layout(
                    plot_bgcolor=CARD_COLOR,
                    paper_bgcolor=CARD_COLOR,
                    font=dict(color=TEXT_COLOR))
                st.plotly_chart(fig_hr_box, use_container_width=True)
                
            with col2:
                st.subheader("Heart Rate Zones")
                hr_zones = [
                    {"zone": "Optimal", "min": 120, "max": 150, "color": ACCENT_COLOR},
                    {"zone": "Effective", "min": 151, "max": 170, "color": PRIMARY_COLOR},
                    {"zone": "High Stress", "min": 171, "max": 190, "color": "#FFA500"},
                    {"zone": "Critical", "min": 191, "max": 220, "color": SECONDARY_COLOR}
                ]
                
                for zone in hr_zones:
                    percentage = ((player_df['heart_rate'] >= zone["min"]) & 
                                 (player_df['heart_rate'] <= zone["max"])).mean() * 100
                    st.metric(zone["zone"], f"{percentage:.1f}%", 
                              delta_color="off", 
                              help=f"{zone['min']}-{zone['max']} bpm")
                
                st.divider()
                st.metric("Avg Heart Rate", f"{player_df['heart_rate'].mean():.0f} bpm")
                st.metric("Max Heart Rate", f"{player_df['heart_rate'].max():.0f} bpm")
                st.metric("HR Stress Index", f"{player_df['hr_stress_index'].mean():.2f}")
                
                # HR performance metrics
                st.subheader("Performance Metrics")
                st.metric("Shooting Efficiency in Optimal HR", "62%", "↑ 8%")
                st.metric("Decision Making Efficiency", "87%", "↑ 12% in Optimal HR")
        
        with tab2:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # Velocity with acceleration overlay
                fig_vel = px.line(
                    player_df, 
                    x='time', 
                    y='velocity',
                    title=f"{selected_player} Velocity Profile",
                    markers=True,
                    template='plotly_dark',
                    color_discrete_sequence=[PRIMARY_COLOR]
                )
                
                fig_vel.add_trace(go.Scatter(
                    x=player_df['time'],
                    y=player_df['acceleration'],
                    mode='lines',
                    name='Acceleration',
                    yaxis='y2',
                    line=dict(color=ACCENT_COLOR)
                ))
                
                fig_vel.update_layout(
                    xaxis_title="Time (seconds)",
                    yaxis_title="Velocity (m/s)",
                    yaxis2=dict(title='Acceleration (m/s²)', overlaying='y', side='right'),
                    hovermode="x unified",
                    plot_bgcolor=CARD_COLOR,
                    paper_bgcolor=CARD_COLOR,
                    font=dict(color=TEXT_COLOR))
                st.plotly_chart(fig_vel, use_container_width=True)
                
                # Additional graph: Velocity vs Acceleration
                st.subheader("Velocity vs Acceleration Profile")
                fig_vel_acc = px.scatter(
                    player_df,
                    x='velocity',
                    y='acceleration',
                    color='tactical_situation',
                    size='player_load',
                    template='plotly_dark',
                    trendline='ols',
                    color_discrete_sequence=SPAIN_COLORS
                )
                fig_vel_acc.update_layout(
                    plot_bgcolor=CARD_COLOR,
                    paper_bgcolor=CARD_COLOR,
                    font=dict(color=TEXT_COLOR))
                st.plotly_chart(fig_vel_acc, use_container_width=True)
                
            with col2:
                st.subheader("Velocity Metrics")
                st.metric("Max Velocity", f"{player_df['velocity'].max():.1f} m/s")
                st.metric("Avg Velocity", f"{player_df['velocity'].mean():.1f} m/s")
                st.metric("High Intensity Sprints", 
                         f"{(player_df['velocity'] > 6).sum()}",
                         "↑ 12% vs Avg")
                
                st.divider()
                st.subheader("Acceleration Metrics")
                st.metric("Max Acceleration", f"{player_df['acceleration'].max():.1f} m/s²")
                st.metric("Avg Acceleration", f"{player_df['acceleration'].mean():.1f} m/s²")
                st.metric("High-Intensity Bursts", f"{player_df['high_intensity_burst'].sum()}")
                
                st.divider()
                st.subheader("Performance Impact")
                st.metric("Drive Success Rate", "78%", "↑ 15% when Accel >4 m/s²")
                st.metric("Defensive Stops", "85%", "↑ 20% when Vel >5 m/s")
        
        with tab3:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # Metabolic Power Visualization
                fig_mp = px.line(
                    player_df, 
                    x='time', 
                    y='metabolic_power',
                    title=f"{selected_player} Metabolic Power Profile",
                    markers=True,
                    template='plotly_dark',
                    color_discrete_sequence=[SECONDARY_COLOR]
                )
                
                # Add high-intensity thresholds
                fig_mp.add_hline(y=0.5, line_dash="dash", line_color="green", annotation_text="Moderate Intensity")
                fig_mp.add_hline(y=0.8, line_dash="dash", line_color="orange", annotation_text="High Intensity")
                fig_mp.add_hline(y=1.0, line_dash="dash", line_color="red", annotation_text="Elite Intensity")
                
                fig_mp.update_layout(
                    xaxis_title="Time (seconds)",
                    yaxis_title="Metabolic Power (W/kg)",
                    hovermode="x unified",
                    plot_bgcolor=CARD_COLOR,
                    paper_bgcolor=CARD_COLOR,
                    font=dict(color=TEXT_COLOR))
                st.plotly_chart(fig_mp, use_container_width=True)
                
                # Additional graph: Acceleration Distribution
                st.subheader("Acceleration Distribution")
                fig_acc_dist = px.histogram(
                    player_df,
                    x='acceleration',
                    nbins=20,
                    color='tactical_situation',
                    template='plotly_dark',
                    color_discrete_sequence=SPAIN_COLORS
                )
                fig_acc_dist.update_layout(
                    plot_bgcolor=CARD_COLOR,
                    paper_bgcolor=CARD_COLOR,
                    font=dict(color=TEXT_COLOR))
                st.plotly_chart(fig_acc_dist, use_container_width=True)
                
            with col2:
                st.subheader("Metabolic Power")
                st.metric("Avg Metabolic Power", f"{player_df['metabolic_power'].mean():.2f} W/kg")
                st.metric("Peak Metabolic Power", f"{player_df['metabolic_power'].max():.2f} W/kg")
                st.metric("High Power Bursts", 
                         f"{(player_df['metabolic_power'] > 0.8).sum()}",
                         "↑ 15% vs Avg")
                
                st.divider()
                st.subheader("Fatigue Metrics")
                st.metric("Fatigue Index", f"{player_df['fatigue_index'].max():.2f}")
                st.metric("Fatigue Slope", f"{player_df['fatigue_slope'].mean():.2f} bpm/s")
                
                st.divider()
                st.subheader("Performance Impact")
                st.metric("Shot Accuracy", "58%", "↓ 12% when MP >0.9")
                st.metric("Turnover Rate", "12%", "↑ 8% when MP >0.9")
        
        with tab4:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # PlayerLoad timeline
                fig_pl = px.line(
                    player_df, 
                    x='time', 
                    y='player_load',
                    title=f"{selected_player} PlayerLoad Accumulation",
                    markers=True,
                    template='plotly_dark',
                    color_discrete_sequence=[PRIMARY_COLOR]
                )
                fig_pl.add_trace(go.Scatter(
                    x=player_df['time'],
                    y=player_df['exertion_index'],
                    mode='lines',
                    name='Exertion Index',
                    yaxis='y2',
                    line=dict(color=ACCENT_COLOR)
                ))
                fig_pl.update_layout(
                    yaxis2=dict(title='Exertion Index', overlaying='y', side='right'),
                    plot_bgcolor=CARD_COLOR,
                    paper_bgcolor=CARD_COLOR,
                    font=dict(color=TEXT_COLOR))
                st.plotly_chart(fig_pl, use_container_width=True)
                
                # Additional graph: PlayerLoad Efficiency
                st.subheader("PlayerLoad Efficiency")
                fig_eff = px.scatter(
                    player_df,
                    x='player_load',
                    y='velocity',
                    color='acceleration',
                    size='heart_rate',
                    template='plotly_dark',
                    trendline='ols',
                    color_continuous_scale='viridis'
                )
                fig_eff.update_layout(
                    plot_bgcolor=CARD_COLOR,
                    paper_bgcolor=CARD_COLOR,
                    font=dict(color=TEXT_COLOR))
                st.plotly_chart(fig_eff, use_container_width=True)
                
            with col2:
                st.subheader("PlayerLoad Metrics")
                st.metric("Total PlayerLoad", f"{player_df['player_load'].sum():.0f}")
                st.metric("Avg PlayerLoad/min", f"{player_df['player_load_per_min'].mean():.2f}")
                st.metric("Max Exertion", f"{player_df['exertion_index'].max():.1f}")
                
                st.divider()
                st.subheader("Recovery Metrics")
                st.metric("Recovery Rate", f"{player_df['recovery_rate'].mean():.2f} bpm/min")
                st.metric("High Exertion Events", f"{player_df[player_df['exertion_index'] > 80].shape[0]}")
                
                st.divider()
                st.subheader("Performance Impact")
                st.metric("Efficiency Drop", "15%", "↓ when PL >400")
                st.metric("Injury Risk", "High", "When PL >450 and HR >180")

# Enhanced Heart Rate Analysis Tab
elif analysis_focus == "Heart Rate Analysis":
    st.subheader("Advanced Heart Rate Performance Intelligence")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Heart Rate vs Performance
        st.subheader("Heart Rate vs Shooting Efficiency")
        shots_df = df[df['success'] >= 0]  # Only shot actions
        
        if not shots_df.empty:
            fig_hr_shot = px.scatter(
                shots_df,
                x='heart_rate',
                y='success',
                color='zone',
                facet_col='player',
                facet_col_wrap=3,
                trendline='ols',
                title="Shooting Success by Heart Rate and Court Zone",
                labels={'success': 'Shot Success (1=made)', 'heart_rate': 'Heart Rate (bpm)'},
                template='plotly_dark',
                color_discrete_sequence=SPAIN_COLORS
            )
            fig_hr_shot.update_layout(
                plot_bgcolor=CARD_COLOR,
                paper_bgcolor=CARD_COLOR,
                font=dict(color=TEXT_COLOR))
            st.plotly_chart(fig_hr_shot, use_container_width=True)
        else:
            st.warning("No shot data available in selected range")
            
        # HR Zones Analysis
        st.subheader("Heart Rate Zones Performance")
        hr_bins = [0, 140, 160, 180, 200]
        hr_labels = ['Optimal', 'Effective', 'High Stress', 'Critical']
        shots_df['hr_zone'] = pd.cut(shots_df['heart_rate'], bins=hr_bins, labels=hr_labels)
        
        if not shots_df.empty:
            zone_perf = shots_df.groupby('hr_zone')['success'].mean().reset_index()
            fig_hr_zone = px.bar(
                zone_perf,
                x='hr_zone',
                y='success',
                color='hr_zone',
                title="Shooting Efficiency by HR Zone",
                labels={'success': 'Shooting Percentage'},
                template='plotly_dark',
                color_discrete_sequence=SPAIN_COLORS
            )
            fig_hr_zone.update_layout(
                plot_bgcolor=CARD_COLOR,
                paper_bgcolor=CARD_COLOR,
                font=dict(color=TEXT_COLOR))
            st.plotly_chart(fig_hr_zone, use_container_width=True)
            
        # HR Recovery Analysis
        st.subheader("Heart Rate Recovery Analysis")
        high_intensity_df = df[df['acceleration'] > 4].copy()
        recovery_data = []
        
        for player in high_intensity_df['player'].unique():
            player_events = high_intensity_df[high_intensity_df['player'] == player]
            for idx, event in player_events.iterrows():
                event_time = event['time']
                post_hr = df[(df['player'] == player) & 
                            (df['time'] > event_time) & 
                            (df['time'] <= event_time + 5)]['heart_rate'].values
                if len(post_hr) > 0:
                    recovery = event['heart_rate'] - post_hr[-1]
                    recovery_data.append({
                        'player': player,
                        'event_time': event_time,
                        'recovery': recovery,
                        'position': event['position']
                    })
                    
        recovery_df = pd.DataFrame(recovery_data)
        
        if not recovery_df.empty:
            fig_recovery = px.box(
                recovery_df,
                x='position',
                y='recovery',
                color='position',
                title="HR Recovery After High-Intensity Events",
                template='plotly_dark',
                color_discrete_sequence=SPAIN_COLORS
            )
            fig_recovery.update_layout(
                plot_bgcolor=CARD_COLOR,
                paper_bgcolor=CARD_COLOR,
                font=dict(color=TEXT_COLOR))
            st.plotly_chart(fig_recovery, use_container_width=True)
    
    with col2:
        st.subheader("Heart Rate Analysis")
        
        # Heart rate distribution
        fig_hr_dist = px.histogram(
            filtered_df,
            x='heart_rate',
            nbins=20,
            title="Heart Rate Distribution",
            template='plotly_dark',
            color_discrete_sequence=[PRIMARY_COLOR]
        )
        fig_hr_dist.update_layout(
            plot_bgcolor=CARD_COLOR,
            paper_bgcolor=CARD_COLOR,
            font=dict(color=TEXT_COLOR))
        st.plotly_chart(fig_hr_dist, use_container_width=True)
        
        # HR zones
        st.subheader("Optimal HR Zones")
        st.markdown("""
        <div class='tactical-card'>
            - **Optimal (120-150 bpm):** 42% of time<br>
            - **Effective (151-170 bpm):** 35% of time<br>
            - **High Stress (171-190 bpm):** 18% of time<br>
            - **Critical (>190 bpm):** 5% of time
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        st.metric("Shooting Efficiency in Optimal Zone", "62%", "↑ 8% vs Other Zones")
        st.metric("Decision Making Efficiency", "87%", "↑ 12% vs High Stress")
        
        st.divider()
        st.subheader("Recommendations")
        st.markdown("""
        <div class='tactical-card'>
            - **Guards:** Maintain HR <170 bpm for optimal playmaking<br>
            - **Bigs:** Limit time in Critical zone to <5%<br>
            - **Team:** Implement HR-controlled rotations
        </div>
        """, unsafe_allow_html=True)

# Enhanced Tactical Insights Tab
elif analysis_focus == "Tactical Insights":
    st.subheader("Advanced Tactical Intelligence")
    
    tab1, tab2, tab3 = st.tabs(["Pick-and-Roll", "Defensive Execution", "Shot Creation"])
    
    with tab1:
        st.subheader("Pick-and-Roll Intelligence")
        pnr_df = df[df['tactical_situation'] == 'Pick-and-Roll']
        
        if not pnr_df.empty:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # Player comparison
                fig_pnr = px.line(
                    pnr_df,
                    x='time',
                    y='velocity',
                    color='player',
                    facet_row='role',
                    title="Player Velocity During Pick-and-Roll",
                    hover_data=['action', 'heart_rate'],
                    template='plotly_dark',
                    color_discrete_sequence=SPAIN_COLORS
                )
                fig_pnr.update_layout(
                    plot_bgcolor=CARD_COLOR,
                    paper_bgcolor=CARD_COLOR,
                    font=dict(color=TEXT_COLOR))
                st.plotly_chart(fig_pnr, use_container_width=True)
                
                # Additional graph: Ball Handler Acceleration vs Screener Movement
                st.subheader("Ball Handler vs Screener Coordination")
                handler_df = pnr_df[(pnr_df['role'] == 'Offense') & (pnr_df['ball_handler'])]
                screener_df = pnr_df[(pnr_df['role'] == 'Offense') & (~pnr_df['ball_handler'])]
                
                if not handler_df.empty and not screener_df.empty:
                    handler_accel = handler_df.groupby('time')['acceleration'].mean().reset_index()
                    screener_vel = screener_df.groupby('time')['velocity'].mean().reset_index()
                    
                    fig_coord = go.Figure()
                    fig_coord.add_trace(go.Scatter(
                        x=handler_accel['time'],
                        y=handler_accel['acceleration'],
                        mode='lines',
                        name='Handler Acceleration',
                        line=dict(color=PRIMARY_COLOR)
                    ))
                    fig_coord.add_trace(go.Scatter(
                        x=screener_vel['time'],
                        y=screener_vel['velocity'],
                        mode='lines',
                        name='Screener Velocity',
                        yaxis='y2',
                        line=dict(color=ACCENT_COLOR)
                    ))
                    fig_coord.update_layout(
                        title="Ball Handler Acceleration vs Screener Velocity",
                        xaxis_title="Time (seconds)",
                        yaxis_title="Acceleration (m/s²)",
                        yaxis2=dict(title='Velocity (m/s)', overlaying='y', side='right'),
                        template='plotly_dark',
                        plot_bgcolor=CARD_COLOR,
                        paper_bgcolor=CARD_COLOR,
                        font=dict(color=TEXT_COLOR)
                    )
                    st.plotly_chart(fig_coord, use_container_width=True)
            
            with col2:
                st.subheader("Efficiency Metrics")
                st.metric("Ball Handler Success", "68%", "↑ 8% from avg")
                st.metric("Roll Man Scoring", "1.25 PPP", "↑ 0.15 from avg")
                st.metric("Defensive Disruption", "0.92 PPP", "↓ 0.08 from opp avg")
                
                st.divider()
                st.subheader("Physiological Metrics")
                st.metric("Avg HR Increase", "+18 bpm", "Ball Handler")
                st.metric("PlayerLoad", "42 AU", "Per Action")
                
                st.divider()
                st.subheader("Screen Effectiveness")
                st.metric("Separation Created", "2.8m", "↑ 0.3m vs Avg")
                
                st.divider()
                st.subheader("Recommendations")
                st.markdown("""
                <div class='tactical-card'>
                    - Increase ball handler acceleration by 10%<br>
                    - Optimize screener timing to 0.3s after screen<br>
                    - Target 70% of PNRs in paint area
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.subheader("Defensive Execution Intelligence")
        defense_df = df[df['player'].str.startswith('D')]
        
        if not defense_df.empty:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # Defensive pressure visualization
                st.subheader("Defensive Pressure Index")
                defense_df['def_pressure'] = defense_df['velocity'] * defense_df['acceleration']
                
                fig_pressure = px.density_contour(
                    defense_df,
                    x='x',
                    y='y',
                    z='def_pressure',
                    histfunc='avg',
                    title="Defensive Pressure by Court Area",
                    template='plotly_dark',
                    color_continuous_scale='thermal'
                )
                fig_pressure.update_layout(
                    xaxis_range=[0, 28],
                    yaxis_range=[0, 15],
                    plot_bgcolor=CARD_COLOR,
                    paper_bgcolor=CARD_COLOR,
                    font=dict(color=TEXT_COLOR))
                st.plotly_chart(fig_pressure, use_container_width=True)
                
                # Player defensive efficiency
                st.subheader("Defensive Efficiency by Player")
                def_eff = defense_df.groupby('player').agg({
                    'defensive_eff': 'mean',
                    'velocity': 'mean',
                    'acceleration': 'max'
                }).reset_index()
                
                fig_def_eff = px.bar(
                    def_eff,
                    x='player',
                    y='defensive_eff',
                    color='defensive_eff',
                    title="Defensive Efficiency Score",
                    template='plotly_dark',
                    color_continuous_scale='viridis'
                )
                fig_def_eff.update_layout(
                    plot_bgcolor=CARD_COLOR,
                    paper_bgcolor=CARD_COLOR,
                    font=dict(color=TEXT_COLOR))
                st.plotly_chart(fig_def_eff, use_container_width=True)
            
            with col2:
                st.subheader("Defensive Metrics")
                st.metric("Defensive Pressure Index", "42.5", "↑ 5.2 vs Avg")
                st.metric("Closeout Efficiency", "87%", "↑ 12% league avg")
                st.metric("Reaction Time", "0.9s", "↓ 0.3s vs Avg")
                
                st.divider()
                st.subheader("Physiological Impact")
                st.metric("Avg HR During Defense", "168 bpm", "↑ 8 bpm vs Offense")
                st.metric("PlayerLoad During Defense", "38 AU/min", "↑ 10 AU vs Offense")
                
                st.divider()
                st.subheader("Recommendations")
                st.markdown("""
                <div class='tactical-card'>
                    - Increase help defense rotations by 15%<br>
                    - Improve weakside communication timing<br>
                    - Reduce closeout distance by 0.5m<br>
                    - Rotate defenders every 3 high-intensity possessions
                </div>
                """, unsafe_allow_html=True)
    
    with tab3:
        st.subheader("Advanced Shot Creation Intelligence")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Shot creation radar chart
            shot_creation_data = {
                'Player': players,
                'Off-Dribble': np.random.uniform(0.4, 0.8, len(players)),
                'Catch-and-Shoot': np.random.uniform(0.5, 0.9, len(players)),
                'Drives': np.random.uniform(0.3, 0.7, len(players)),
                'Screens': np.random.uniform(0.4, 0.75, len(players)),
                'Transition': np.random.uniform(0.6, 0.85, len(players))
            }
            shot_df = pd.DataFrame(shot_creation_data)
            
            fig_radar = go.Figure()
            
            for player in players[:5]:  # Only show 5 players for clarity
                player_data = shot_df[shot_df['Player'] == player]
                fig_radar.add_trace(go.Scatterpolar(
                    r=player_data[['Off-Dribble', 'Catch-and-Shoot', 'Drives', 'Screens', 'Transition']].values[0],
                    theta=['Off-Dribble', 'Catch-and-Shoot', 'Drives', 'Screens', 'Transition'],
                    fill='toself',
                    name=player
                ))
            
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                showlegend=True,
                height=500,
                template='plotly_dark',
                plot_bgcolor=CARD_COLOR,
                paper_bgcolor=CARD_COLOR,
                font=dict(color=TEXT_COLOR)
            )
            st.plotly_chart(fig_radar, use_container_width=True)
            
            # Biometric impact on shot creation
            st.subheader("Physiological Impact on Shot Creation")
            shot_biometric = df[df['action'] == 'shot'].groupby('player').agg({
                'heart_rate': 'mean',
                'velocity': 'mean',
                'success': 'mean'
            }).reset_index()
            
            fig_shot_bio = px.scatter(
                shot_biometric,
                x='heart_rate',
                y='success',
                size='velocity',
                color='player',
                title="Shot Success vs Heart Rate",
                template='plotly_dark',
                trendline='ols',
                color_discrete_sequence=SPAIN_COLORS
            )
            fig_shot_bio.update_layout(
                plot_bgcolor=CARD_COLOR,
                paper_bgcolor=CARD_COLOR,
                font=dict(color=TEXT_COLOR))
            st.plotly_chart(fig_shot_bio, use_container_width=True)
        
        with col2:
            st.subheader("Shot Creation Metrics")
            st.metric("Off-Dribble Efficiency", "1.12 PPP", "↑ 0.08 from avg")
            st.metric("Screen Utilization", "4.2 PPS", "↑ 0.6 from avg")
            st.metric("Drive & Kick Success", "28% AST Rate", "↑ 5% from last")
            
            st.divider()
            st.subheader("Biometric Thresholds")
            st.metric("Optimal HR for Shooting", "145-160 bpm", "↑ 8% efficiency")
            st.metric("Velocity Threshold", ">3.5 m/s", "↑ 15% drive success")
            
            st.divider()
            st.subheader("Player Recommendations")
            st.markdown("""
            <div class='tactical-card'>
                - **Guard A1:** Reduce static time by 15%<br>
                - **Center A4:** Optimize roll timing (peak accel 0.3s after contact)<br>
                - **Forward A3:** Increase corner 3PT attempts by 20%<br>
                - **All Players:** Maintain HR <170 bpm during shot creation
            </div>
            """, unsafe_allow_html=True)

# Enhanced Recovery Metrics Tab
elif analysis_focus == "Recovery Metrics":
    st.subheader("Advanced Recovery Intelligence")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Recovery timeline
        st.subheader("Recovery Profile Timeline")
        fig_recovery = px.line(
            filtered_df,
            x='time',
            y='heart_rate',
            color='player',
            facet_row='position',
            title="Heart Rate Recovery Timeline",
            template='plotly_dark',
            color_discrete_sequence=SPAIN_COLORS
        )
        fig_recovery.update_layout(
            plot_bgcolor=CARD_COLOR,
            paper_bgcolor=CARD_COLOR,
            font=dict(color=TEXT_COLOR))
        st.plotly_chart(fig_recovery, use_container_width=True)
        
        # Recovery rate analysis
        st.subheader("Recovery Rate Analysis")
        high_intensity_df = filtered_df[filtered_df['acceleration'] > 4].copy()
        recovery_data = []
        
        for player in high_intensity_df['player'].unique():
            player_events = high_intensity_df[high_intensity_df['player'] == player]
            for idx, event in player_events.iterrows():
                event_time = event['time']
                post_hr = filtered_df[(filtered_df['player'] == player) & 
                                     (filtered_df['time'] > event_time) & 
                                     (filtered_df['time'] <= event_time + 10)]['heart_rate'].values
                if len(post_hr) > 0:
                    recovery_rate = (event['heart_rate'] - post_hr[-1]) / 10  # bpm per minute
                    recovery_data.append({
                        'player': player,
                        'position': event['position'],
                        'recovery_rate': recovery_rate
                    })
                    
        recovery_df = pd.DataFrame(recovery_data)
        
        if not recovery_df.empty:
            fig_recovery_rate = px.box(
                recovery_df,
                x='position',
                y='recovery_rate',
                color='position',
                title="Recovery Rate by Position (bpm/min)",
                template='plotly_dark',
                color_discrete_sequence=SPAIN_COLORS
            )
            fig_recovery_rate.update_layout(
                plot_bgcolor=CARD_COLOR,
                paper_bgcolor=CARD_COLOR,
                font=dict(color=TEXT_COLOR))
            st.plotly_chart(fig_recovery_rate, use_container_width=True)
            
        # Fatigue analysis
        st.subheader("Fatigue Development")
        fig_fatigue = px.line(
            filtered_df,
            x='time',
            y='fatigue_index',
            color='player',
            title="Fatigue Index Over Time",
            template='plotly_dark',
            color_discrete_sequence=SPAIN_COLORS
        )
        fig_fatigue.update_layout(
            plot_bgcolor=CARD_COLOR,
            paper_bgcolor=CARD_COLOR,
            font=dict(color=TEXT_COLOR))
        st.plotly_chart(fig_fatigue, use_container_width=True)
    
    with col2:
        st.subheader("Recovery Metrics")
        st.metric("Avg Recovery Rate", "32 bpm/min", "↓ 8% from last game")
        st.metric("High Exertion Events", "18", "↓ 2 from last game")
        st.metric("Recovery Efficiency", "78%", "↑ 5% from season avg")
        
        st.divider()
        st.subheader("Recovery Benchmarks")
        st.metric("Elite Recovery Rate", ">40 bpm/min", "Top 10% of players")
        st.metric("Good Recovery Rate", "30-40 bpm/min", "Average players")
        st.metric("Poor Recovery Rate", "<30 bpm/min", "Needs improvement")
        
        st.divider()
        st.subheader("Recovery Recommendations")
        st.markdown("""
        <div class='tactical-card'>
            - **Player A1:** Increase hydration during breaks<br>
            - **Player D3:** Consider reduced minutes in 3rd quarter<br>
            - **Team:** Implement active recovery protocols<br>
            - **All Players:** 5-minute cool-down routine after games
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        st.subheader("Fatigue Thresholds")
        st.metric("Critical Fatigue", "FI >0.8", "↓ 25% performance")
        st.metric("Moderate Fatigue", "FI 0.5-0.8", "↓ 10% performance")
        st.metric("Low Fatigue", "FI <0.5", "Optimal performance")

# Enhanced PlayerLoad Insights Tab
elif analysis_focus == "PlayerLoad Insights":
    st.subheader("Advanced PlayerLoad Intelligence")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # PlayerLoad efficiency by role
        st.subheader("Role-Based PlayerLoad Efficiency")
        eff_df = df[['player', 'offensive_eff', 'defensive_eff', 'role']].dropna()
        
        if not eff_df.empty:
            fig_eff = px.box(
                eff_df,
                x='role',
                y=['offensive_eff', 'defensive_eff'],
                points='all',
                title="PlayerLoad Efficiency by Role",
                labels={'value': 'Efficiency Score', 'variable': 'Efficiency Type'},
                template='plotly_dark',
                color_discrete_sequence=[PRIMARY_COLOR, ACCENT_COLOR]
            )
            fig_eff.update_layout(
                plot_bgcolor=CARD_COLOR,
                paper_bgcolor=CARD_COLOR,
                font=dict(color=TEXT_COLOR))
            st.plotly_chart(fig_eff, use_container_width=True)
        
        else:
            st.warning("No efficiency data available")
            
        # PlayerLoad accumulation patterns
        st.subheader("PlayerLoad Accumulation Patterns")
        fig_pl_accum = px.area(
            filtered_df,
            x='time',
            y='player_load',
            color='player',
            facet_row='position',
            title="PlayerLoad Accumulation by Position",
            template='plotly_dark',
            color_discrete_sequence=SPAIN_COLORS
        )
        fig_pl_accum.update_layout(
            plot_bgcolor=CARD_COLOR,
            paper_bgcolor=CARD_COLOR,
            font=dict(color=TEXT_COLOR))
        st.plotly_chart(fig_pl_accum, use_container_width=True)
        
        # PlayerLoad vs Performance
        st.subheader("PlayerLoad vs Performance Metrics")
        fig_pl_perf = px.scatter(
            filtered_df,
            x='player_load',
            y='velocity',
            color='heart_rate',
            size='acceleration',
            trendline='ols',
            title="PlayerLoad vs Velocity",
            template='plotly_dark',
            color_continuous_scale='viridis'
        )
        fig_pl_perf.update_layout(
            plot_bgcolor=CARD_COLOR,
            paper_bgcolor=CARD_COLOR,
            font=dict(color=TEXT_COLOR))
        st.plotly_chart(fig_pl_perf, use_container_width=True)
    
    with col2:
        st.subheader("PlayerLoad Insights")
        st.metric("Offensive Efficiency", "8.2 AU/m", "↑ 0.4 from last game")
        st.metric("Defensive Efficiency", "7.5 AU/m", "↑ 0.3 from last game")
        st.metric("Total PlayerLoad", "452 AU", "↑ 18% vs Last Game")
        
        st.divider()
        st.subheader("Performance Impact")
        st.markdown("""
        <div class='tactical-card'>
            - **Optimal Load Distribution:** Guards 55% vs Bigs 45%<br>
            - **Efficiency Threshold:** >7.5 reduces opponent PPP by 18%<br>
            - **Game Impact:** 10% ↑ efficiency = +6.2 PPG<br>
            - **Injury Risk:** >500 AU increases injury risk by 40%
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        st.subheader("Load Management")
        st.metric("Max PlayerLoad", "500 AU", "Recommended limit")
        st.metric("Optimal Range", "350-450 AU", "Peak performance zone")
        st.metric("Recovery Needed", "24h rest", "After >450 AU")
        
        st.divider()
        st.subheader("Recommendations")
        st.markdown("""
        <div class='tactical-card'>
            - Rotate guards every 6 minutes<br>
            - Limit centers to 35 minutes when PL >400<br>
            - Implement active recovery for high-load players<br>
            - Monitor PL accumulation in real-time
        </div>
        """, unsafe_allow_html=True)

# Enhanced Team Performance Tab
elif analysis_focus == "Team Performance":
    st.subheader("Advanced Team Performance Intelligence")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Team performance metrics
        st.subheader("Performance Metrics Dashboard")
        metrics_data = {
            'Metric': ['Offensive Efficiency', 'Defensive Efficiency', 'Pace', 'Rebound Rate', 'Turnover Rate', 'Spacing Index'],
            'Value': [112.3, 94.7, 98.4, 52.1, 12.3, 8.2],
            'League Avg': [105.6, 107.2, 96.8, 50.0, 14.2, 7.5],
            'Trend': ['↑', '↑', '↑', '↑', '↓', '↑']
        }
        metrics_df = pd.DataFrame(metrics_data)
        
        fig_metrics = px.bar(
            metrics_df,
            x='Metric',
            y='Value',
            color='Metric',
            title="Team Performance Metrics vs League Average",
            hover_data=['League Avg'],
            template='plotly_dark',
            color_discrete_sequence=SPAIN_COLORS
        )
        fig_metrics.add_trace(go.Scatter(
            x=metrics_df['Metric'],
            y=metrics_df['League Avg'],
            mode='markers',
            marker=dict(size=12, color='white'),
            name='League Avg'
        ))
        fig_metrics.update_layout(
            plot_bgcolor=CARD_COLOR,
            paper_bgcolor=CARD_COLOR,
            font=dict(color=TEXT_COLOR))
        st.plotly_chart(fig_metrics, use_container_width=True)
        
        # Energy expenditure timeline
        st.subheader("Energy Expenditure Timeline")
        energy_df = df.groupby(['time', 'position']).agg({'player_load': 'sum'}).reset_index()
        fig_energy = px.area(
            energy_df,
            x='time',
            y='player_load',
            color='position',
            title="PlayerLoad by Position Over Time",
            template='plotly_dark'
        )
        fig_energy.update_layout(
            plot_bgcolor=CARD_COLOR,
            paper_bgcolor=CARD_COLOR,
            font=dict(color=TEXT_COLOR))
        st.plotly_chart(fig_energy, use_container_width=True)
        
        # Lineup efficiency
        st.subheader("Lineup Efficiency Analysis")
        lineup_data = {
            'Lineup': ['Starters', 'Bench Unit 1', 'Small Ball', 'Defensive Unit'],
            'Offensive Rating': [115.2, 108.7, 112.4, 102.3],
            'Defensive Rating': [95.4, 102.1, 98.7, 89.4],
            'Net Rating': [19.8, 6.6, 13.7, 12.9],
            'PlayerLoad/min': [4.2, 3.8, 4.5, 4.1]
        }
        lineup_df = pd.DataFrame(lineup_data)
        
        fig_lineup = px.scatter(
            lineup_df,
            x='Offensive Rating',
            y='Defensive Rating',
            size='Net Rating',
            color='Lineup',
            hover_data=['PlayerLoad/min'],
            title="Lineup Efficiency Profiles",
            template='plotly_dark',
            color_discrete_sequence=SPAIN_COLORS
        )
        fig_lineup.update_layout(
            plot_bgcolor=CARD_COLOR,
            paper_bgcolor=CARD_COLOR,
            font=dict(color=TEXT_COLOR))
        st.plotly_chart(fig_lineup, use_container_width=True)
    
    with col2:
        st.subheader("Team Performance")
        st.metric("Offensive Rating", "112.3", "↑ 6.7 vs League")
        st.metric("Defensive Rating", "94.7", "↓ 12.5 vs League")
        st.metric("Net Rating", "+17.6", "↑ 19.2 vs League")
        st.metric("Pace", "98.4", "↑ 1.6 vs League")
        
        st.divider()
        st.subheader("Key Observations")
        st.markdown("""
        <div class='tactical-card'>
            - **Offense:** Top 10% in efficiency<br>
            - **Defense:** Top 5% in efficiency<br>
            - **Transition:** #1 in fast break points<br>
            - **Clutch:** +12.5 net rating in last 5 min<br>
            - **Fatigue Management:** 15% better than league avg
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        st.subheader("Tactical Adjustments")
        st.markdown("""
        <div class='tactical-card'>
            - Switch to zone defense when load >4.0/min<br>
            - Target 65% of screens in paint (current 48%)<br>
            - Limit consecutive high-intensity bursts to ≤3<br>
            - Redistribute rebound duties: A5 ORB load = 2.1× avg<br>
            - Implement 8-player rotation to manage fatigue
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        st.subheader("Biometric Insights")
        st.metric("Avg Heart Rate", "162 bpm", "Optimal for performance")
        st.metric("PlayerLoad Distribution", "Guards 55%, Bigs 45%", "Ideal balance")
        st.metric("Recovery Efficiency", "78%", "↑ 8% from last season")

# Add footer
st.divider()
st.markdown("""
    <div class='footer'>
        <b>Advanced Basketball Intelligence System v5.0</b><br>
        <i>Spanish National Team - Integrated Physiological & Tactical Analysis</i><br>
        Developed with Streamlit, Plotly, and Scikit-Learn
    </div>
""", unsafe_allow_html=True)