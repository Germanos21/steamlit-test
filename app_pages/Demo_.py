import streamlit as st
from src.components.sections import show_header, show_search_results, show_ebay_search_form, show_cart
from src.components.chatbot import show_chatbot
from src.components.footer import streamlit_footer

st.header("Input Your Criteria")
with st.expander("Use our simple form to specify product requirements, budget, and delivery preferences.", expanded=True):
    show_ebay_search_form()

st.header("Search for Suppliers")
with st.expander("AMPA searches Alibaba's vast database to find matching suppliers instantly.", expanded=True):
    show_search_results()

# Add shopping cart display
st.header("Shopping Cart")
with st.expander("View and manage items in your shopping cart"):
    col_cart, col_chat = st.columns([2, 3], gap="small")
    with col_cart:
        show_cart()
    with col_chat:
        show_chatbot()

streamlit_footer()
