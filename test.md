```shell
uv run python - <<'PY'
from langchain.agents import create_agent
from model import model
from tools import read_chapter, read_chapter_summary

reader = create_agent(
    model=model,
    tools=[read_chapter_summary, read_chapter],
    system_prompt="""
回答小说问题前，先通过工具获取依据。
快速回顾剧情时，优先读取摘要。
需要精确细节或引用原话时，读取正文。
不要把猜测写成已确认事实。
""",
)

result = reader.invoke({
    "messages": [{
        "role": "user",
        "content": "第4章中，执事制止追击时说的原话是什么？请逐字引用。",
    }]
})

for message in result["messages"]:
    if message.type == "ai" and message.tool_calls:
        print("模型请求：", message.tool_calls)
    if message.type == "tool":
        print("工具返回：", message.name, message.content)

print("最后回答：", result["messages"][-1].content)
PY

```
