import streamlit as st
import time
import random


def streamlit_roi_ver1():
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
                "Average hourly rate of procurement staff (AED)", 20, 100, 40
            )

        with calc_col3:
            ampa_reduction = st.slider(
                "Expected time reduction with AMPA (%)", 30, 90, 60
            )

        savings = current_hours * hourly_rate * (ampa_reduction / 100) * 52

        st.metric("Estimated Annual Savings", f"AED{savings:,.2f}")


def streamlit_roi_ver2():
    # ROI Calculator
    st.subheader("Calculate Your Potential ROI", divider=True)

    with st.form(key="roi_calculator_ver_2"):
        # Employee details
        st.subheader("Employee Information")
        col1, col2 = st.columns(2)

        with col1:
            monthly_salary = st.number_input(
                "Monthly salary of procurement employee (AED)",
                min_value=3000,
                max_value=30000,
                value=10000,
                step=1000,
            )

        with col2:
            working_hours = st.number_input(
                "Working hours per month",
                min_value=120,
                max_value=240,
                value=176,  # Based on standard 22 working days at 8 hours
                step=8,
            )

        # Procurement workload
        st.subheader("Current Procurement Process")
        col3, col4 = st.columns(2)

        with col3:
            procurement_percentage = st.slider(
                "Percentage of time spent on procurement tasks",
                min_value=10,
                max_value=100,
                value=70,
                step=5,
            )

        with col4:
            num_procurements = st.number_input(
                "Average number of procurement cycles per month",
                min_value=1,
                max_value=100,
                value=15,
                step=1,
            )

        # Company digitization level
        st.subheader("Company Profile")
        company_profile = st.selectbox(
            "Select your company's current procurement digitization level",
            options=[
                "Paper-based process (70-80% time reduction with AMPA)",
                "Basic digital tools (50-60% time reduction with AMPA)",
                "Partial automation (30-40% time reduction with AMPA)",
                "Advanced systems (20-30% time reduction with AMPA)",
            ],
            index=1,
        )

        # Map selection to time reduction percentage
        time_reduction_map = {
            "Paper-based process (70-80% time reduction with AMPA)": 75,
            "Basic digital tools (50-60% time reduction with AMPA)": 55,
            "Partial automation (30-40% time reduction with AMPA)": 35,
            "Advanced systems (20-30% time reduction with AMPA)": 25,
        }

        time_reduction = time_reduction_map[company_profile]

        # Form submission button
        submitted = st.form_submit_button("Calculate ROI")

        if submitted:
            # Calculate hourly rate
            hourly_rate = monthly_salary / working_hours

            # Calculate hours spent on procurement
            procurement_hours = working_hours * (procurement_percentage / 100)

            # Calculate time saved
            hours_saved_monthly = procurement_hours * (time_reduction / 100)

            # Calculate monetary value of time saved
            monthly_savings = hours_saved_monthly * hourly_rate
            annual_savings = monthly_savings * 12

            # Calculate productivity increase
            additional_procurements = num_procurements * (time_reduction / 100)

            # Display results
            st.success("ROI Analysis Complete")

            col_savings, col_productivity = st.columns(2)

            with col_savings:
                st.metric("Annual Cost Savings", f"AED {annual_savings:,.2f}")
                st.text(f"Monthly savings: AED {monthly_savings:,.2f}")

            with col_productivity:
                st.metric(
                    "Additional Procurement Capacity",
                    f"{additional_procurements:.1f} cycles/month",
                )
                st.text(f"Hours saved per month: {hours_saved_monthly:.1f}")
                st.text(f"Hours saved annually: {hours_saved_monthly * 12:.1f}")

            # Calculation explanation in expander
            with st.expander("View Calculation Methodology"):
                st.subheader("How We Calculate Your ROI")

                st.subheader("Step 1: Calculate Hourly Rate", anchor=False)
                st.code(
                    f"Hourly Rate = Monthly Salary ÷ Working Hours = {monthly_salary} ÷ {working_hours} = AED {hourly_rate:.2f}"
                )

                st.subheader(
                    "Step 2: Calculate Time Spent on Procurement", anchor=False
                )
                st.code(
                    f"Procurement Hours = Working Hours × Procurement Percentage = {working_hours} × {procurement_percentage}% = {procurement_hours:.2f} hours"
                )

                st.subheader("Step 3: Calculate Time Saved with AMPA", anchor=False)
                st.code(
                    f"Hours Saved = Procurement Hours × Time Reduction = {procurement_hours:.2f} × {time_reduction}% = {hours_saved_monthly:.2f} hours per month"
                )

                st.subheader("Step 4: Calculate Financial Savings", anchor=False)
                st.code(
                    f"Monthly Savings = Hours Saved × Hourly Rate = {hours_saved_monthly:.2f} × {hourly_rate:.2f} = AED {monthly_savings:.2f}"
                )
                st.code(
                    f"Annual Savings = Monthly Savings × 12 = {monthly_savings:.2f} × 12 = AED {annual_savings:.2f}"
                )

                st.subheader("Step 5: Calculate Productivity Increase", anchor=False)
                st.code(
                    f"Additional Procurement Capacity = Current Cycles × Time Reduction = {num_procurements} × {time_reduction}% = {additional_procurements:.2f} additional cycles per month"
                )

                st.subheader("What This Means For Your Business:", anchor=False)
                st.text(
                    f"By implementing AMPA, your procurement employee can save {hours_saved_monthly:.1f} hours per month."
                )
                st.text(
                    f"This translates to AED {annual_savings:.2f} in annual cost savings and the capacity to"
                )
                st.text(
                    f"handle {additional_procurements:.1f} more procurement cycles per month with the same resources."
                )

                if time_reduction > 50:
                    st.text(
                        "💡 Insight: With over 50% time reduction, you may want to consider reallocating"
                    )
                    st.text(
                        "some of the saved time to strategic procurement initiatives or other value-adding activities."
                    )

            # ROI information
            st.info(
                "Note: For a complete ROI calculation including payback period, please contact our sales team for AMPA pricing information."
            )


