import React, { useState, useEffect, useRef } from 'react';
import { 
  MapPin, 
  Search, 
  Scan, 
  Home, 
  Users, 
  Camera, 
  MessageCircle, 
  User, 
  ShoppingBag, 
  Map, 
  Award, 
  Zap, 
  Tent, 
  Building, 
  BookOpen, 
  Compass,
  ChevronRight,
  Bell,
  Upload
} from 'lucide-react';
import SquareView from './SquareView';
import { getSecrets, createSecret, uploadImage } from './api/supabase';

// --- Mock Data ---

const CATEGORIES = [
  { id: 1, name: '博物馆', icon: <Building size={24} />, color: 'bg-blue-100 text-blue-600' },
  { id: 2, name: '自然探索', icon: <Compass size={24} />, color: 'bg-green-100 text-green-600' },
  { id: 3, name: '科技馆', icon: <Zap size={24} />, color: 'bg-purple-100 text-purple-600' },
  { id: 4, name: '冬夏令营', icon: <Tent size={24} />, color: 'bg-orange-100 text-orange-600' },
  { id: 5, name: '研学团', icon: <Users size={24} />, color: 'bg-red-100 text-red-600' },
  { id: 6, name: '读书会', icon: <BookOpen size={24} />, color: 'bg-teal-100 text-teal-600' },
  { id: 7, name: '寻找宝藏', icon: <Map size={24} />, color: 'bg-yellow-100 text-yellow-600' },
  { id: 8, name: '全部', icon: <Award size={24} />, color: 'bg-gray-100 text-gray-600' },
];



const GROUP_TASKS = [
  { id: 1, school: '光明小学', title: '春季植物园研学任务', date: '2023-10-25', status: '进行中', count: 45 },
  { id: 2, school: '实验三小', title: '科技馆小小讲解员', date: '2023-11-02', status: '报名中', count: 120 },
];

const FRIENDS_POSTS = [
  { id: 1, user: '乐乐妈妈', avatar: 'bg-pink-200', content: '今天带乐乐去了天文馆，孩子特别喜欢那个黑洞模型！打卡成功！', likes: 23, time: '10分钟前', image: 'https://images.unsplash.com/photo-1444703686981-a3abbc4d4fe3?auto=format&fit=crop&q=80&w=300&h=200' },
  { id: 2, user: '小明同学', avatar: 'bg-blue-200', content: '集齐了5个自然探索徽章，我的宠物小精灵进化啦！', likes: 45, time: '1小时前', image: null },
];

// --- Components ---

