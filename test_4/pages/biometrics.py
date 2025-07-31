import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
from sklearn.cluster import KMeans

# --- Color Definitions ---
THEME_PRIMARY = "#FF6B6B"
THEME_SECONDARY = "#4ECDC4"
SPAIN_YELLOW = "#FFC400"
SPAIN_BLUE = "#004D98"

def render(df, selected_player):
    """Renders the complete Player Biometrics page with all original analyses."""
    
    if selected_player == 'All Players':
        st.info("Please select a specific player from the sidebar to view detailed biometric data.")
        return

    player_df = df.copy()
    if player_df.empty:
        st.warning("No data available for the selected player in the specified time range.")
        return

    st.subheader(f"Advanced Physiological Metrics for {selected_player}")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Heart Rate", "Velocity", "Acceleration", "PlayerLoad"])

    with tab1:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("<h4>Heart Rate with Game Context</h4>", unsafe_allow_html=True)
            fig_hr = px.line(player_df, x='time', y='heart_rate', markers=True, template="plotly_white",
                             hover_data=['action', 'tactical_situation', 'zone'])
            fig_hr.update_traces(line_color=THEME_PRIMARY)

            for situation in player_df['tactical_situation'].unique():
                sit_df = player_df[player_df['tactical_situation'] == situation]
                if not sit_df.empty:
                    fig_hr.add_vrect(
                        x0=sit_df['time'].min(), x1=sit_df['time'].max(),
                        fillcolor=SPAIN_YELLOW if situation == "Pick-and-Roll" else SPAIN_BLUE,
                        opacity=0.15, line_width=0, annotation_text=situation, annotation_position="top left"
                    )
            
            fig_hr.update_layout(xaxis_title="Time (seconds)", yaxis_title="Heart Rate (bpm)", hovermode="x unified")
            st.plotly_chart(fig_hr, use_container_width=True)
            
            st.markdown("---")
            st.markdown("<h4>Performance Analysis by HR Zone</h4>", unsafe_allow_html=True)
            hr_zones_bins = [0, 140, 160, 180, 220] # Expanded top bin
            hr_zones_labels = ['Optimal (<140)', 'Effective (140-160)', 'High Stress (160-180)', 'Critical (>180)']
            player_df['hr_zone'] = pd.cut(player_df['heart_rate'], bins=hr_zones_bins, labels=hr_zones_labels)
            
            zone_stats = player_df.groupby('hr_zone').agg(
                Avg_Velocity=('velocity', 'mean'), Max_Acceleration=('acceleration', 'max'),
                Shooting_Pct=('success', lambda x: x[x != -1].mean() if len(x[x != -1]) > 0 else np.nan),
                Avg_PlayerLoad=('player_load', 'mean')
            ).reset_index()
            
            st.dataframe(zone_stats.style.format({
                'Avg_Velocity': '{:.2f}', 'Max_Acceleration': '{:.2f}',
                'Shooting_Pct': '{:.1%}', 'Avg_PlayerLoad': '{:.2f}'
            }), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("<h4>Velocity & Acceleration Profile</h4>", unsafe_allow_html=True)
            fig_vel = go.Figure()
            fig_vel.add_trace(go.Scatter(x=player_df['time'], y=player_df['velocity'], name='Velocity', line=dict(color=THEME_PRIMARY)))
            fig_vel.add_trace(go.Scatter(x=player_df['time'], y=player_df['acceleration'], name='Acceleration', yaxis='y2', line=dict(color=THEME_SECONDARY, dash='dash')))
            
            fig_vel.update_layout(template="plotly_white", xaxis_title="Time (seconds)",
                                  yaxis=dict(title='Velocity (m/s)'),
                                  yaxis2=dict(title='Acceleration (m/s²)', overlaying='y', side='right'),
                                  hovermode="x unified", legend=dict(x=0, y=1.1, orientation='h'))
            st.plotly_chart(fig_vel, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("<h4>Acceleration by Game Situation</h4>", unsafe_allow_html=True)
            fig_acc_box = px.box(player_df, x='tactical_situation', y='acceleration', color='tactical_situation',
                                 points="all", template="plotly_white")
            st.plotly_chart(fig_acc_box, use_container_width=True)

            st.markdown("---")
            st.markdown("<h4>Statistical Significance (ANOVA)</h4>", unsafe_allow_html=True)
            situations = player_df['tactical_situation'].unique()
            if len(situations) > 1:
                groups = [player_df[player_df['tactical_situation'] == s]['acceleration'].dropna() for s in situations]
                # Ensure all groups have data before running ANOVA
                groups = [g for g in groups if len(g) > 1]
                if len(groups) > 1:
                    f_val, p_val = stats.f_oneway(*groups)
                    c1, c2 = st.columns(2)
                    c1.metric("F-Statistic", f"{f_val:.2f}")
                    c2.metric("P-Value", f"{p_val:.4f}", "Significant" if p_val < 0.05 else "Not Significant")
                else:
                    st.info("Not enough data across different situations to perform ANOVA test.")
            st.markdown('</div>', unsafe_allow_html=True)

    with tab4:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("<h4>PlayerLoad vs. Performance Metrics</h4>", unsafe_allow_html=True)
            fig_pl_perf = px.scatter(
                player_df, x='player_load', y='velocity', size='acceleration',
                color='heart_rate', trendline='ols', template="plotly_white",
                color_continuous_scale=px.colors.sequential.OrRd,
                hover_data=['time', 'tactical_situation']
            )
            st.plotly_chart(fig_pl_perf, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)