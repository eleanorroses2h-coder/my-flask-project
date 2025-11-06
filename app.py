from flask import Flask, request, jsonify
from flask_cors import CORS  # 导入 CORS
from openai import OpenAI
import logging
import json
import os

# 直接硬编码 API key
client = OpenAI(api_key="YOUR_ACTUAL_API_KEY")  # 替换为你实际的 API key

# logging 设置
logging.basicConfig(
    filename="agent.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

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

# 创建 Flask 应用实例
app = Flask(__name__)
CORS(app)  # 启用 CORS

# 定义根路径路由
@app.route('/', methods=['GET'])
def home():
    return "Welcome to the Resume Generator API"

@app.route('/resume', methods=['POST'])
def generate_resume():
    content = request.json.get('content')
    if not content:
        return jsonify({"error": "Missing 'content' parameter"}), 400

    # 调用生成简历函数
    answer = think_and_write_resume(content)

    return jsonify({"response": answer})

if __name__ == '__main__':
    app.run(debug=True)
