import os
from dotenv import load_dotenv
import pandas as pd
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent


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

def create_csv_agent(dataframe):
    """Create a pandas dataframe agent with the given dataframe"""
    return create_pandas_dataframe_agent(
        llm=llm,
        df=dataframe,
        verbose=True,
        allow_dangerous_code=True
    )


CSV_PROMPT_PREFIX = """
First set the pandas display options to show all the columns,
get the column names, then answer the question.
"""

CSV_PROMPT_SUFFIX = """
- **ALWAYS** before giving the Final Answer, try another method.
Then reflect on the answers of the two methods you did and ask yourself
if it answers correctly the original question.
If you are not sure, try another method.
- If the methods tried do not give the same result, reflect and
try again until you have two methods that have the same result.
- If you still cannot arrive to a consistent result, say that
you are not sure of the answer.
- If you are sure of the correct answer, create a beautiful
and thorough response using Markdown.
- **DO NOT MAKE UP AN ANSWER OR USE PRIOR KNOWLEDGE,
ONLY USE THE RESULTS OF THE CALCULATIONS YOU HAVE DONE**.
- **ALWAYS**, as part of your "Final Answer", explain how you got
to the answer on a section that starts with: "\n\nExplanation:\n".
In the explanation, mention the column names that you used to get
to the final answer.
"""

# QUESTION = "How many firms are located in India and have no websites?"

# response = agent.invoke(CSV_PROMPT_PREFIX + QUESTION + CSV_PROMPT_SUFFIX)
# print(f"Response: {response['output']}")
