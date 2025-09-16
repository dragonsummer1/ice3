<template>
  <div class="tips">
    <div class="container">
      <h2>哈尔滨旅游避坑指南</h2>
      
      <div class="tips-categories">
        <div class="category-nav">
          <button 
            v-for="category in categories" 
            :key="category.id" 
            :class="['category-btn', { active: activeCategory === category.id }]"
            @click="activeCategory = category.id"
          >
            {{ category.name }}
          </button>
        </div>
        
        <div class="category-content">
          <!-- 交通避坑 -->
          <div v-if="activeCategory === 'transport'" class="category-section">
            <h3>交通避坑</h3>
            <div class="tip-item">
              <h4>🚕 出租车陷阱</h4>
              <p>哈尔滨部分出租车司机可能会以各种理由不打表或绕路。建议：</p>
              <ul>
                <li>一定要选择正规出租车，查看是否有营运证</li>
                <li>上车前确认是否打表，若司机拒绝打表可选择更换车辆</li>
                <li>提前了解大致路线和费用，避免被绕路</li>
                <li>保留发票，遇到问题可拨打投诉电话</li>
              </ul>
            </div>
            
            <div class="tip-item">
              <h4>🚌 公交注意事项</h4>
              <p>冬季哈尔滨公交可能会因天气原因延误。建议：</p>
              <ul>
                <li>提前规划行程，预留充足时间</li>
                <li>准备零钱或下载哈尔滨公交APP</li>
                <li>冰雪天气道路湿滑，上下车请注意安全</li>
              </ul>
            </div>
            
            <div class="tip-item">
              <h4>🚗 租车自驾风险</h4>
              <p>冬季哈尔滨路面结冰，自驾需特别谨慎。建议：</p>
              <ul>
                <li>选择四驱车辆并配备雪地胎</li>
                <li>了解冰雪路面驾驶技巧，控制车速</li>
                <li>提前检查车辆状况，特别是刹车和防冻液</li>
                <li>购买全面的车辆保险</li>
              </ul>
            </div>
          </div>
          
          <!-- 景点避坑 -->
          <div v-else-if="activeCategory === 'attractions'" class="category-section">
            <h3>景点避坑</h3>
            <div class="tip-item">
              <h4>🎫 门票购买陷阱</h4>
              <p>哈尔滨部分热门景点存在高价票、假票等问题。建议：</p>
              <ul>
                <li>通过官方渠道或正规旅行社购买门票</li>
                <li>注意辨别门票真伪，查看防伪标识</li>
                <li>冰雪大世界等景点有日场和夜场之分，价格不同</li>
                <li>关注官方公众号，有时会推出优惠活动</li>
              </ul>
            </div>
            
            <div class="tip-item">
              <h4>⏰ 排队与时间安排</h4>
              <p>哈尔滨热门景点冬季人流量大，排队时间长。建议：</p>
              <ul>
                <li>避开节假日和周末高峰期</li>
                <li>提前到达景点，错峰游览</li>
                <li>冰雪大世界建议下午4点左右入场，可以同时欣赏白天和夜晚景色</li>
                <li>合理安排每日行程，避免赶场</li>
              </ul>
            </div>
            
            <div class="tip-item">
              <h4>📸 拍照陷阱</h4>
              <p>景区内可能有人以免费拍照为噱头，收取高额费用。建议：</p>
              <ul>
                <li>明确拍照费用后再拍摄</li>
                <li>不要轻易相信"免费拍照"的宣传</li>
                <li>重要景点提前了解最佳拍摄位置和时间</li>
              </ul>
            </div>
          </div>
          
          <!-- 住宿避坑 -->
          <div v-else-if="activeCategory === 'accommodation'" class="category-section">
            <h3>住宿避坑</h3>
            <div class="tip-item">
              <h4>🏨 酒店预订陷阱</h4>
              <p>冬季是哈尔滨旅游旺季，酒店价格波动大。建议：</p>
              <ul>
                <li>提前至少1个月预订酒店，特别是节假日期间</li>
                <li>选择市中心或景点附近的酒店，方便出行</li>
                <li>注意查看酒店评价，特别是关于供暖和热水的评价</li>
                <li>确认酒店是否提供接送服务</li>
              </ul>
            </div>
            
            <div class="tip-item">
              <h4>❄️ 冬季住宿注意事项</h4>
              <p>哈尔滨冬季寒冷，住宿有特殊需求。建议：</p>
              <ul>
                <li>确认酒店供暖情况，要求24小时热水</li>
                <li>选择有空调或地热的房间</li>
                <li>注意室内外温差，避免感冒</li>
                <li>贵重物品妥善保管，建议使用酒店保险箱</li>
              </ul>
            </div>
          </div>
          
          <!-- 饮食避坑 -->
          <div v-else-if="activeCategory === 'food'" class="category-section">
            <h3>饮食避坑</h3>
            <div class="tip-item">
              <h4>🍲 餐厅选择陷阱</h4>
              <p>哈尔滨部分餐厅可能存在价格虚高、服务质量差等问题。建议：</p>
              <ul>
                <li>选择大众点评、美团等平台上评价高的餐厅</li>
                <li>注意查看菜单价格，避免被宰</li>
                <li>中央大街等景区内餐厅价格普遍偏高，可选择景区外就餐</li>
                <li>尝试当地特色美食，但注意适量，避免肠胃不适</li>
              </ul>
            </div>
            
            <div class="tip-item">
              <h4>☕ 饮品与小吃</h4>
              <p>哈尔滨冬季寒冷，饮品和小吃选择有讲究。建议：</p>
              <ul>
                <li>适量饮用当地特色饮品如格瓦斯、秋林红肠等</li>
                <li>注意食品卫生，选择正规摊位购买小吃</li>
                <li>冬季户外活动后，避免立即饮用过烫的饮品</li>
              </ul>
            </div>
          </div>
          
          <!-- 购物避坑 -->
          <div v-else-if="activeCategory === 'shopping'" class="category-section">
            <h3>购物避坑</h3>
            <div class="tip-item">
              <h4>🛍️ 特产购买陷阱</h4>
              <p>购买哈尔滨特产时需注意辨别真伪和价格。建议：</p>
              <ul>
                <li>选择正规商场或超市购买特产</li>
                <li>秋林红肠、大列巴等特产注意查看生产日期和保质期</li>
                <li>不要轻易相信景区内流动商贩的推销</li>
                <li>比较价格后再购买，避免被宰</li>
              </ul>
            </div>
            
            <div class="tip-item">
              <h4>💍 珠宝与纪念品</h4>
              <p>哈尔滨以冰雪文化和俄罗斯风情著称，购买纪念品需谨慎。建议：</p>
              <ul>
                <li>水晶、玛瑙等珠宝建议到正规商店购买并索要鉴定证书</li>
                <li>俄罗斯套娃等纪念品注意品质和价格</li>
                <li>理性消费，不要被商家的夸大宣传所迷惑</li>
              </ul>
            </div>
          </div>
          
          <!-- 安全避坑 -->
          <div v-else-if="activeCategory === 'safety'" class="category-section">
            <h3>安全避坑</h3>
            <div class="tip-item">
              <h4>❄️ 冰雪活动安全</h4>
              <p>哈尔滨冬季冰雪活动丰富，但安全第一。建议：</p>
              <ul>
                <li>选择正规滑雪场和冰上活动场所</li>
                <li>遵守场地规则，听从工作人员指导</li>
                <li>滑雪等高危活动建议购买保险并聘请教练</li>
                <li>注意保暖，避免冻伤</li>
              </ul>
            </div>
            
            <div class="tip-item">
              <h4>👮 人身与财产安全</h4>
              <p>旅游期间注意人身和财产安全。建议：</p>
              <ul>
                <li>保管好身份证、护照等重要证件</li>
                <li>贵重物品随身携带，不要放在酒店房间</li>
                <li>避免前往人员稀少的地方，特别是夜间</li>
                <li>了解当地紧急电话，如报警110、急救120等</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
      
      <div class="user-tips">
        <h3>用户分享的实用贴士</h3>
        <div class="user-tip-list">
          <div class="user-tip-item" v-for="tip in userTips" :key="tip.id">
            <div class="tip-header">
              <span class="user-name">{{ tip.user }}</span>
              <span class="tip-date">{{ tip.date }}</span>
            </div>
            <p class="tip-content">{{ tip.content }}</p>
            <div class="tip-actions">
              <button @click="likeTip(tip.id)">👍 {{ tip.likes }}</button>
              <button>💬 评论</button>
            </div>
          </div>
        </div>
        
        <div class="share-tip">
          <h4>分享你的避坑经验</h4>
          <textarea v-model="newTip" placeholder="请分享你的哈尔滨旅游避坑经验..." rows="4"></textarea>
          <button @click="submitTip">提交</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TipsView',
  data() {
    return {
      categories: [
        { id: 'transport', name: '交通避坑' },
        { id: 'attractions', name: '景点避坑' },
        { id: 'accommodation', name: '住宿避坑' },
        { id: 'food', name: '饮食避坑' },
        { id: 'shopping', name: '购物避坑' },
        { id: 'safety', name: '安全避坑' }
      ],
      activeCategory: 'transport',
      userTips: [
        {
          id: 1,
          user: '冰雪旅行者',
          date: '2024-01-15',
          content: '去冰雪大世界一定要穿防滑鞋！景区内地面很滑，我看到好多人摔倒了。另外，建议下午4点左右入场，可以看白天和夜晚两种不同的景色，非常值得！',
          likes: 42
        },
        {
          id: 2,
          user: '哈尔滨常客',
          date: '2024-01-10',
          content: '中央大街的餐厅价格普遍偏高，建议去离中央大街不远的其他街道就餐，价格更实惠，味道也更地道。推荐去道外区尝试正宗的哈尔滨美食。',
          likes: 36
        },
        {
          id: 3,
          user: '南方游客',
          date: '2024-01-05',
          content: '作为南方人，第一次来哈尔滨被冻得够呛。建议多穿几层，贴身的保暖内衣很重要，还有帽子、围巾、手套缺一不可。另外，手机在低温下很容易没电，最好准备一个保暖套或者充电宝。',
          likes: 58
        }
      ],
      newTip: ''
    }
  },
  methods: {
    likeTip(tipId) {
      const tip = this.userTips.find(t => t.id === tipId)
      if (tip) {
        tip.likes++
      }
    },
    submitTip() {
      if (this.newTip.trim()) {
        const now = new Date()
        const formattedDate = now.getFullYear() + '-' + 
                             String(now.getMonth() + 1).padStart(2, '0') + '-' + 
                             String(now.getDate()).padStart(2, '0')
        
        this.userTips.unshift({
          id: Date.now(),
          user: '匿名用户',
          date: formattedDate,
          content: this.newTip,
          likes: 0
        })
        
        this.newTip = ''
        alert('感谢您的分享！')
      } else {
        alert('请输入内容后再提交')
      }
    },
    // 滚动触发动画
    animateOnScroll() {
      const elements = document.querySelectorAll('.tip-item, .category-nav, .category-content, .user-tips')
      elements.forEach(element => {
        const position = element.getBoundingClientRect()
        // 元素进入视口
        if (position.top < window.innerHeight - 100 && position.bottom >= 0) {
          element.classList.add('fade-in-up')
        }
      })
    }
  },
  mounted() {
    // 添加滚动事件监听
    window.addEventListener('scroll', this.animateOnScroll)
    // 初始化时执行一次，确保可视区域内的元素也能被动画化
    this.animateOnScroll()
  },
  beforeUnmount() {
    // 清理事件监听器
    window.removeEventListener('scroll', this.animateOnScroll)
  }
}
</script>

