#!/usr/bin/env python3
"""
最简单的测试服务器
"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return '''
    <html>
    <head><title>测试服务器</title></head>
    <body>
        <h1>🎉 服务器正常运行！</h1>
        <p>如果你能看到这个页面，说明Flask服务器工作正常。</p>
        <p>当前时间: <span id="time"></span></p>
        <script>
            document.getElementById('time').textContent = new Date().toLocaleString();
        </script>
    </body>
    </html>
    '''

if __name__ == '__main__':
    print("🚀 启动测试服务器...")
    print("📡 访问地址: http://127.0.0.1:9000")
    print("🔧 如果能访问这个地址，说明Flask工作正常")
    print("=" * 50)
    
    try:
        app.run(host='127.0.0.1', port=9000, debug=True)
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        import traceback
        traceback.print_exc()
