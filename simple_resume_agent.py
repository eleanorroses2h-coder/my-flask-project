from openai import OpenAI
import logging
import json
import os

# logging 设置
logging.basicConfig(
    filename="agent.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

# 从环境变量读取 key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 尝试加载旧记忆
def load_memory():
    try:
        with open("memory.json", "r", encoding="utf-8") as f:
            return f.read()
    except:
        return ""

agent_memory = load_memory()

def think_and_write_resume(prompt):
    global agent_memory

    logging.info(f"USER INPUT: {prompt}")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "你是一个专业的简历撰写顾问，负责优化用户简历。"},
            {"role": "assistant", "content": agent_memory},
            {"role": "user", "content": prompt}
        ]
    )

    reply = response.choices[0].message.content

    logging.info(f"AGENT OUTPUT: {reply}")

    # 保存到内存
    agent_memory += "\n" + reply

    # 写入文件
    with open("memory.json", "w", encoding="utf-8") as f:
        f.write(agent_memory)

    return reply


print("=== Resume Agent 已启动 ===")

# 捕获用户输入并控制程序退出
try:
    while True:
        content = input("> 你想让简历怎么写？\n> ")
        if content.lower() in ["exit", "quit"]:
            print("=== Agent 退出 ===")
            break  # 正常退出循环
        answer = think_and_write_resume(content)
        print("\nAgent: ", answer, "\n")

except KeyboardInterrupt:
    print("\n=== 程序中断 ===")
