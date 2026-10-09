import argparse
from pathlib import Path

inputs = {
    "messages": [
        {
            "role": "user",
            "content": """
                  请继续创作这本小说的下一章。

                  本次创作约 300 字用于测试。
                  完成后保存新章节、更新小说进度，并报告执行结果。
            """
        }
    ]
}

def continue_novel() -> None:
    from agent import agent

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


def main() -> int:
    parser = argparse.ArgumentParser(
        description="继续创作小说，或为已保存的章节补生成摘要。",
    )
    parser.add_argument(
        "--summary",
        type=int,
        metavar="章节号",
        help="只为指定章节生成摘要，不续写小说或更新进度。",
    )
    args = parser.parse_args()

    if args.summary is not None:
        if args.summary < 1:
            parser.error("摘要章节号必须大于等于 1。")

        from tools import generate_chapter_summary

        result = generate_chapter_summary.invoke({"chapter": args.summary})
        print(result)

        summary_path = Path("novel/summaries") / f"{args.summary:03d}.md"
        if not summary_path.is_file():
            return 1
        if not summary_path.read_text(encoding="utf-8").strip():
            return 1
        return 0

    continue_novel()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
