import React, { useState } from 'react';
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
  Bell
} from 'lucide-react';

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

const HOT_ACTIVITIES = [
  { 
    id: 1, 
    title: '上海天文馆小小宇航员', 
    subtitle: '沉浸式宇宙探索', 
    price: '178', 
    sales: '4563', 
    image: 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&q=80&w=300&h=200',
    tag: '热销榜'
  },
  { 
    id: 2, 
    title: '南京博物院历史解密', 
    subtitle: '守护国宝 · 探索传奇', 
    price: '138', 
    sales: '8065', 
    image: 'https://images.unsplash.com/photo-1599939571322-792a326991f2?auto=format&fit=crop&q=80&w=300&h=200',
    tag: '金牌讲师'
  },
  { 
    id: 3, 
    title: '野生动物园奇妙夜', 
    subtitle: '与动物做邻居', 
    price: '276', 
    sales: '3.8万', 
    image: 'https://images.unsplash.com/photo-1534567153574-2b12153a87f0?auto=format&fit=crop&q=80&w=300&h=200',
    tag: '限时特价'
  },
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

// Module: Square (Similar to the reference image Home)
const SquareView = () => (
  <div className="pb-24">
    <Header />
    
    {/* Grid Categories */}
    <div className="mx-4 -mt-8 bg-white rounded-2xl p-4 shadow-lg grid grid-cols-4 gap-y-4 relative z-20">
      {CATEGORIES.map((cat) => (
        <div key={cat.id} className="flex flex-col items-center space-y-2">
          <div className={`${cat.color} w-12 h-12 rounded-2xl flex items-center justify-center mb-1`}>
            {cat.icon}
          </div>
          <span className="text-xs text-gray-600 font-medium">{cat.name}</span>
        </div>
      ))}
    </div>

    {/* Hot Sales / Recommendations */}
    <div className="mt-6 px-4">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-lg font-bold text-gray-800 flex items-center">
          <span className="text-red-500 mr-2">🔥</span> 热销榜
        </h2>
        <span className="text-xs text-gray-400 flex items-center">4.8万人正在选购 <ChevronRight size={12}/></span>
      </div>
      
      <div className="grid grid-cols-2 gap-3">
        {HOT_ACTIVITIES.map((item) => (
          <div key={item.id} className="bg-white rounded-xl overflow-hidden shadow-sm border border-gray-100 flex flex-col h-full">
            <div className="relative h-28 bg-gray-200">
              <img src={item.image} alt={item.title} className="w-full h-full object-cover" />
              <div className="absolute top-2 left-2 bg-yellow-400 text-[10px] font-bold px-2 py-0.5 rounded text-yellow-900">
                {item.tag}
              </div>
            </div>
            <div className="p-3 flex flex-col flex-1 justify-between">
              <div>
                <h3 className="font-bold text-sm text-gray-800 line-clamp-1">{item.title}</h3>
                <p className="text-xs text-blue-500 mt-1 bg-blue-50 inline-block px-1 rounded">{item.subtitle}</p>
              </div>
              <div className="mt-2 flex items-baseline justify-between">
                <span className="text-red-500 font-bold text-base">¥{item.price}<span className="text-xs text-gray-400 font-normal">起</span></span>
                <span className="text-[10px] text-gray-400">已售{item.sales}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>

    {/* Ad Banner */}
    <div className="mt-6 mx-4 rounded-xl bg-gradient-to-r from-green-100 to-blue-100 p-4 flex items-center justify-between border border-green-200">
      <div>
        <h3 className="font-bold text-green-800">新品预售 · 北海钦州营</h3>
        <p className="text-xs text-green-600 mt-1">限时抢购 20℃温暖冬日</p>
      </div>
      <button className="bg-green-600 text-white text-xs px-3 py-1.5 rounded-full font-bold shadow-md">立即查看</button>
    </div>
  </div>
);

// Module: Check-in (The core unique feature)
const CheckInView = () => (
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
          <button className="bg-red-500 text-white px-4 py-2 rounded-full text-sm font-bold shadow-md active:scale-95 transition-transform">
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
  </div>
);

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
        return <SquareView />;
      case 'group':
        return <GroupView />;
      case 'checkin':
        return <CheckInView />;
      case 'friends':
        return <FriendsView />;
      case 'mine':
        return <MineView />;
      default:
        return <SquareView />;
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