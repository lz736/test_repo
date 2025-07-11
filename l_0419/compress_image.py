#!/usr/bin/env python3
"""
图片压缩工具
"""

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("❌ 需要安装PIL库: pip install Pillow")

import os

def compress_image(input_path, output_path, max_size_kb=500):
    """压缩图片到指定大小以下"""
    if not PIL_AVAILABLE:
        return False
    
    try:
        # 打开图片
        with Image.open(input_path) as img:
            # 转换为RGB模式（如果是RGBA）
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # 获取原始大小
            original_size = os.path.getsize(input_path)
            print(f"📏 原始文件大小: {original_size / 1024:.1f} KB")
            
            # 如果已经足够小，直接复制
            if original_size <= max_size_kb * 1024:
                img.save(output_path, 'JPEG', quality=85)
                print(f"✅ 图片已经足够小，保存为: {output_path}")
                return True
            
            # 计算压缩比例
            width, height = img.size
            print(f"📐 原始尺寸: {width}x{height}")
            
            # 逐步压缩
            quality = 85
            scale = 1.0
            
            while quality > 20:
                # 调整尺寸
                new_width = int(width * scale)
                new_height = int(height * scale)
                
                if scale < 1.0:
                    resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                else:
                    resized_img = img
                
                # 保存到临时文件测试大小
                temp_path = output_path + '.tmp'
                resized_img.save(temp_path, 'JPEG', quality=quality)
                
                # 检查文件大小
                temp_size = os.path.getsize(temp_path)
                
                if temp_size <= max_size_kb * 1024:
                    # 达到目标大小
                    os.rename(temp_path, output_path)
                    print(f"✅ 压缩成功!")
                    print(f"📏 压缩后大小: {temp_size / 1024:.1f} KB")
                    print(f"📐 压缩后尺寸: {new_width}x{new_height}")
                    print(f"🎯 压缩质量: {quality}")
                    return True
                
                # 删除临时文件
                os.remove(temp_path)
                
                # 调整参数
                if quality > 50:
                    quality -= 10
                elif scale > 0.5:
                    scale -= 0.1
                    quality = 85  # 重置质量
                else:
                    quality -= 5
            
            print("❌ 无法压缩到目标大小")
            return False
            
    except Exception as e:
        print(f"❌ 压缩失败: {e}")
        return False

if __name__ == "__main__":
    input_file = "123.png"
    output_file = "123_compressed.jpg"
    
    if not os.path.exists(input_file):
        print(f"❌ 输入文件不存在: {input_file}")
    elif not PIL_AVAILABLE:
        print("请先安装Pillow库: pip install Pillow")
    else:
        print(f"🔧 开始压缩图片: {input_file}")
        success = compress_image(input_file, output_file, max_size_kb=500)
        
        if success:
            print(f"🎉 压缩完成! 输出文件: {output_file}")
            print("现在可以使用压缩后的图片进行测试:")
            print(f"   img:{output_file} 分析这张图片")
        else:
            print("💡 建议:")
            print("   1. 使用更小的原始图片")
            print("   2. 或直接使用网络图片链接")
            print("   3. 安装Pillow库进行图片处理")
