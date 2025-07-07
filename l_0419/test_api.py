#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
方舟AI图像识别API测试脚本
支持多种测试场景和错误处理
"""

import requests
import json
import time
import sys
from typing import Dict, Any

class ArkAPITester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'ArkAPITester/1.0'
        })
    
    def print_separator(self, title: str):
        """打印分隔线"""
        print(f"\n{'='*50}")
        print(f" {title}")
        print(f"{'='*50}")
    
    def print_success(self, message: str):
        """打印成功信息"""
        print(f"✅ {message}")
    
    def print_error(self, message: str):
        """打印错误信息"""
        print(f"❌ {message}")
    
    def print_info(self, message: str):
        """打印信息"""
        print(f"ℹ️  {message}")
    
    def test_health_check(self) -> bool:
        """测试健康检查接口"""
        self.print_separator("健康检查测试")
        
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200:
                data = response.json()
                self.print_success(f"健康检查成功: {data}")
                return True
            else:
                self.print_error(f"健康检查失败: HTTP {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            self.print_error("无法连接到API服务，请确保服务已启动")
            return False
        except Exception as e:
            self.print_error(f"健康检查异常: {str(e)}")
            return False
    
    def test_chat_normal(self) -> bool:
        """测试普通聊天接口"""
        self.print_separator("普通聊天测试")
        
        test_data = {
            "messages": [
                {
                    "image_url": "https://ark-project.tos-cn-beijing.ivolces.com/images/view.jpeg",
                    "text": "这是哪里？请详细描述一下这个地方。"
                }
            ],
            "stream": False
        }
        
        try:
            start_time = time.time()
            response = self.session.post(f"{self.base_url}/chat", json=test_data)
            end_time = time.time()
            
            if response.status_code == 200:
                data = response.json()
                self.print_success(f"普通聊天成功 (耗时: {end_time - start_time:.2f}秒)")
                self.print_info(f"回复内容: {data['content']}")
                return True
            else:
                self.print_error(f"普通聊天失败: HTTP {response.status_code}")
                self.print_error(f"错误信息: {response.text}")
                return False
        except Exception as e:
            self.print_error(f"普通聊天异常: {str(e)}")
            return False
    
    def test_chat_stream(self) -> bool:
        """测试流式聊天接口"""
        self.print_separator("流式聊天测试")
        
        test_data = {
            "messages": [
                {
                    "image_url": "https://ark-project.tos-cn-beijing.ivolces.com/images/view.jpeg",
                    "text": "请详细分析这张图片中的场景、建筑和可能的用途。"
                }
            ]
        }
        
        try:
            start_time = time.time()
            response = self.session.post(f"{self.base_url}/chat/stream", json=test_data, stream=True)
            end_time = time.time()
            
            if response.status_code == 200:
                self.print_success(f"流式聊天连接成功 (耗时: {end_time - start_time:.2f}秒)")
                self.print_info("开始接收流式数据:")
                
                full_content = ""
                chunk_count = 0
                
                for line in response.iter_lines():
                    if line:
                        line_str = line.decode('utf-8')
                        if line_str.startswith('data: '):
                            data_str = line_str[6:]  # 移除 'data: ' 前缀
                            if data_str == '[DONE]':
                                break
                            try:
                                data_json = json.loads(data_str)
                                content = data_json['content']
                                full_content += content
                                chunk_count += 1
                                print(content, end='', flush=True)
                            except json.JSONDecodeError:
                                continue
                
                print()  # 换行
                self.print_success(f"流式聊天完成，共接收 {chunk_count} 个数据块")
                self.print_info(f"完整回复长度: {len(full_content)} 字符")
                return True
            else:
                self.print_error(f"流式聊天失败: HTTP {response.status_code}")
                self.print_error(f"错误信息: {response.text}")
                return False
        except Exception as e:
            self.print_error(f"流式聊天异常: {str(e)}")
            return False
    
    def test_multiple_images(self) -> bool:
        """测试多图片对话"""
        self.print_separator("多图片对话测试")
        
        test_data = {
            "messages": [
                {
                    "image_url": "https://ark-project.tos-cn-beijing.ivolces.com/images/view.jpeg",
                    "text": "这是第一张图片，请描述一下。"
                },
                {
                    "image_url": "https://ark-project.tos-cn-beijing.ivolces.com/images/view.jpeg",
                    "text": "这是第二张图片，与第一张有什么不同？"
                }
            ],
            "stream": False
        }
        
        try:
            response = self.session.post(f"{self.base_url}/chat", json=test_data)
            
            if response.status_code == 200:
                data = response.json()
                self.print_success("多图片对话成功")
                self.print_info(f"回复内容: {data['content']}")
                return True
            else:
                self.print_error(f"多图片对话失败: HTTP {response.status_code}")
                return False
        except Exception as e:
            self.print_error(f"多图片对话异常: {str(e)}")
            return False
    
    def test_error_handling(self) -> bool:
        """测试错误处理"""
        self.print_separator("错误处理测试")
        
        # 测试无效的图片URL
        test_cases = [
            {
                "name": "无效图片URL",
                "data": {
                    "messages": [
                        {
                            "image_url": "https://invalid-url-that-does-not-exist.com/image.jpg",
                            "text": "这张图片是什么？"
                        }
                    ],
                    "stream": False
                }
            },
            {
                "name": "空消息列表",
                "data": {
                    "messages": [],
                    "stream": False
                }
            },
            {
                "name": "缺少必要字段",
                "data": {
                    "messages": [
                        {
                            "image_url": "https://example.com/image.jpg"
                            # 缺少 text 字段
                        }
                    ],
                    "stream": False
                }
            }
        ]
        
        all_passed = True
        
        for test_case in test_cases:
            try:
                response = self.session.post(f"{self.base_url}/chat", json=test_case["data"])
                
                if response.status_code in [400, 422, 500]:
                    self.print_success(f"{test_case['name']} - 正确返回错误状态码: {response.status_code}")
                else:
                    self.print_error(f"{test_case['name']} - 应该返回错误状态码，但返回了: {response.status_code}")
                    all_passed = False
                    
            except Exception as e:
                self.print_error(f"{test_case['name']} - 异常: {str(e)}")
                all_passed = False
        
        return all_passed
    
    def test_performance(self) -> bool:
        """测试性能"""
        self.print_separator("性能测试")
        
        test_data = {
            "messages": [
                {
                    "image_url": "https://ark-project.tos-cn-beijing.ivolces.com/images/view.jpeg",
                    "text": "请简单描述这张图片。"
                }
            ],
            "stream": False
        }
        
        times = []
        success_count = 0
        
        for i in range(3):  # 测试3次
            try:
                start_time = time.time()
                response = self.session.post(f"{self.base_url}/chat", json=test_data)
                end_time = time.time()
                
                if response.status_code == 200:
                    times.append(end_time - start_time)
                    success_count += 1
                    self.print_info(f"第 {i+1} 次测试: {times[-1]:.2f}秒")
                else:
                    self.print_error(f"第 {i+1} 次测试失败: HTTP {response.status_code}")
                    
            except Exception as e:
                self.print_error(f"第 {i+1} 次测试异常: {str(e)}")
        
        if times:
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
            
            self.print_success(f"性能测试完成: 成功 {success_count}/3 次")
            self.print_info(f"平均响应时间: {avg_time:.2f}秒")
            self.print_info(f"最快响应时间: {min_time:.2f}秒")
            self.print_info(f"最慢响应时间: {max_time:.2f}秒")
            
            return success_count >= 2  # 至少2次成功才算通过
        else:
            self.print_error("性能测试失败: 没有成功的请求")
            return False
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始方舟AI图像识别API测试")
        print(f"📡 目标服务器: {self.base_url}")
        
        test_results = []
        
        # 运行各项测试
        tests = [
            ("健康检查", self.test_health_check),
            ("普通聊天", self.test_chat_normal),
            ("流式聊天", self.test_chat_stream),
            ("多图片对话", self.test_multiple_images),
            ("错误处理", self.test_error_handling),
            ("性能测试", self.test_performance)
        ]
        
        for test_name, test_func in tests:
            try:
                result = test_func()
                test_results.append((test_name, result))
            except Exception as e:
                self.print_error(f"{test_name}测试出现未捕获异常: {str(e)}")
                test_results.append((test_name, False))
        
        # 输出测试总结
        self.print_separator("测试总结")
        
        passed = sum(1 for _, result in test_results if result)
        total = len(test_results)
        
        for test_name, result in test_results:
            status = "✅ 通过" if result else "❌ 失败"
            print(f"{test_name}: {status}")
        
        print(f"\n📊 总体结果: {passed}/{total} 项测试通过")
        
        if passed == total:
            self.print_success("🎉 所有测试通过！API服务运行正常")
            return True
        else:
            self.print_error(f"⚠️  有 {total - passed} 项测试失败，请检查API服务")
            return False

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="方舟AI图像识别API测试工具")
    parser.add_argument("--url", default="http://localhost:8000", 
                       help="API服务器地址 (默认: http://localhost:8000)")
    parser.add_argument("--test", choices=["health", "chat", "stream", "multi", "error", "performance", "all"],
                       default="all", help="指定测试类型 (默认: all)")
    
    args = parser.parse_args()
    
    tester = ArkAPITester(args.url)
    
    if args.test == "all":
        success = tester.run_all_tests()
        sys.exit(0 if success else 1)
    elif args.test == "health":
        success = tester.test_health_check()
    elif args.test == "chat":
        success = tester.test_chat_normal()
    elif args.test == "stream":
        success = tester.test_chat_stream()
    elif args.test == "multi":
        success = tester.test_multiple_images()
    elif args.test == "error":
        success = tester.test_error_handling()
    elif args.test == "performance":
        success = tester.test_performance()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 