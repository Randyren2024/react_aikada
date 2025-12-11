#!/usr/bin/env python3
"""
Supabase存储桶验证脚本
用于检查存储桶是否已正确创建
"""

import os
import sys
from dotenv import load_dotenv
from supabase import create_client

# 加载环境变量
load_dotenv()
backend_env = os.path.join(os.path.dirname(__file__), 'backend', '.env')
if os.path.exists(backend_env):
    load_dotenv(backend_env)

# 获取环境变量
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ 错误: 缺少Supabase配置信息")
    sys.exit(1)

print("✅ 环境变量加载成功")

# 初始化Supabase客户端
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def check_bucket_status():
    """检查存储桶状态"""
    try:
        print("\n🔍 检查Supabase存储桶状态...")
        
        # 获取所有存储桶
        buckets = supabase.storage.list_buckets()
        
        print(f"📊 找到 {len(buckets)} 个存储桶:")
        for bucket in buckets:
            print(f"  - {bucket.name} (公共: {bucket.public})")
        
        # 检查image存储桶是否存在（用户创建的是image，不是images）
        bucket_name = 'image'
        bucket_exists = any(bucket.name == bucket_name for bucket in buckets)
        
        if bucket_exists:
            print(f"\n✅ 存储桶 '{bucket_name}' 存在")
            
            # 测试上传权限
            try:
                # 创建一个简单的测试文件
                test_content = b"test"
                test_path = f"test-{os.urandom(4).hex()}.txt"
                
                result = supabase.storage.from_(bucket_name).upload(
                    test_path, 
                    test_content,
                    {"content-type": "text/plain"}
                )
                
                print(f"✅ 上传测试成功")
                
                # 清理测试文件
                supabase.storage.from_(bucket_name).remove([test_path])
                print(f"✅ 清理测试文件成功")
                
                return True
                
            except Exception as upload_error:
                print(f"❌ 上传测试失败: {upload_error}")
                return False
                
        else:
            print(f"\n❌ 存储桶 '{bucket_name}' 不存在")
            print("\n📋 请按照以下步骤手动创建存储桶:")
            print("1. 登录 https://supabase.com")
            print("2. 进入你的项目")
            print("3. 点击左侧菜单的 'Storage'")
            print("4. 点击 'New Bucket'")
            print("5. 输入名称: images")
            print("6. 选择 'Public' 权限")
            print("7. 点击 'Create Bucket'")
            return False
            
    except Exception as e:
        print(f"❌ 检查存储桶状态失败: {e}")
        return False

def test_image_upload_api():
    """测试图片上传API"""
    try:
        print("\n🔍 测试图片上传API...")
        
        # 创建一个简单的测试图片（1x1像素的PNG）
        import base64
        test_image_data = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==")
        
        import requests
        files = {
            'file': ('test.png', test_image_data, 'image/png')
        }
        data = {
            'user_id': 'test_user_123'
        }
        
        response = requests.post('http://localhost:5000/api/upload/image', files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 图片上传API测试成功")
            print(f"   返回URL: {result.get('url')}")
            return True
        else:
            print(f"❌ 图片上传API测试失败 (状态码: {response.status_code})")
            print(f"   错误信息: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 图片上传API测试异常: {e}")
        return False

def main():
    print("=== Supabase存储桶验证 ===")
    
    # 检查存储桶状态
    bucket_ok = check_bucket_status()
    
    if bucket_ok:
        # 测试图片上传API
        api_ok = test_image_upload_api()
        
        if api_ok:
            print("\n🎉 所有测试通过！图片上传功能已就绪")
        else:
            print("\n⚠️  存储桶存在但API测试失败，请检查后端服务")
    else:
        print("\n❌ 存储桶配置未完成，请先创建存储桶")

if __name__ == "__main__":
    main()