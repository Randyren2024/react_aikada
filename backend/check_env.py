#!/usr/bin/env python3
"""
环境变量检查脚本 - 用于诊断Supabase配置问题
"""

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

print("环境变量检查:")
print("=" * 40)

# 检查Supabase相关环境变量
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase_anon_key = os.getenv("SUPABASE_ANON_KEY")

print(f"SUPABASE_URL: {supabase_url}")
print(f"SUPABASE_KEY: {supabase_key[:20] + '...' if supabase_key else '未设置'}")
print(f"SUPABASE_ANON_KEY: {supabase_anon_key[:20] + '...' if supabase_anon_key else '未设置'}")

print("\n环境变量文件内容:")
try:
    with open('.env', 'r') as f:
        content = f.read()
        print(content)
except FileNotFoundError:
    print("错误: 未找到.env文件")

print("\n建议:")
if not supabase_url:
    print("❌ 缺少SUPABASE_URL")
if not supabase_key and not supabase_anon_key:
    print("❌ 缺少SUPABASE_KEY或SUPABASE_ANON_KEY")

if supabase_url and (supabase_key or supabase_anon_key):
    print("✅ 环境变量配置正确")
else:
    print("❌ 环境变量配置有误，请检查.env文件")