<style scoped>
/* 导入全局动画样式 */
@import '../assets/animations.css';

.tips {
  padding: 30px 0;
  position: relative;
  overflow: hidden;
}

/* 背景装饰 */
.tips::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(0, 86, 179, 0.03) 0%, rgba(0, 173, 239, 0.03) 100%);
  z-index: -1;
}

.tips h2 {
  text-align: center;
  font-size: 2.2rem;
  margin-bottom: 30px;
  color: #0056b3;
  position: relative;
  display: inline-block;
  left: 50%;
  transform: translateX(-50%);
}

/* 标题装饰线 */
.tips h2::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(90deg, transparent, #0056b3, transparent);
  border-radius: 2px;
}

.tips-categories {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
  justify-content: center;
}

.category-nav {
  flex: 0 0 220px;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  border: 1px solid rgba(255, 255, 255, 0.5);
  opacity: 1; /* 默认可见 */
  transform: translateY(0); /* 默认位置 */
  transition: opacity 0.8s ease, transform 0.8s ease;
}

.category-btn {
  display: block;
  width: 100%;
  padding: 12px 16px;
  margin-bottom: 12px;
  border: 1px solid #ddd;
  background: white;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: left;
  border-radius: 8px;
  font-size: 1rem;
  position: relative;
  overflow: hidden;
}

