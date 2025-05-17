import os
from dotenv import load_dotenv
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

# Load environment variables from .env file
load_dotenv()

