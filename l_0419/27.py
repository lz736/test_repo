from flask import Flask, request, jsonify, Response
import os
from volcenginesdkarkruntime import Ark
import json

app = Flask(__name__)

# 初始化Ark客户端，推荐用环境变量存储API Key
client = Ark(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key="d802b8de-3c68-4cf2-8ae2-9fb769d0592a"
)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    messages = data.get('messages')
    question = data.get('question')
    stream = data.get('stream', False)
    if messages:
        # 如果有多轮对话，直接用
        pass
    elif question:
        messages = [
            {"role": "system", "content": "你是人工智能助手."},
            {"role": "user", "content": question},
        ]
    else:
        return jsonify({'error': '缺少 question 或 messages'}), 400

    # 保存历史对话到 json 文件
    history_file = 'chat_history.json'
    try:
        if os.path.exists(history_file):
            with open(history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
        else:
            history = []
        history.append(messages)
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print('保存历史对话失败:', e)

    try:
        if stream:
            def generate():
                stream_resp = client.chat.completions.create(
                    model="deepseek-v3-250324",
                    messages=messages,
                    stream=True,
                )
                for chunk in stream_resp:
                    if chunk.choices and chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content
            return Response(generate(), mimetype='text/plain')
        else:
            completion = client.chat.completions.create(
                model="deepseek-v3-250324",
                messages=messages,
            )
            return jsonify({'reply': completion.choices[0].message.content})
    except Exception as e:
        import traceback
        print("后端异常：", e)
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
