import os

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("LLM_BASE_URL")
MODEL_ID = os.getenv("LLM_MODEL_ID")
API_KEY = os.getenv("LLM_API_KEY")


# 本地推理模型可能很久才写出完整 JSON。
# 流式读取 + 较长 read 超时，避免卡在等响应头时 ReadTimeout。
model = ChatOpenAI(
    base_url=BASE_URL,
    model=MODEL_ID,
    api_key=API_KEY,

    use_responses_api=True,

    reasoning={
        "effort": "high",
    },

    store=False,
    output_version="responses/v1",

    timeout=300,
    max_retries=2,
    streaming=True,
)
