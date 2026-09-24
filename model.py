import os

import httpx2
from langchain_openai import ChatOpenAI

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


# 本地推理模型可能很久才写出完整 JSON。
# 流式读取 + 较长 read 超时，避免卡在等响应头时 ReadTimeout。
model = ChatOpenAI(
    base_url=BASE_URL,
    model=MODEL_ID,
    api_key=API_KEY,
    timeout=httpx2.Timeout(
        connect=10.0,
        read=600.0,
        write=30.0,
        pool=10.0,
    ),
    max_retries=2,
    streaming=True,
)
