import os
import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 获取Supabase配置
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# 验证配置是否存在
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase configuration is missing. Please check your .env file.")

# 使用requests实现简单的Supabase客户端功能
class SupabaseClient:
    def __init__(self, url, key):
        self.url = url.rstrip('/')
        self.key = key
        self.headers = {
            'apikey': self.key,
            'Authorization': f'Bearer {self.key}',
            'Content-Type': 'application/json'
        }
    
    def from_(self, table_name):
        return Table(self, table_name)

class Table:
    def __init__(self, client, table_name):
        self.client = client
        self.table_name = table_name
    
    def select(self, columns):
        return Query(self, columns)
    
    def insert(self, data):
        return InsertQuery(self, data)
    
    def update(self, data):
        return UpdateQuery(self, data)
    
    def delete(self):
        return DeleteQuery(self)

class Query:
    def __init__(self, table, columns):
        self.table = table
        self.columns = columns
        self.filters = []
    
    def eq(self, column, value):
        self.filters.append(f'{column}=eq.{value}')
        return self
    
    def limit(self, count):
        self.limit_count = count
        return self
    
    def execute(self):
        base_url = f'{self.table.client.url}/rest/v1/{self.table.table_name}'
        params = {'select': self.columns}
        
        if self.filters:
            for filter in self.filters:
                params[filter.split('=')[0]] = filter.split('=')[1]
        
        if hasattr(self, 'limit_count'):
            params['limit'] = self.limit_count
        
        try:
            response = requests.get(base_url, headers=self.table.client.headers, params=params)
            response.raise_for_status()
            return {'data': response.json(), 'error': None}
        except requests.exceptions.RequestException as e:
            return {'data': None, 'error': str(e)}

class InsertQuery:
    def __init__(self, table, data):
        self.table = table
        self.data = data
        self.returning = '*'  # 默认返回所有列
    
    def returning(self, columns):
        self.returning = columns
        return self
    
    def execute(self):
        base_url = f'{self.table.client.url}/rest/v1/{self.table.table_name}'
        params = {'returning': self.returning}
        
        try:
            response = requests.post(
                base_url,
                headers=self.table.client.headers,
                params=params,
                json=self.data
            )
            response.raise_for_status()
            return {'data': response.json(), 'error': None}
        except requests.exceptions.RequestException as e:
            return {'data': None, 'error': str(e)}

class UpdateQuery:
    def __init__(self, table, data):
        self.table = table
        self.data = data
        self.filters = []
        self.returning = '*'  # 默认返回所有列
    
    def eq(self, column, value):
        self.filters.append(f'{column}=eq.{value}')
        return self
    
    def returning(self, columns):
        self.returning = columns
        return self
    
    def execute(self):
        base_url = f'{self.table.client.url}/rest/v1/{self.table.table_name}'
        params = {'returning': self.returning}
        
        if self.filters:
            for filter in self.filters:
                params[filter.split('=')[0]] = filter.split('=')[1]
        
        try:
            response = requests.patch(
                base_url,
                headers=self.table.client.headers,
                params=params,
                json=self.data
            )
            response.raise_for_status()
            return {'data': response.json(), 'error': None}
        except requests.exceptions.RequestException as e:
            return {'data': None, 'error': str(e)}

class DeleteQuery:
    def __init__(self, table):
        self.table = table
        self.filters = []
        self.returning = '*'  # 默认返回所有列
    
    def eq(self, column, value):
        self.filters.append(f'{column}=eq.{value}')
        return self
    
    def returning(self, columns):
        self.returning = columns
        return self
    
    def execute(self):
        base_url = f'{self.table.client.url}/rest/v1/{self.table.table_name}'
        params = {'returning': self.returning}
        
        if self.filters:
            for filter in self.filters:
                params[filter.split('=')[0]] = filter.split('=')[1]
        
        try:
            response = requests.delete(
                base_url,
                headers=self.table.client.headers,
                params=params
            )
            response.raise_for_status()
            return {'data': response.json(), 'error': None}
        except requests.exceptions.RequestException as e:
            return {'data': None, 'error': str(e)}

class StorageBucket:
    def __init__(self, client, bucket_name):
        self.client = client
        self.bucket_name = bucket_name
    
    def upload(self, file_path, file_content, content_type='application/octet-stream'):
        """上传文件到存储桶"""
        base_url = f'{self.client.url}/storage/v1/object/{self.bucket_name}/{file_path}'
        headers = {
            'apikey': self.client.key,
            'Authorization': f'Bearer {self.client.key}',
            'Content-Type': content_type
        }
        
        try:
            response = requests.put(
                base_url,
                headers=headers,
                data=file_content
            )
            response.raise_for_status()
            return {'data': {'path': file_path}, 'error': None}
        except requests.exceptions.RequestException as e:
            return {'data': None, 'error': str(e)}
    
    def get_public_url(self, file_path):
        """获取文件的公开URL"""
        return f'{self.client.url}/storage/v1/object/public/{self.bucket_name}/{file_path}'

class StorageClient:
    def __init__(self, client):
        self.client = client
    
    def bucket(self, bucket_name):
        """获取存储桶实例"""
        return StorageBucket(self.client, bucket_name)
    
    def list_buckets(self):
        """列出所有存储桶"""
        base_url = f'{self.client.url}/storage/v1/buckets'
        headers = {
            'apikey': self.client.key,
            'Authorization': f'Bearer {self.client.key}'
        }
        
        try:
            response = requests.get(base_url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}

# 扩展 SupabaseClient 添加 storage 属性
class EnhancedSupabaseClient(SupabaseClient):
    def __init__(self, url, key):
        super().__init__(url, key)
        self.storage = StorageClient(self)

# 初始化增强的 Supabase 客户端
supabase = EnhancedSupabaseClient(SUPABASE_URL, SUPABASE_KEY)