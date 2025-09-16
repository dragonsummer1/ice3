<template>
  <div class="home">
    <!-- 雪花飘落效果容器 -->
    <div class="snow-container"></div>
    
    <div class="hero">
      <div class="container">
        <h2 class="hero-title typewriter">欢迎来到哈尔滨冰雪旅游指南</h2>
        <p class="hero-subtitle">探索冰雪奇缘，畅享北国风光</p>
      </div>
    </div>
    
    <div class="features">
      <div class="container">
        <h3>核心功能</h3>
        <div class="feature-cards">
          <div class="card card-hover" @click="goTo('transport')">
            <div class="card-icon">🚌</div>
            <h4>交通票价查询</h4>
            <p>获取哈尔滨各类交通工具的详细票价信息和乘坐指南</p>
          </div>
          
          <div class="card card-hover" @click="goTo('tips')">
            <div class="card-icon">⚠️</div>
            <h4>避坑指南</h4>
            <p>实用的旅游贴士，帮助您避开常见陷阱，享受完美旅程</p>
          </div>
          
          <div class="card card-hover" @click="goTo('forum')">
            <div class="card-icon">💬</div>
            <h4>旅游论坛</h4>
            <p>与其他游客交流经验，分享心得，获取最新旅游信息</p>
          </div>
        </div>
      </div>
    </div>
    
    <div class="highlight">
      <div class="container">
        <h3>哈尔滨热门景点</h3>
        <div class="scenic-spots">
          <div class="spot flip-card">
            <div class="flip-card-inner">
              <div class="flip-card-front">
                <img src="https://ts1.tc.mm.bing.net/th/id/R-C.7d07203bba9f27da6f3920746a18a027?rik=l%2bm%2fjlg0Q4d0lw&riu=http%3a%2f%2fimg95.699pic.com%2fphoto%2f50116%2f4211.jpg_wh860.jpg&ehk=ZylboPWKeOXXAS7LoRPu6EkaQxyD6y6Y9X6cLgGnjUg%3d&risl=&pid=ImgRaw&r=0" alt="哈尔滨冰雪大世界" style="width: 100%; height: 200px; object-fit: cover;">
                <h4>哈尔滨冰雪大世界</h4>
                <p>世界最大的冰雪主题乐园，每年吸引数百万游客</p>
              </div>
              <div class="flip-card-back glass-effect">
                <h4>哈尔滨冰雪大世界</h4>
                <p>开放时间: 09:00-21:30</p>
                <p>门票价格: 330元/人</p>
                <p>推荐游玩时间: 3-4小时</p>
              </div>
            </div>
          </div>
          
          <div class="spot flip-card">
            <div class="flip-card-inner">
              <div class="flip-card-front">
                <img src="https://ts2.tc.mm.bing.net/th/id/OIP-C.QWlj3cBTGXnXT9dDzNHc1AHaE8?rs=1&pid=ImgDetMain" alt="中央大街" style="width: 100%; height: 200px; object-fit: cover;">
                <h4>中央大街</h4>
                <p>百年历史的商业老街，充满欧洲风情的建筑和特色美食</p>
              </div>
              <div class="flip-card-back glass-effect">
                <h4>中央大街</h4>
                <p>开放时间: 全天开放</p>
                <p>门票价格: 免费</p>
                <p>推荐游玩时间: 2-3小时</p>
              </div>
            </div>
          </div>
          
          <div class="spot flip-card">
            <div class="flip-card-inner">
              <div class="flip-card-front">
                <img src="https://youimg1.c-ctrip.com/target/100h180000013yt7w5EA2.jpg" alt="松花江" style="width: 100%; height: 200px; object-fit: cover;">
                <h4>松花江</h4>
                <p>冬季可以在江上进行各种冰上活动，感受北国特色</p>
              </div>
              <div class="flip-card-back glass-effect">
                <h4>松花江</h4>
                <p>开放时间: 全天开放</p>
                <p>门票价格: 免费（部分活动收费）</p>
                <p>推荐游玩时间: 1-2小时</p>
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
  name: 'HomeView',
  methods: {
    goTo(route) {
      this.$router.push(`/${route}`)
    },
    
    // 创建雪花飘落效果
    createSnowflakes() {
      const snowContainer = document.querySelector('.snow-container');
      if (!snowContainer) return;
      
      // 清除已有的雪花
      snowContainer.innerHTML = '';
      
      const snowflakeCount = 100; // 雪花数量
      
      for (let i = 0; i < snowflakeCount; i++) {
        const snowflake = document.createElement('div');
        snowflake.classList.add('snowflake');
        
        // 随机大小
        const size = Math.random() * 8 + 2;
        snowflake.style.width = `${size}px`;
        snowflake.style.height = `${size}px`;
        
        // 随机位置
        snowflake.style.left = `${Math.random() * 100}%`;
        
        // 随机动画持续时间
        const duration = Math.random() * 10 + 5;
        snowflake.style.animationDuration = `${duration}s`;
        
        // 随机动画延迟
        const delay = Math.random() * 10;
        snowflake.style.animationDelay = `${delay}s`;
        
        // 随机透明度
        snowflake.style.opacity = Math.random() * 0.8 + 0.2;
        
        // 随机动画速度
        snowflake.style.animationTimingFunction = `cubic-bezier(${Math.random() * 0.3 + 0.1}, 0, ${Math.random() * 0.3 + 0.7}, 1)`;
        
        snowContainer.appendChild(snowflake);
      }
    },
    
    // 页面滚动时为元素添加动画
    animateOnScroll() {
      const elements = document.querySelectorAll('.card, .spot');
      
      elements.forEach(element => {
        const elementPosition = element.getBoundingClientRect().top;
        const screenPosition = window.innerHeight / 1.2;
        
        if (elementPosition < screenPosition) {
          element.style.opacity = '1';
          element.style.transform = 'translateY(0)';
        }
      });
    }
  },
  
  mounted() {
    // 创建雪花
    this.createSnowflakes();
    
    // 初始设置
    document.querySelectorAll('.card, .spot').forEach(element => {
      element.style.opacity = '0';
      element.style.transform = 'translateY(30px)';
      element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    });
    
    // 监听滚动事件
    window.addEventListener('scroll', this.animateOnScroll);
    
    // 初始触发一次
    this.animateOnScroll();
  },
  
  beforeUnmount() {
    // 清理事件监听器
    window.removeEventListener('scroll', this.animateOnScroll);
  }
}
</script>

