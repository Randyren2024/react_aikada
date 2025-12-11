#!/usr/bin/env python3
"""
Supabase存储桶创建脚本
用于检查和创建必要的存储桶
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
    print(f"SUPABASE_URL: {SUPABASE_URL}")
    print(f"SUPABASE_KEY: {SUPABASE_KEY}")
    sys.exit(1)

print("✅ 环境变量加载成功")
print(f"Supabase URL: {SUPABASE_URL}")

# 初始化Supabase客户端
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def check_and_create_bucket(bucket_name, public=True):
    """检查并创建存储桶"""
    try:
        # 检查存储桶是否存在
        print(f"\n🔍 检查存储桶 '{bucket_name}'...")
        
        # 获取所有存储桶
        buckets = supabase.storage.list_buckets()
        bucket_exists = any(bucket.name == bucket_name for bucket in buckets)
        
        if bucket_exists:
            print(f"✅ 存储桶 '{bucket_name}' 已存在")
            return True
        else:
            print(f"❌ 存储桶 '{bucket_name}' 不存在，正在创建...")
            
            # 创建存储桶
            result = supabase.storage.create_bucket(
                bucket_name,
                options={
                    "public": public,
                    "file_size_limit": 1024 * 1024 * 5,  # 5MB
                    "allowed_mime_types": ["image/png", "image/jpeg", "image/gif", "image/webp"]
                }
            )
            
            print(f"✅ 存储桶 '{bucket_name}' 创建成功")
            print(f"   公共访问: {public}")
            print(f"   文件大小限制: 5MB")
            print(f"   允许的文件类型: PNG, JPEG, GIF, WebP")
            return True
            
    except Exception as e:
        print(f"❌ 处理存储桶 '{bucket_name}' 时出错: {e}")
        return False

def main():
    print("=== Supabase存储桶配置检查 ===")
    
    # 检查并创建必要的存储桶
    buckets_to_create = [
        ("images", True),  # 图片存储桶，公开访问
    ]
    
    all_success = True
    for bucket_name, is_public in buckets_to_create:
        success = check_and_create_bucket(bucket_name, is_public)
        if not success:
            all_success = False
    
    if all_success:
        print("\n🎉 所有存储桶配置完成！")
        print("\n📋 下一步操作：")
        print("1. 在Supabase控制台验证存储桶设置")
        print("2. 测试图片上传功能")
        print("3. 检查存储桶权限配置")
    else:
        print("\n⚠️  部分存储桶配置失败，请检查Supabase项目权限")
        print("\n🔧 手动创建存储桶步骤：")
        print("1. 登录 https://supabase.com")
        print("2. 进入你的项目")
        print("3. 点击左侧菜单的 'Storage'")
        print("4. 点击 'New Bucket'")
        print("5. 输入名称: images")
        print("6. 选择 'Public' 权限")
        print("7. 点击 'Create Bucket'")

if __name__ == "__main__":
    main()