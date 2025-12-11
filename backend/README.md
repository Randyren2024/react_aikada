# 打卡达人 API 文档

## 项目概述

打卡达人是一个专注于日常打卡、手账记录和任务管理的应用程序。本API提供了完整的后端支持，包括用户系统、打卡功能、手账系统和任务管理等核心功能。

## 技术栈

- Flask 框架
- Supabase 数据库
- RESTful API 设计

## 环境配置

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置文件

在项目根目录创建 `.env` 文件，并配置以下内容：

```
# Supabase Configuration
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_api_key
```

### 启动服务器

```bash
python app.py
```

服务器将在 `http://localhost:5000` 启动。

## API 端点

### 1. 用户系统 (User System)

#### 获取用户信息

```
GET /api/users/{user_id}
```

**响应示例：**

```json
{
  "data": {
    "id": "user123",
    "name": "张三",
    "avatar": "https://example.com/avatar.jpg",
    "bio": "热爱生活，喜欢打卡",
    "created_at": "2023-01-01T00:00:00.000Z",
    "updated_at": "2023-01-02T00:00:00.000Z"
  }
}
```

#### 更新用户信息

```
PUT /api/users/{user_id}
```

**请求体：**

```json
{
  "name": "李四",
  "bio": "更新后的个人简介"
}
```

**响应示例：**

```json
{
  "data": {
    "id": "user123",
    "name": "李四",
    "avatar": "https://example.com/avatar.jpg",
    "bio": "更新后的个人简介",
    "created_at": "2023-01-01T00:00:00.000Z",
    "updated_at": "2023-01-03T00:00:00.000Z"
  }
}
```

#### 获取用户统计信息

```
GET /api/users/{user_id}/stats
```

**响应示例：**

```json
{
  "data": {
    "user_id": "user123",
    "total_checkins": 150,
    "checkin_streak": 30,
    "total_journals": 50,
    "total_tasks_completed": 200
  }
}
```

### 2. 打卡记录 (Check-ins)

#### 获取用户打卡记录

```
GET /api/checkins?user_id=user123
```

**响应示例：**

```json
{
  "data": [
    {
      "id": "checkin123",
      "user_id": "user123",
      "content": "今天完成了运动打卡",
      "images": ["https://example.com/image1.jpg"],
      "location": "健身房",
      "created_at": "2023-01-01T08:00:00.000Z"
    }
  ]
}
```

#### 创建打卡记录

```
POST /api/checkins
```

**请求体：**

```json
{
  "user_id": "user123",
  "content": "今天完成了阅读打卡",
  "images": ["https://example.com/book.jpg"],
  "location": "书房"
}
```

**响应示例：**

```json
{
  "data": {
    "id": "checkin456",
    "user_id": "user123",
    "content": "今天完成了阅读打卡",
    "images": ["https://example.com/book.jpg"],
    "location": "书房",
    "created_at": "2023-01-02T10:00:00.000Z"
  }
}
```

#### 更新打卡记录

```
PUT /api/checkins/{checkin_id}
```

**请求体：**

```json
{
  "content": "更新后的打卡内容"
}
```

**响应示例：**

```json
{
  "data": {
    "id": "checkin123",
    "user_id": "user123",
    "content": "更新后的打卡内容",
    "images": ["https://example.com/image1.jpg"],
    "location": "健身房",
    "created_at": "2023-01-01T08:00:00.000Z"
  }
}
```

#### 删除打卡记录

```
DELETE /api/checkins/{checkin_id}
```

**响应示例：**

```json
{
  "message": "Checkin deleted successfully"
}
```

### 3. 手账系统 (Journal System)

#### 获取用户手账条目

```
GET /api/journals?user_id=user123
```

**响应示例：**

```json
{
  "data": [
    {
      "id": "journal123",
      "user_id": "user123",
      "title": "今日心情",
      "content": "今天天气很好，心情也很棒！",
      "mood": "happy",
      "weather": "sunny",
      "tags": ["心情", "生活"],
      "images": [],
      "is_public": false,
      "created_at": "2023-01-01T12:00:00.000Z",
      "updated_at": "2023-01-01T12:00:00.000Z"
    }
  ]
}
```

#### 创建手账条目

```
POST /api/journals
```

**请求体：**

```json
{
  "user_id": "user123",
  "title": "旅行日记",
  "content": "今天去了美丽的海滩，度过了愉快的一天。",
  "mood": "excited",
  "weather": "sunny",
  "tags": ["旅行", "海滩"],
  "images": ["https://example.com/beach.jpg"],
  "is_public": true
}
```

**响应示例：**

