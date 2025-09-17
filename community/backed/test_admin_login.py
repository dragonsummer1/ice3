import requests
import json

# 测试管理员登录API
def test_admin_login():
    login_url = 'http://localhost:5000/api/auth/login'
    
    # 管理员登录凭证
    credentials = {
        'username': 'admin',
        'password': 'admin123',
        'tabId': 'test_tab_123'
    }
    
    # 发送登录请求
    print(f'尝试登录管理员账号: {credentials["username"]}')
    response = requests.post(login_url, json=credentials)
    
    # 打印响应结果
    print(f'登录响应状态码: {response.status_code}')
    print(f'登录响应内容: {response.text}')
    
    if response.status_code == 200:
        # 获取用户信息
        user_data = response.json().get('user')
        print(f'登录成功！用户信息: {user_data}')
        
        # 检查是否是管理员
        if user_data and user_data.get('is_admin'):
            print('✅ 用户是管理员！')
        else:
            print('❌ 用户不是管理员！')
        
        # 获取当前用户信息
        current_user_url = 'http://localhost:5000/api/auth/current-user'
        headers = {'X-Tab-Id': 'test_tab_123'}
        current_user_response = requests.get(current_user_url, headers=headers)
        print(f'当前用户响应: {current_user_response.status_code}')
        print(f'当前用户内容: {current_user_response.text}')
    
if __name__ == '__main__':
    test_admin_login()