/* 按钮悬浮效果 */
.category-btn:hover {
  background: linear-gradient(45deg, #0056b3, #007bff);
  color: white;
  border-color: #0056b3;
  transform: translateX(5px);
  box-shadow: 0 4px 12px rgba(0, 86, 179, 0.3);
}

/* 按钮伪元素动画 */
.category-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.5s;
}

.category-btn:hover::before {
  left: 100%;
}

.category-btn.active {
  background: linear-gradient(45deg, #0056b3, #007bff);
  color: white;
  border-color: #0056b3;
  box-shadow: 0 4px 12px rgba(0, 86, 179, 0.3);
}

.category-content {
  flex: 1;
  min-width: 300px;
  max-width: 800px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  border: 1px solid rgba(255, 255, 255, 0.5);
  opacity: 1; /* 默认可见 */
  transform: translateY(0); /* 默认位置 */
  transition: opacity 0.8s ease, transform 0.8s ease;
}

.category-section h3 {
  font-size: 1.8rem;
  margin-bottom: 25px;
  color: #0056b3;
  position: relative;
  padding-bottom: 10px;
}

/* 二级标题装饰 */
.category-section h3::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 60px;
  height: 3px;
  background: linear-gradient(90deg, #0056b3, #007bff);
  border-radius: 1.5px;
}

.tip-item {
  margin-bottom: 35px;
  padding: 20px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  border-left: 4px solid #0056b3;
  transition: all 0.3s ease;
  opacity: 1; /* 默认可见 */
  transform: translateY(0); /* 默认位置 */
  transition: opacity 0.6s ease, transform 0.6s ease;
}

/* 卡片悬浮效果 */
.tip-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.12);
}

