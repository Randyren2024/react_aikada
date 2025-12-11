// API基础URL
const API_BASE_URL = 'http://localhost:5000/api';

// 通用请求函数
const request = async (url, options = {}) => {
  try {
    const response = await fetch(`${API_BASE_URL}${url}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
};

// 导出API函数示例
export const getCheckins = async (userId) => {
  return request(`/checkins?user_id=${userId}`);
};

export const createCheckin = async (checkinData) => {
  return request('/checkins', {
    method: 'POST',
    body: JSON.stringify(checkinData),
  });
};

export const getBadges = async (userId) => {
  return request(`/badges?user_id=${userId}`);
};

// 获取活动列表
export const getActivities = async () => {
  return request('/activities');
};

// 获取热销活动
export const getHotActivities = async () => {
  return request('/hot-activities');
};

// =====================
// 我的密室功能 API
// =====================

// 获取密室消息列表
export const getSecrets = async (userId, page = 1, pageSize = 10) => {
  return request(`/secrets?user_id=${userId}&page=${page}&page_size=${pageSize}`);
};

// 创建密室消息
export const createSecret = async (secretData) => {
  return request('/secrets', {
    method: 'POST',
    body: JSON.stringify(secretData),
  });
};

// 更新密室消息
export const updateSecret = async (secretId, updateData) => {
  return request(`/secrets/${secretId}`, {
    method: 'PUT',
    body: JSON.stringify(updateData),
  });
};

// 删除密室消息
export const deleteSecret = async (secretId) => {
  return request(`/secrets/${secretId}`, {
    method: 'DELETE',
  });
};

// =====================
// 图片上传功能
// =====================

// 上传图片到服务器
export const uploadImage = async (file, userId) => {
  try {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('user_id', userId);

    const response = await fetch(`${API_BASE_URL}/upload/image`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error uploading image:', error);
    throw error;
  }
};