import json
import os
from typing import List
import requests
from fastapi import HTTPException, FastAPI
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from starlette import status
from models import CryptoAnalysisResponse, CryptoRequest

load_dotenv()

OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")
OPENROUTER_URL = os.getenv("OPENROUTER_URL")
COINGECKO_URL = os.getenv("COINGECKO_URL")

app = FastAPI(description="AI powered crypto Analysis API")

llm= ChatOllama(model="llama3.2:1b")

@tool
def get_crypto_data(coin_list: List[str]):
    """Calls coingecko API and retune row JSON market data"""
    if not coin_list:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No coins provided")

    coins = ",".join(coin_list)

    params = {
        "vs_currency": "usd",
        "ids": coins
    }
    crypto_api_repo = requests.get(COINGECKO_URL, params=params)
    return crypto_api_repo.json()

@tool
def analyze_crypto_data(raw_market_data:str):
    """Takes row json crypto market data coming from get_crypto_data tool , analyzes it using LLM and outputs cryptoAnalysisResponse"""
    chat_prompt = ChatPromptTemplate.from_template(
        """
   You are a "CryptoAnalyst - AI" a professional cryptocurrency market analyst

   You will be given recent market data for multiple cryptocurrencies (price, market cap, volume, 24h change)
   Here is market data :
   {market_data}

   Rules:
   - Return one analysis per cryptocurrency
   - Provide 3 key_factory and 3 insights per coin
   -Base you reasoning on given metric (e.g price change market cap trend)


   """
    )
    chain = chat_prompt | llm.with_structured_output(CryptoAnalysisResponse)
    output: CryptoAnalysisResponse = chain.invoke({"market_data": raw_market_data})
    return output


tools = [get_crypto_data,analyze_crypto_data]
system_prompt = """
Use get_crypto_data tool to first fetch raw market data,
Then you should use that raw market data to call analyze_crypto_data tool
Use the response from analyze_crypto_data to provide final output
"""
agent = create_agent(model=llm,tools=tools,system_prompt=system_prompt)

crypto = ["bitcoin","ethereum"]
result =agent.invoke({"messages" :[HumanMessage(content=f"analyze cryptocurrencies:{','.join(crypto)}")]})



# for message in result["messages"]:
#     print(message)
@app.post("/crypto/analysis",request_model=CryptoAnalysisResponse)
def analyze_crypro(request: CryptoRequest):
    result = agent.invoke({
        message
    })
    return get_crypto_analysis_response(request.coins)