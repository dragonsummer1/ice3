<template>
  <div class="transport">
    <div class="container">
      <h2 class="section-title">哈尔滨交通票价查询</h2>
      
      <div class="tabs">
        <button 
          v-for="tab in tabs" 
          :key="tab.id" 
          :class="['tab', { active: activeTab === tab.id }]"
          @click="switchTab(tab.id)"
        >
          {{ tab.name }}
        </button>
      </div>
      
      <div class="tab-content">
        <!-- 公交票价 -->
        <div v-if="activeTab === 'bus'" class="tab-pane">
          <div class="fare-info">
            <h3>公交票价信息</h3>
            <div class="info-card">
              <div class="card-header">
                <h4>普通公交线路</h4>
              </div>
              <div class="card-body">
                <ul>
                  <li>票价：1元/次（空调车2元/次）</li>
                  <li>支付方式：现金、公交卡、支付宝、微信</li>
                  <li>公交卡折扣：普通卡9折，学生卡5折</li>
                  <li>换乘优惠：90分钟内换乘享受1次0.5元优惠</li>
                </ul>
              </div>
            </div>
            
            <div class="info-card">
              <div class="card-header">
                <h4>旅游专线</h4>
              </div>
              <div class="card-body">
                <ul>
                  <li>冰雪大世界专线：票价2元</li>
                  <li>太阳岛专线：票价2元</li>
                  <li>伏尔加庄园专线：票价5元</li>
                  <li>机场巴士：票价20元</li>
                </ul>
              </div>
            </div>
          </div>
          
          <div class="route-planner">
            <h3>公交线路查询</h3>
            <div class="search-form">
              <input type="text" v-model="fromPlace" placeholder="出发地">
              <input type="text" v-model="toPlace" placeholder="目的地">
              <button @click="searchRoute">查询线路</button>
            </div>
            
            <div v-if="searchResult" class="search-result">
              <h4>推荐线路：</h4>
              <p>{{ searchResult }}</p>
            </div>
          </div>
        </div>
        
        <!-- 地铁票价 -->
        <div v-else-if="activeTab === 'subway'" class="tab-pane">
          <div class="fare-info">
            <h3>地铁票价信息</h3>
            <div class="info-card">
              <div class="card-header">
                <h4>票价标准</h4>
              </div>
              <div class="card-body">
                <ul>
                  <li>起步价：2元（6公里内）</li>
                  <li>6-10公里：3元</li>
                  <li>10-14公里：4元</li>
                  <li>14-21公里：5元</li>
                  <li>21-28公里：6元</li>
                  <li>28公里以上：每增加10公里增加1元</li>
                </ul>
              </div>
            </div>
            
            <div class="info-card">
              <div class="card-header">
                <h4>支付方式与优惠</h4>
              </div>
              <div class="card-body">
                <ul>
                  <li>支付方式：现金、公交卡、支付宝、微信</li>
                  <li>公交卡折扣：9折</li>
                  <li>学生卡：5折</li>
                  <li>老年卡：免费（65岁以上）</li>
                </ul>
              </div>
            </div>
          </div>
          
          <div class="subway-map">
            <h3>哈尔滨地铁线路图</h3>
            <div class="map-placeholder">
              <p>点击查看完整地铁线路图</p>
            </div>
          </div>
        </div>
        
        <!-- 出租车票价 -->
        <div v-else-if="activeTab === 'taxi'" class="tab-pane">
          <div class="fare-info">
            <h3>出租车票价信息</h3>
            <div class="info-card">
              <div class="card-header">
                <h4>普通出租车</h4>
              </div>
              <div class="card-body">
                <ul>
                  <li>起步价：9元（3公里内）</li>
                  <li>3公里以上：每公里1.9元</li>
                  <li>等候费：每5分钟1.9元</li>
                  <li>夜间费（22:00-次日5:00）：起步价10元，3公里以上每公里2.2元</li>
                </ul>
              </div>
            </div>
            
            <div class="info-card">
              <div class="card-header">
                <h4>网约车</h4>
              </div>
              <div class="card-body">
                <ul>
                  <li>滴滴出行：起步价10元左右，视车型而定</li>
                  <li>曹操出行：起步价12元左右</li>
                  <li>高德打车：整合多家平台，价格波动较大</li>
                </ul>
              </div>
            </div>
          </div>
          
          <div class="taxi-tips">
            <h3>乘坐出租车小贴士</h3>
            <ul>
              <li>建议提前确认目的地和大致费用</li>
              <li>保留发票，以便投诉或物品遗失时使用</li>
              <li>冬季高峰期可能会出现打车难的情况</li>
              <li>冰雪天气道路湿滑，请注意安全</li>
            </ul>
          </div>
        </div>
        
        <!-- 其他交通 -->
        <div v-else-if="activeTab === 'other'" class="tab-pane">
          <div class="fare-info">
            <h3>其他交通工具</h3>
            <div class="info-card">
              <div class="card-header">
                <h4>机场交通</h4>
              </div>
              <div class="card-body">
                <ul>
                  <li>机场大巴：票价20元，车程约40分钟</li>
                  <li>出租车：约100-150元，视交通情况而定</li>
                  <li>地铁：目前暂未直达，需转乘公交</li>
                </ul>
              </div>
            </div>
            
            <div class="info-card">
              <div class="card-header">
                <h4>火车/高铁</h4>
              </div>
              <div class="card-body">
                <ul>
                  <li>哈尔滨站：位于市中心，交通便利</li>
                  <li>哈尔滨西站：高铁主要站点，有地铁直达</li>
                  <li>哈尔滨东站：主要办理普通列车业务</li>
                </ul>
              </div>
            </div>
            
            <div class="info-card">
              <div class="card-header">
                <h4>共享单车/共享汽车</h4>
              </div>
              <div class="card-body">
                <ul>
                  <li>共享单车：1-2元/30分钟，冬季可能减少投放</li>
                  <li>共享汽车：时租约30-50元/小时，日租约200-300元/天</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TransportView',
  data() {
    return {
      tabs: [
        { id: 'bus', name: '公交车' },
        { id: 'subway', name: '地铁' },
        { id: 'taxi', name: '出租车' },
        { id: 'other', name: '其他交通' }
      ],
      activeTab: 'bus',
      fromPlace: '',
      toPlace: '',
      searchResult: ''
    }
  },
  methods: {
    searchRoute() {
      if (this.fromPlace && this.toPlace) {
        // 这里模拟查询结果，实际项目中应该调用API
        this.searchResult = `从${this.fromPlace}到${this.toPlace}，建议乘坐101路公交车，票价1元，约30分钟到达。`
      } else {
        alert('请输入出发地和目的地')
      }
    },
    // 添加一个明确的切换标签页方法
    switchTab(tabId) {
      this.activeTab = tabId;
      console.log('切换到标签页:', tabId);
    }
  },
  mounted() {
    // 页面滚动时为元素添加动画
    const animateOnScroll = () => {
      const elements = document.querySelectorAll('.info-card, .tab-pane');
      
      elements.forEach(element => {
        const elementPosition = element.getBoundingClientRect().top;
        const screenPosition = window.innerHeight / 1.2;
        
        if (elementPosition < screenPosition) {
          element.style.opacity = '1';
          element.style.transform = 'translateY(0)';
        }
      });
    };
    
    // 初始设置
    document.querySelectorAll('.info-card, .tab-pane').forEach(element => {
      element.style.opacity = '0';
      element.style.transform = 'translateY(30px)';
      element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    });
    
    // 监听滚动事件
    window.addEventListener('scroll', animateOnScroll);
    
    // 初始触发一次
    animateOnScroll();
    
    // 保存到实例属性，以便在beforeUnmount中访问
    this._animateOnScroll = animateOnScroll;
  },
  
  // Vue 3中的生命周期钩子，用于清理事件监听器
  beforeUnmount() {
    if (this._animateOnScroll) {
      window.removeEventListener('scroll', this._animateOnScroll);
    }
  }
}
</script>

