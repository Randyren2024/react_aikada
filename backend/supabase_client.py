import os
import json
import urllib.request
import urllib.parse
import urllib.error
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 获取Supabase配置
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_ROLE') or os.getenv('SUPABASE_KEY')

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

    def _http(self, method, url, headers=None, data=None):
        req = urllib.request.Request(url, data=data, method=method)
        for k, v in (headers or {}).items():
            req.add_header(k, v)
        try:
            with urllib.request.urlopen(req) as resp:
                body = resp.read()
                status = resp.getcode()
                hdrs = dict(resp.headers)
                return status, hdrs, body
        except urllib.error.HTTPError as e:
            try:
                return e.code, dict(e.headers), e.read()
            except Exception:
                return e.code, {}, b''
        except urllib.error.URLError as e:
            raise RuntimeError(str(e))

class Result:
    def __init__(self, data=None, error=None, count=None):
        self.data = data
        self.error = error
        self.count = count

class Table:
    def __init__(self, client, table_name):
        self.client = client
        self.table_name = table_name
    
    def select(self, columns, **kwargs):
        return Query(self, columns, **kwargs)
    
    def insert(self, data):
        return InsertQuery(self, data)
    
    def update(self, data):
        return UpdateQuery(self, data)
    
    def delete(self):
        return DeleteQuery(self)

class Query:
    def __init__(self, table, columns, **kwargs):
        self.table = table
        self.columns = columns
        self.filters = []
        self.order_by = None
        self.order_desc = False
        self.range_start = None
        self.range_end = None
        self.count_pref = kwargs.get('count')
    
    def eq(self, column, value):
        self.filters.append(f'{column}=eq.{value}')
        return self
    
    def limit(self, count):
        self.limit_count = count
        return self
    
    def order(self, column, desc=False):
        self.order_by = column
        self.order_desc = desc
        return self
    
    def range(self, start, end):
        self.range_start = start
        self.range_end = end
        return self
    
    def execute(self):
        base_url = f'{self.table.client.url}/rest/v1/{self.table.table_name}'
        headers = dict(self.table.client.headers)
        params = {'select': self.columns}
        if self.filters:
            for f in self.filters:
                params[f.split('=')[0]] = f.split('=')[1]
        if hasattr(self, 'limit_count'):
            params['limit'] = self.limit_count
        if self.order_by:
            params['order'] = f"{self.order_by}.{('desc' if self.order_desc else 'asc')}"
        if self.range_start is not None and self.range_end is not None:
            headers['Range'] = f'items={self.range_start}-{self.range_end}'
        if self.count_pref:
            headers['Prefer'] = f'count={self.count_pref}'
        # build query string
        qs = '&'.join(f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items())
        url = f"{base_url}?{qs}" if qs else base_url
        status, hdrs, body = self.table.client._http('GET', url, headers=headers)
        if status >= 200 and status < 300:
            try:
                data = json.loads(body.decode('utf-8')) if body else []
            except Exception:
                data = []
            count = None
            if self.count_pref:
                count_hdr = hdrs.get('Content-Range')
                if count_hdr and '/' in count_hdr:
                    try:
                        count = int(count_hdr.split('/')[-1])
                    except Exception:
                        count = None
            return Result(data=data, count=count, error=None)
        else:
            return Result(data=None, error=body.decode('utf-8') if body else f'status {status}')

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
        params = {}
        
        qs = '&'.join(f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items())
        url = f"{base_url}?{qs}" if qs else base_url
        headers = dict(self.table.client.headers)
        headers['Prefer'] = 'return=representation'
        body = json.dumps(self.data).encode('utf-8')
        status, hdrs, resp_body = self.table.client._http('POST', url, headers=headers, data=body)
        if 200 <= status < 300:
            try:
                return Result(data=json.loads(resp_body.decode('utf-8')), error=None)
            except Exception:
                return Result(data=[], error=None)
        else:
            return Result(data=None, error=resp_body.decode('utf-8') if resp_body else f'status {status}')

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
        
        qs = '&'.join(f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items())
        url = f"{base_url}?{qs}" if qs else base_url
        headers = dict(self.table.client.headers)
        body = json.dumps(self.data).encode('utf-8')
        status, hdrs, resp_body = self.table.client._http('PATCH', url, headers=headers, data=body)
        if 200 <= status < 300:
            try:
                return Result(data=json.loads(resp_body.decode('utf-8')), error=None)
            except Exception:
                return Result(data=[], error=None)
        else:
            return Result(data=None, error=resp_body.decode('utf-8') if resp_body else f'status {status}')

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
        
        qs = '&'.join(f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items())
        url = f"{base_url}?{qs}" if qs else base_url
        headers = dict(self.table.client.headers)
        status, hdrs, resp_body = self.table.client._http('DELETE', url, headers=headers)
        if 200 <= status < 300:
            try:
                return Result(data=json.loads(resp_body.decode('utf-8')), error=None)
            except Exception:
                return Result(data=[], error=None)
        else:
            return Result(data=None, error=resp_body.decode('utf-8') if resp_body else f'status {status}')

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
        
        status, hdrs, body = self.client._http('PUT', base_url, headers=headers, data=file_content)
        if 200 <= status < 300:
            return Result(data={'path': file_path}, error=None)
        else:
            return Result(data=None, error=body.decode('utf-8') if body else f'status {status}')
    
    def get_public_url(self, file_path):
        """获取文件的公开URL"""
        return f'{self.client.url}/storage/v1/object/public/{self.bucket_name}/{file_path}'

class StorageClient:
    def __init__(self, client):
        self.client = client
    
    def bucket(self, bucket_name):
        """获取存储桶实例"""
        return StorageBucket(self.client, bucket_name)
    def from_(self, bucket_name):
        bucket = StorageBucket(self.client, bucket_name)
        class BucketCompat:
            def upload(self_inner, path, file, file_options=None):
                ct = None
                if file_options and isinstance(file_options, dict):
                    ct = file_options.get('content-type') or file_options.get('Content-Type')
                return bucket.upload(path, file, ct or 'application/octet-stream')
            def get_public_url(self_inner, path):
                return {'data': {'publicUrl': bucket.get_public_url(path)}}
        return BucketCompat()
    
    def list_buckets(self):
        """列出所有存储桶"""
        base_url = f'{self.client.url}/storage/v1/buckets'
        headers = {
            'apikey': self.client.key,
            'Authorization': f'Bearer {self.client.key}'
        }
        
        status, hdrs, body = self.client._http('GET', base_url, headers=headers)
        if 200 <= status < 300:
            try:
                return json.loads(body.decode('utf-8'))
            except Exception:
                return []
        else:
            return {'error': body.decode('utf-8') if body else f'status {status}'}

# 扩展 SupabaseClient 添加 storage 属性
class EnhancedSupabaseClient(SupabaseClient):
    def __init__(self, url, key):
        super().__init__(url, key)
        self.storage = StorageClient(self)
    def table(self, table_name):
        return self.from_(table_name)

# 初始化增强的 Supabase 客户端
supabase = EnhancedSupabaseClient(SUPABASE_URL, SUPABASE_KEY)
