import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from utils.charts import create_court_figure

# --- Color Definitions ---
THEME_PRIMARY = "#FF6B6B"
SPAIN_RED = "#C60B1E"
SPAIN_BLUE = "#004D98"

def render(df, time_range):
    """Renders the complete Tactical Insights page with all original analyses."""
    st.subheader("Advanced Tactical Intelligence")
    df_filtered = df[(df['time'] >= time_range[0]) & (df['time'] <= time_range[1])]

    tab1, tab2, tab3 = st.tabs(["Pick-and-Roll", "Defensive Execution", "Shot Creation"])

    with tab1:
        st.markdown("<h4>Pick-and-Roll Intelligence</h4>", unsafe_allow_html=True)
        pnr_df = df_filtered[df_filtered['tactical_situation'] == 'Pick-and-Roll']
        if not pnr_df.empty:
            with st.container():
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("<h5>Player Velocity During PnR</h5>", unsafe_allow_html=True)
                fig_pnr = px.line(
                    pnr_df, x='time', y='velocity', color='player', facet_row='role',
                    template="plotly_white", hover_data=['action', 'heart_rate'],
                    color_discrete_sequence=px.colors.qualitative.Vivid
                )
                st.plotly_chart(fig_pnr, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with st.container():
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("<h5>Physiological Demand During PnR</h5>", unsafe_allow_html=True)
                pl_df = pnr_df.groupby(['player', 'role']).agg(
                    player_load=('player_load', 'sum'),
                    exertion_index=('exertion_index', 'max')
                ).reset_index()
                fig_pl = px.bar(
                    pl_df, x='player', y='player_load', color='role', barmode='group',
                    template="plotly_white", hover_data=['exertion_index'],
                    color_discrete_map={'Offense': SPAIN_RED, 'Defense': SPAIN_BLUE}
                )
                st.plotly_chart(fig_pl, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No Pick-and-Roll data available in the selected time range.")

    with tab2:
        st.markdown("<h4>Defensive Execution Intelligence</h4>", unsafe_allow_html=True)
        defense_df = df_filtered[df_filtered['player'].str.startswith('D')]
        if not defense_df.empty:
            with st.container():
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("<h5>Defensive Positioning Heatmap</h5>", unsafe_allow_html=True)
                fig_heatmap = px.density_heatmap(
                    defense_df, x='x', y='y', nbinsx=28, nbinsy=15,
                    color_continuous_scale="Reds", histfunc="count"
                )
                court_fig = create_court_figure()
                for trace in court_fig.data: fig_heatmap.add_trace(trace)
                for shape in court_fig.layout.shapes: fig_heatmap.add_shape(shape)
                fig_heatmap.update_layout(template="plotly_white", title_text="")
                st.plotly_chart(fig_heatmap, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with st.container():
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("<h5>Defensive Efficiency Profile</h5>", unsafe_allow_html=True)
                eff_df = defense_df.groupby('player').agg(
                    defensive_eff=('defensive_eff', 'mean'),
                    velocity=('velocity', 'mean'),
                    acceleration=('acceleration', 'max')
                ).reset_index()
                fig_eff = px.scatter(
                    eff_df, x='velocity', y='defensive_eff', size='acceleration',
                    color='player', title="Defensive Efficiency Profile", hover_name='player',
                    template="plotly_white", color_discrete_sequence=px.colors.qualitative.Dark24
                )
                st.plotly_chart(fig_eff, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No defensive player data available in the selected time range.")

    with tab3:
        st.markdown("<h4>Advanced Shot Creation Intelligence (Simulated)</h4>", unsafe_allow_html=True)
        players = df_filtered['player'].unique()
        if len(players) > 0:
            with st.container():
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("<h5>Shot Creation Profile</h5>", unsafe_allow_html=True)
                np.random.seed(42)
                shot_data = {
                    'Player': players,
                    'Off-Dribble Shots': np.random.randint(3, 12, len(players)),
                    'Catch-and-Shoot': np.random.randint(5, 15, len(players)),
                    'Drives per Game': np.random.randint(8, 20, len(players)),
                    'FG% Off Screens': np.random.uniform(0.35, 0.55, len(players)),
                }
                shot_df = pd.DataFrame(shot_data)
                
                fig_radar = go.Figure()
                categories = ['Off-Dribble Shots', 'Catch-and-Shoot', 'Drives per Game', 'FG% Off Screens']
                for i, player in enumerate(shot_df['Player']):
                    player_data = shot_df[shot_df['Player'] == player]
                    values = player_data[categories].values.flatten().tolist()
                    fig_radar.add_trace(go.Scatterpolar(
                        r=values, theta=categories, fill='toself', name=player,
                        line=dict(color=px.colors.qualitative.Bold[i % len(px.colors.qualitative.Bold)])
                    ))
                fig_radar.update_layout(template="plotly_white", polar=dict(radialaxis=dict(visible=True, range=[0, 20])))
                st.plotly_chart(fig_radar, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No player data available to generate shot creation profiles.")