```json
{
  "data": {
    "id": "journal456",
    "user_id": "user123",
    "title": "旅行日记",
    "content": "今天去了美丽的海滩，度过了愉快的一天。",
    "mood": "excited",
    "weather": "sunny",
    "tags": ["旅行", "海滩"],
    "images": ["https://example.com/beach.jpg"],
    "is_public": true,
    "created_at": "2023-01-02T14:00:00.000Z",
    "updated_at": "2023-01-02T14:00:00.000Z"
  }
}
```

### 4. 任务系统 (Task System)

#### 获取用户任务

```
GET /api/tasks?user_id=user123&status=pending
```

**响应示例：**

```json
{
  "data": [
    {
      "id": "task123",
      "user_id": "user123",
      "title": "完成项目报告",
      "description": "撰写并提交季度项目报告",
      "due_date": "2023-01-15T23:59:59.000Z",
      "status": "pending",
      "priority": "high",
      "category": "工作",
      "reminder": "2023-01-14T10:00:00.000Z",
      "created_at": "2023-01-01T09:00:00.000Z",
      "updated_at": "2023-01-01T09:00:00.000Z"
    }
  ]
}
```

#### 创建任务

```
POST /api/tasks
```

**请求体：**

```json
{
  "user_id": "user123",
  "title": "学习Flask",
  "description": "完成Flask框架的学习",
  "due_date": "2023-02-01T23:59:59.000Z",
  "priority": "medium",
  "category": "学习"
}
```

**响应示例：**

```json
{
  "data": {
    "id": "task456",
    "user_id": "user123",
    "title": "学习Flask",
    "description": "完成Flask框架的学习",
    "due_date": "2023-02-01T23:59:59.000Z",
    "status": "pending",
    "priority": "medium",
    "category": "学习",
    "reminder": null,
    "created_at": "2023-01-02T16:00:00.000Z",
    "updated_at": "2023-01-02T16:00:00.000Z"
  }
}
```

## 数据模型

### 用户表 (users)

| 字段名 | 类型 | 描述 |
|--------|------|------|
| id | UUID | 用户ID |
| name | String | 用户名 |
| avatar | String | 头像URL |
| bio | Text | 个人简介 |
| created_at | Timestamp | 创建时间 |
| updated_at | Timestamp | 更新时间 |

### 打卡记录表 (checkins)

| 字段名 | 类型 | 描述 |
|--------|------|------|
| id | UUID | 打卡ID |
| user_id | UUID | 用户ID |
| content | Text | 打卡内容 |
| images | Array | 图片URL数组 |
| location | String | 打卡地点 |
| created_at | Timestamp | 创建时间 |

### 手账表 (journals)

| 字段名 | 类型 | 描述 |
|--------|------|------|
| id | UUID | 手账ID |
| user_id | UUID | 用户ID |
| title | String | 标题 |
| content | Text | 内容 |
| mood | String | 心情 |
| weather | String | 天气 |
| tags | Array | 标签数组 |
| images | Array | 图片URL数组 |
| is_public | Boolean | 是否公开 |
| created_at | Timestamp | 创建时间 |
| updated_at | Timestamp | 更新时间 |

### 任务表 (tasks)

| 字段名 | 类型 | 描述 |
|--------|------|------|
| id | UUID | 任务ID |
| user_id | UUID | 用户ID |
| title | String | 标题 |
| description | Text | 描述 |
| due_date | Timestamp | 截止日期 |
| status | String | 状态 |
| priority | String | 优先级 |
| category | String | 分类 |
| reminder | Timestamp | 提醒时间 |
| created_at | Timestamp | 创建时间 |
| updated_at | Timestamp | 更新时间 |

## 错误处理

所有API端点都遵循统一的错误响应格式：

```json
{
  "error": "错误信息描述"
}
```

常见的HTTP状态码：

- 200: 成功
- 201: 创建成功
- 400: 请求参数错误
- 404: 资源未找到
- 500: 服务器内部错误

## 开发指南

### 添加新的API端点

1. 在 `routes.py` 文件中定义新的路由函数
2. 使用 `@api_bp.route()` 装饰器指定URL路径和HTTP方法
3. 实现请求处理逻辑
4. 返回JSON格式的响应

### 数据库操作

使用Supabase客户端进行数据库操作：

```python
# 查询数据
supabase.from_('table_name').select('*').eq('column', value).execute()

# 插入数据
supabase.from_('table_name').insert(data).execute()

# 更新数据
supabase.from_('table_name').update(data).eq('column', value).execute()

# 删除数据
supabase.from_('table_name').delete().eq('column', value).execute()
```

## 部署建议

- 使用 Gunicorn 或 uWSGI 作为生产服务器
- 配置 Nginx 作为反向代理
- 启用 HTTPS
- 设置适当的日志记录
- 配置监控和告警

## 版本历史

- v1.0.0: 初始版本，包含用户系统、打卡功能、手账系统和任务管理

## 贡献指南

欢迎提交Issue和Pull Request！

## 许可证

MIT License