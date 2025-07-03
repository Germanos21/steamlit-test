import streamlit as st


def read_file(filePath):
    with open(filePath, "r") as file:
        return file.read()


def streamlit_markdown_file(filePath: str):
    markdownContent = read_file(filePath=filePath)
    st.markdown(markdownContent, unsafe_allow_html=True)