<style scoped>
.transport {
  background-color: white;
  padding: 60px 0;
  position: relative;
}

/* 背景装饰 */
.transport::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, rgba(0, 86, 179, 0.05), transparent);
  border-radius: 50%;
  transform: translate(50%, -50%);
  z-index: 0;
}

.section-title {
  text-align: center;
  font-size: 2.5rem;
  margin-bottom: 50px;
  color: #0056b3;
  position: relative;
  display: inline-block;
  left: 50%;
  transform: translateX(-50%);
  padding: 10px 20px;
  z-index: 1;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 20%;
  width: 60%;
  height: 3px;
  background: linear-gradient(90deg, transparent, #0056b3, transparent);
}

.tabs {
  display: flex;
  justify-content: center;
  margin-bottom: 40px;
  position: relative;
  z-index: 1;
}

.tab {
  padding: 12px 25px;
  background-color: transparent;
  border: none;
  font-size: 1.2rem;
  color: #666;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  margin: 0 5px;
}

.tab::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, #0056b3, #003d82);
  transform: scaleX(0);
  transition: transform 0.3s ease;
  transform-origin: left;
}

.tab.active::before {
  transform: scaleX(1);
}

.tab.active {
  color: #0056b3;
  font-weight: bold;
}

.tab:hover {
  color: #0056b3;
  transform: translateY(-2px);
}

