#!/usr/bin/env python3
"""
Supabase存储桶测试脚本
用于检查存储桶配置和图片上传功能
"""

import os
import sys
import uuid
import requests
from supabase import create_client, Client

# 加载环境变量配置
try:
    from dotenv import load_dotenv
    # 尝试从当前目录和backend目录加载环境变量
    load_dotenv()
    backend_env = os.path.join(os.path.dirname(__file__), 'backend', '.env')
    if os.path.exists(backend_env):
        load_dotenv(backend_env)
    print("环境变量加载成功")
except ImportError:
    print("警告: 无法加载dotenv，将使用系统环境变量")

# 获取环境变量
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("错误: 缺少Supabase配置信息")
    print(f"SUPABASE_URL: {SUPABASE_URL}")
    print(f"SUPABASE_KEY: {SUPABASE_KEY}")
    sys.exit(1)

# 初始化Supabase客户端
supabase = create_client(supabase_url, supabase_key)

def test_storage_buckets():
    """测试存储桶列表"""
    try:
        print("正在检查Supabase存储桶...")
        buckets = supabase.storage.list_buckets()
        print(f"找到 {len(buckets)} 个存储桶:")
        for bucket in buckets:
            print(f"  - {bucket.name} (公共: {bucket.public})")
        
        # 检查images存储桶是否存在
        bucket_name = 'image'
        bucket_exists = any(bucket.name == bucket_name for bucket in buckets)
        if bucket_exists:
            print(f"✅ 存储桶 '{bucket_name}' 存在")
        else:
            print(f"❌ 存储桶 '{bucket_name}' 不存在")
            print("请在Supabase控制台创建存储桶:")
            print("1. 登录 https://supabase.com")
            print("2. 进入你的项目")
            print("3. 点击左侧菜单的 'Storage'")
            print("4. 点击 'New Bucket'")
            print("5. 输入名称: images")
            print("6. 选择 'Public' 权限")
            print("7. 点击 'Create Bucket'")
        
        return bucket_exists
    except Exception as e:
        print(f"❌ 检查存储桶失败: {e}")
        return False

def test_image_upload():
    """测试图片上传API"""
    try:
        print("\n正在测试图片上传API...")
        
        # 创建一个简单的测试图片
        test_image_path = "test_image.png"
        with open(test_image_path, 'wb') as f:
            # 创建一个1x1像素的PNG图片
            f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x00^\xdd\x86\x1f\x00\x00\x00\x00IEND\xaeB`\x82')
        
        # 准备上传数据
        files = {'file': open(test_image_path, 'rb')}
        data = {'user_id': 'test-user-123'}
        
        # 发送请求
        response = requests.post('http://localhost:5000/api/upload/image', files=files, data=data)
        
        # 清理测试文件
        os.remove(test_image_path)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 图片上传成功:")
            print(f"   URL: {result.get('url')}")
            print(f"   路径: {result.get('path')}")
            print(f"   存储桶: {result.get('bucket')}")
            return True
        else:
            error_msg = response.json().get('error', 'Unknown error')
            print(f"❌ 图片上传失败 (状态码: {response.status_code}): {error_msg}")
            return False
            
    except Exception as e:
        print(f"❌ 测试图片上传失败: {e}")
        return False

def test_secret_creation():
    """测试创建秘密API"""
    try:
        print("\n正在测试创建秘密API...")
        
        # 准备测试数据
        data = {
            'user_id': 'test-user-123',
            'content': '这是一条测试秘密消息',
            'image_url': 'https://example.com/test.jpg'  # 测试图片URL
        }
        
        # 发送请求
        response = requests.post('http://localhost:5000/api/secrets', json=data)
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ 创建秘密成功:")
            print(f"   ID: {result.get('data', {}).get('id')}")
            print(f"   内容: {result.get('data', {}).get('content')}")
            return True
        else:
            error_msg = response.json().get('error', 'Unknown error')
            print(f"❌ 创建秘密失败 (状态码: {response.status_code}): {error_msg}")
            return False
            
    except Exception as e:
        print(f"❌ 测试创建秘密失败: {e}")
        return False

if __name__ == "__main__":
    print("=== Supabase存储和API功能测试 ===")
    
    # 测试存储桶
    bucket_ok = test_storage_buckets()
    
    # 测试API功能
    if bucket_ok:
        upload_ok = test_image_upload()
        secret_ok = test_secret_creation()
        
        if upload_ok and secret_ok:
            print("\n🎉 所有测试通过！图片上传和创建秘密功能正常。")
        else:
            print("\n⚠️ 部分测试失败，请检查错误信息。")
    else:
        print("\n❌ 存储桶检查失败，无法继续测试。")
    
    print("\n=== 测试完成 ===")