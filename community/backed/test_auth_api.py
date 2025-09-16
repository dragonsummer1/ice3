import requests
import json

# 测试登录API
def test_login():
    url = 'http://localhost:5000/api/auth/login'
    headers = {
        'Content-Type': 'application/json',
        'Origin': 'http://localhost:3000'  # 模拟前端域名
    }
    data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), allow_redirects=False)
        print(f"状态码: {response.status_code}")
        print(f"响应头: {response.headers}")
        print(f"响应内容: {response.json()}")
        
        # 检查CORS头
        if 'Access-Control-Allow-Origin' in response.headers:
            print(f"CORS Allow Origin: {response.headers['Access-Control-Allow-Origin']}")
        if 'Access-Control-Allow-Credentials' in response.headers:
            print(f"CORS Allow Credentials: {response.headers['Access-Control-Allow-Credentials']}")
            
    except Exception as e:
        print(f"请求异常: {e}")

if __name__ == '__main__':
    test_login()