.tab-content {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  position: relative;
  z-index: 1;
}

.fare-info h3 {
  font-size: 1.8rem;
  margin-bottom: 25px;
  color: #333;
  padding-bottom: 10px;
  border-bottom: 2px solid #f0f0f0;
}

.info-card {
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  margin-bottom: 25px;
  overflow: hidden;
  transition: all 0.3s ease;
  position: relative;
}

.info-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}

.card-header {
  background: linear-gradient(135deg, #0056b3 0%, #003d82 100%);
  padding: 15px 20px;
  color: white;
}

.card-header h4 {
  font-size: 1.3rem;
  margin: 0;
  text-shadow: 0 1px 2px rgba(0,0,0,0.2);
}

.card-body {
  padding: 25px;
}

.card-body ul {
  list-style: none;
  padding: 0;
}

.card-body li {
  margin-bottom: 12px;
  padding-left: 25px;
  position: relative;
  line-height: 1.6;
  color: #555;
}

.card-body li::before {
  content: "✓";
  color: #0056b3;
  font-weight: bold;
  position: absolute;
  left: 0;
  background: rgba(0, 86, 179, 0.1);
  width: 18px;
  height: 18px;
  border-radius: 50%;
  text-align: center;
  font-size: 12px;
  line-height: 18px;
}

/* 标签页切换动画 */
.tab-pane {
  animation: fadeIn 0.5s ease-in;
}

.route-planner,
.subway-map,
.taxi-tips {
  margin-top: 30px;
}

.route-planner h3,
.subway-map h3,
.taxi-tips h3 {
  font-size: 1.5rem;
  margin-bottom: 20px;
  color: #333;
}

.search-form {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.search-form input {
  flex: 1;
  min-width: 200px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.search-form button {
  padding: 10px 20px;
  background-color: #0056b3;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.search-form button:hover {
  background-color: #004085;
}

.search-result {
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 4px;
}

.map-placeholder {
  background-color: #f8f9fa;
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.map-placeholder:hover {
  background-color: #e9ecef;
}

.taxi-tips ul {
  list-style: none;
  padding: 0;
}

.taxi-tips li {
  padding: 10px 0;
  padding-left: 20px;
  position: relative;
}

.taxi-tips li::before {
  content: "•";
  color: #0056b3;
  font-size: 1.5rem;
  position: absolute;
  left: 0;
  top: -5px;
}

@media (max-width: 768px) {
  .tabs {
    flex-direction: column;
    align-items: center;
  }
  
  .tab {
    width: 100%;
    max-width: 300px;
  }
  
  .search-form {
    flex-direction: column;
  }
  
  .search-form input {
    width: 100%;
  }
}
</style>