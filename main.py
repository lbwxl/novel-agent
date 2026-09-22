import os
from pathlib import Path

from langchain_openai import ChatOpenAI
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

    # 最多等 2 分钟
    timeout=120,

    # 调试阶段失败就直接报错，不自动重试
    max_retries=0,
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
章节：第 {chapter} 章
目标字数：约 {word_count} 字
"""
    )
])


chain = prompt | model


def generate_chapter(
    genre,
    protagonist,
    chapter,
    word_count,
):
    print("开始生成小说...")
    print(f"模型：{MODEL_ID}")
    print(f"接口：{BASE_URL}")

    try:
        response = chain.invoke({
            "genre": genre,
            "protagonist": protagonist,
            "chapter": chapter,
            "word_count": word_count,
        })

        print("模型生成完成")

        return response.content

    except Exception as error:
        print()
        print("模型调用失败")
        print("异常类型：", type(error).__name__)
        print("异常内容：", error)

        raise


def save_chapter(chapter, content):
    chapters_dir = Path("novel/chapters")

    chapters_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    file_path = chapters_dir / f"{chapter:03d}.md"

    file_path.write_text(
        content,
        encoding="utf-8"
    )

    return file_path


chapter = 1

content = generate_chapter(
    genre="玄幻",
    protagonist="林深",
    chapter=chapter,

    # 调试阶段先别写 1000 字
    word_count=200,
)


file_path = save_chapter(
    chapter=chapter,
    content=content,
)


print(f"小说已保存：{file_path}")