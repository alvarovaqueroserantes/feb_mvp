import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans

# --- Color Definitions ---
THEME_PRIMARY = "#FF6B6B"
THEME_SECONDARY = "#4ECDC4"
THEME_ACCENT = "#45AAF2"

def render(df):
    """Renders the Recovery Metrics page."""
    st.markdown("<h3>Advanced Physiological Recovery Intelligence</h3>", unsafe_allow_html=True)

    recovery_df = df[df['recovery_phase'] != 'Normal'].copy()

    if recovery_df.empty:
        st.info("No significant exertion or recovery phases detected in the selected timeframe.")
        return

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<h4>Player Recovery Profiles</h4>", unsafe_allow_html=True)
        fig_recovery = px.scatter(
            recovery_df, x='time', y='heart_rate', color='recovery_phase',
            size='exertion_index', facet_row='player', template="plotly_white",
            title="Recovery & High Exertion Phases by Player",
            hover_data=['tactical_situation'],
            color_discrete_map={'High Exertion': THEME_PRIMARY, 'Recovery Phase': THEME_SECONDARY}
        )
        st.plotly_chart(fig_recovery, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<h4>Recovery Performance Metrics</h4>", unsafe_allow_html=True)
        metrics_df = recovery_df.groupby('player').agg(
            Recovery_Rate=('heart_rate', lambda x: (x.max() - x.min()) / len(x) if len(x) > 0 else 0),
            Recovery_Events=('time', 'count'),
            Avg_Exertion=('exertion_index', 'mean')
        ).reset_index()

        fig_metrics = px.bar(
            metrics_df, x='Player', y=['Recovery_Rate', 'Recovery_Events'], barmode='group',
            template="plotly_white", title="Recovery Metrics Comparison"
        )
        st.plotly_chart(fig_metrics, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<h4>Recovery Profile Clustering (AI)</h4>", unsafe_allow_html=True)
        if len(metrics_df) > 2:
            kmeans = KMeans(n_clusters=min(3, len(metrics_df)), random_state=42, n_init=10)
            metrics_df['cluster'] = kmeans.fit_predict(metrics_df[['Recovery_Rate', 'Recovery_Events', 'Avg_Exertion']]).astype(str)
            fig_cluster = px.scatter_3d(
                metrics_df, x='Recovery_Rate', y='Recovery_Events', z='Avg_Exertion',
                color='cluster', text='Player', title="3D Recovery Profile Clusters",
                template="plotly_white"
            )
            fig_cluster.update_traces(textposition='top center')
            st.plotly_chart(fig_cluster, use_container_width=True)
        else:
            st.warning("Not enough data to perform clustering on recovery profiles.")
        st.markdown('</div>', unsafe_allow_html=True)