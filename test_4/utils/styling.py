import streamlit as st
import os

def load_css(file_path):
    """Loads a CSS file and injects it into the Streamlit app."""
    try:
        with open(file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"CSS file not found at {file_path}")

def card_container():
    """Returns a Streamlit container with the 'card' class for styling."""
    return st.container()

def inject_custom_css():
    """A wrapper function to load all necessary CSS."""
    css_path = os.path.join("styles", "main.css")
    load_css(css_path)

def render_header(title, subtitle):
    """Renders a styled main page header."""
    st.markdown(
        f"""
        <div style="text-align: left; margin-bottom: 2rem;">
            <h1 style="color: #262730; font-size: 2.5rem; font-weight: 700;">{title}</h1>
            <p style="color: #555; font-size: 1.1rem;">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True
    )