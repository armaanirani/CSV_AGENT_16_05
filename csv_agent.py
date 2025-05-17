import os
from dotenv import load_dotenv
import pandas as pd
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain_experimental.agents.agent_toolkits import create_csv_agent, create_pandas_dataframe_agent


# Load environment variables from .env file
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

### Note: groq models viz. "gemma2-9b-it" and "llama-3.1-8b-instant" only work. Gemma is better.

llm = ChatGroq(
    model="gemma2-9b-it",
    temperature=0,
    api_key=GROQ_API_KEY
)

# llm = ChatOpenAI(
#     model="gpt-4.1-mini-2025-04-14",
#     temperature=0,
#     api_key=OPENAI_API_KEY
# )

# Read the CSV file and handle missing values
df = pd.read_csv("./data/Architecture_firms_india.csv")

# Create the CSV agent
agent = create_pandas_dataframe_agent(
    llm=llm,
    df=df,
    verbose=True,
    allow_dangerous_code=True
)

response = agent.invoke(input="How many firms are located in India?")
print(response)
