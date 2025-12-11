import React, { useState, useEffect } from 'react';
import { ChevronRight } from 'lucide-react';
import { getHotActivities } from './api/supabase';

// Module: Square (Similar to the reference image Home)
const SquareView = ({ CATEGORIES, Header }) => {
  const [hotActivities, setHotActivities] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHotActivities = async () => {
      try {
        const data = await getHotActivities();
        // 转换数据格式以匹配前端组件期望的格式
        const formattedActivities = data.map(activity => ({
          id: activity.id,
          title: activity.name,
          subtitle: activity.description,
          price: activity.price.toFixed(0),
          sales: activity.sales_count > 10000 ? `${(activity.sales_count / 10000).toFixed(1)}万` : activity.sales_count.toString(),
          image: activity.image_url,
          tag: activity.tag
        }));
        setHotActivities(formattedActivities);
      } catch (error) {
        console.error('Error fetching hot activities:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchHotActivities();
  }, []);

  if (loading) {
    return <div className="text-center py-4">加载中...</div>;
  }

  return (
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
          {hotActivities.map((item) => (
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
};

export default SquareView;