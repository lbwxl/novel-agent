from agent import agent

inputs = {
    "messages": [
        {
            "role": "user",
            "content": """
                我想继续写这本小说的下一章。
    
                请你自行读取需要的信息，
                了解小说目前的进度和前文剧情，
                然后告诉我下一章应该重点推进什么内容。
            """
        }
    ]
}

for chunk in agent.stream(
    inputs,
    stream_mode="updates",
    debug=True,
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