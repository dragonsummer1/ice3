import requests

# 登录获取JWT令牌
login_data = {
    'username': 'admin',  # 管理员用户名是admin
    'password': 'admin123'  # 根据db_init.py文件，管理员密码是admin123
}

# 发送登录请求
print("发送登录请求...")
login_response = requests.post('http://localhost:5000/api/auth/login', json=login_data)
print(f"登录响应状态码: {login_response.status_code}")
print(f"登录响应内容: {login_response.json()}")

# 从响应的cookies中获取JWT令牌
cookies = login_response.cookies
print(f"登录后获取的cookies: {cookies}")

# 使用获取的JWT令牌调用统计数据API
print("\n调用统计数据API...")
# 从cookies中提取JWT令牌
jwt_token = cookies.get('access_token_cookie')
if jwt_token:
    print(f"提取的JWT令牌: {jwt_token}")
    # 方法1: 使用cookie
    stats_response = requests.get('http://localhost:5000/api/admin/stats', cookies=cookies)
    print(f"统计数据API响应状态码(使用cookie): {stats_response.status_code}")
    print(f"统计数据API响应内容(使用cookie): {stats_response.json()}")
    
    # 方法2: 使用Authorization头
    headers = {'Authorization': f'Bearer {jwt_token}'}
    stats_response2 = requests.get('http://localhost:5000/api/admin/stats', headers=headers)
    print(f"统计数据API响应状态码(使用Authorization头): {stats_response2.status_code}")
    print(f"统计数据API响应内容(使用Authorization头): {stats_response2.json()}")
else:
    print("未获取到JWT令牌")