def streamlit_roi_ver3():
    # ROI Calculator
    st.subheader("Calculate Your Potential ROI", divider=True)

    with st.form(key="roi_calculator_ver3"):
        # Employee details
        st.subheader("Employee Information")
        col1, col2 = st.columns(2)

        with col1:
            monthly_salary = st.number_input(
                "Monthly salary of procurement employee (AED)",
                min_value=3000,
                max_value=30000,
                value=10000,
                step=1000,
            )

        with col2:
            working_hours = st.number_input(
                "Working hours per month",
                min_value=120,
                max_value=240,
                value=176,  # Based on standard 22 working days at 8 hours
                step=8,
            )

        # Procurement workload
        st.subheader("Current Procurement Process")

        # Supplier search time
        st.text("Time spent on supplier search and qualification:")
        col3, col4 = st.columns(2)

        with col3:
            search_hours = st.number_input(
                "Hours spent searching for suppliers per procurement",
                min_value=1,
                max_value=40,
                value=8,
                step=1,
            )

        with col4:
            num_procurements = st.number_input(
                "Number of new procurements per month",
                min_value=1,
                max_value=50,
                value=5,
                step=1,
            )

        # Communication time
        st.text("Time spent on supplier communication:")
        col5, col6 = st.columns(2)

        with col5:
            email_hours = st.number_input(
                "Hours spent on email communication per supplier",
                min_value=0.5,
                max_value=20.0,
                value=4.0,
                step=0.5,
            )

        with col6:
            suppliers_per_procurement = st.number_input(
                "Average suppliers contacted per procurement",
                min_value=1,
                max_value=20,
                value=3,
                step=1,
            )

        # Company digitization level
        st.subheader("Company Profile")
        company_profile = st.selectbox(
            "Select your company's current procurement digitization level",
            options=[
                "Paper-based process (70-80% time reduction with AMPA)",
                "Basic digital tools (50-60% time reduction with AMPA)",
                "Partial automation (30-40% time reduction with AMPA)",
                "Advanced systems (20-30% time reduction with AMPA)",
            ],
            index=1,
        )

        # Map selection to time reduction percentage
        time_reduction_map = {
            "Paper-based process (70-80% time reduction with AMPA)": 75,
            "Basic digital tools (50-60% time reduction with AMPA)": 55,
            "Partial automation (30-40% time reduction with AMPA)": 35,
            "Advanced systems (20-30% time reduction with AMPA)": 25,
        }

        # Different reduction rates for different activities
        search_reduction = time_reduction_map[company_profile]
        communication_reduction = (
            time_reduction_map[company_profile] * 0.9
        )  # Communication might be slightly less improved

        # Form submission button
        submitted = st.form_submit_button("Calculate ROI")

        if submitted:
            # Calculate hourly rate
            hourly_rate = monthly_salary / working_hours

            # Calculate total time spent on procurement activities
            total_search_time = search_hours * num_procurements
            total_communication_time = (
                email_hours * suppliers_per_procurement * num_procurements
            )
            total_procurement_time = total_search_time + total_communication_time

            # Calculate time saved
            search_time_saved = total_search_time * (search_reduction / 100)
            communication_time_saved = total_communication_time * (
                communication_reduction / 100
            )
            total_time_saved = search_time_saved + communication_time_saved

            # Calculate monetary value of time saved
            monthly_savings = total_time_saved * hourly_rate
            annual_savings = monthly_savings * 12

            # Calculate productivity increase
            time_efficiency_ratio = (
                total_time_saved / total_procurement_time
                if total_procurement_time > 0
                else 0
            )
            additional_capacity = num_procurements * time_efficiency_ratio

            # Display results
            st.success("ROI Analysis Complete")

            col_savings, col_productivity = st.columns(2)

            with col_savings:
                st.metric("Annual Cost Savings", f"AED {annual_savings:,.2f}")
                st.text(f"Monthly savings: AED {monthly_savings:,.2f}")

            with col_productivity:
                st.metric("Time Saved", f"{total_time_saved:.1f} hours/month")
                st.text(
                    f"Additional capacity: {additional_capacity:.1f} more procurements/month"
                )

            # Calculation explanation in expander
            with st.expander("View Calculation Methodology"):
                st.subheader("How We Calculate Your ROI")

                st.subheader("Step 1: Calculate Hourly Rate", anchor=False)
                st.code(
                    f"Hourly Rate = Monthly Salary ÷ Working Hours = {monthly_salary} ÷ {working_hours} = AED {hourly_rate:.2f}"
                )

                st.subheader("Step 2: Calculate Current Time Investment", anchor=False)
                st.code(
                    f"Search Time = Hours per Search × Procurements = {search_hours} × {num_procurements} = {total_search_time} hours/month"
                )
                st.code(
                    f"Communication Time = Hours per Supplier × Suppliers × Procurements = {email_hours} × {suppliers_per_procurement} × {num_procurements} = {total_communication_time} hours/month"
                )
                st.code(
                    f"Total Procurement Time = {total_search_time} + {total_communication_time} = {total_procurement_time} hours/month"
                )

                st.subheader("Step 3: Calculate Time Saved with AMPA", anchor=False)
                st.code(
                    f"Search Time Saved = {total_search_time} × {search_reduction}% = {search_time_saved:.2f} hours/month"
                )
                st.code(
                    f"Communication Time Saved = {total_communication_time} × {communication_reduction:.1f}% = {communication_time_saved:.2f} hours/month"
                )
                st.code(
                    f"Total Time Saved = {search_time_saved:.2f} + {communication_time_saved:.2f} = {total_time_saved:.2f} hours/month"
                )

                st.subheader("Step 4: Calculate Financial Savings", anchor=False)
                st.code(
                    f"Monthly Savings = Total Time Saved × Hourly Rate = {total_time_saved:.2f} × {hourly_rate:.2f} = AED {monthly_savings:.2f}"
                )
                st.code(
                    f"Annual Savings = Monthly Savings × 12 = {monthly_savings:.2f} × 12 = AED {annual_savings:.2f}"
                )

                st.subheader("Step 5: Calculate Productivity Increase", anchor=False)
                st.code(
                    f"Time Efficiency Ratio = Total Time Saved ÷ Total Procurement Time = {total_time_saved:.2f} ÷ {total_procurement_time} = {time_efficiency_ratio:.2f}"
                )
                st.code(
                    f"Additional Capacity = Current Procurements × Efficiency Ratio = {num_procurements} × {time_efficiency_ratio:.2f} = {additional_capacity:.2f} additional procurements per month"
                )

                st.subheader("What This Means For Your Business:", anchor=False)
                st.text(
                    f"By implementing AMPA, your procurement employee can save {total_time_saved:.1f} hours per month."
                )
                st.text(
                    f"This translates to AED {annual_savings:.2f} in annual cost savings and the capacity to"
                )
                st.text(
                    f"handle approximately {additional_capacity:.1f} more procurement cycles per month with the same resources."
                )

                if search_reduction > 50:
                    st.text(
                        "💡 Insight: With significant time reduction in supplier search, your employee will have"
                    )
                    st.text(
                        "more time to focus on strategic supplier relationships and negotiation."
                    )
                st.code(
                    f"Hourly Rate = Monthly Salary ÷ Working Hours = {10000} ÷ {100} = AED {100:.2f}",
                    line_numbers=True,
                    wrap_lines=True,
                )
                st.markdown(
                    f":green[:blue-background[Hourly Rate = Monthly Salary ÷ Working Hours = {10000} ÷ {100} = AED {100:.2f}]]",
                    help="click to go to Get In Touch",
                )
                st.success("This is a success message!", icon="✅")
                st.info("This is a purely informational message", icon="ℹ️")
                st.markdown("[Go To Get In Touch](#get-in-touch)")
                # ROI information
                st.info(
                    "Note: For a complete ROI calculation including payback period, please contact our sales team for AMPA pricing information."
                )


