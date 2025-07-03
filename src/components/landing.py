import streamlit as st

def streamlit_landing():
    """
    Display the complete AMPA (Automated Procurement Assistant) dashboard in Streamlit.
    This function contains all UI elements and logic for the AMPA presentation.
    """

    header_col1, header_col2 = st.columns([1, 3])

    with header_col1:
        st.image("https://placehold.co/150x150")
        st.caption("AMPA Logo")

    with header_col2:
        st.title("Streamline Your Procurement Process with AMPA")
        st.text(
            "Tired of spending up to 48 hours on manual procurement? AMPA automates supplier communications and provides data-driven insights to save you time and money."
        )

    st.divider()

    # Main content in tabs
    tabs = st.tabs(["Overview", "Features", "Benefits", "Get Started"])

    # Overview Tab
    with tabs[0]:
        col1, col2 = st.columns([3, 2])

        with col1:
            st.header("Introduction")
            st.text(
                """
                Retailers often face delays and inefficiencies due to time-consuming manual procurement tasks.
                AMPA integrates with leading supplier platforms like Alibaba to automate supplier searches,
                communications, and decision-making, delivering real-time insights through an intuitive dashboard.
                """
            )

        with col2:
            st.image("https://placehold.co/400x300")
            st.caption("Procurement Process Visualization")

    # Features Tab
    with tabs[1]:
        st.header("Key Features")

        col1, col2 = st.columns(2)

        with col1:
            with st.container():
                st.subheader("Automated Supplier Search")
                st.text(
                    "Instantly find suppliers matching your criteria using Alibaba's API."
                )
                st.image("https://placehold.co/300x200")
                st.caption("Supplier Search")

            with st.container():
                st.subheader("Intelligent Chatbot")
                st.text(
                    "Get personalized supplier recommendations and answers to your questions."
                )
                st.image("https://placehold.co/300x200")
                st.caption("AI Chatbot")

        with col2:
            with st.container():
                st.subheader("Automated Emails")
                st.text(
                    "Effortlessly send and track introductory and follow-up emails to suppliers."
                )
                st.image("https://placehold.co/300x200")
                st.caption("Email Automation")

            with st.container():
                st.subheader("Real-Time Dashboard")
                st.text(
                    "Monitor procurement activities, supplier partnerships, and event reports in one place."
                )
                st.image("https://placehold.co/300x200")
                st.caption("Analytics Dashboard")

    # Benefits Tab
    with tabs[2]:
        st.header("Benefits")

        benefit_cols = st.columns(4)

        benefits = [
            {
                "title": "Increased Efficiency",
                "description": "Significantly reduce the time and effort spent on procurement.",
                "icon": "https://placehold.co/100x100",
            },
            {
                "title": "Cost Savings",
                "description": "Optimize supplier selection to secure the best prices and terms.",
                "icon": "https://placehold.co/100x100",
            },
            {
                "title": "Better Decision-Making",
                "description": "Leverage data and AI insights to choose the right suppliers.",
                "icon": "https://placehold.co/100x100",
            },
            {
                "title": "Enhanced Relationships",
                "description": "Streamline communications for smoother, more productive interactions.",
                "icon": "https://placehold.co/100x100",
            },
        ]

        for i, benefit in enumerate(benefits):
            with benefit_cols[i]:
                st.image(benefit["icon"], width=100)
                st.caption(benefit["title"])
                st.subheader(benefit["title"], divider=True)
                st.text(benefit["description"])

        # ROI Calculator
        st.subheader("Calculate Your Potential ROI", divider=True)

        with st.container():
            calc_col1, calc_col2, calc_col3 = st.columns(3)

            with calc_col1:
                current_hours = st.slider(
                    "Current hours spent on procurement per week", 1, 48, 20
                )

            with calc_col2:
                hourly_rate = st.slider(
                    "Average hourly rate of procurement staff ($)", 20, 100, 40
                )

            with calc_col3:
                ampa_reduction = st.slider(
                    "Expected time reduction with AMPA (%)", 30, 90, 60
                )

            savings = current_hours * hourly_rate * (ampa_reduction / 100) * 52

            st.metric("Estimated Annual Savings", f"${savings:,.2f}")

    # Get Started Tab
    with tabs[3]:
        st.header("Get In Touch", divider=True)
        st.text("Ready to transform your procurement process?")

        with st.form("get_in_touch"):
            st.text_input("Company Name")
            st.text_input("Contact Person")
            st.text_input("Email")
            st.text_input("Phone")
            st.text_area("Specific Requirements")
            st.form_submit_button("Send")

    # Footer
    st.divider()

    footer_col1, footer_col2, footer_col3 = st.columns(3)

    with footer_col1:
        st.text("AMPA - Automating procurement for any industry.")

    with footer_col2:
        st.text("Privacy Policy | Terms of Service")

    with footer_col3:
        st.text("© 2025 e& Enterprise")