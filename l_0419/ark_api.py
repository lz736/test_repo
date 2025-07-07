from flask import Flask, request, jsonify
import os
from volcenginesdkarkruntime import Ark

app = Flask(__name__)

# 初始化Ark客户端，推荐用环境变量存储API Key
client = Ark(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key="d802b8de-3c68-4cf2-8ae2-9fb769d0592a"
)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    image_url = data.get('image_url')
    question = data.get('question')
    if not image_url or not question:
        return jsonify({'error': '缺少 image_url 或 question'}), 400

    response = client.chat.completions.create(
        model="doubao-seed-1-6-250615",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url},
                    },
                    {"type": "text", "text": question},
                ],
            }
        ],
        stream=True
    )

    ai_reply = ""
    for chunk in response:
        if chunk.choices[0].delta.content:
            ai_reply += chunk.choices[0].delta.content

    return jsonify({'reply': ai_reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 