def streamlit_roi_ver4():
    st.subheader("Procurement ROI Calculator")

    with st.form(key="procurement_roi_form"):
        st.header("Monetary Perspective")
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            current_contract_value = st.number_input(
                "Current Annual Contract Value (AED)",
                min_value=100000,
                max_value=100000000,
                value=10000000,
                step=100000,
            )
        with col_m2:
            new_contract_value = st.number_input(
                "Annual New Suppliers' Contract Value (AED)",
                min_value=100000,
                max_value=100000000,
                value=9000000,
                step=100000,
            )

        st.markdown("---")
        st.header("Time Perspective")
        st.markdown("### Procurement Event Time Savings")
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            manual_time = st.number_input(
                "Manual Time per Supplier Event (hours)",
                min_value=0.0,
                max_value=20.0,
                value=7.3,
                step=0.1,
            )
            ai_time = st.number_input(
                "AI-Assisted Time per Supplier Event (hours)",
                min_value=0.0,
                max_value=5.0,
                value=0.14,
                step=0.1,
            )
            events_per_year = st.number_input(
                "Procurement Events per Year",
                min_value=1,
                max_value=1000,
                value=264,
                step=1,
            )
        with col_t2:
            setup_time = st.number_input(
                "Setup & Configuration Time (hours, one-time in first year)",
                min_value=0,
                max_value=100,
                value=40,
                step=1,
            )
            oversight_time = st.number_input(
                "Oversight & Review Time per Cycle (hours)",
                min_value=0,
                max_value=10,
                value=2,
                step=1,
            )
            cycles_per_year = st.number_input(
                "Number of Cycles/Orders per Year",
                min_value=1,
                max_value=100,
                value=12,
                step=1,
            )
            working_hours_per_day = st.number_input(
                "Working Hours per Day (for Operational Savings)",
                min_value=1,
                max_value=24,
                value=8,
                step=1,
            )
            operational_days_saved = st.number_input(
                "Operational Days Saved per Order",
                min_value=0,
                max_value=30,
                value=5,
                step=1,
            )

        submitted = st.form_submit_button("Calculate ROI")

        if submitted:
            # Monetary calculations
            cost_savings = current_contract_value - new_contract_value
            monetary_roi = (
                (cost_savings / current_contract_value) * 100
                if current_contract_value > 0
                else 0
            )

            # Time calculations: Procurement events
            time_saved_per_event = manual_time - ai_time
            total_procurement_time_saved = time_saved_per_event * events_per_year

            # Time calculations: Operational savings
            operational_time_saved = (
                operational_days_saved * working_hours_per_day * cycles_per_year
            )

            total_time_saved = total_procurement_time_saved + operational_time_saved

            # Time efficiency ratios
            first_year_investment = setup_time + (oversight_time * cycles_per_year)
            subsequent_years_investment = oversight_time * cycles_per_year

            efficiency_ratio_first_year = (
                total_time_saved / first_year_investment
                if first_year_investment > 0
                else 0
            )
            efficiency_ratio_subsequent = (
                total_time_saved / subsequent_years_investment
                if subsequent_years_investment > 0
                else 0
            )

            st.success("ROI Analysis Complete")
            col_result1, col_result2 = st.columns(2)
            with col_result1:
                st.metric("Monetary Cost Savings", f"AED {cost_savings:,.2f}")
                st.metric("Monetary ROI", f"{monetary_roi:.2f}%")
            with col_result2:
                st.metric("Annual Time Saved", f"{total_time_saved:,.1f} hours")
                st.text(
                    f"Time Efficiency Ratio (First Year): {efficiency_ratio_first_year:.2f}"
                )
                st.text(
                    f"Time Efficiency Ratio (Subsequent Years): {efficiency_ratio_subsequent:.2f}"
                )


