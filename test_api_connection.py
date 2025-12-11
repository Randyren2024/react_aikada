import requests
import json

# 测试健康检查端点
print("测试健康检查端点...")
try:
    response = requests.get("http://localhost:5000/health")
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.text}")
    print("✅ 健康检查端点正常")
except Exception as e:
    print(f"❌ 健康检查端点错误: {e}")

# 测试获取打卡记录端点
print("\n测试获取打卡记录端点...")
try:
    response = requests.get("http://localhost:5000/api/checkins?user_id=1")
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.text}")
    print("✅ 获取打卡记录端点正常")
except Exception as e:
    print(f"❌ 获取打卡记录端点错误: {e}")

# 测试创建打卡记录端点
print("\n测试创建打卡记录端点...")
try:
    checkin_data = {
        "user_id": "1",
        "content": "测试打卡内容",
        "location": "测试地点"
    }
    response = requests.post("http://localhost:5000/api/checkins", json=checkin_data)
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.text}")
    print("✅ 创建打卡记录端点正常")
except Exception as e:
    print(f"❌ 创建打卡记录端点错误: {e}")