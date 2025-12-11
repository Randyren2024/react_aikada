from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client
import os
from datetime import datetime
from dotenv import load_dotenv

# 导入API路由
from routes import api_bp

# 加载环境变量
load_dotenv()

app = Flask(__name__)
# 配置CORS以支持所有来源的请求
CORS(app, origins='*', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'], 
     allow_headers=['Content-Type', 'Authorization', 'apikey', 'X-CSRF-Token'])

# 初始化Supabase客户端
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY") or os.getenv("SUPABASE_ANON_KEY")

if not supabase_url or not supabase_key:
    print("错误: 缺少Supabase配置信息")
    print(f"SUPABASE_URL: {supabase_url}")
    print(f"SUPABASE_KEY: {supabase_key}")
    exit(1)

supabase: Client = create_client(supabase_url, supabase_key)

# 初始化API蓝图中的Supabase客户端
from routes import init_supabase
init_supabase(supabase)

# 注册API蓝图
app.register_blueprint(api_bp, url_prefix='/api')

# 基础路由
@app.route('/')
def hello():
    return jsonify({"message": "打卡达人API服务器运行正常"})

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

# 基础路由保持不变，其他API路由已通过蓝图导入

if __name__ == '__main__':
    print("正在启动打卡达人API服务器...")
    print(f"Supabase URL: {supabase_url}")
    print(f"Supabase Key: {supabase_key[:20]}...")  # 只显示密钥前20位用于调试
    print("服务器将在 http://localhost:5000 运行")
    print("健康检查端点: http://localhost:5000/health")
    print("API端点前缀: /api")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)