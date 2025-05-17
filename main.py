import streamlit as st
from csv_agent import create_csv_agent
import pandas as pd

st.set_page_config(page_title="CSV Agent", layout="wide")

# Initialize session state for agent and dataframe
if 'agent' not in st.session_state:
    st.session_state.agent = None
    st.session_state.df = None

# Sidebar for file upload
with st.sidebar:
    st.title("CSV Agent")
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    if uploaded_file is not None:
        st.session_state.df = pd.read_csv(uploaded_file)
        st.session_state.agent = create_csv_agent(st.session_state.df)
        st.success("File uploaded successfully!")

# Main content area
st.title("CSV Agent")

# Display dataframe
st.subheader("Current Data")
st.dataframe(st.session_state.df)

# Question input
question = st.text_input("Ask a question about the data:", 
                        placeholder="e.g. How many firms are in India?")

if question:
    if st.session_state.agent is None:
        st.warning("Please upload a CSV file first")
    else:
        with st.spinner("Analyzing data..."):
            response = st.session_state.agent.invoke(question)
            st.markdown("### Answer")
            st.markdown(response['output'])

            # Show raw response in expander
            with st.expander("See raw response"):
                st.json(response)
