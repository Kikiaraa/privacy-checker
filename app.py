from flask import Flask, request, jsonify
from prompt_builder import build_prompt
from zhipu_request import call_zhipu

app = Flask(__name__)

# 读取知识库文本，启动时加载一次即可
with open("kb_text.txt", "r", encoding="utf-8") as f:
    kb_text = f.read()

@app.route("/api/ask", methods=["POST"])
def ask():
    data = request.json
    data_item = data.get("data_item", "").strip()
    usage = data.get("usage", "").strip()

    if not data_item or not usage:
        return jsonify({"error": "缺少 data_item 或 usage 参数"}), 400

    # 构造 prompt
    prompt = build_prompt(data_item, usage, kb_text)

    # 调用智谱清言GLM API
    answer = call_zhipu(prompt)

    return jsonify({"answer": answer})


@app.route("/")
def index():
    # 返回前端页面
    from flask import send_from_directory
    return send_from_directory(".", "index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