def streamlit_roi_ver5():
    st.subheader("Procurement ROI Calculator")

    with st.form(key="procurement_roi_form_ver5"):
        st.header("Monetary Perspective")
        current_contract_value = st.number_input(
            "Current Annual Contract Value (AED)",
            min_value=100000,
            max_value=100000000,
            value=10000000,
            step=100000,
        )
        # Fixed assumption: New Suppliers' Contract Value is 75% of current value (i.e., 25% cost reduction)
        fixed_new_contract_value = current_contract_value * 0.75
        st.info(
            f"New Suppliers' Contract Value (Fixed): AED {fixed_new_contract_value:,.2f} (25% cost reduction)"
        )

        st.markdown("---")
        st.header("Time Perspective - Supplier Discovery")
        st.markdown(
            "Based on research from Veridion, manual supplier discovery takes an average of **7.3 hours** per event, "
            "while AI-assisted discovery takes only **0.14 hours**—saving **7.16 hours** per event. Procurement "
            "managers typically handle about **264 events per year**."
        )

        manual_time = st.number_input(
            "Manual Time per Supplier Event (hours)",
            min_value=0.0,
            max_value=20.0,
            value=7.3,
            step=0.1,
        )
        # Fixed value: AI-Assisted Time per Supplier Event is set to 0.14 hours.
        fixed_ai_time = 0.14
        st.info(f"AI-Assisted Time per Supplier Event (Fixed): {fixed_ai_time} hours")

        events_per_year = st.number_input(
            "Procurement Events per Year",
            min_value=1,
            max_value=1000,
            value=264,
            step=1,
        )

        # Include average hourly cost for the procurement professional.
        hourly_cost = st.number_input(
            "Average Hourly Cost for Procurement Professional (AED)",
            min_value=50,
            max_value=1000,
            value=220,
            step=10,
        )

        submitted = st.form_submit_button("Calculate ROI")

        if submitted:
            # Monetary calculations
            cost_savings = current_contract_value - fixed_new_contract_value
            monetary_roi = (
                (cost_savings / current_contract_value) * 100
                if current_contract_value > 0
                else 0
            )

            # Time calculations for supplier discovery
            time_saved_per_event = manual_time - fixed_ai_time
            total_time_saved = time_saved_per_event * events_per_year

            # Labor cost savings calculation based on time saved
            labor_cost_savings = total_time_saved * hourly_cost

            st.success("ROI Analysis Complete")
            col_result1, col_result2 = st.columns(2)
            with col_result1:
                st.metric("Monetary Cost Savings", f"AED {cost_savings:,.2f}")
                st.metric("Monetary ROI", f"{monetary_roi:.2f}%")
            with col_result2:
                st.metric("Annual Time Saved", f"{total_time_saved:,.1f} hours")
                st.metric("Labor Cost Savings", f"AED {labor_cost_savings:,.2f}")


