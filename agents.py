from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI


# model setup
llm = ChatOpenAI(
    model="openai/gpt-4o-mini",  # OpenRouter uses the format "provider/model-name"
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0,
)

#first agent  of searching the web for recent and reliable information on a topic and return the titles, urls, and snippets
def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search],
    )
    
#second agent of scraping and returning clean text content from a given URL for deeper reading.
def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url],
    )
    

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
])


writer_chain = writer_prompt | llm | StrOutputParser()


#critic_chain
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Weaknesses:
- ...
- ...

Suggestions for Improvement:
- ...
- ..."""),
])

critic_chain = critic_prompt | llm | StrOutputParser()