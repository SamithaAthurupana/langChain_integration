import os
from dotenv import load_dotenv
from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import YoutubeLoader
from typing import Optional, List
from pydantic import BaseModel, Field


load_dotenv()

OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")
OPENROUTER_URL = os.getenv("OPENROUTER_URL")
COINGECKO_URL = os.getenv("COINGECKO_URL")


class YoutubeAnalysisResponse(BaseModel):
    title: str = Field(description="Title of the video")
    summary: str = Field(description="Summary of the video")
    key_topics: List[str] = Field(description="Key topics covered in the video")

class QuizQuestion(BaseModel):
    question: str =Field(description="A question generate by the video transcript")
    options: List[str] = Field(description="4 answers for the question")
    correct_answer: str = Field("Correct Answer")

class QuizResponse(BaseModel):
    title: str
    questions: List[QuizQuestion]

class YoutubeRequest(BaseModel):
    url: str

# print(transcript)
#response_llm = ChatOllama(model="llam3.2:1b")
             # llama model and open router key
llm = ChatOpenAI(model="meta-llama/llama-3.3-70b-instruct:free",
                     base_url=OPENROUTER_URL, api_key=OPENROUTER_KEY)
            # ChatGoogleGenerativeAI
# summarizer_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
# response_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash").with_structured_output()

analysis_llm = llm.with_structured_output(YoutubeAnalysisResponse)

analysis_prompt = ChatPromptTemplate.from_template(
    """
    You are an expert content analyst .
    analyse the following youtube video transcript
    
    {transcript}
    
    Extract:
    - Main topics covered
    - Summary of the video
    - Recommended audience
    """
)

quiz_prompt = ChatPromptTemplate.from_template("""
    You are an expert exam paper maker.
    Your job is to generate a quiz base on following  transcript
    
    {transcript}

    - Generate exactly 10 questions
    - Each question should be a multiple choice (A,B,C,D)
    - Mark the correct answer
""")
quiz_llm = llm.with_structured_output(QuizResponse)

app = FastAPI(title="AI Video Analysis tool")

@app.post("/get-video-analysis")
def get_video_analysis(request: YoutubeRequest):

    loader = YoutubeLoader.from_youtube_url(
        request.url, add_video_info = False
    )
    transcript = loader.load()[0].page_content
    analysis_chain = analysis_prompt | analysis_llm

    response: YoutubeAnalysisResponse = analysis_chain.invoke({"transcript": transcript})

    return response

@app.post("/generate_quiz")
def get_quiz_resp(request: YoutubeRequest):
    loader = YoutubeLoader.from_youtube_url(
        request.url, add_video_info = False
    )
    transcript = loader.load()[0].page_content
    quiz_chain = quiz_llm | analysis_llm
    response: QuizResponse = quiz_chain.invoke({"transcript": transcript})

    return response

#write an API to get highlights in the video, Summary of the video
#, pros and cons of the video, Targeted audience of the video
#{title: str Title of the video
#, key_topics: List[str] key topics covered in the video,
# summary: str Summary of the video
# recommended_audience: str