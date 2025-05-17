import streamlit as st
from csv_agent import create_csv_agent, CSV_PROMPT_PREFIX, CSV_PROMPT_SUFFIX
import pandas as pd
import time

# Set page config with theme
st.set_page_config(
    page_title="CSV Data Analyst",
    layout="wide",
    page_icon="📊"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .stTextInput input {
        font-size: 16px !important;
    }
    .stMarkdown h3 {
        color: #2e86ab;
    }
    .stDataFrame {
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'agent' not in st.session_state:
    st.session_state.agent = None
    st.session_state.df = None
    st.session_state.last_question = None

# Sidebar with enhanced UI
with st.sidebar:
    st.title("📊 CSV Data Analyst")
    st.markdown("Upload a CSV file to analyze its data using AI.")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    if uploaded_file is not None:
        with st.spinner("Processing file..."):
            st.session_state.df = pd.read_csv(uploaded_file)
            st.session_state.agent = create_csv_agent(st.session_state.df)
            time.sleep(1)  # Simulate processing
            st.success(f"✅ {uploaded_file.name} loaded successfully!")
            if 'balloons_shown' not in st.session_state:
                st.balloons()
                st.session_state.balloons_shown = True

    st.markdown("---")
    st.markdown("**Sample Questions:**")
    st.code("How many rows are there?")
    st.code("What are the unique values in column X?")
    st.code("Show summary statistics")

# Main content
st.title("📊 CSV Data Analyst")
st.markdown("Ask questions about your data and get AI-powered insights.")

if st.session_state.df is not None:
    # Data summary section
    with st.expander("📋 Data Summary", expanded=True):
        cols = st.columns(3)
        cols[0].metric("Rows", len(st.session_state.df))
        cols[1].metric("Columns", len(st.session_state.df.columns))
        cols[2].metric("Missing Values", st.session_state.df.isnull().sum().sum())

    # Data preview
    st.subheader("🔍 Data Preview")
    st.dataframe(st.session_state.df, use_container_width=True)

    # Question input with better UX
    question = st.text_area("Ask a question about the data:", 
                          placeholder="e.g. What's the average value in column X?\nHow many rows match condition Y?",
                          height=100)
    
    col1, col2 = st.columns([1, 3])
    with col1:
        submit_btn = st.button("Analyze", type="primary")
    with col2:
        if st.session_state.last_question:
            st.write(f"Last question: *{st.session_state.last_question}*")

    if submit_btn and question:
        st.session_state.last_question = question
        if st.session_state.agent is None:
            st.error("Please upload a valid CSV file first")
        else:
            with st.spinner("🔍 Analyzing your data..."):
                try:
                    response = st.session_state.agent.invoke(CSV_PROMPT_PREFIX + question + CSV_PROMPT_SUFFIX)
                    st.markdown("### 📝 Answer")
                    st.markdown(response['output'])
                    
                    # Enhanced response display
                    with st.expander("📊 View Detailed Analysis"):
                        st.json(response)
                        st.download_button(
                            label="Download Analysis",
                            data=str(response),
                            file_name="analysis_results.json",
                            mime="application/json"
                        )
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    st.exception(e)
else:
    st.info("👈 Upload a CSV file to begin analysis")
