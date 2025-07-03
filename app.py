import streamlit as st
from streamlit_navigation_bar import st_navbar
from streamlit_extras.bottom_container import bottom
from pathlib import Path

st.set_page_config(
    layout="wide",
    page_icon="assets/eand-logo/small/Red/e&-lockup_Enterprise_engl_vert_red_rgb-cropped.svg"
)

BASE_DIR = Path(__file__).parent

with open(BASE_DIR / "assets" / "style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

ALL_PAGES = [
    st.Page(
        page="app_pages/Home_.py",
        title="AMPA - Automatic Market Procurement Agent"
        ),
    st.Page(
        page="app_pages/Demo_.py",
        title="Shop & Chat Interface"
        ),
]


ALL_PAGES_TITLE_KEY = [
    "Home",
    "Demo",
]


# Initialize session state for navigation if it doesn't exist
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

stNavbarOut = st_navbar(
    ALL_PAGES_TITLE_KEY,
    logo_path=str(BASE_DIR / "assets" / "eand-logo" / "small" / "White" / "e&-lockup_Enterprise_engl_vert_White_rgb-cropped.svg"),
    logo_page=None,
    options={
        "show_menu": False,
        "use_padding": True,
    },
    styles={
        "nav": {
            "justify-content": "left",
            "margin-bottom": "40 rem",
        },
        "span": {
            "border-radius": "0.5rem",
            "padding": "0.625rem",
        },
        "active": {
            "background-color": "rgba(255, 255, 255, 0.25)",
        },
        "hover": {
            "background-color": "rgba(255, 255, 255, 0.1)",
        },
    },
    key="navBarMain",
)

st.container(height=10, border=False)


def getPage(navBarPageSelected: str):
    for i in range(0, len(ALL_PAGES_TITLE_KEY)):
        if navBarPageSelected == ALL_PAGES_TITLE_KEY[i]:
            return (ALL_PAGES[i])
    return (None)


# Handle navigation when navbar selection changes
if st.session_state["navBarMain"] and st.session_state["navBarMain"][0]:
    selected_page = st.session_state["navBarMain"][0]
    if selected_page != st.session_state.current_page:
        st.session_state.current_page = selected_page
        pageToSwitch = getPage(selected_page)
        if pageToSwitch:
            st.switch_page(pageToSwitch)

# st.write(st.session_state)

# with bottom():
#     st.divider()
#     footer_col1, footer_col2, footer_col3 = st.columns(3)

#     with footer_col1:
#         st.text("AMPA - Automatic Market Procurement Agent")

#     with footer_col2:
#         st.text("Privacy Policy | Terms of Service")

#     with footer_col3:
#         st.text("© 2025 e& Enterprise")

# Use the navigation component
pg = st.navigation(ALL_PAGES)
pg.run()
