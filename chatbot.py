
import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough


load_dotenv()

# Load FAISS vector DB
print("Loading FAISS vector store...")
vectorstore = FAISS.load_local(
    "faiss_index",
    OpenAIEmbeddings(model="text-embedding-3-small"),  
    allow_dangerous_deserialization=True
)

# Set up Gemini model (using Gemini 1.5 Flash)
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",   
    temperature=0.3,
    max_output_tokens=250,  
)

# Prompt template
template = """
You are a helpful assistant for the Electrical Engineering Department website.
Answer the user's question using ONLY the provided context below.

Context:
{context}

Question: {question}

Answer:
"""

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=template
)

# New Clean RAG Chain (Runnable version)
rag_chain = (
    RunnableParallel({
        "context": vectorstore.as_retriever(),   # retrieve from FAISS
        "question": RunnablePassthrough()        # passthrough user input
    })
    | prompt                                   # fill prompt
    | llm                                      # send to Gemini model
    | StrOutputParser()                        # parse back plain text
)

# Function to get final answer
def get_answer(query):
    return rag_chain.invoke(query)    # ✅ Modern .invoke() style (no .run())
