from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from memory_utils import get_session_history
import os
from dotenv import load_dotenv

load_dotenv()

system_prompt = """
You are a warm, emotionally intelligent AI assistant named DSCPL.
You speak like a wise friend — calm, spiritual, and compassionate.
Use gentle emojis where helpful. Be real, kind, and encouraging.But don't use
lot of emojis,use very minimal.
"""

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",  
    temperature=0.7,
    google_api_key=os.environ["GOOGLE_API_KEY"]
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

chain = prompt | llm

chat_with_memory = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

def get_chat_chain():
    return chat_with_memory
