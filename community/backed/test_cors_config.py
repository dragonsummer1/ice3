import requests
import json

# 测试登录API的URL
login_url = 'http://localhost:5000/api/auth/login'

# 测试凭证
credentials = {
    'username': 'admin',
    'password': 'admin123'
}

# 设置请求头，模拟前端请求
headers = {
    'Content-Type': 'application/json',
    'Origin': 'http://localhost:3000'  # 模拟前端源
}

# 发送OPTIONS预检请求
print("发送OPTIONS预检请求...")
options_response = requests.options(login_url, headers=headers)
print(f"OPTIONS响应状态码: {options_response.status_code}")
print("OPTIONS响应头:")
for key, value in options_response.headers.items():
    if key.lower().startswith('access-control'):
        print(f"  {key}: {value}")

# 发送实际的登录请求
print("\n发送登录POST请求...")
try:
    # 允许携带凭证（cookie）
    response = requests.post(
        login_url, 
        data=json.dumps(credentials), 
        headers=headers,
        cookies={},  # 初始化空cookies
        allow_redirects=False
    )
    
    print(f"POST响应状态码: {response.status_code}")
    
    # 打印CORS相关响应头
    print("POST响应CORS头:")
    cors_headers = False
    for key, value in response.headers.items():
        if key.lower().startswith('access-control'):
            cors_headers = True
            print(f"  {key}: {value}")
    
    if not cors_headers:
        print("  未找到CORS相关响应头")
    
    # 打印响应内容
    print("POST响应内容:")
    try:
        print(f"  {response.json()}")
    except json.JSONDecodeError:
        print(f"  无法解析响应内容: {response.text}")
        
    # 打印Set-Cookie头
    print("POST响应Cookie头:")
    if 'Set-Cookie' in response.headers:
        print(f"  {response.headers['Set-Cookie']}")
    else:
        print("  未找到Set-Cookie头")
        
except requests.exceptions.RequestException as e:
    print(f"请求异常: {e}")