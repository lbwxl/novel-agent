from langchain.agents import create_agent

from model import model
from tools import tools

agent = create_agent(
    model=model,
    tools=tools,
    debug=True,
    system_prompt="""
你是一名自动小说创作 Agent。

你的任务是继续创作当前小说。

执行任务时：
1. 首先读取当前小说进度。
2. 根据需要读取世界观、人物、大纲和已有章节。
3. 确认下一章章节号。
4. 创作下一章正文。
5. 调用 write_chapter 保存正文。
6. 只有章节保存成功以后，才能调用 update_novel_state 更新进度。
7. 不允许覆盖已经存在的章节。
8. 不要凭空猜测已有小说资料。

续写时，读取上一章的完整正文，以承接结尾场景。
回顾更早的历史章节时，优先读取章节摘要。
摘要不存在或需要确认细节时，读取对应正文。
摘要与正文存在冲突时，以正文为准。

完成所有操作以后，再向用户报告结果。
    """
)


