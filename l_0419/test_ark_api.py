import requests
import json
import os
import base64

# 尝试导入PIL用于图片压缩
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("💡 提示：安装 Pillow 库可以自动压缩大图片: pip install Pillow")

url = "http://127.0.0.1:5000/ask"

def compress_image_if_needed(img_path, max_size_kb=800):
    """
    检查图片大小，如果太大则自动压缩
    返回: (处理后的图片路径, 是否进行了压缩)
    """
    if not os.path.exists(img_path):
        return img_path, False

    # 检查文件大小
    file_size = os.path.getsize(img_path)
    file_size_kb = file_size / 1024

    print(f"📏 图片文件大小: {file_size_kb:.1f} KB")

    # 如果文件小于限制，直接返回
    if file_size_kb <= max_size_kb:
        print("✅ 图片大小合适，无需压缩")
        return img_path, False

    # 如果PIL不可用，给出提示
    if not PIL_AVAILABLE:
        print(f"⚠️ 图片较大({file_size_kb:.1f} KB > {max_size_kb} KB)，建议安装Pillow进行自动压缩")
        print("   命令: pip install Pillow")
        return img_path, False

    # 进行压缩
    print(f"🔧 图片较大({file_size_kb:.1f} KB)，开始自动压缩...")

    try:
        # 生成压缩后的文件名
        name, ext = os.path.splitext(img_path)
        compressed_path = f"{name}_compressed.jpg"

        # 打开并压缩图片
        with Image.open(img_path) as img:
            # 转换为RGB模式
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')

            width, height = img.size
            print(f"📐 原始尺寸: {width}x{height}")

            # 逐步压缩直到满足大小要求
            quality = 85
            scale = 1.0

            while quality > 20:
                # 调整尺寸
                if scale < 1.0:
                    new_width = int(width * scale)
                    new_height = int(height * scale)
                    resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                else:
                    resized_img = img

                # 保存并检查大小
                resized_img.save(compressed_path, 'JPEG', quality=quality)
                compressed_size = os.path.getsize(compressed_path)
                compressed_size_kb = compressed_size / 1024

                if compressed_size_kb <= max_size_kb:
                    print(f"✅ 压缩成功! 大小: {compressed_size_kb:.1f} KB")
                    if scale < 1.0:
                        print(f"📐 压缩后尺寸: {int(width * scale)}x{int(height * scale)}")
                    print(f"🎯 压缩质量: {quality}")
                    return compressed_path, True

                # 调整压缩参数
                if quality > 60:
                    quality -= 15
                elif scale > 0.6:
                    scale -= 0.2
                    quality = 85
                else:
                    quality -= 10

            # 如果还是太大，使用最小设置
            print(f"⚠️ 使用最大压缩，最终大小: {compressed_size_kb:.1f} KB")
            return compressed_path, True

    except Exception as e:
        print(f"❌ 压缩失败: {e}")
        return img_path, False
def get_image_content(img_path_or_url):
    """处理图片，支持本地文件和网络链接，自动压缩大图片"""
    if img_path_or_url.startswith('http://') or img_path_or_url.startswith('https://'):
        print(f"🌐 使用网络图片: {img_path_or_url}")
        return {"type": "image_url", "image_url": {"url": img_path_or_url}}
    else:
        # 本地图片转base64
        try:
            # 尝试多个可能的路径
            possible_paths = [
                img_path_or_url,  # 原始路径
                os.path.join('.', img_path_or_url),  # 当前目录
                os.path.join('l_0419', img_path_or_url),  # l_0419目录
                os.path.abspath(img_path_or_url)  # 绝对路径
            ]

            actual_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    actual_path = path
                    break

            if actual_path is None:
                print(f"❌ 错误：图片文件不存在: {img_path_or_url}")
                print(f"📁 当前工作目录: {os.getcwd()}")
                print(f"🔍 尝试过的路径:")
                for path in possible_paths:
                    print(f"   - {path}")
                return None

            print(f"✅ 找到图片文件: {actual_path}")

            # 检查并压缩图片（如果需要）
            processed_path, was_compressed = compress_image_if_needed(actual_path)

            # 读取处理后的图片
            with open(processed_path, 'rb') as f:
                img_bytes = f.read()

            # 获取文件扩展名
            ext = os.path.splitext(processed_path)[-1][1:] or 'png'

            # 转换为base64
            b64 = base64.b64encode(img_bytes).decode('utf-8')
            b64_size_kb = len(b64) / 1024

            print(f"📊 Base64编码大小: {b64_size_kb:.1f} KB")

            if was_compressed:
                print(f"🗑️ 可以删除临时压缩文件: {processed_path}")

            return {"type": "image_url", "image_url": {"url": f"data:image/{ext};base64,{b64}"}}

        except Exception as e:
            print(f"❌ 错误：读取图片失败: {e}")
            return None

stream = False  # True 测试流式，False 测试非流式
DEFAULT_MODEL = "eepseek-v3-250324"

messages = [
    {"role": "system", "content": "你是人工智能助手."}
]

print("💬 AI助手已启动！")
print("📝 使用说明：")
print("   - 普通聊天：直接输入文字")
print("   - 图片聊天：输入 'img:图片路径或链接 你的问题'")
print("   - 例如：img:https://example.com/image.jpg 这是什么？")
print("   - 例如：img:./photo.jpg 分析这张图片")
print("   - 退出：输入 '退出'、'exit' 或 'quit'")
print("=" * 50)

while True:
    question = input("\n你：")
    if question.strip() in ["退出", "exit", "quit"]:
        print("对话结束。"); break

    # 检查是否包含图片
    if 'img:' in question:
        parts = question.split('img:', 1)  # 只分割一次，防止图片路径中有冒号
        text = parts[0].strip()
        img_info = parts[1].strip()

        # 进一步分割图片路径和问题文本
        img_parts = img_info.split(' ', 1)
        img_path = img_parts[0]
        img_question = img_parts[1] if len(img_parts) > 1 else ""

        # 组合完整的问题文本
        full_text = f"{text} {img_question}".strip()
        if not full_text:
            full_text = "请分析这张图片"

        # 处理图片
        image_content = get_image_content(img_path)
        if image_content is None:
            print("❌ 图片处理失败，请检查图片路径或网络连接")
            continue

        content = [
            {"type": "text", "text": full_text},
            image_content
        ]
        messages.append({"role": "user", "content": content})
        print(f"🖼️ 已添加图片: {img_path}")
    else:
        messages.append({"role": "user", "content": question})
    data = {
        "messages": messages,
        "stream": stream
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
        print(f"📡 状态码: {response.status_code}")
        try:
            result = response.json()
            reply = result.get("reply")
            model_used = result.get("model", "未知")

            if reply:
                print(f"🤖 助手 ({model_used})：{reply}")
                # 如果服务端返回了完整的消息历史，使用它；否则手动添加
                if "messages" in result:
                    messages = result["messages"]
                else:
                    messages.append({"role": "assistant", "content": reply})
            else:
                print("❌ 服务端返回空回复")
                print("原始响应:", result)
        except Exception as e:
            print(f"❌ 解析JSON失败: {e}")
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
        #d:\Pictures\GenshinImpactCloudGame\GenshinlmpactPhoto 2023_08_25 16_37_03.png