import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def render(df, time_range):
    """Renders the Team Performance page."""
    st.markdown("<h3>Advanced Team Performance Intelligence</h3>", unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<h4>Performance Metrics Dashboard (Simulated)</h4>", unsafe_allow_html=True)
        metrics_data = {
            'Metric': ['Offensive Efficiency', 'Defensive Efficiency', 'Pace', 'Rebound Rate', 'Turnover Rate'],
            'Value': [112.3, 94.7, 98.4, 52.1, 12.3],
            'League Avg': [105.6, 107.2, 96.8, 50.0, 14.2]
        }
        metrics_df = pd.DataFrame(metrics_data)
        fig_metrics = px.bar(
            metrics_df, x='Metric', y='Value', color='Metric',
            template="plotly_white", title="Team Performance Metrics vs. League Average",
            hover_data=['League Avg']
        )
        fig_metrics.add_trace(go.Scatter(
            x=metrics_df['Metric'], y=metrics_df['League Avg'],
            mode='markers', marker=dict(size=12, color='black', symbol='diamond'), name='League Avg'
        ))
        st.plotly_chart(fig_metrics, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<h4>Lineup Efficiency Analysis (Simulated)</h4>", unsafe_allow_html=True)
        lineup_data = {
            'Lineup': ['Starters', 'Bench Unit 1', 'Small Ball', 'Defensive Unit'],
            'Offensive Rating': [115.2, 108.7, 112.4, 102.3],
            'Defensive Rating': [95.4, 102.1, 98.7, 89.4],
            'Net Rating': [19.8, 6.6, 13.7, 12.9],
            'PlayerLoad/min': [4.2, 3.8, 4.5, 4.1]
        }
        lineup_df = pd.DataFrame(lineup_data)
        fig_lineup = px.scatter(
            lineup_df, x='Offensive Rating', y='Defensive Rating',
            size='Net Rating', color='Lineup', hover_data=['PlayerLoad/min'],
            template="plotly_white", title="Lineup Efficiency Profiles (Bubble size = Net Rating)",
            size_max=50
        )
        # Invert y-axis because lower defensive rating is better
        fig_lineup.update_yaxes(autorange="reversed")
        st.plotly_chart(fig_lineup, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<h4>AI-Generated Team Insights</h4>", unsafe_allow_html=True)
        st.markdown("""
        - **Optimal Rotation Pattern:** 6-minute intervals for starting guards maximizes performance before fatigue-related decline.
        - **Fatigue Threshold:** Team shooting efficiency drops by 15% when average PlayerLoad exceeds 450 per player.
        - **Defensive Synergy:** The D4-D5 frontcourt pairing reduces opponent points in the paint by 12%.
        - **Clutch Performance:** In the last 5 minutes, offensive efficiency increases by 18% when the primary ball-handler's heart rate is below 165 bpm.
        """)
        st.markdown('</div>', unsafe_allow_html=True)