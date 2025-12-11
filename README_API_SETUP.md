# 爱咔哒应用 API 集成指南

本指南将帮助您设置和运行爱咔哒应用的Flask后端API和React前端，实现与Supabase数据库的集成。

## 项目结构

```
react_aikada/
├── backend/              # Flask后端
│   ├── __init__.py      # 包初始化文件
│   ├── app.py           # Flask应用入口
│   ├── routes.py        # API路由定义
│   ├── requirements.txt # 后端依赖
│   └── .env             # 环境变量配置
├── src/
│   ├── api/             # 前端API相关
│   │   └── supabase.js  # Supabase客户端配置
│   ├── App.jsx          # 主应用组件
│   └── main.jsx         # 应用入口
├── package.json         # 前端依赖和脚本
└── README_API_SETUP.md  # 本指南
```

## 前置条件

1. 已安装 Python 3.8+ 和 Node.js 16+
2. 已创建 Supabase 项目，并获取了项目 URL 和 API 密钥

## 后端设置 (Flask + Supabase)

### 1. 安装后端依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 配置环境变量

确保 `.env` 文件包含以下配置：

```
# Supabase Configuration
SUPABASE_URL=https://pdpgcuogpdghahdjngkx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBkcGdjdW9ncGRnaGFoZGpuZ2t4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjUyNzUzNjgsImV4cCI6MjA4MDg1MTM2OH0.RF8KwbAthRyh31AsLfUgCqW3bZewi8XR1E_OSqkHIdI
```

### 3. 启动Flask服务器

```bash
cd backend
python app.py
```

服务器将在 `http://localhost:5000` 上运行

## 前端设置 (React + Supabase)

### 1. 安装前端依赖

```bash
npm install
```

### 2. 启动React开发服务器

```bash
npm run dev
```

应用将在 `http://localhost:5173` 上运行

## API 端点说明

### 1. 我爱打卡模块

- `GET /api/checkins?user_id=:id` - 获取用户的所有打卡记录
- `POST /api/checkins` - 创建新的打卡记录
- `GET /api/badges?user_id=:id` - 获取用户的徽章和成就

### 2. 卡友圈模块

- `GET /api/friends?user_id=:id` - 获取用户的好友
- `GET /api/users/search?interest=:interest` - 搜索兴趣相投的用户

### 3. 团体项目模块

- `GET /api/groups` - 获取所有团体项目
- `GET /api/groups/:id` - 获取特定团体项目的详情
- `POST /api/groups/:id/join` - 用户加入团体项目

### 4. 广场模块

- `GET /api/plaza?page=:page&limit=:limit` - 获取广场动态
- `POST /api/plaza/posts` - 发布广场动态

## 数据库表结构建议

### 1. users 表
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  age INTEGER,
  grade VARCHAR(20),
  avatar_url TEXT,
  interests TEXT[],
  created_at TIMESTAMP DEFAULT NOW()
);
```

### 2. checkins 表
```sql
CREATE TABLE checkins (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  activity_type VARCHAR(50),
  location TEXT,
  description TEXT,
  photos TEXT[],
  geolocation JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### 3. badges 表
```sql
CREATE TABLE badges (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  name VARCHAR(100) NOT NULL,
  description TEXT,
  icon_url TEXT,
  earned_at TIMESTAMP DEFAULT NOW()
);
```

### 4. groups 表
```sql
CREATE TABLE groups (
  id UUID PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  description TEXT,
  leader_id UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT NOW()
);
```

### 5. group_members 表
```sql
CREATE TABLE group_members (
  id UUID PRIMARY KEY,
  group_id UUID REFERENCES groups(id),
  user_id UUID REFERENCES users(id),
  joined_at TIMESTAMP DEFAULT NOW()
);
```

### 6. plaza_posts 表
```sql
CREATE TABLE plaza_posts (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  content TEXT NOT NULL,
  photos TEXT[],
  created_at TIMESTAMP DEFAULT NOW()
);
```

### 7. friends 表
```sql
CREATE TABLE friends (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  friend_id UUID REFERENCES users(id),
  status VARCHAR(20) DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT NOW()
);
```

## 启动脚本

### 同时启动前后端 (推荐)

在项目根目录运行：

```bash
# 终端1: 启动后端
npm run server

# 终端2: 启动前端
npm run dev
```

### 单独启动

```bash
# 前端
npm run dev

# 后端
cd backend
python app.py
```

## 测试 API

可以使用 Postman 或 curl 测试 API 端点：

```bash
# 测试健康检查
curl http://localhost:5000/api/health

# 测试获取打卡记录（替换为实际用户ID）
curl http://localhost:5000/api/checkins?user_id=1234-5678-9012-3456
```

## 前端使用示例

在 React 组件中使用 Supabase 客户端：

```javascript
import { getCheckins } from '../api/supabase';

const CheckinList = ({ userId }) => {
  const [checkins, setCheckins] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCheckins = async () => {
      try {
        const data = await getCheckins(userId);
        setCheckins(data);
      } catch (error) {
        console.error('Failed to fetch checkins:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchCheckins();
  }, [userId]);

  // 渲染打卡记录
  return (
    <div>
      {/* 组件内容 */}
    </div>
  );
};
```

## 故障排除

### 1. 后端启动失败

- 检查 Python 版本是否符合要求
- 确保所有依赖已正确安装
- 验证 `.env` 文件中的 Supabase 配置是否正确

### 2. 前端无法连接到后端

- 确保 CORS 已在 Flask 中正确配置
- 检查前后端服务器是否在正确的端口上运行
- 验证 API 调用的 URL 是否正确

### 3. Supabase 连接问题

- 确保 Supabase 项目已激活
- 检查 API 密钥是否具有正确的权限
- 验证网络连接是否正常

## 安全注意事项

1. **API 密钥管理**：
   - 不要将敏感的 API 密钥提交到版本控制系统
   - 考虑使用不同的密钥用于开发和生产环境

2. **用户认证**：
   - 在生产环境中实现完整的用户认证系统
   - 考虑使用 Supabase Auth 或其他认证解决方案

3. **数据验证**：
   - 在前端和后端都进行数据验证
   - 避免直接将用户输入传递到数据库

## 后续开发建议

1. 实现用户认证和授权系统
2. 添加数据缓存以提高性能
3. 实现文件上传功能（用于照片等）
4. 添加错误日志和监控系统
5. 实现 API 文档（如使用 Swagger/OpenAPI）

如有任何问题，请查看相关文档或寻求技术支持。