.tip-item h4 {
  font-size: 1.3rem;
  margin-bottom: 15px;
  color: #333;
  display: flex;
  align-items: center;
  gap: 8px;
}

.tip-item p {
  margin-bottom: 15px;
  color: #666;
  line-height: 1.7;
}

.tip-item ul {
  padding-left: 25px;
  color: #666;
}

.tip-item li {
  margin-bottom: 8px;
  line-height: 1.6;
  position: relative;
}

/* 列表项装饰 */
.tip-item li::marker {
  color: #0056b3;
  font-size: 1.2em;
}

.user-tips {
  margin-top: 40px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  border: 1px solid rgba(255, 255, 255, 0.5);
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.8s ease, transform 0.8s ease;
}

.user-tips h3 {
  font-size: 1.6rem;
  margin-bottom: 20px;
  color: #0056b3;
  position: relative;
  padding-bottom: 10px;
}

.user-tips h3::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 50px;
  height: 3px;
  background: linear-gradient(90deg, #0056b3, #007bff);
  border-radius: 1.5px;
}

.user-tip-list {
  margin-bottom: 30px;
}

.user-tip-item {
  padding: 20px;
  margin-bottom: 15px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  transition: all 0.3s ease;
}

.user-tip-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.tip-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.user-name {
  font-weight: bold;
  color: #0056b3;
  font-size: 1.05rem;
}

.tip-date {
  color: #999;
  font-size: 0.9rem;
}

.tip-content {
  margin-bottom: 12px;
  color: #666;
  line-height: 1.7;
  padding: 10px 0;
}

.tip-actions button {
  margin-right: 10px;
  padding: 6px 12px;
  border: none;
  background: linear-gradient(45deg, #0056b3, #007bff);
  color: white;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
  font-weight: 500;
}

.tip-actions button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0, 86, 179, 0.3);
}

.share-tip h4 {
  font-size: 1.2rem;
  margin-bottom: 10px;
  color: #333;
}

.share-tip textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  resize: vertical;
  margin-bottom: 10px;
}

.share-tip button {
  padding: 10px 20px;
  background-color: #0056b3;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.share-tip button:hover {
  background-color: #004085;
}

@media (max-width: 768px) {
  .tips-categories {
    flex-direction: column;
  }
  
  .category-nav {
    flex: none;
    width: 100%;
  }
  
  .category-btn {
    display: inline-block;
    width: auto;
    margin-right: 10px;
  }
}
</style>