import streamlit as st
from src.components.footer import streamlit_footer
from src.components.roi import streamlit_roi_ver10
from pathlib import Path
import os

BASE_DIR = Path(__file__).parent.parent
os.chdir(str(BASE_DIR))

header_col1, header_col2 = st.columns([1, 3], gap="large")

with header_col1:
    st.image(
        image="assets/images/ampa-logos/ampa-square-ver2.png",
        use_container_width=True,
        output_format="JPEG",
        # caption="AMPA Logo",
    )

with header_col2:
    st.title("Streamline Your Supplier Discovery Process with AMPA")
    # st.title("Automatic Market Procurement Agent")
    st.text("Tired of spending up to 48 hours on manual procurement?")
    st.text(
        "Automatic Market Procurement Agent, or AMPA for short, communicates with suppliers for you and provides data-driven insights to save you time and money."
    )

st.divider()

# Main content in tabs
tabs = st.tabs(["Overview", "Features", "Benefits", "Get In Touch"])

# Overview Tab
with tabs[0]:
    col1, col2 = st.columns([2, 3], gap="large")

    with col1:
        st.header("Introduction", divider=True)
        st.text(
            "Retailers often face delays and inefficiencies due to time-consuming manual procurement tasks."
        )
        st.text(
            "AMPA integrates with leading supplier platforms like Alibaba to automate supplier searches, communications, and decision-making, delivering real-time insights through an intuitive dashboard."
        )

    with col2:
        st.image(
            image="assets/images/ampa-hla/HLA-AMPA-Investor-with-border-white.png",
            use_container_width=True,
            caption="Procurement Process Visualization",
            output_format="PNG",
        )

# Features Tab
with tabs[1]:
    st.header("Key Features", divider=True)

    features = [
        {
            "title": "Dynamic Filtering Search",
            "description": "Faceted search to find suppliers across several B2B platforms such as Alibaba.",
            "image": "assets/images/ampa-features/ampa-feature-search-b2b.gif",
            "caption": "Supplier Search",
        },
        {
            "title": "Agentic AI Communicator",
            "description": "AI agentic system will contact and negotiate with new suppliers through email.",
            "image": "assets/images/ampa-features/ampa-feature-agent.gif",
            "caption": "Email Automation",
        },
        {
            "title": "LLM-powered Assistant",
            "description": "Chat with an assistant and effortlessly re-rank the most relevant suppliers.",
            "image": "assets/images/ampa-features/ampa-feature-llm.gif",
            "caption": "Chat Assistant",
        },
        {
            "title": "SRM Dashboard",
            "description": "Monitor supplier responses, automated document drafts and more.",
            "image": "assets/images/ampa-features/ampa-feature-dashboard.gif",
            "caption": "Admin Dashboard",
        },
    ]

    # st.title("Phase 1")
    col1, col2 = st.columns(2, vertical_alignment="top", gap="large")
    columns = [col1, col1, col2, col2]

    for i, feature in enumerate(features):
        with columns[i]:
            st.subheader(feature["title"], divider=True)
            with st.container(border=True):
                st.info(feature["description"])
                st.image(
                    image=feature["image"],
                    output_format="GIF",
                    use_container_width=True,
                    caption=feature["caption"],
                )


# Benefits Tab
with tabs[2]:
    st.header("Benefits", divider=True)


    benefits = [
        {
            "title": "Increased Efficiency",
            "description": "Significantly reduce manual effort spent on procurement search.",
            "icon": "assets/images/ampa-benefits/ampa-benefit-efficiency-large-fast.gif",
        },
        {
            "title": "Cost Savings",
            "description": "Optimize supplier selection to secure the best prices and terms.",
            "icon": "assets/images/ampa-benefits/ampa-benefit-cost-large-fast.gif",
        },
        {
            "title": "Better Decision-Making",
            "description": "Deep Reasoning AI with real time data to meet search criteria.",
            "icon": "assets/images/ampa-benefits/ampa-benefit-decision-large-fast.gif",
        },
        {
            "title": "Wider Supplier Network",
            "description": "Outreach to more suppliers online for unlimited opportunities.",
            "icon": "assets/images/ampa-benefits/ampa-benefit-network-large-fast.gif",
        },
    ]
    cols = st.columns(len(benefits), vertical_alignment="bottom", gap="medium")
    for i, benefit in enumerate(benefits):
        with cols[i]:
            # header = benefit["title"]
            # st.markdown(f"#### {header}")
            st.subheader(benefit["title"], divider=True, anchor=False)
    cols = st.columns(len(benefits), vertical_alignment="bottom", gap="medium")
    for i, benefit in enumerate(benefits):
        with cols[i]:
            with st.columns([1, 2, 1])[1]:
                st.image(
                    image=benefit["icon"],
                    output_format="GIF",
                    use_container_width=True,
                )
            # with st.popover("click me!"):
            #     st.info(benefit["description"])
    cols = st.columns(len(benefits), vertical_alignment="top", gap="medium")
    for i, benefit in enumerate(benefits):
        with cols[i]:
            st.success(benefit["description"], icon=":material/verified:")

    # for i, benefit in enumerate(benefits):
    #     benefit_cols = st.columns(4, vertical_alignment="top", gap="large")
    #     with benefit_cols[i]:
    #         st.image(
    #             image=benefit["icon"],
    #             # width=100,
    #             output_format="GIF",
    #             # use_container_width=True,
    #         )
    #         st.subheader(benefit["title"], divider=True, anchor=False)
    #         st.info(benefit["description"])

    streamlit_roi_ver10()

# Get Started Tab
with tabs[3]:
    st.header("Get In Touch", divider=True)
    st.text("Ready to transform your procurement process?")
    col1, col2 = st.columns([3, 1])
    with col1:
        with st.form("get_in_touch"):
            st.text_input("Name")
            st.text_input("Company Name")
            st.text_input("Email")
            st.text_input("Phone")
            st.text_area("Specific Requirements")
            st.form_submit_button("Send")
    with col2:
        st.image(
            image="assets/images/misc/500x1440-px.svg",
            use_container_width=True,
            # output_format="PNG",
        )


streamlit_footer()