def streamlit_roi_ver6():
    st.subheader("Procurement ROI Calculator")

    with st.form(key="procurement_roi_form_ver6"):
        st.header("Monetary Perspective")
        current_contract_value = st.number_input(
            "Current Annual Contract Value (AED)",
            min_value=100000,
            max_value=100000000,
            value=10000000,
            step=100000,
        )
        # Fixed assumption: New Suppliers' Contract Value is 75% of current value (i.e., 25% cost reduction)
        fixed_new_contract_value = current_contract_value * 0.75
        st.info(
            f"New Suppliers' Contract Value (Fixed): AED {fixed_new_contract_value:,.2f} (25% cost reduction)"
        )

        st.markdown("---")
        st.header("Time Perspective - Supplier Discovery")
        st.markdown(
            "Based on research from Veridion, manual supplier discovery takes an average of **7.3 hours** per event, "
            "while AI-assisted discovery takes only **0.14 hours** per event."
        )

        manual_time = st.number_input(
            "Manual Time per Supplier Event (hours)",
            min_value=0.0,
            max_value=20.0,
            value=7.3,
            step=0.1,
        )
        # Fixed value: AI-Assisted Time per Supplier Event is set to 0.14 hours.
        fixed_ai_time = 0.14
        st.info(f"AI-Assisted Time per Supplier Event (Fixed): {fixed_ai_time} hours")

        events_per_year = st.number_input(
            "Procurement Events per Year",
            min_value=1,
            max_value=1000,
            value=264,
            step=1,
        )

        submitted = st.form_submit_button("Calculate ROI")

        if submitted:
            # Monetary calculations
            cost_savings = current_contract_value - fixed_new_contract_value
            monetary_roi = (
                (cost_savings / current_contract_value) * 100
                if current_contract_value > 0
                else 0
            )

            # Time calculations for supplier discovery
            total_manual_time = manual_time * events_per_year
            total_ai_time = fixed_ai_time * events_per_year
            total_time_saved = total_manual_time - total_ai_time

            # Calculate time efficiency as a percentage of manual time saved
            time_efficiency_percentage = (
                ((total_time_saved) / total_manual_time) * 100 if manual_time > 0 else 0
            )

            st.success("ROI Analysis Complete")
            col_result1, col_result2 = st.columns(2)
            with col_result1:
                st.metric("Monetary Cost Savings", f"AED {cost_savings:,.2f}")
                st.metric("Monetary ROI", f"{monetary_roi:.2f}%")
            with col_result2:
                st.metric("Annual Time Saved", f"{total_time_saved:,.1f} hours")
                st.metric(
                    "Time Efficiency Improvement", f"{time_efficiency_percentage:.2f}%"
                )


