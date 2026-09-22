import os
from pathlib import Path

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage


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
        """
            你是一名擅长写网络小说的专业小说作家。
            你必须严格参考以下小说资料进行创作。
            必须自然承接上一章剧情
            【世界观】
            {world}
            
            【人物设定】
            {characters}
            
            【小说大纲】
            {outline}
            
            【上一章内容】
            {previous_chapter}
        """
    ),
    (
        "human",
        """
            请创作一章小说。
            
            小说类型：{genre}
            主人公：{protagonist}
            章节：第 {chapter} 章
            目标字数：约 {word_count} 字
            
            要求：
            1. 不要违反已有世界观
            2. 不要随意修改人物设定
            3. 剧情应尽量符合小说大纲
        """
    )
])


chain = prompt | model


def generate_chapter(
    genre,
    protagonist,
    chapter,
    word_count,
    world,
    characters,
    outline,
    previous_chapter,
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
            "world": world,
            "characters": characters,
            "outline": outline,
            "previous_chapter": previous_chapter,
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

def read_novel_file(filename):
    file_path = Path("novel") / filename

    return file_path.read_text(
        encoding="utf-8"
    )

def read_previous_chapter(chapter):
    if chapter <= 1:
        return "这是第一章，没有上一章内容。"

    previous_chapter = chapter - 1

    file_path = Path("novel/chapters") / f"{previous_chapter:03d}.md"

    if not file_path.exists():
        return "未找到上一章内容。"

    return file_path.read_text(
        encoding="utf-8"
    )

@tool
def read_world():
    """读取小说世界观设定。"""
    return Path("novel/world.md").read_text(
        encoding="utf-8"
    )

@tool
def read_characters():
    """读取小说人物设定"""
    return Path("novel/characters.md").read_text(
        encoding="utf-8"
    )

@tool
def read_outline():
    """读取小说整体大纲"""
    return Path("novel/outline.md").read_text(
        encoding="utf-8"
    )

world = read_novel_file("world.md")
characters  = read_novel_file("characters.md")
outline  = read_novel_file("outline.md")

chapter = 2

previous_chapter = read_previous_chapter(chapter)

# content = generate_chapter(
#     genre="玄幻",
#     protagonist="林深",
#     chapter=chapter,
#
#     # 调试阶段先别写 1000 字
#     word_count=200,
#     world=world,
#     characters=characters,
#     outline=outline,
#     previous_chapter=previous_chapter
# )
#
#
# file_path = save_chapter(
#     chapter=chapter,
#     content=content,
# )


# print(f"小说已保存：{file_path}")

tools = [
    read_world,
    read_characters,
    read_outline,
]

model_with_tools = model.bind_tools(tools)

messages = [
    HumanMessage(
        content="我要继续创作小说，在开始创作之前，请先读取小说的世界观设定。"
    )
]

response = model_with_tools.invoke(messages)
messages.append(response)

print("第一次模型返回：")
print(response.tool_calls)

tools_by_name = {
    tool.name: tool
    for tool in tools
}
print('tools_by_name', tools_by_name)
for tool_call in response.tool_calls:
    tool_name = tool_call["name"]
    tool_args = tool_call["args"]

    tool = tools_by_name[tool_name]
    result = tool.invoke(tool_args)

    tool_message = ToolMessage(
        content=result,
        tool_call_id=tool_call["id"],
    )

    messages.append(tool_message)


final_response = model_with_tools.invoke(messages)

print("模型最终问题：")
print(final_response.content)
