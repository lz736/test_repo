import requests

url = "http://127.0.0.1:5000/ask"
data = {
    "image_url": "https://mmbiz.qpic.cn/sz_mmbiz_jpg/UicQ7HgWiaUb2qlHtWibUZlHElxQfK1hqPg3IPVicSeVekNledLSiarptgPWjXo5Tp0iaYPWPzTgZ2nBZk4By6kgCG0g/640?wx_fmt=jpeg&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1",  # 替换为你要测试的图片链接
    "question": "这张图片里有什么？"                   # 替换为你要问的问题
}

response = requests.post(url, json=data)
print("状态码:", response.status_code)
print("返回内容(原始):", response.text)
try:
    print("返回内容(JSON):", response.json())
except Exception as e:
    print("解析JSON失败:", e)