def streamlit_roi_ver7():
    st.header("ROI Calculator", divider=True)

    with st.form(key="procurement_roi_form_ver7"):
        # st.markdown("## Monetary Perspective")
        st.subheader("Monetary Perspective", divider=True)

        col_mon_input, col_mon_graphic = st.columns([2, 1], gap="large")
        with col_mon_input:

            current_contract_value = st.number_input(
                "Current Annual Contract Value (AED)",
                min_value=100000,
                max_value=1000000000,
                value=10000000,
                step=10000,
            )

            st.info(
                "AMPA can bring an average of 25% cost reduction in supplier contracts"
            )
        with col_mon_graphic:

            st.image(
                image="https://placehold.co/500x400",
                caption="In some South East Europe countries, it is estimated that 90% of public supplier contracts are costing 25% more than they should, and not due to any corruption taking place, but because searching for alternate suppliers in order to optimize spending is never very high on the priority list.",
            )

        # st.divider()
        # st.markdown("## Time Perspective - Supplier Discovery")
        st.subheader("Time Perspective", divider=True)

        col_time_input, col_time_graphic = st.columns([3, 2], gap="large")
        with col_time_input:
            st.markdown(
                "Based on research from Veridion, manual supplier discovery takes an average of **7.3 hours** per event, "
                "while AI-assisted discovery takes only **0.14 hours** per event."
            )

            manual_time = st.slider(
                "Manual Time per Supplier Event (hours)",
                min_value=1.0,
                max_value=48.0,
                value=7.3,
                step=0.1,
                format="%.1f hrs",
            )

            fixed_ai_time = 0.14
            st.info(
                f"""
                    AI-Assisted Time per Supplier Event can be as low as: {fixed_ai_time} hours.\n
                    Which is around {fixed_ai_time * 60} minutes.
                """
            )

            events_per_year = st.slider(
                "Procurement Events per Year",
                min_value=1,
                max_value=1000,
                value=264,
                step=1,
                format="%d events",
            )

        with col_time_graphic:
            st.image(
                image="assets/images/ampa-roi/veridion-statistics-chart.png",
                caption="Shocking Statistics",
                output_format="PNG",
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
            total_ai_time = fixed_ai_time * events_per_year
            total_time_saved = total_manual_time - total_ai_time
            # Calculate time efficiency percentage
            time_efficiency_percentage = (
                (manual_time / fixed_ai_time) * 100 if manual_time > 0 else 0
            )

            st.success("ROI Analysis Complete")
            col_result1, col_result2 = st.columns(2)
            with col_result1:
                st.metric("Monetary Cost Savings", f"AED {cost_savings:,.2f}")
                st.metric("Monetary ROI", f"{monetary_roi:.2f}%")
            with col_result2:
                st.metric("Annual Time Saved", f"{total_time_saved:,.1f} hours")
                st.metric(
                    "Time Efficiency Improvement", f"{time_efficiency_percentage:.2f}%"
                )


def streamlit_roi_ver8():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.header("ROI Calculator", divider=True)

        with st.form(key="procurement_roi_form_ver8"):
            # st.markdown("## Monetary Perspective")
            st.subheader("Monetary Perspective", divider=True)

            current_contract_value = st.number_input(
                "Current Annual Contract Value (AED)",
                min_value=100000,
                max_value=1000000000,
                value=10000000,
                step=10000,
            )

            st.info(
                "AMPA can bring an average of 25% cost reduction in supplier contracts"
            )
            # st.divider()
            # st.markdown("## Time Perspective - Supplier Discovery")
            st.subheader("Time Perspective", divider=True)

            st.markdown(
                "Manual supplier discovery takes an average of **7.3 hours** per event, "
                "while AI-assisted discovery takes only **0.14 hours** per event."
            )

            manual_time = st.slider(
                "Manual Time per Supplier Event (hours)",
                min_value=1.0,
                max_value=48.0,
                value=7.3,
                step=0.1,
                format="%.1f hrs",
            )

            fixed_ai_time = 0.14
            st.info(
                f"""
                    AI-Assisted Time per Supplier Event can be as low as: {fixed_ai_time} hours.\n
                    Which is around {fixed_ai_time * 60} minutes.
                """
            )

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
                total_ai_time = fixed_ai_time * events_per_year
                total_time_saved = total_manual_time - total_ai_time
                # Calculate time efficiency percentage
                time_efficiency_percentage = (
                    (manual_time / fixed_ai_time) * 100 if manual_time > 0 else 0
                )

                st.success("ROI Analysis Complete")
                col_result1, col_result2 = st.columns(2)
                with col_result1:
                    st.metric("Monetary Cost Savings", f"AED {cost_savings:,.2f}")
                    st.metric("Monetary ROI", f"{monetary_roi:.2f}%")
                with col_result2:
                    st.metric("Annual Time Saved", f"{total_time_saved:,.1f} hours")
                    st.metric(
                        "Time Efficiency Improvement",
                        f"{time_efficiency_percentage:.2f}%",
                    )


def streamlit_roi_ver9():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.header("ROI Calculator", divider=True)

        with st.form(key="procurement_roi_form_ver9"):
            # st.markdown("## Monetary Perspective")
            st.subheader("Monetary Perspective", divider=True)

            current_contract_value = st.number_input(
                "Total Contract Budget/Year (AED)",
                min_value=100000,
                max_value=1000000000,
                value=10000000,
                step=10000,
            )

            # st.divider()
            # st.markdown("## Time Perspective - Supplier Discovery")
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

                st.success("ROI Analysis Complete")
                col_result1, col_result2 = st.columns(2)
                with col_result1:
                    st.metric("Monetary Cost Savings", f"{cost_savings:,.0f} AED")
                    st.metric("Monetary ROI", f"{monetary_roi:.0f}%")
                with col_result2:
                    st.metric("Annual Time Saved", f"{total_time_saved:,.0f} hours")
                    st.metric(
                        "Time Efficiency Improvement",
                        f"{time_efficiency_percentage:.0f}%",
                    )
                st.info(
                    f"""
                        AI-Assisted Time per Supplier Event: {ai_time:.2f} hours.\n
                        Which is around {ai_time * 60:.1f} minutes.
                    """
                )


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
