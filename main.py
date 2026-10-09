from agent import agent

inputs = {
    "messages": [
        {
            "role": "user",
            "content": """
                  本次为了观察上下文的使用：
                  请先读取第 1～3 章摘要，再读取第 4 章完整正文。
                  结合世界观、人物设定和大纲，继续创作下一章。
                 请继续创作这本小说的下一章。

                你需要自行了解当前小说进度、上一章剧情、
                世界观、人物设定和小说大纲。

                本次先创作约 300 字用于测试。

                完成创作后：
                1. 保存新章节
                2. 更新小说进度
                3. 最后告诉我执行结果
            """
        }
    ]
}

for chunk in agent.stream(
    inputs,
    stream_mode="updates",
):
    if "model" in chunk:
        print()
        print("🤖 模型完成一次思考")

        messages = chunk["model"]["messages"]

        for message in messages:
            if message.tool_calls:
                print("模型准备调用工具：")

                for tool_call in message.tool_calls:
                    print(
                        "-",
                        tool_call["name"],
                        tool_call["args"],
                    )

            elif message.content:
                print("模型回答：")
                print(message.content)

    if "tools" in chunk:
        print()
        print("🔧 工具执行完成")

        messages = chunk["tools"]["messages"]

        for message in messages:
            print("工具：", message.name)
            print("结果：", message.content)
