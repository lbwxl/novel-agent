from langchain.agents import create_agent
from database_tools import read_database_chapter
from model import model

agent = create_agent(
  model=model,
  tools=[read_database_chapter],
  system_prompt="你是一个章节查询助手。"
        "回答章节内容的问题时，必须调用工具查询学习数据库。"
        "如果章节不存在，就如实说明，不要编造正文。"
)

if __name__ == "__main__":
    inputs = {
        "messages": [
            {
                "role": "user",
                "content": "请读取第 1 章，告诉我林深做了什么。",
            }
        ]
    }

    for chunk in agent.stream(inputs, stream_mode="updates"):
        if "model" in chunk:
            for message in chunk["model"]["messages"]:
                if message.tool_calls:
                    print("模型请求工具：", message.tool_calls)
                else:
                    print("模型回答：", message.content)

        if "tools" in chunk:
            for message in chunk["tools"]["messages"]:
                print("工具返回：", message.content)
