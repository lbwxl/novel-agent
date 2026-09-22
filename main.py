import os

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

BASE_URL = os.getenv(
    "LLM_BASE_URL",
    "http://127.0.0.1:8081/v1"
)

MODEL_ID = os.getenv(
    "LLM_MODEL_ID",
    "local-qwen36"
)

API_KEY = os.getenv(
    "LLM_API_KEY",
    "SK-LOCAL-NOT-CHECKED"
)

model = ChatOpenAI(
    base_url=BASE_URL,
    model=MODEL_ID,
    api_key=API_KEY,
)

messages = [
    SystemMessage(
        content="你是一名擅长写网络小说的专业小说作家"
    ),
    HumanMessage(
        content="请给我写一个玄幻小说的开头，大约300字。"
    )
]

response = model.invoke(messages)
print(response.content)