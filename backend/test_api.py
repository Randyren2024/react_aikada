#!/usr/bin/env python3
"""
API测试脚本 - 用于验证打卡达人API是否正常工作
"""

import requests
import json

# API基础URL
BASE_URL = "http://localhost:5000/api"

def test_health_check():
    """测试健康检查端点"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"健康检查测试:")
        print(f"  状态码: {response.status_code}")
        print(f"  响应: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"  错误: {e}")
        return False

def test_get_checkins():
    """测试获取打卡记录"""
    try:
        response = requests.get(f"{BASE_URL}/checkins?user_id=1")
        print(f"\n获取打卡记录测试:")
        print(f"  状态码: {response.status_code}")
        print(f"  响应: {response.text[:200]}...")
        return response.status_code == 200
    except Exception as e:
        print(f"  错误: {e}")
        return False

def test_create_checkin():
    """测试创建打卡记录"""
    try:
        data = {
            "user_id": "1",
            "content": "测试打卡内容",
            "location": "测试地点"
        }
        response = requests.post(f"{BASE_URL}/checkins", json=data)
        print(f"\n创建打卡记录测试:")
        print(f"  状态码: {response.status_code}")
        print(f"  响应: {response.text[:200]}...")
        return response.status_code == 201
    except Exception as e:
        print(f"  错误: {e}")
        return False

def test_get_users():
    """测试获取用户信息"""
    try:
        response = requests.get(f"{BASE_URL}/users/1")
        print(f"\n获取用户信息测试:")
        print(f"  状态码: {response.status_code}")
        print(f"  响应: {response.text[:200]}...")
        return response.status_code == 200
    except Exception as e:
        print(f"  错误: {e}")
        return False

def main():
    """运行所有测试"""
    print("开始测试打卡达人API...")
    print("=" * 50)
    
    # 测试健康检查端点
    health_ok = test_health_check()
    
    if health_ok:
        print("\n✅ 服务器正常运行，继续测试其他端点...")
        
        # 测试各个API端点
        tests = [
            ("获取打卡记录", test_get_checkins),
            ("获取用户信息", test_get_users),
            ("创建打卡记录", test_create_checkin),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            if test_func():
                print(f"✅ {test_name} - 通过")
                passed += 1
            else:
                print(f"❌ {test_name} - 失败")
        
        print(f"\n测试结果: {passed}/{total} 个测试通过")
    else:
        print("\n❌ 服务器未正常运行，请检查服务器状态")
    
    print("\n测试完成！")

if __name__ == "__main__":
    main()