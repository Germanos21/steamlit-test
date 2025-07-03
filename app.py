import streamlit as st
from pathlib import Path

st.set_page_config(
    layout="wide",
    page_icon="assets/eand-logo/small/Red/e&-lockup_Enterprise_engl_vert_red_rgb-cropped.svg"
)

BASE_DIR = Path(__file__).parent

with open(BASE_DIR / "assets" / "style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Inject global responsive CSS for text scaling
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
  font-size: clamp(14px, 1.2vw, 18px);
}
h1, .stMarkdown h1 {
  font-size: clamp(2rem, 4vw, 3rem) !important;
}
h2, .stMarkdown h2 {
  font-size: clamp(1.5rem, 3vw, 2.5rem) !important;
}
h3, .stMarkdown h3 {
  font-size: clamp(1.2rem, 2.5vw, 2rem) !important;
}
.stMarkdown, .stCaption, .stTextInput, .stSelectbox, .stSlider, .stButton, .stMetric, .stRadio, .stNumberInput {
  font-size: clamp(1rem, 2vw, 1.3rem) !important;
}
.stButton>button {
  font-size: clamp(1rem, 2vw, 1.3rem) !important;
}
</style>
""", unsafe_allow_html=True)

# You can add main page content here if you want a landing page.
st.title("Welcome to AMPA - Automatic Market Procurement Agent")
st.write("Use the sidebar to navigate between pages.")
