import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

load_dotenv()

OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")
OPENROUTER_URL = os.getenv("OPENROUTER_URL")
COINGECKO_URL = os.getenv("COINGECKO_URL")

@tool
def add(x:int,y:int):
    """Adds two numbers"""
    return x + y
@tool
def subtrack(x:int,y:int):
    """Subtack two numbers"""
    return  x -y
model = ChatOpenAI(model="meta-llama/llama-3.3-70b-instruct:free",
                     base_url=OPENROUTER_URL, api_key=OPENROUTER_KEY)
# model= ChatOllama(model="llama3.2:1b")
tools = [add,subtrack]

agent = create_agent(model=model,tools= tools)

result = agent.invoke({
    "messages" : [HumanMessage(content="What is 45 + 35")]
})

for message in result["messages"]:
    print(message)