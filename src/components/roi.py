import streamlit as st
import time
import random


def streamlit_roi_ver10():
    col1, col2 = st.columns([5, 2])

    # Initialize variables outside the form so they're available to both columns
    cost_savings = 0
    monetary_roi = 0
    total_time_saved = 0
    time_efficiency_percentage = 0
    ai_time = 0
    calculation_done = False

    with col1:
        st.header("ROI Calculator", divider=True)

        with st.form(key="procurement_roi_form_ver10"):
            st.subheader("Monetary Perspective", divider=True)

            current_contract_value = st.number_input(
                "Total Contract Budget/Year (AED)",
                min_value=100000,
                max_value=1000000000,
                value=10000000,
                step=10000,
            )

            st.subheader("Time Perspective", divider=True)

            st.info(
                "Manual supplier discovery takes an average of **7.3 hours** per event, "
                "while AI-assisted discovery is typically **52 times faster**."
            )

            with st.container(border=True):
                manual_time = st.slider(
                    "Manual Time per Supplier Event (hours)",
                    min_value=1.0,
                    max_value=48.0,
                    value=7.3,
                    step=0.1,
                    format="%d hrs",
                )

                # Calculate AI time dynamically as 1/52 of manual time
                ai_time = manual_time / 52

            with st.container(border=True):
                events_per_year = st.slider(
                    "Procurement Events per Year",
                    min_value=1,
                    max_value=1000,
                    value=264,
                    step=1,
                    format="%d events",
                )

            submitted = st.form_submit_button("Calculate ROI")
            if submitted:
                # Monetary calculations
                fixed_new_contract_value = current_contract_value * 0.75
                cost_savings = current_contract_value - fixed_new_contract_value
                monetary_roi = (
                    (cost_savings / current_contract_value) * 100
                    if current_contract_value > 0
                    else 0
                )

                # Time calculations for supplier discovery
                total_manual_time = manual_time * events_per_year
                total_ai_time = ai_time * events_per_year
                total_time_saved = total_manual_time - total_ai_time
                # Calculate time efficiency percentage
                time_efficiency_percentage = (
                    (manual_time / ai_time) * 100 if manual_time > 0 else 0
                )

                # Set flag that calculation is complete
                calculation_done = True

                # Notification in col1 that calculation is complete
                # st.success("ROI Analysis Complete! See results in the right panel.")

    # Display results in col2
    with col2:
        if calculation_done:
            st.header("Results", divider=True)

            with st.container(border=True):
                progress_text = "Calculating..."
                my_bar = st.progress(0, text=progress_text)

                for percent_complete in range(100):
                    time.sleep(random.randrange(1, 10) * 0.001)
                    my_bar.progress(percent_complete + 1, text=progress_text)
                time.sleep(1)
                my_bar.empty()
                st.metric("Monetary Cost Savings", f"{cost_savings:,.0f} AED")
                st.metric("Monetary ROI", f"{monetary_roi:.0f}%")

                st.metric("Annual Time Saved", f"{total_time_saved:,.0f} hours")
                st.metric(
                    "Time Efficiency Improvement", f"{time_efficiency_percentage:.0f}%"
                )

                st.info(
                    f"""
                    AI-Assisted Time per Supplier Event: {ai_time:.2f} hours.\n
                    Which is around {ai_time * 60:.0f} minutes.
                    """
                )
