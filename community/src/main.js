import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
// 导入Element Plus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
// 导入axios并配置全局设置
import axios from 'axios'

// 设置axios基础URL
axios.defaults.baseURL = 'http://localhost:5000'
// 全局设置withCredentials，确保所有跨域请求都能携带凭证
axios.defaults.withCredentials = true

// 添加请求拦截器，确保跨域请求携带凭证
axios.interceptors.request.use(
  (config) => {
    config.withCredentials = true
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 添加响应拦截器，处理CORS错误
axios.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    // 处理CORS错误
    if (error.message.includes('Network Error') || 
        (error.response && error.response.status === 0)) {
      console.error('CORS错误或网络连接问题：', error.message)
    }
    return Promise.reject(error)
  }
)
// import{loadOml2d} from 'oh-my-live2d'
// loadOml2d({
//     models:[
//         {
//         path:'https://model.oml2d.com/cat-black/model.json',
//         position:[-10,20]
//     }
//     ]
// })
// oml2d.onLoad((status)=>{
//     switch(status){
//         case 'success':
//             console.log('加载成功')
//             break
//             case'falil':
//                 console.error('加载失败')
//                 break
//                 case'load':
//                     console.log('加载中')
//                     break
//     }
// })

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
// 使用Element Plus并配置中文语言
app.use(ElementPlus, { locale: zhCn })
app.mount('#app')