<style scoped>
.hero {
  background: linear-gradient(135deg, #0056b3 0%, #003d82 100%);
  background-size: 400% 400%;
  animation: gradientShift 15s ease infinite;
  color: white;
  text-align: center;
  padding: 150px 0;
  position: relative;
  overflow: hidden;
}

.hero::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" preserveAspectRatio="none"><polygon points="0,100 100,0 100,100" fill="rgba(255,255,255,0.05)"/></svg>');
  background-size: cover;
}

.hero-title {
  font-size: 3rem;
  margin-bottom: 20px;
  text-shadow: 0 2px 10px rgba(0,0,0,0.2);
  animation: slideInTop 0.8s ease-out;
}

.hero-subtitle {
    font-size: 1.5rem;
    opacity: 0;
    animation: fadeIn 1s ease-out 0.5s forwards;
  }

  /* 雪花容器样式 */
  .snow-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 9999;
  }

  .features {
    background-color: white;
    padding: 60px 0;
  }

  .features h3 {
    text-align: center;
    font-size: 2rem;
    margin-bottom: 40px;
    color: #0056b3;
    position: relative;
    display: inline-block;
    left: 50%;
    transform: translateX(-50%);
    padding: 10px 20px;
  }

  .features h3::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 20%;
    width: 60%;
    height: 3px;
    background: linear-gradient(90deg, transparent, #0056b3, transparent);
  }

  /* 功能卡片样式增强 */
  .feature-cards {
    display: flex;
    justify-content: space-between;
    gap: 20px;
    flex-wrap: wrap;
  }

  .card {
    flex: 1;
    min-width: 280px;
    background-color: #f9f9f9;
    border-radius: 10px;
    padding: 30px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    text-align: center;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    transition: transform 0.3s, box-shadow 0.3s;
  }

  .card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 5px;
    background: linear-gradient(90deg, #0056b3, #003d82);
    transform: scaleX(0);
    transition: transform 0.3s ease;
    transform-origin: left;
  }

  .card:hover::before {
    transform: scaleX(1);
  }

  .card:hover {
    transform: translateY(-10px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.12);
  }

  .card-icon {
    font-size: 3rem;
    margin-bottom: 20px;
    transition: transform 0.3s ease;
  }

  .card:hover .card-icon {
    transform: scale(1.2) rotate(10deg);
  }

  .card h4 {
    font-size: 1.5rem;
    margin-bottom: 15px;
    color: #333;
  }

  .card p {
    color: #666;
    line-height: 1.6;
  }

  /* 景点展示样式增强 */
  .highlight {
    background-color: #f8f9fa;
    padding: 60px 0;
  }

  .highlight h3 {
    text-align: center;
    font-size: 2rem;
    margin-bottom: 40px;
    color: #0056b3;
    position: relative;
    display: inline-block;
    left: 50%;
    transform: translateX(-50%);
    padding: 10px 20px;
  }

  .highlight h3::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 20%;
    width: 60%;
    height: 3px;
    background: linear-gradient(90deg, transparent, #0056b3, transparent);
  }

  .scenic-spots {
    display: flex;
    justify-content: space-between;
    gap: 20px;
    flex-wrap: wrap;
  }

  .spot {
    flex: 1;
    min-width: 280px;
    background-color: white;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    height: 320px;
  }

  .flip-card {
    perspective: 1000px;
  }

  .flip-card-inner {
    position: relative;
    width: 100%;
    height: 100%;
    text-align: center;
    transition: transform 0.8s ease;
    transform-style: preserve-3d;
  }

  .flip-card:hover .flip-card-inner {
    transform: rotateY(180deg);
  }

  .flip-card-front,
  .flip-card-back {
    position: absolute;
    width: 100%;
    height: 100%;
    backface-visibility: hidden;
    border-radius: 10px;
    overflow: hidden;
  }

  .flip-card-front {
    background-color: white;
  }

  .flip-card-back {
    background: linear-gradient(135deg, #0056b3 0%, #003d82 100%);
    color: white;
    transform: rotateY(180deg);
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 20px;
  }

  .flip-card-front img {
    width: 100%;
    height: 200px;
    object-fit: cover;
    transition: transform 0.5s ease;
  }

  .flip-card-front:hover img {
    transform: scale(1.1);
  }

  .flip-card-front h4 {
    font-size: 1.3rem;
    margin: 15px 0 10px;
    color: #333;
  }

  .flip-card-front p {
    color: #666;
    padding: 0 20px 20px;
    font-size: 0.95rem;
  }

  .flip-card-back h4 {
    font-size: 1.5rem;
    margin-bottom: 15px;
    text-shadow: 0 2px 4px rgba(0,0,0,0.2);
  }

  .flip-card-back p {
    margin: 8px 0;
    font-size: 1rem;
    text-shadow: 0 1px 2px rgba(0,0,0,0.2);
  }

  /* 响应式布局优化 */
  @media (max-width: 768px) {
    .feature-cards,
    .scenic-spots {
      flex-direction: column;
      align-items: center;
    }
    
    .hero-title {
      font-size: 2.2rem;
    }
    
    .hero-subtitle {
      font-size: 1.2rem;
    }
    
    .card, .spot {
      width: 100%;
    }
  }
</style>