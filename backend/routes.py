from flask import Blueprint, jsonify, request
import datetime
import requests
import os
from supabase import create_client, Client

# 创建API蓝图
api_bp = Blueprint('api', __name__)

# Supabase客户端将在app.py中初始化并传入
supabase = None

def init_supabase(supabase_client):
    """初始化Supabase客户端"""
    global supabase
    supabase = supabase_client

# =====================
# 0. 用户系统 (User System)
# =====================

# 获取用户信息
@api_bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        response = supabase.table('users').select('*').eq('id', user_id).execute()
        if not response.data:
            return jsonify({'error': 'User not found'}), 404
        return jsonify({'data': response.data[0]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 更新用户信息
@api_bp.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        # 添加更新时间
        if 'updated_at' not in data:
            data['updated_at'] = datetime.datetime.now().isoformat()
        
        response = supabase.table('users').update(data).eq('id', user_id).execute()
        return jsonify({'data': response.data[0]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 获取用户统计信息
@api_bp.route('/users/<user_id>/stats', methods=['GET'])
def get_user_stats(user_id):
    try:
        response = supabase.table('user_stats').select('*').eq('user_id', user_id).execute()
        if not response.data:
            return jsonify({'data': {}}), 200
        return jsonify({'data': response.data[0]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# =====================
# 1. 我爱打卡 (My Check-ins)
# =====================


# 获取用户的所有打卡记录
@api_bp.route('/checkins', methods=['GET'])
def get_checkins():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400
    
    try:
        response = supabase.table('checkins').select('*').eq('user_id', user_id).execute()
        return jsonify({'data': response.data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 创建新的打卡记录
@api_bp.route('/checkins', methods=['POST'])
def create_checkin():
    data = request.get_json()
    
    # 验证必要字段
    if not data.get('user_id') or not data.get('content'):
        return jsonify({'error': 'user_id and content are required'}), 400
    
    try:
        # 构建请求数据
        checkin_data = {
            'user_id': data['user_id'],
            'content': data['content'],
            'images': data.get('images', []),
            'location': data.get('location'),
            'created_at': datetime.datetime.now().isoformat()
        }
        
        # 使用存储过程创建打卡记录
        # 注意：这里使用我们之前创建的存储过程，需要根据实际情况调整
        response = supabase.table('checkins').insert(checkin_data).execute()
        return jsonify({'data': response.data[0]}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 更新打卡记录
@api_bp.route('/checkins/<checkin_id>', methods=['PUT'])
def update_checkin(checkin_id):
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        response = supabase.table('checkins').update(data).eq('id', checkin_id).execute()
        return jsonify({'data': response.data[0]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 删除打卡记录
@api_bp.route('/checkins/<checkin_id>', methods=['DELETE'])
def delete_checkin(checkin_id):
    try:
        response = supabase.table('checkins').delete().eq('id', checkin_id).execute()
        return jsonify({'message': 'Checkin deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 获取用户的徽章和成就
@api_bp.route('/badges', methods=['GET'])
def get_badges():
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400
    
    try:
        response = supabase.table('user_badges') \
            .select('id, badge_id, unlocked_at, badges(*)') \
            .eq('user_id', user_id) \
            .order('unlocked_at', desc=True) \
            .execute()
        
        return jsonify({
            'data': response.data,
            'total': len(response.data)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 获取单个徽章详情
@api_bp.route('/badges/<badge_id>', methods=['GET'])
def get_badge(badge_id):
    try:
        response = supabase.table('badges').select('*').eq('id', badge_id).execute()
        if not response.data:
            return jsonify({'error': 'Badge not found'}), 404
        return jsonify({'data': response.data[0]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 解锁新徽章
@api_bp.route('/badges/unlock', methods=['POST'])
def unlock_badge():
    data = request.get_json()
    
    if not data or 'user_id' not in data or 'badge_id' not in data:
        return jsonify({'error': 'user_id and badge_id are required'}), 400
    
    try:
        # 检查是否已经解锁
        existing = supabase.table('user_badges') \
            .select('id') \
            .eq('user_id', data['user_id']) \
            .eq('badge_id', data['badge_id']) \
            .execute()
        
        if existing.data:
            return jsonify({'error': 'Badge already unlocked'}), 400
        
        # 解锁新徽章
        unlock_data = {
            'user_id': data['user_id'],
            'badge_id': data['badge_id'],
            'unlocked_at': datetime.datetime.now().isoformat()
        }
        
        response = supabase.table('user_badges').insert(unlock_data).execute()
        return jsonify({'data': response.data[0]}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# =====================
# 2. 卡友圈 (Check-in Friends)
# =====================

# 获取用户的好友
@api_bp.route('/friends', methods=['GET'])
def get_friends():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400
    
    try:
        response = supabase.table('friends').select('*').eq('user_id', user_id).execute()
        return jsonify({'data': response.data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# =====================
# 3. 团体项目 (Group Projects)
# =====================

# 获取所有团体项目
@api_bp.route('/groups', methods=['GET'])
def get_groups():
    try:
        response = supabase.table('groups').select('*').execute()
        return jsonify({'data': response.data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 获取特定团体项目的详情
@api_bp.route('/groups/<group_id>', methods=['GET'])
def get_group_details(group_id):
    try:
        response = supabase.table('groups').select('*').eq('id', group_id).execute()
        if not response.data:
            return jsonify({'error': 'Group not found'}), 404
        return jsonify({'data': response.data[0]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# =====================
# 4. 广场 (Plaza)
# =====================

# 获取广场动态 (简化版，使用limit代替range)
@api_bp.route('/plaza', methods=['GET'])
def get_plaza_feed():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 20))
    
    try:
        # 简化版：只使用limit，不支持分页
        response = supabase.table('plaza_posts').select('*').limit(limit).execute()
        return jsonify({'data': response.data, 'page': page, 'limit': limit}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# =====================
# 6. 任务系统 (Task System)
# =====================

# 获取用户的任务
@api_bp.route('/tasks', methods=['GET'])
def get_tasks():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400
    
    status = request.args.get('status')
    
    try:
        query = supabase.table('tasks').select('*').eq('user_id', user_id)
        
        if status:
            query = query.eq('status', status)
        
        response = query.execute()
        return jsonify({'data': response.data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 创建新任务
@api_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    
    # 验证必要字段
    if not data.get('user_id') or not data.get('title') or not data.get('due_date'):
        return jsonify({'error': 'user_id, title, and due_date are required'}), 400
    
    try:
        # 构建请求数据
        task_data = {
            'user_id': data['user_id'],
            'title': data['title'],
            'description': data.get('description'),
            'due_date': data['due_date'],
            'status': data.get('status', 'pending'),
            'priority': data.get('priority', 'medium'),
            'category': data.get('category'),
            'reminder': data.get('reminder'),
            'created_at': datetime.datetime.now().isoformat(),
            'updated_at': datetime.datetime.now().isoformat()
        }
        
        response = supabase.table('tasks').insert(task_data).execute()
        return jsonify({'data': response.data[0]}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 更新任务
@api_bp.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        # 添加更新时间
        data['updated_at'] = datetime.datetime.now().isoformat()
        
        response = supabase.table('tasks').update(data).eq('id', task_id).execute()
        return jsonify({'data': response.data[0]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 删除任务
@api_bp.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        response = supabase.table('tasks').delete().eq('id', task_id).execute()
        return jsonify({'message': 'Task deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 获取任务统计信息
@api_bp.route('/tasks/stats', methods=['GET'])
def get_task_stats():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400
    
    try:
        # 这里可以使用我们之前创建的视图或存储过程
        response = supabase.table('user_task_stats').select('*').eq('user_id', user_id).execute()
        return jsonify({'data': response.data[0] if response.data else {}}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# =====================
# 5. 手账系统 (Journal System)
# =====================

# 获取用户的手账条目
@api_bp.route('/journals', methods=['GET'])
def get_journals():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400
    
    try:
        response = supabase.table('journals').select('*').eq('user_id', user_id).execute()
        return jsonify({'data': response.data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 创建新的手账条目
@api_bp.route('/journals', methods=['POST'])
def create_journal():
    data = request.get_json()
    
    # 验证必要字段
    if not data.get('user_id') or not data.get('title') or not data.get('content'):
        return jsonify({'error': 'user_id, title, and content are required'}), 400
    
    try:
        # 构建请求数据
        journal_data = {
            'user_id': data['user_id'],
            'title': data['title'],
            'content': data['content'],
            'mood': data.get('mood'),
            'weather': data.get('weather'),
            'tags': data.get('tags', []),
            'images': data.get('images', []),
            'is_public': data.get('is_public', False),
            'created_at': datetime.datetime.now().isoformat(),
            'updated_at': datetime.datetime.now().isoformat()
        }
        
        response = supabase.table('journals').insert(journal_data).execute()
        return jsonify({'data': response.data[0]}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 更新手账条目
@api_bp.route('/journals/<journal_id>', methods=['PUT'])
def update_journal(journal_id):
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        # 添加更新时间
        data['updated_at'] = datetime.datetime.now().isoformat()
        
        response = supabase.table('journals').update(data).eq('id', journal_id).execute()
        return jsonify({'data': response.data[0]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 删除手账条目
@api_bp.route('/journals/<journal_id>', methods=['DELETE'])
def delete_journal(journal_id):
    try:
        response = supabase.table('journals').delete().eq('id', journal_id).execute()
        return jsonify({'message': 'Journal entry deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# =====================
# 我的密室功能 API
# =====================

# 获取密室消息列表
@api_bp.route('/secrets', methods=['GET'])
def get_secrets():
    user_id = request.args.get('user_id')
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400
    
    try:
        offset = (page - 1) * page_size
        response = supabase.table('secrets') \
            .select('*') \
            .eq('user_id', user_id) \
            .order('created_at', desc=True) \
            .range(offset, offset + page_size - 1) \
            .execute()
        
        # 获取总记录数
        total_response = supabase.table('secrets') \
            .select('id', count='exact') \
            .eq('user_id', user_id) \
            .execute()
        
        return jsonify({
            'data': response.data,
            'total': total_response.count,
            'page': page,
            'page_size': page_size
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 创建密室消息
@api_bp.route('/secrets', methods=['POST'])
def create_secret():
    data = request.get_json()
    
    if not data or 'user_id' not in data or 'content' not in data:
        return jsonify({'error': 'user_id and content are required'}), 400
    
    try:
        # 添加创建和更新时间
        secret_data = {
            'user_id': data['user_id'],
            'content': data['content'],
            'created_at': datetime.datetime.now().isoformat(),
            'updated_at': datetime.datetime.now().isoformat()
        }
        
        # 如果有图片URL，添加到数据中
        if 'image_url' in data:
            secret_data['image_url'] = data['image_url']
        
        response = supabase.table('secrets').insert(secret_data).execute()
        return jsonify({'data': response.data[0]}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 更新密室消息
@api_bp.route('/secrets/<secret_id>', methods=['PUT'])
def update_secret(secret_id):
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        # 更新时间
        data['updated_at'] = datetime.datetime.now().isoformat()
        
        response = supabase.table('secrets').update(data).eq('id', secret_id).execute()
        if not response.data:
            return jsonify({'error': 'Secret not found'}), 404
        return jsonify({'data': response.data[0]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 删除密室消息
@api_bp.route('/secrets/<secret_id>', methods=['DELETE'])
def delete_secret(secret_id):
    try:
        response = supabase.table('secrets').delete().eq('id', secret_id).execute()
        if not response.data:
            return jsonify({'error': 'Secret not found'}), 404
        return jsonify({'message': 'Secret deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# =====================
# 图片上传到 Supabase 存储
# =====================

from flask import request, jsonify
from werkzeug.utils import secure_filename
import os
import uuid

# 上传图片到 Supabase 存储
@api_bp.route('/upload/image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    user_id = request.form.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400
    
    try:
        # 生成唯一的文件名
        filename = secure_filename(file.filename)
        ext = os.path.splitext(filename)[1]
        unique_filename = f"{user_id}/{uuid.uuid4()}{ext}"
        
        # 上传到 Supabase 存储
        # 使用用户创建的 'image' 存储桶（不是 'images'）
        bucket_name = 'image'
        
        # 检查存储桶是否存在
        try:
            buckets = supabase.storage.list_buckets()
            bucket_exists = any(bucket.name == bucket_name for bucket in buckets)
            if not bucket_exists:
                return jsonify({'error': f'存储桶 {bucket_name} 不存在，请在Supabase控制台创建'}), 400
        except Exception as bucket_err:
            return jsonify({'error': f'检查存储桶失败: {str(bucket_err)}'}), 500
        
        # 读取文件内容
        file_content = file.read()
        
        # 上传文件
        response = supabase.storage.from_(bucket_name).upload(
            path=unique_filename,
            file=file_content,
            file_options={'content-type': file.content_type}
        )
        
        # 获取文件的公共URL
        public_url = supabase.storage.from_(bucket_name).get_public_url(unique_filename)
        
        return jsonify({
            'url': public_url,
            'path': unique_filename,
            'bucket': bucket_name
        }), 200
    except Exception as e:
        print(f"图片上传错误: {str(e)}")
        return jsonify({'error': f'图片上传失败: {str(e)}'}), 500