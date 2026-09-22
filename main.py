import os

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate


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


prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "你是一名擅长写网络小说的专业小说作家。"
    ),
    (
        "human",
        """
            请创作一章小说。
            小说类型：{genre}
            主人公：{protagonist}
            章节：第{chapter} 章
            目标字数：{word_count} 字
        """
    )
])

messages = prompt.invoke({
    "genre": "玄幻",
    "protagonist": "林深",
    "chapter": 1,
    "word_count": 1000,
})

response = model.invoke(messages)
print(response.content)