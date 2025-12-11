#!/usr/bin/env python3
"""
简单API测试脚本 - 测试图片上传和创建秘密功能
"""

import requests
import json
import base64

# API基础URL
BASE_URL = "http://localhost:5000/api"

def test_health():
    """测试健康检查接口"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"健康检查: {response.status_code} - {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"健康检查失败: {e}")
        return False

def test_image_upload():
    """测试图片上传API"""
    try:
        # 创建一个简单的测试图片（1x1像素的PNG）
        test_image_data = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==")
        
        files = {
            'file': ('test.png', test_image_data, 'image/png')
        }
        data = {
            'user_id': 'test_user_123'
        }
        
        response = requests.post(f"{BASE_URL}/upload/image", files=files, data=data)
        print(f"图片上传测试: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"上传成功: {json.dumps(result, indent=2)}")
            return result.get('public_url')
        else:
            print(f"上传失败: {response.text}")
            return None
            
    except Exception as e:
        print(f"图片上传测试失败: {e}")
        return None

def test_create_secret(image_url=None):
    """测试创建秘密API"""
    try:
        data = {
            'user_id': 'test_user_123',
            'content': '这是一个测试秘密',
        }
        
        if image_url:
            data['image_url'] = image_url
        
        response = requests.post(f"{BASE_URL}/secrets", json=data)
        print(f"创建秘密测试: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"创建成功: {json.dumps(result, indent=2)}")
            return True
        else:
            print(f"创建失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"创建秘密测试失败: {e}")
        return False

def main():
    print("开始API测试...")
    print("=" * 50)
    
    # 测试健康检查
    if not test_health():
        print("❌ 后端服务器不可用")
        return
    
    print("✅ 后端服务器正常运行")
    
    # 测试图片上传
    print("\n测试图片上传...")
    image_url = test_image_upload()
    
    # 测试创建秘密
    print("\n测试创建秘密...")
    success = test_create_secret(image_url)
    
    if success:
        print("\n✅ API测试完成")
    else:
        print("\n❌ API测试失败")

if __name__ == "__main__":
    main()