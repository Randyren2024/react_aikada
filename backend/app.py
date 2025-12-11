from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client
import os
from datetime import datetime
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = Flask(__name__)
CORS(app)

# 初始化Supabase客户端
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY") or os.getenv("SUPABASE_ANON_KEY")

if not supabase_url or not supabase_key:
    print("错误: 缺少Supabase配置信息")
    print(f"SUPABASE_URL: {supabase_url}")
    print(f"SUPABASE_KEY: {supabase_key}")
    exit(1)

supabase: Client = create_client(supabase_url, supabase_key)

# 基础路由
@app.route('/')
def hello():
    return jsonify({"message": "打卡达人API服务器运行正常"})

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

# 打卡记录相关路由
@app.route('/api/checkins', methods=['GET'])
def get_checkins():
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({"error": "缺少user_id参数"}), 400
        
        # 获取用户的打卡记录
        result = supabase.table('checkins').select('*').eq('user_id', user_id).execute()
        return jsonify({"data": result.data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/checkins', methods=['POST'])
def create_checkin():
    try:
        data = request.get_json()
        
        # 验证必要字段
        required_fields = ['user_id', 'content']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"缺少必要字段: {field}"}), 400
        
        # 创建打卡记录
        checkin_data = {
            'user_id': data['user_id'],
            'content': data['content'],
            'location': data.get('location', ''),
            'created_at': datetime.now().isoformat()
        }
        
        result = supabase.table('checkins').insert(checkin_data).execute()
        return jsonify({"data": result.data}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 用户相关路由
@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        # 获取用户信息
        result = supabase.table('users').select('*').eq('id', user_id).single().execute()
        if not result.data:
            return jsonify({"error": "用户不存在"}), 404
        return jsonify({"data": result.data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.get_json()
        
        # 更新用户信息
        update_data = {}
        if 'nickname' in data:
            update_data['nickname'] = data['nickname']
        if 'avatar_url' in data:
            update_data['avatar_url'] = data['avatar_url']
        if 'bio' in data:
            update_data['bio'] = data['bio']
        
        if not update_data:
            return jsonify({"error": "没有要更新的字段"}), 400
        
        result = supabase.table('users').update(update_data).eq('id', user_id).execute()
        return jsonify({"data": result.data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("正在启动打卡达人API服务器...")
    print(f"Supabase URL: {supabase_url}")
    print(f"Supabase Key: {supabase_key[:20]}...")  # 只显示密钥前20位用于调试
    print("服务器将在 http://localhost:5000 运行")
    print("健康检查端点: http://localhost:5000/health")
    print("API端点前缀: /api")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)