import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.preprocessing import StandardScaler

# --- Color Definitions ---
THEME_PRIMARY = "#FF6B6B"
THEME_SECONDARY = "#4ECDC4"
THEME_ACCENT = "#45AAF2"
SPAIN_RED = "#C60B1E"
SPAIN_BLUE = "#004D98"
SPAIN_YELLOW = "#FFC400"

def render(df, ai_models, selected_model_name):
    """Renders the complete overview page, merging original analysis with new design."""
    st.subheader("Game Performance Summary")
    
    # --- Top-level KPIs ---
    if not df.empty:
        col1, col2, col3, col4 = st.columns(4)
        avg_hr = df['heart_rate'].mean()
        max_vel = df['velocity'].max()
        total_pl = df['player_load'].sum()
        off_eff = df['offensive_eff'].mean(skipna=True)
        def_eff = df['defensive_eff'].mean(skipna=True)

        with col1:
            st.metric("Avg Heart Rate", f"{avg_hr:.0f} bpm", f"{'High' if avg_hr > 170 else 'Optimal' if avg_hr > 150 else 'Low'}")
        with col2:
            st.metric("Max Velocity", f"{max_vel:.1f} m/s", f"{'Explosive' if max_vel > 6.0 else 'Moderate'}")
        with col3:
            st.metric("Total PlayerLoad", f"{total_pl:.0f}", f"{'High' if total_pl > 500 else 'Moderate'}")
        with col4:
            eff_value = off_eff if not np.isnan(off_eff) else def_eff
            eff_label = "Offensive" if not np.isnan(off_eff) else "Defensive"
            st.metric(f"{eff_label} Efficiency", f"{eff_value:.2f}" if not np.isnan(eff_value) else "N/A", f"{'Excellent' if not np.isnan(eff_value) and eff_value > 8.0 else 'Good'}")
    else:
        st.warning("No data available for the selected filters.")
        return

    st.markdown("---")
    
    # --- Main Layout ---
    main_col, side_col = st.columns([3, 1])

    with main_col:
        # --- Player Efficiency Bar Chart ---
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("<h4>Player Efficiency Analysis</h4>", unsafe_allow_html=True)
            eff_df = df.groupby('player').agg(offensive_eff=('offensive_eff', 'mean'), defensive_eff=('defensive_eff', 'mean')).reset_index().melt(id_vars='player', var_name='efficiency_type', value_name='efficiency')
            if not eff_df.dropna().empty:
                fig_eff = px.bar(
                    eff_df.dropna(), x='player', y='efficiency', color='efficiency_type', barmode='group',
                    color_discrete_map={'offensive_eff': SPAIN_RED, 'defensive_eff': SPAIN_BLUE},
                    labels={'efficiency': 'Efficiency Score', 'efficiency_type': 'Efficiency Type', 'player': 'Player'},
                    template="plotly_white"
                )
                fig_eff.update_layout(legend_title_text='')
                st.plotly_chart(fig_eff, use_container_width=True)
            else:
                st.info("No efficiency data to display for the current selection.")
            st.markdown('</div>', unsafe_allow_html=True)

        # --- Tactical Insights Text ---
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("<h4>Tactical Performance Insights</h4>", unsafe_allow_html=True)
            st.markdown("""
            - **Pick-and-Roll Execution:** A1's acceleration increased by 40% during drive phase.
            - **Defensive Coordination:** D4-D5 communication gap (1.2s) exploited in 3 possessions.
            - **Shooting Efficiency:** Corner 3PT% 48% vs Wing 3PT% 35%.
            - **PlayerLoad Distribution:** Guards carry 55% of offensive load vs 45% for bigs.
            - **Recovery Patterns:** Backcourt recovers 25% faster after high-intensity sprints.
            """)
            st.markdown('</div>', unsafe_allow_html=True)

    with side_col:
        # --- Static KPIs ---
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("<h4>Performance Indicators</h4>", unsafe_allow_html=True)
            st.metric("Offensive Efficiency", "1.12 PPP", "↑ 0.08 vs Avg")
            st.metric("Defensive Efficiency", "0.89 PPP", "↓ 0.11 vs Avg")
            st.metric("Transition Success", "68%", "↑ 12% vs Avg")
            st.metric("Set Play Success", "54%", "↓ 3% vs Avg")
            st.markdown('</div>', unsafe_allow_html=True)

        # --- Player Load Pie Chart ---
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("<h4>Player Load Distribution</h4>", unsafe_allow_html=True)
            pl_df = df.groupby('player')['player_load'].sum().reset_index()
            if not pl_df.empty:
                fig_pl = px.pie(
                    pl_df, names='player', values='player_load', hole=0.4,
                    color_discrete_sequence=[THEME_PRIMARY, THEME_SECONDARY, THEME_ACCENT, SPAIN_YELLOW, "#264653"],
                    template="plotly_white"
                )
                fig_pl.update_layout(legend_title_text='Player', showlegend=False)
                fig_pl.update_traces(textinfo='percent+label', textposition='inside')
                st.plotly_chart(fig_pl, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # --- AI Clustering Section ---
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"<h4>AI Player Profiling: {selected_model_name}</h4>", unsafe_allow_html=True)
        cluster_df = df.groupby('player').agg({
            'heart_rate': 'mean', 'velocity': 'mean', 'acceleration': 'max',
            'player_load': 'sum', 'offensive_eff': 'mean', 'defensive_eff': 'mean'
        }).reset_index().dropna()

        if len(cluster_df) > 2:
            scaler = StandardScaler()
            # Ensure we only scale numeric columns, excluding 'player'
            numeric_cols = cluster_df.select_dtypes(include=np.number).columns
            scaled_data = scaler.fit_transform(cluster_df[numeric_cols])
            
            model = ai_models[selected_model_name]

            if selected_model_name in ["PCA", "t-SNE"]:
                transformed = model.fit_transform(scaled_data)
                cluster_df['dim1'], cluster_df['dim2'] = transformed[:, 0], transformed[:, 1]
                fig_cluster = px.scatter(
                    cluster_df, x='dim1', y='dim2', text='player', color='player',
                    title=f"{selected_model_name} Player Profiling", template="plotly_white",
                    color_discrete_sequence=px.colors.qualitative.Vivid
                )
                fig_cluster.update_traces(textposition='top center')
            else:  # KMeans or DBSCAN
                clusters = model.fit_predict(scaled_data)
                cluster_df['cluster'] = clusters.astype(str)
                fig_cluster = px.scatter(
                    cluster_df, x='heart_rate', y='player_load', color='cluster',
                    size='velocity', hover_name='player', title=f"{selected_model_name} Player Clustering",
                    template="plotly_white", color_discrete_sequence=px.colors.qualitative.Bold
                )
            st.plotly_chart(fig_cluster, use_container_width=True)
        else:
            st.warning("Insufficient unique player data for AI clustering. Select 'All Players' or a larger time range.")
        st.markdown('</div>', unsafe_allow_html=True)