const TabBar = ({ activeTab, setActiveTab }) => {
  const tabs = [
    { id: 'square', label: '广场', icon: <Home size={22} /> },
    { id: 'group', label: '团体', icon: <Users size={22} /> },
    { id: 'checkin', label: '打卡', icon: <Camera size={28} />, isMain: true },
    { id: 'friends', label: '卡友圈', icon: <MessageCircle size={22} /> },
    { id: 'mine', label: '我的', icon: <User size={22} /> },
  ];

  return (
    <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-100 pb-safe pt-2 px-4 shadow-[0_-5px_15px_rgba(0,0,0,0.04)] z-50">
      <div className="flex justify-between items-end pb-2">
        {tabs.map((tab) => {
          const isActive = activeTab === tab.id;
          if (tab.isMain) {
            return (
              <div key={tab.id} className="relative -top-5" onClick={() => setActiveTab(tab.id)}>
                <div className={`w-16 h-16 rounded-full flex items-center justify-center shadow-lg transform transition-transform active:scale-95 border-4 border-white ${isActive ? 'bg-red-500' : 'bg-green-500'}`}>
                  <div className="text-white">
                    {tab.icon}
                  </div>
                </div>
                <div className="text-center text-xs font-medium text-gray-500 mt-1">{tab.label}</div>
              </div>
            );
          }
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex flex-col items-center justify-center space-y-1 w-12 ${isActive ? 'text-green-600' : 'text-gray-400'}`}
            >
              {tab.icon}
              <span className="text-[10px] font-medium">{tab.label}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
};

const Header = () => (
  <div className="bg-gradient-to-r from-orange-400 to-red-500 p-4 pb-12 rounded-b-[2rem] shadow-md relative z-10">
    <div className="flex items-center space-x-3 mb-2">
      <div className="flex items-center text-white font-medium text-sm">
        <span>深圳</span>
        <MapPin size={14} className="ml-1" />
      </div>
      <div className="flex-1 bg-white/20 backdrop-blur-sm rounded-full h-9 flex items-center px-3 border border-white/30">
        <Search size={16} className="text-white/80 mr-2" />
        <input 
          type="text" 
          placeholder="搜索：古罗马 / 恐龙展" 
          className="bg-transparent border-none outline-none text-white placeholder-white/70 text-sm w-full" 
        />
        <button className="bg-white text-orange-500 text-xs font-bold px-3 py-1 rounded-full ml-1">搜索</button>
      </div>
      <Scan size={24} className="text-white" />
    </div>
  </div>
);



// Module: Check-in (The core unique feature)
const CheckInView = () => {
  const [activeSubTab, setActiveSubTab] = useState('checkin');
  const [showSecretModal, setShowSecretModal] = useState(false);
  const [showPhotoModal, setShowPhotoModal] = useState(false);
  const [secretContent, setSecretContent] = useState('');
  const [selectedImage, setSelectedImage] = useState(null);
  const [selectedImageFile, setSelectedImageFile] = useState(null);
  const [secrets, setSecrets] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  // 摄像头相关状态
  const [showCamera, setShowCamera] = useState(false);
  const [cameraStream, setCameraStream] = useState(null);
  const [isFrontCamera, setIsFrontCamera] = useState(true);
  const [cameraError, setCameraError] = useState(null);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  
  // 模拟用户ID（实际应该从登录状态获取）
  const userId = 'user-123';
  
  // 加载密室消息
  useEffect(() => {
    if (activeSubTab === 'secrets') {
      loadSecrets();
    }
  }, [activeSubTab]);
  
  // 组件卸载时停止摄像头
  useEffect(() => {
    return () => {
      if (cameraStream) {
        cameraStream.getTracks().forEach(track => track.stop());
      }
    };
  }, [cameraStream]);
  
  // 获取密室消息
  const loadSecrets = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await getSecrets(userId);
      setSecrets(response.data || []);
    } catch (err) {
      console.error('Error loading secrets:', err);
      setError('加载悄悄话失败，请稍后重试');
    } finally {
      setLoading(false);
    }
  };
  
  // 处理图片选择
  const handleImageChange = (e) => {
    console.log('handleImageChange被调用', e.target.files);
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      console.log('选择的文件:', file.name, file.type, file.size);
      setSelectedImageFile(file);
      setSelectedImage(URL.createObjectURL(file));
    } else {
      console.log('没有选择文件');
    }
  };
  
  // 启动摄像头
  const startCamera = async () => {
    try {
      setCameraError(null);
      // 获取摄像头媒体流
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: isFrontCamera ? 'user' : 'environment'
        },
        audio: false
      });
      
      setCameraStream(stream);
      
      // 将媒体流设置到video元素
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
      
      setShowCamera(true);
    } catch (err) {
      console.error('Error starting camera:', err);
      setCameraError('无法访问摄像头，请检查摄像头权限');
    }
  };
  
  // 停止摄像头
  const stopCamera = () => {
    if (cameraStream) {
      cameraStream.getTracks().forEach(track => track.stop());
      setCameraStream(null);
    }
    setShowCamera(false);
  };
  
  // 拍照
  const takePhoto = () => {
    if (!videoRef.current || !canvasRef.current) return;
    
    const canvas = canvasRef.current;
    const video = videoRef.current;
    
    // 设置画布大小与视频一致
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    // 将视频帧绘制到画布
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    // 将画布内容转换为Blob
    canvas.toBlob((blob) => {
      if (blob) {
        // 创建File对象
        const file = new File([blob], 'photo.jpg', { type: 'image/jpeg' });
        
        // 设置选中的图片
        setSelectedImageFile(file);
        setSelectedImage(canvas.toDataURL('image/jpeg'));
        
        // 停止摄像头
        stopCamera();
      }
    }, 'image/jpeg');
  };
  
  // 切换摄像头
  const toggleCamera = async () => {
    // 先停止当前摄像头
    stopCamera();
    
    // 切换摄像头方向
    setIsFrontCamera(!isFrontCamera);
    
    // 重新启动摄像头
    setTimeout(() => {
      startCamera();
    }, 100);
  };
  
  // 处理创建秘密
  const handleCreateSecret = async () => {
    if (!secretContent.trim()) return;
    
    setLoading(true);
    setError(null);
    
    try {
      let imageUrl = null;
      
      // 上传图片（如果有）
      if (selectedImageFile) {
        const uploadResult = await uploadImage(selectedImageFile, userId);
        imageUrl = uploadResult.url;
      }
      
      // 创建秘密
      await createSecret({
        user_id: userId,
        content: secretContent,
        image_url: imageUrl
      });
      
      // 重新加载秘密列表
      await loadSecrets();
      
      // 关闭模态框并重置
      setShowSecretModal(false);
      setSecretContent('');
      setSelectedImage(null);
      setSelectedImageFile(null);
    } catch (err) {
      console.error('Error creating secret:', err);
      setError('创建悄悄话失败，请稍后重试');
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="pb-24 bg-green-50 min-h-screen">
      <div className="bg-green-500 text-white p-6 pt-12 rounded-b-3xl relative overflow-hidden">
        <div className="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -mr-10 -mt-10"></div>
        <div className="flex justify-between items-center mb-6">
          <div>
            <h1 className="text-2xl font-bold">我爱打卡</h1>
            <p className="text-green-100 text-sm mt-1">今天也要元气满满哦！</p>
          </div>
          <div className="w-12 h-12 bg-white rounded-full p-1 shadow-lg">
            <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix" alt="avatar" className="w-full h-full rounded-full" />
          </div>
        </div>
        
        {/* Pet Interaction Placeholder */}
        <div className="bg-white/10 backdrop-blur-md rounded-2xl p-4 flex items-center space-x-4 border border-white/20">
          <div className="w-16 h-16 bg-yellow-300 rounded-full flex items-center justify-center text-4xl shadow-inner relative">
            🐣
            <div className="absolute bottom-0 right-0 bg-red-500 text-[8px] text-white px-1.5 py-0.5 rounded-full">Lv.3</div>
          </div>
          <div className="flex-1">
            <div className="bg-white text-gray-800 text-xs p-2 rounded-lg rounded-tl-none shadow-sm relative mb-1">
              "主人，听说附近的科学馆有个新展览，我们去看看吧？"
            </div>
            <button className="text-[10px] bg-green-700/50 text-white px-2 py-0.5 rounded-full">喂食</button>
            <button className="text-[10px] bg-green-700/50 text-white px-2 py-0.5 rounded-full ml-2">对话</button>
          </div>
        </div>
      </div>

      {/* Sub Navigation Tabs */}
      <div className="bg-white border-b border-green-100 overflow-x-auto whitespace-nowrap">
        <div className="flex">
          <button 
            className={`px-6 py-3 flex-1 text-center font-medium text-sm transition-colors ${activeSubTab === 'checkin' ? 'text-green-600 border-b-2 border-green-600' : 'text-gray-500 hover:text-green-500'}`}
            onClick={() => setActiveSubTab('checkin')}
          >
            打卡记录
          </button>
          <button 
            className={`px-6 py-3 flex-1 text-center font-medium text-sm transition-colors ${activeSubTab === 'secrets' ? 'text-green-600 border-b-2 border-green-600' : 'text-gray-500 hover:text-green-500'}`}
            onClick={() => setActiveSubTab('secrets')}
          >
            我的密室
          </button>
        </div>
      </div>

      {/* Main Content based on Sub Tab */}
      {activeSubTab === 'checkin' ? (
        <>
          {/* i-Map / Footprint */}
          <div className="px-4 -mt-6">
             <div className="bg-white rounded-2xl p-4 shadow-xl border border-green-100">
               <div className="flex justify-between items-center mb-3">
                  <h3 className="font-bold text-gray-800 flex items-center"><Map size={16} className="mr-1 text-green-500"/> 研学足迹 (i-Map)</h3>
                  <span className="text-xs text-gray-400">查看全景图 {'>'}</span>
               </div>
               <div className="h-40 bg-green-50 rounded-xl border-2 border-dashed border-green-200 flex items-center justify-center relative overflow-hidden">
                  {/* Mock Map Elements */}
                  <div className="absolute top-4 left-4 text-2xl animate-bounce">🏛️</div>
                  <div className="absolute bottom-4 right-10 text-2xl">🌲</div>
                  <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-center text-green-300 text-sm">
                      点击点亮地图<br/>生成专属手账
                  </div>
               </div>
             </div>
          </div>

          {/* Current Tasks */}
          <div className="p-4">
            <h3 className="font-bold text-gray-800 mb-3">待完成任务</h3>
            <div className="space-y-3">
              <div className="bg-white p-4 rounded-xl shadow-sm border-l-4 border-red-400 flex justify-between items-center">
                <div>
                  <h4 className="font-bold text-gray-800">打卡植物园温室</h4>
                  <p className="text-xs text-gray-500 mt-1">需上传3张不同植物照片</p>
                </div>
                <button 
                  className="bg-red-500 text-white px-4 py-2 rounded-full text-sm font-bold shadow-md active:scale-95 transition-transform"
                  onClick={() => setShowPhotoModal(true)}
                >
                  去拍照
                </button>
              </div>
              <div className="bg-white p-4 rounded-xl shadow-sm border-l-4 border-blue-400 flex justify-between items-center">
                <div>
                  <h4 className="font-bold text-gray-800">整理周末日记</h4>
                  <p className="text-xs text-gray-500 mt-1">生成智能手账 (i-Storybook)</p>
                </div>
                <button className="bg-blue-500 text-white px-4 py-2 rounded-full text-sm font-bold shadow-md active:scale-95 transition-transform">
                  去生成
                </button>
              </div>
            </div>
          </div>
        </>
      ) : (
        <div className="p-4">
          {/* 我的密室 */}
          <div className="bg-white rounded-2xl p-4 shadow-xl border border-purple-100 mb-4">
            <div className="flex justify-between items-center mb-4">
              <h3 className="font-bold text-gray-800 flex items-center">
                <Tent size={18} className="mr-1 text-purple-500"/>
                我的密室
              </h3>
              <button 
                className="bg-purple-500 text-white px-4 py-2 rounded-full text-sm font-bold shadow-md active:scale-95 transition-transform"
                onClick={() => setShowSecretModal(true)}
              >
                说悄悄话
              </button>
            </div>
            
            {/* 密室消息列表 */}
            <div className="space-y-3">
              {loading ? (
                <div className="text-center text-gray-400 py-8">
                  <p>加载中...</p>
                </div>
              ) : error ? (
                <div className="text-center text-red-400 py-8">
                  <p>{error}</p>
                  <button onClick={loadSecrets} className="text-purple-500 mt-2">重试</button>
                </div>
              ) : secrets.length > 0 ? (
                secrets.map(secret => (
                  <div key={secret.id} className="bg-purple-50 p-3 rounded-xl border border-purple-100">
                    {secret.image_url && (
                      <div className="w-full h-32 bg-gray-100 rounded-lg overflow-hidden mb-2">
                        <img src={secret.image_url} alt="secret" className="w-full h-full object-cover" />
                      </div>
                    )}
                    <p className="text-sm text-gray-700 mb-2">{secret.content}</p>
                    <div className="text-xs text-purple-500">{new Date(secret.created_at).toLocaleString()}</div>
                  </div>
                ))
              ) : (
                <div className="text-center text-gray-400 py-8">
                  <Tent size={32} className="mx-auto mb-2 opacity-50"/>
                  <p>还没有悄悄话，快来写第一个吧！</p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
      
      {/* 拍照选项模态框 */}
      {showPhotoModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl max-w-md w-full">
            <div className="bg-red-500 text-white p-4 rounded-t-2xl flex justify-between items-center">
              <h3 className="font-bold text-lg">选择拍照方式</h3>
              <button onClick={() => setShowPhotoModal(false)} className="text-white hover:text-red-100">
                ✕
              </button>
            </div>
            <div className="p-6 space-y-4">
              <button 
                className="w-full bg-red-500 text-white px-4 py-3 rounded-xl text-sm font-medium hover:bg-red-600 transition-colors flex items-center justify-center"
                onClick={() => {
                  setShowPhotoModal(false);
                  setShowSecretModal(true);
                  setTimeout(() => {
                    startCamera();
                  }, 100);
                }}
              >
                <Camera size={20} className="mr-2" />
                使用摄像头拍照
              </button>
              <button 
                className="w-full bg-gray-500 text-white px-4 py-3 rounded-xl text-sm font-medium hover:bg-gray-600 transition-colors flex items-center justify-center"
                onClick={() => {
                  console.log('上传本地图片按钮被点击');
                  setShowPhotoModal(false);
                  setShowSecretModal(true);
                  setTimeout(() => {
                    const fileInput = document.getElementById('file-upload');
                    if (fileInput) {
                      console.log('找到文件上传input元素:', fileInput);
                      fileInput.click();
                    } else {
                      console.error('未找到文件上传input元素');
                    }
                  }, 100);
                }}
              >
                <Upload size={20} className="mr-2" />
                上传本地图片
              </button>
            </div>
          </div>
        </div>
      )}

      {/* 文件上传input，始终存在于DOM中 */}
      <input 
        type="file" 
        accept="image/*" 
        className="opacity-0 absolute w-0 h-0 overflow-hidden"
        onChange={handleImageChange}
        id="file-upload"
        style={{position: 'absolute', left: '-9999px'}}
      />

      {/* 说悄悄话模态框 */}
      {showSecretModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl max-w-md w-full max-h-[80vh] overflow-y-auto">
            <div className="bg-purple-500 text-white p-4 rounded-t-2xl flex justify-between items-center">
              <h3 className="font-bold text-lg">说悄悄话</h3>
              <button onClick={() => setShowSecretModal(false)} className="text-white hover:text-purple-100">
                ✕
              </button>
            </div>
            
            <div className="p-4">
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">你的秘密</label>
                <textarea 
                  className="w-full border border-gray-300 rounded-xl p-3 h-32 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none"
                  placeholder="在这里写下你的秘密..."
                  value={secretContent}
                  onChange={(e) => setSecretContent(e.target.value)}
                ></textarea>
              </div>
              
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">添加图片 (可选)</label>
                
                {/* 摄像头预览界面 */}
                {showCamera ? (
                  <div className="bg-gray-100 rounded-xl p-4 relative">
                    {/* 视频预览 */}
                    <video 
                      ref={videoRef} 
                      autoPlay 
                      playsInline 
                      className="w-full h-64 object-cover rounded-lg"
                    />
                    <canvas ref={canvasRef} className="hidden" />
                    
                    {/* 摄像头错误提示 */}
                    {cameraError && (
                      <div className="absolute inset-0 bg-black/50 flex items-center justify-center text-white text-sm p-4">
                        {cameraError}
                      </div>
                    )}
                    
                    {/* 摄像头控制按钮 */}
                    <div className="flex justify-between items-center mt-4">
                      <button 
                        className="px-4 py-2 bg-gray-500 text-white rounded-full text-sm font-medium hover:bg-gray-600"
                        onClick={stopCamera}
                      >
                        取消
                      </button>
                      
                      <button 
                        className="w-16 h-16 rounded-full bg-white shadow-lg flex items-center justify-center hover:bg-gray-100 active:scale-95 transition-transform"
                        onClick={takePhoto}
                      >
                        <div className="w-12 h-12 rounded-full bg-red-500"></div>
                      </button>
                      
                      <button 
                        className="px-4 py-2 bg-gray-500 text-white rounded-full text-sm font-medium hover:bg-gray-600"
                        onClick={toggleCamera}
                      >
                        切换摄像头
                      </button>
                    </div>
                  </div>
                ) : (
                  /* 常规图片上传界面 */
                  <>
                    <div className="relative">
                      <div 
                        className="border-2 border-dashed border-gray-300 rounded-xl p-6 text-center hover:border-purple-500 transition-colors cursor-pointer"
                        onClick={() => document.getElementById('file-upload').click()}
                      >
                        <Camera size={32} className="mx-auto mb-2 text-gray-400"/>
                        <p className="text-sm text-gray-500">点击或拖拽图片到这里</p>
                      </div>
                    </div>
                    
                    {/* 使用摄像头按钮 */}
                    <button 
                      className="mt-2 w-full bg-blue-500 text-white px-4 py-2 rounded-full text-sm font-medium hover:bg-blue-600 transition-colors"
                      onClick={startCamera}
                    >
                      <Camera size={16} className="inline mr-1" />
                      使用摄像头拍照
                    </button>
                    
                    {/* 已选择图片预览 */}
                    {selectedImage && (
                      <div className="mt-3 relative">
                        <img src={selectedImage} alt="preview" className="w-full h-40 object-cover rounded-xl border-2 border-purple-500" />
                        <button 
                          className="absolute top-2 right-2 bg-red-500 text-white w-6 h-6 rounded-full flex items-center justify-center text-xs"
                          onClick={() => {
                            setSelectedImage(null);
                            setSelectedImageFile(null);
                          }}
                        >
                          ✕
                        </button>
                      </div>
                    )}
                  </>
                )}
              </div>
              
              <div className="flex justify-end space-x-3">
                <button 
                  className="px-4 py-2 border border-gray-300 rounded-full text-sm font-medium text-gray-700 hover:bg-gray-50"
                  onClick={() => setShowSecretModal(false)}
                  disabled={loading}
                >
                  取消
                </button>
                <button 
                  className="px-4 py-2 bg-purple-500 text-white rounded-full text-sm font-bold hover:bg-purple-600"
                  onClick={handleCreateSecret}
                  disabled={!secretContent.trim() || loading}
                >
                  {loading ? '保存中...' : '保存秘密'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// Module: Groups (Top-down organization)
const GroupView = () => (
  <div className="pb-24 bg-gray-50 min-h-screen">
    <div className="bg-white p-4 pt-12 shadow-sm sticky top-0 z-10">
      <h1 className="text-xl font-bold text-center">团体项目</h1>
      <p className="text-xs text-center text-gray-400 mt-1">学校 / 社区 / 官方活动</p>
    </div>

    <div className="p-4 space-y-4">
      {/* Teacher/Admin Tools (Mock) */}
      <div className="bg-blue-600 text-white rounded-xl p-4 shadow-lg bg-opacity-90">
        <div className="flex items-center justify-between mb-2">
            <h3 className="font-bold">我是老师/领队</h3>
            <span className="text-xs bg-white/20 px-2 py-1 rounded">管理模式</span>
        </div>
        <div className="grid grid-cols-4 gap-2 text-center mt-3">
            {['点名', '定位', '发布', '成果'].map(action => (
                <div key={action} className="bg-white/10 rounded-lg py-2 flex flex-col items-center">
                    <div className="w-8 h-8 rounded-full bg-white/20 mb-1"></div>
                    <span className="text-xs">{action}</span>
                </div>
            ))}
        </div>
      </div>

      <h3 className="font-bold text-gray-700 mt-4">我的团体活动</h3>
      {GROUP_TASKS.map(task => (
        <div key={task.id} className="bg-white rounded-xl p-4 shadow-sm border border-gray-100 relative overflow-hidden">
          <div className="absolute top-0 right-0 bg-blue-100 text-blue-600 text-xs px-2 py-1 rounded-bl-lg font-medium">
            {task.status}
          </div>
          <div className="flex items-start space-x-3">
             <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center text-xl">🏫</div>
             <div>
                 <h4 className="font-bold text-gray-800">{task.title}</h4>
                 <div className="text-xs text-gray-500 mt-1 flex items-center">
                    <Users size={12} className="mr-1"/> {task.school} · {task.count}人参与
                 </div>
                 <div className="text-xs text-gray-400 mt-1">{task.date}</div>
             </div>
          </div>
          <div className="mt-3 pt-3 border-t border-gray-50 flex justify-end">
             <button className="text-xs border border-blue-500 text-blue-500 px-3 py-1 rounded-full mr-2">查看详情</button>
             <button className="text-xs bg-blue-500 text-white px-3 py-1 rounded-full shadow-sm">立即签到</button>
          </div>
        </div>
      ))}
    </div>
  </div>
);

// Module: Friends (Social)
const FriendsView = () => (
  <div className="pb-24 bg-gray-50 min-h-screen">
    <div className="bg-white p-4 pt-12 shadow-sm sticky top-0 z-10 flex justify-between items-center">
      <h1 className="text-xl font-bold">卡友圈</h1>
      <Bell size={20} className="text-gray-600"/>
    </div>
    
    {/* Interest Tags */}
    <div className="bg-white p-2 flex space-x-2 overflow-x-auto mb-2 no-scrollbar">
       {['全部', '同城', '小小科学家', '昆虫迷', '博物馆达人'].map((tag, i) => (
           <span key={i} className={`whitespace-nowrap px-3 py-1 rounded-full text-xs ${i === 0 ? 'bg-green-100 text-green-700 font-bold' : 'bg-gray-100 text-gray-500'}`}>
               {tag}
           </span>
       ))}
    </div>

    <div className="p-2 space-y-3">
        {FRIENDS_POSTS.map(post => (
            <div key={post.id} className="bg-white rounded-xl p-4 shadow-sm">
                <div className="flex items-center space-x-3 mb-2">
                    <div className={`w-8 h-8 rounded-full ${post.avatar}`}></div>
                    <div>
                        <div className="text-sm font-bold text-gray-800">{post.user}</div>
                        <div className="text-[10px] text-gray-400">{post.time}</div>
                    </div>
                </div>
                <p className="text-sm text-gray-700 mb-2">{post.content}</p>
                {post.image && (
                    <div className="rounded-lg overflow-hidden h-40 bg-gray-100 mb-2">
                        <img src={post.image} alt="post" className="w-full h-full object-cover" />
                    </div>
                )}
                <div className="flex justify-between items-center pt-2 text-gray-400 text-xs">
                    <div className="flex space-x-4">
                        <span className="flex items-center"><Award size={14} className="mr-1"/> 赞 {post.likes}</span>
                        <span className="flex items-center"><MessageCircle size={14} className="mr-1"/> 评论</span>
                    </div>
                    <button className="text-gray-300">•••</button>
                </div>
            </div>
        ))}
    </div>
  </div>
);

// Module: Mine (Profile + Mall)
const MineView = () => (
  <div className="pb-24 bg-gray-50 min-h-screen">
     <div className="bg-green-500 text-white pt-16 pb-20 px-6 rounded-b-[30%]">
        <div className="flex items-center space-x-4">
            <div className="w-16 h-16 bg-white rounded-full border-2 border-white shadow-md overflow-hidden">
                <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix" alt="avatar" />
            </div>
            <div>
                <h2 className="text-xl font-bold">快乐小明</h2>
                <div className="text-xs bg-green-600 inline-block px-2 py-0.5 rounded-full mt-1 border border-green-400">
                    小学三年级 · 探险家 Lv.5
                </div>
            </div>
        </div>
        <div className="flex justify-around mt-6 text-center">
            <div>
                <div className="font-bold text-lg">12</div>
                <div className="text-xs opacity-80">我的勋章</div>
            </div>
            <div>
                <div className="font-bold text-lg">890</div>
                <div className="text-xs opacity-80">卡豆</div>
            </div>
            <div>
                <div className="font-bold text-lg">5</div>
                <div className="text-xs opacity-80">关注</div>
            </div>
        </div>
     </div>

     <div className="px-4 -mt-12">
        {/* Mall Entry */}
        <div className="bg-white rounded-2xl p-4 shadow-lg flex items-center justify-between mb-4 border border-orange-100 relative overflow-hidden">
            <div className="absolute right-0 top-0 bottom-0 w-20 bg-gradient-to-l from-orange-100 to-transparent"></div>
            <div className="flex items-center space-x-3 relative z-10">
                <div className="w-10 h-10 bg-orange-100 rounded-full flex items-center justify-center text-orange-500">
                    <ShoppingBag size={20} />
                </div>
                <div>
                    <h3 className="font-bold text-gray-800">我的商城</h3>
                    <p className="text-xs text-gray-400">用卡豆兑换精美礼品</p>
                </div>
            </div>
            <button className="bg-orange-500 text-white text-xs px-3 py-1.5 rounded-full font-bold relative z-10">去兑换</button>
        </div>

        {/* Menu Grid */}
        <div className="bg-white rounded-2xl p-4 shadow-sm">
            <div className="grid grid-cols-3 gap-y-6">
                {[
                    {name: '我的订单', icon: '📦'},
                    {name: '我的手账', icon: '📔'},
                    {name: '家庭成员', icon: '👨‍👩‍👧'},
                    {name: '地址管理', icon: '📍'},
                    {name: '专属客服', icon: '🎧'},
                    {name: '设置', icon: '⚙️'}
                ].map((item, i) => (
                    <div key={i} className="flex flex-col items-center">
                        <span className="text-2xl mb-1">{item.icon}</span>
                        <span className="text-xs text-gray-600">{item.name}</span>
                    </div>
                ))}
            </div>
        </div>
     </div>
  </div>
);

// Main App Component
const App = () => {
  const [activeTab, setActiveTab] = useState('square');

  const renderContent = () => {
    switch (activeTab) {
      case 'square':
        return <SquareView CATEGORIES={CATEGORIES} Header={Header} />;
      case 'group':
        return <GroupView />;
      case 'checkin':
        return <CheckInView />;
      case 'friends':
        return <FriendsView />;
      case 'mine':
        return <MineView />;
      default:
        return <SquareView CATEGORIES={CATEGORIES} Header={Header} />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {renderContent()}
      <TabBar activeTab={activeTab} setActiveTab={setActiveTab} />
    </div>
  );
};

export default App;