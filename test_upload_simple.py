#!/usr/bin/env python3
"""
简单的图片上传测试脚本
"""

import requests
import base64
import json

BASE_URL = "http://localhost:5000/api"

def test_image_upload():
    """测试图片上传API"""
    try:
        print("🔍 测试图片上传API...")
        
        # 创建一个简单的测试图片（1x1像素的PNG）
        test_image_data = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==")
        
        files = {
            'file': ('test.png', test_image_data, 'image/png')
        }
        data = {
            'user_id': 'test_user_123'
        }
        
        response = requests.post(f"{BASE_URL}/upload/image", files=files, data=data)
        print(f"📊 上传响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 图片上传成功！")
            print(f"   返回URL: {result.get('url')}")
            print(f"   文件路径: {result.get('path')}")
            print(f"   存储桶: {result.get('bucket')}")
            return True
        else:
            print(f"❌ 图片上传失败")
            print(f"   错误信息: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        return False

def test_secret_creation():
    """测试创建秘密API"""
    try:
        print("\n🔍 测试创建秘密API...")
        
        secret_data = {
            'user_id': 'test_user_123',
            'content': '这是一个测试秘密消息'
        }
        
        response = requests.post(f"{BASE_URL}/secrets", json=secret_data)
        print(f"📊 创建秘密响应状态码: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print("✅ 秘密创建成功！")
            print(f"   秘密ID: {result.get('data', {}).get('id')}")
            print(f"   内容: {result.get('data', {}).get('content')}")
            return True
        else:
            print(f"❌ 创建秘密失败")
            print(f"   错误信息: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        return False

def main():
    print("=== 图片上传和秘密创建功能测试 ===")
    
    # 测试图片上传
    upload_ok = test_image_upload()
    
    # 测试创建秘密
    secret_ok = test_secret_creation()
    
    if upload_ok and secret_ok:
        print("\n🎉 所有测试通过！图片上传和创建秘密功能正常。")
        print("\n📋 下一步：")
        print("1. 打开前端页面测试完整功能")
        print("2. 使用摄像头拍照或上传本地图片")
        print("3. 点击'保存秘密'按钮验证功能")
    else:
        print("\n⚠️ 部分测试失败，请检查错误信息。")

if __name__ == "__main__":
    main()