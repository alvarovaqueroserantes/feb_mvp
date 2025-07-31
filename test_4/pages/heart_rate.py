import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.cluster import KMeans

# --- Color Definitions ---
THEME_PRIMARY = "#FF6B6B"
THEME_SECONDARY = "#4ECDC4"

def render(df, time_range):
    """Renders the Heart Rate Analysis page."""
    st.markdown("<h3>Advanced Heart Rate Performance Intelligence</h3>", unsafe_allow_html=True)
    df_filtered = df[(df['time'] >= time_range[0]) & (df['time'] <= time_range[1])]

    col1, col2 = st.columns(2)

    with col1:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("<h4>Heart Rate vs. Shooting Efficiency</h4>", unsafe_allow_html=True)
            shots_df = df_filtered[df_filtered['success'] >= 0]
            if not shots_df.empty:
                fig_hr_shot = px.scatter(
                    shots_df, x='heart_rate', y='success', color='zone', facet_col='player',
                    facet_col_wrap=4, trendline='ols', template="plotly_white",
                    labels={'success': 'Shot Success (1=Made)', 'heart_rate': 'Heart Rate (bpm)'},
                    title="Shooting Success by Heart Rate and Court Zone"
                )
                fig_hr_shot.update_traces(marker=dict(size=8, opacity=0.7))
                st.plotly_chart(fig_hr_shot, use_container_width=True)

                st.markdown("<h4>Optimal HR Threshold Analysis</h4>", unsafe_allow_html=True)
                thresholds, results = np.arange(140, 190, 5), []
                for thresh in thresholds:
                    below = shots_df[shots_df['heart_rate'] < thresh]['success'].mean()
                    above = shots_df[shots_df['heart_rate'] >= thresh]['success'].mean()
                    results.append({'Threshold': thresh, 'FG% Below': below, 'FG% Above': above, 'Difference': below - above})

                results_df = pd.DataFrame(results)
                fig_thresh = px.line(
                    results_df.melt(id_vars='Threshold'), x='Threshold', y='value', color='variable',
                    template="plotly_white", title="Shooting Efficiency by HR Threshold",
                    labels={'value': 'Field Goal %', 'variable': 'Metric'}
                )
                st.plotly_chart(fig_thresh, use_container_width=True)
                optimal_thresh = results_df.iloc[results_df['Difference'].idxmax()]
                st.success(f"**Optimal Performance Threshold:** Shooting efficiency drops most significantly above **{optimal_thresh['Threshold']} bpm**.")

            else:
                st.warning("No shot data available in selected time range.")
            st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("<h4>Heart Rate Response to Game Events</h4>", unsafe_allow_html=True)
            events = df_filtered[df_filtered['action'].isin(['shot', 'foul', 'turnover', 'steal'])].copy()
            if not events.empty:
                event_hr_data = []
                for _, event in events.iterrows():
                    player, event_time = event['player'], event['time']
                    pre_hr = df_filtered[(df_filtered['player'] == player) & (df_filtered['time'].between(event_time - 5, event_time - 1))]['heart_rate'].mean()
                    post_hr = df_filtered[(df_filtered['player'] == player) & (df_filtered['time'].between(event_time + 1, event_time + 5))]['heart_rate'].mean()
                    if pd.notna(pre_hr) and pd.notna(post_hr):
                        event_hr_data.append({'Player': player, 'Event': event['action'], 'HR_Change': post_hr - pre_hr, 'Pre_HR': pre_hr})

                if event_hr_data:
                    event_hr_df = pd.DataFrame(event_hr_data)
                    fig_hr_event = px.box(
                        event_hr_df, x='Event', y='HR_Change', color='Event',
                        template="plotly_white", title="Heart Rate Change After Key Events",
                        labels={'HR_Change': 'HR Change (bpm)'}
                    )
                    st.plotly_chart(fig_hr_event, use_container_width=True)

                    st.markdown("<h4>Player Recovery Profiles</h4>", unsafe_allow_html=True)
                    recovery_df = event_hr_df.groupby('Player').agg({'HR_Change': 'mean', 'Pre_HR': 'mean'}).reset_index()
                    if len(recovery_df) > 2:
                        kmeans = KMeans(n_clusters=min(3, len(recovery_df)), random_state=42, n_init=10)
                        recovery_df['cluster'] = kmeans.fit_predict(recovery_df[['HR_Change', 'Pre_HR']]).astype(str)
                        fig_recovery_cluster = px.scatter(
                            recovery_df, x='Pre_HR', y='HR_Change', color='cluster', text='Player',
                            template="plotly_white", title="Player Recovery Style Clustering",
                            labels={'Pre_HR': 'Average Pre-Event HR', 'HR_Change': 'Average HR Change'}
                        )
                        fig_recovery_cluster.update_traces(textposition='top center')
                        st.plotly_chart(fig_recovery_cluster, use_container_width=True)
                else:
                    st.info("Not enough data to calculate HR change around events.")
            else:
                st.warning("No key game events in selected time range.")
            st.markdown('</div>', unsafe_allow_html=True)