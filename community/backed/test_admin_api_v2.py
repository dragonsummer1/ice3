import requests
import json

# 使用完整API路径测试管理员API访问权限
def test_admin_api_access():
    # 使用完整的API路径
    login_url = 'http://localhost:5000/api/auth/login'
    admin_dashboard_url = 'http://localhost:5000/api/admin/dashboard'
    admin_users_url = 'http://localhost:5000/api/admin/users?page=1&per_page=20'
    
    # 管理员登录凭证
    credentials = {
        'username': 'admin',
        'password': 'admin123',
        'tabId': 'test_admin_api_tab_v2'
    }
    
    # 创建一个会话对象来保持cookie
    session = requests.Session()
    
    # 发送登录请求
    print(f'尝试登录管理员账号...')
    response = session.post(login_url, json=credentials)
    
    if response.status_code == 200:
        print(f'登录成功！状态码: {response.status_code}')
        
        # 打印会话cookies
        print(f'会话cookies: {session.cookies.get_dict()}')
        
        # 使用标签页ID和cookie访问管理接口
        headers = {'X-Tab-Id': 'test_admin_api_tab_v2'}
        
        # 测试管理员仪表盘接口
        print('\n测试访问管理员仪表盘接口...')
        dashboard_response = session.get(admin_dashboard_url, headers=headers)
        print(f'仪表盘响应状态码: {dashboard_response.status_code}')
        print(f'仪表盘响应内容: {dashboard_response.text}')
        
        # 测试用户管理接口
        print('\n测试访问用户管理接口...')
        users_response = session.get(admin_users_url, headers=headers)
        print(f'用户管理响应状态码: {users_response.status_code}')
        print(f'用户管理响应内容: {users_response.text}')
    else:
        print(f'登录失败！状态码: {response.status_code}')
        print(f'登录响应内容: {response.text}')

if __name__ == '__main__':
    test_admin_api_access()