import axios from 'axios';

// 设置axios配置
axios.defaults.baseURL = 'http://localhost:5000';
axios.defaults.withCredentials = true; // 允许携带凭证

// 测试登录函数
async function testLogin() {
    console.log('开始测试前端登录请求...');
    
    try {
        // 发送登录请求
        const response = await axios.post('/api/auth/login', {
            username: 'admin',
            password: 'admin123'
        }, {
            headers: {
                'Content-Type': 'application/json',
                'Origin': 'http://localhost:3000'
            },
            withCredentials: true
        });
        
        console.log('登录请求成功!');
        console.log(`响应状态码: ${response.status}`);
        
        // 打印CORS相关头
        console.log('CORS响应头:');
        for (const [key, value] of Object.entries(response.headers)) {
            if (key.toLowerCase().startsWith('access-control')) {
                console.log(`  ${key}: ${value}`);
            }
        }
        
        // 打印响应数据
        console.log('登录成功，用户数据:');
        console.log(response.data);
        
        // 测试请求受保护的资源
        console.log('\n测试访问受保护的资源...');
        const profileResponse = await axios.get('/api/auth/current-user', {
            headers: {
                'Origin': 'http://localhost:3000'
            },
            withCredentials: true
        });
        
        console.log('受保护资源访问成功!');
        console.log('当前用户信息:');
        console.log(profileResponse.data);
        
    } catch (error) {
        console.error('登录请求失败:');
        if (error.response) {
            // 服务器返回了错误状态码
            console.error(`状态码: ${error.response.status}`);
            console.error('响应数据:', error.response.data);
            console.error('响应头:', error.response.headers);
        } else if (error.request) {
            // 请求已发送但没有收到响应
            console.error('没有收到响应:', error.request);
        } else {
            // 设置请求时发生错误
            console.error('请求错误:', error.message);
        }
        console.error('错误配置:', error.config);
    }
}

// 运行测试
console.log('请确保已安装axios: npm install axios');
console.log('正在执行测试...\n');
testLogin();

// 为了ES模块兼容性，导出一个空对象
export default {};