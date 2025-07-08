import requests
import json
import os
import base64

url = "http://127.0.0.1:5000/ask"
def get_image_content(img_path_or_url):
    if img_path_or_url.startswith('http://') or img_path_or_url.startswith('https://'):
        return {"type": "image_url", "image_url": img_path_or_url}
    else:
        # 本地图片转base64
        with open(img_path_or_url, 'rb') as f:
            img_bytes = f.read()
        ext = os.path.splitext(img_path_or_url)[-1][1:] or 'png'
        b64 = base64.b64encode(img_bytes).decode('utf-8')
        return {"type": "image_url", "image_url": f"data:image/{ext};base64,{b64}"}

stream = False  # True 测试流式，False 测试非流式
DEFAULT_MODEL = "doubao-mix-v1"

messages = [
    {"role": "system", "content": "你是人工智能助手."}
]

while True:
    question = input("你：")
    if question.strip() in ["退出", "exit", "quit"]:
        print("对话结束。"); break
    model = DEFAULT_MODEL
    # 检查是否包含图片
    if 'img:' in question:
        parts = question.split('img:')
        text = parts[0].strip()
        img_path = parts[1].strip()
        content = []
        if text:
            content.append({"type": "text", "text": text})
        content.append(get_image_content(img_path))
        messages.append({"role": "user", "content": content})
        model = DEFAULT_MODEL  # 图片强制用doubao
    else:
        messages.append({"role": "user", "content": question})
    data = {
        "messages": messages,
        "stream": stream,
        "model": model
    }
    if stream:
        response = requests.post(url, json=data, stream=True)
        print("状态码:", response.status_code)
        print("流式返回内容:")
        for line in response.iter_lines(decode_unicode=True):
            if line:
                print(line, end="", flush=True)
        print()
    else:
        response = requests.post(url, json=data)
        print("状态码:", response.status_code)
        try:
            reply = response.json().get("reply")
            print("助手：", reply)
            messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            print("解析JSON失败:", e)
            print("返回内容(原始):", response.text)
    # 保存对话到本地json
    history_file = 'chat_history.json'
    try:
        if os.path.exists(history_file):
            with open(history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
        else:
            history = []
        history.append(list(messages))
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print('保存历史对话失败:', e)