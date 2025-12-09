import os
from dotenv import load_dotenv
from fastapi import FastAPI
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

load_dotenv()

OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")
OPENROUTER_URL = os.getenv("OPENROUTER_URL")
COINGECKO_URL = os.getenv("COINGECKO_URL")

#response_llm = ChatOllama(model="llam3.2:1b")

             # llama model and open router key
# summarizer_llm = ChatOpenAI(model="meta-llama/llama-3.3-70b-instruct:free",
#                      base_url=OPENROUTER_URL, api_key=OPENROUTER_KEY)
# response_llm = ChatOpenAI(model="meta-llama/llama-3.3-70b-instruct:free",
#                      base_url=OPENROUTER_URL, api_key=OPENROUTER_KEY)

            # ChatGoogleGenerativeAI
summarizer_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
response_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

car_model = "axio"
brand = "toyota"

urls = [
    f"https://ikman.lk/en/ads?query={car_model}",
    f"https://patpat.lk/en/sri-lanka/vehicle/car/{brand}/{car_model}"
]

loader = WebBaseLoader(urls)
docs = loader.load()

print(docs)

summarizer_prompt = ChatPromptTemplate.from_template(
    """Extract car price, location and manufacture years : \n\n {docs}"""
)

summarizer_chain = summarizer_prompt | summarizer_llm
ads_summary = summarizer_chain.invoke({"docs": "\n".join([doc.page_content for doc in docs])})

response_prompt = ChatPromptTemplate.from_template(
    """
    You are an automotive assistant helping users find the best car deals.
    here is a summarized list of car as for {car_model}.
    
    {ads_summary}
    
    Highlight key insights, suggest buyer types, and provide a 2-3 sentence summary.
    also provide best average price to buy.
    """
)

response_chain = response_prompt | response_llm
resp = response_chain.invoke({
    "ads_summary": ads_summary,
    "car_model": car_model
})
print(resp)

app = FastAPI(title="AI vehicle Analysis Tool")