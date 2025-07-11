#!/usr/bin/env python3
"""
检查服务器状态
"""

import requests
import time

def check_server(url, name):
    """检查单个服务器"""
    try:
        response = requests.get(url, timeout=5)
        print(f"✅ {name}: 正常运行 (状态码: {response.status_code})")
        return True
    except requests.exceptions.ConnectionError:
        print(f"❌ {name}: 连接失败 (服务器未运行)")
        return False
    except requests.exceptions.Timeout:
        print(f"⏰ {name}: 连接超时")
        return False
    except Exception as e:
        print(f"❌ {name}: 错误 - {e}")
        return False

def main():
    print("🔍 检查所有服务器状态")
    print("=" * 50)
    
    servers = [
        ("http://127.0.0.1:5000", "后端API服务器 (27.py)"),
        ("http://127.0.0.1:8000", "完整Web界面 (web_chat.py)"),
        ("http://127.0.0.1:8001", "简化Web界面 (simple_web_chat.py)"),
        ("http://127.0.0.1:8002", "工作版界面 (working_chat.py)"),
    ]
    
    running_count = 0
    
    for url, name in servers:
        if check_server(url, name):
            running_count += 1
        time.sleep(0.5)  # 避免请求过快
    
    print("\n" + "=" * 50)
    print(f"📊 运行状态: {running_count}/{len(servers)} 个服务器正在运行")
    
    if running_count == 0:
        print("\n🚨 没有服务器在运行！")
        print("🔧 请启动服务器:")
        print("   python 27.py          # 后端API")
        print("   python working_chat.py # Web界面")
    elif running_count < len(servers):
        print("\n⚠️ 部分服务器未运行")
        print("💡 建议启动所有服务器以获得完整功能")
    else:
        print("\n🎉 所有服务器都在正常运行！")

if __name__ == "__main__":
    main()
