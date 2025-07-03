import streamlit as st


def streamlit_logo(logoBigUrl: str, logoSmallUrl: str):
    logoExpandedUrl = "assets/eand-logo/large/White/e& enterprise_logo_white.png"
    logoMinimizedUrl = "assets/eand-logo/small/White/e&-lockup_Enterprise_engl_vert_White_rgb.png"

    st.logo(
        logoBigUrl,
        size="large",
        icon_image=logoSmallUrl,
    )
