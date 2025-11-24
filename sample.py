import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")
OPENROUTER_URL = os.getenv("OPENROUTER_URL")

chat_prompt = ChatPromptTemplate.from_template(
    """
    You re a expert humorous poem writer

    You will be give a word as input, Then you should write a humorous poem for it

    Below is the word

    {word}
    """
)
llm = ChatOpenAI(model="meta-llama/llama-3.3-70b-instruct:free",
                 base_url=OPENROUTER_URL, api_key=OPENROUTER_KEY)

responses_chain = chat_prompt | llm  # LCEL = langchain expression language

resp = responses_chain.invoke({"word": "Namal Rajapaksha"})

print(resp.content)