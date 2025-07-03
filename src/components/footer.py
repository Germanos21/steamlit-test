import streamlit as st


def streamlit_footer():
    st.divider()
    footer_col1, footer_col2, footer_col3, footer_col4 = st.columns(4, gap="small", vertical_alignment="center")

    with footer_col1:
        st.link_button("AMPA - Automatic Market Procurement Agent", "/", type="tertiary")

    with footer_col2:
        st.link_button("Terms of Service", "https://www.eandenterprise.com/en/general/general-terms.html", type="tertiary")

    with footer_col3:
        st.link_button("Privacy Policy", "https://www.eandenterprise.com/en/general/privacy-policy.html", type="tertiary")

    with footer_col4:
        # st.text("© 2025 e& Enterprise")
        st.link_button("© 2025 e& Enterprise", "https://www.eandenterprise.com/en/index.html", type="tertiary")
