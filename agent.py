from langchain.agents import create_agent

from model import model
from tools import tools

agent = create_agent(
    model=model,
    tools=tools,
    system_prompt="""
        你是一名专业小说创作助手。

        你的任务是帮助继续创作小说。
        
        你可以根据需要主动读取：
        - 当前小说进度
        - 世界观
        - 人物设定
        - 小说大纲
        - 已有章节
        
        不要凭空猜测已有小说内容。
        
        在获得足够的信息以后，
        再给出最终回答。
    """
)