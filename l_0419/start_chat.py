#!/usr/bin/env python3
"""
启动聊天系统 - 同时启动后端API和Web界面
"""

import subprocess
import time
import sys
import os
import requests
from threading import Thread

def start_backend():
    """启动后端API服务器"""
    print("🚀 启动后端API服务器...")
    try:
        # 使用27.py作为后端
        subprocess.run([sys.executable, "27.py"], cwd=os.getcwd())
    except KeyboardInterrupt:
        print("🛑 后端服务器已停止")

def start_frontend():
    """启动前端Web界面"""
    print("🌐 启动Web界面...")
    try:
        subprocess.run([sys.executable, "web_chat.py"], cwd=os.getcwd())
    except KeyboardInterrupt:
        print("🛑 Web界面已停止")

def check_backend():
    """检查后端是否启动"""
    for i in range(30):  # 等待30秒
        try:
            response = requests.get("http://127.0.0.1:5000/", timeout=2)
            print("✅ 后端API服务器已启动")
            return True
        except:
            if i == 0:
                print("⏳ 等待后端API服务器启动...")
            time.sleep(1)
    
    print("❌ 后端API服务器启动失败")
    return False

def main():
    """主函数"""
    print("🎉 启动AI聊天系统")
    print("=" * 50)
    
    # 检查依赖
    try:
        import flask
        print("✅ Flask已安装")
    except ImportError:
        print("❌ 请安装Flask: pip install flask")
        return
    
    try:
        from volcenginesdkarkruntime import Ark
        print("✅ 方舟SDK已安装")
    except ImportError:
        print("❌ 请安装方舟SDK: pip install volcenginesdkarkruntime")
        return
    
    try:
        from PIL import Image
        print("✅ Pillow已安装")
    except ImportError:
        print("⚠️ Pillow未安装，图片压缩功能不可用")
        print("   安装命令: pip install Pillow")
    
    print("\n📋 系统组件:")
    print("   - 后端API: http://127.0.0.1:5000")
    print("   - Web界面: http://127.0.0.1:8000")
    print("   - 支持功能: 文本聊天 + 图片分析")
    
    try:
        # 启动后端服务器（在新线程中）
        backend_thread = Thread(target=start_backend, daemon=True)
        backend_thread.start()
        
        # 等待后端启动
        if not check_backend():
            print("❌ 无法启动后端服务器，请检查端口5000是否被占用")
            return
        
        print("\n🌐 启动Web界面...")
        print("📱 请在浏览器中访问: http://127.0.0.1:8000")
        print("🔧 按 Ctrl+C 停止服务")
        print("=" * 50)
        
        # 启动前端（在主线程中）
        start_frontend()
        
    except KeyboardInterrupt:
        print("\n👋 感谢使用AI聊天系统！")
    except Exception as e:
        print(f"❌ 启动失败: {e}")

if __name__ == "__main__":
    main()
