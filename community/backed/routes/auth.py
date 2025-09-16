from flask import Blueprint, request, jsonify, flash, redirect, url_for, session
from flask_login import login_user, logout_user, login_required, current_user
from models.user import User
from models.db import db
from werkzeug.security import check_password_hash

# 创建蓝图
bp = Blueprint('auth', __name__)

# 注册路由
@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # 验证数据
    if not data or 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({'error': '请提供完整的注册信息'}), 400
    
    # 检查用户名是否已存在
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': '用户名已存在'}), 400
    
    # 检查邮箱是否已存在
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': '邮箱已被注册'}), 400
    
    # 创建新用户
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    
    # 保存到数据库
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': '注册成功，请登录'}), 201

# 为了支持标签页隔离，我们需要修改登录机制
# 使用一个自定义的会话管理方式，基于标签页ID

# 存储不同标签页的用户会话
# 在实际生产环境中，应该使用更持久化的存储方式，如Redis
# 这里使用字典作为简单示例
# key: tabId, value: user_id
_tab_sessions = {}

# 登录路由
@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # 验证数据
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': '请提供用户名和密码'}), 400
    
    # 从请求体或请求头中获取标签页ID
    tab_id = data.get('tabId') or request.headers.get('X-Tab-Id')
    if not tab_id:
        return jsonify({'error': '标签页ID缺失'}), 400
    
    # 查找用户
    user = User.query.filter_by(username=data['username']).first()
    
    # 验证用户和密码
    if not user:
        # 用户名不存在
        return jsonify({'error': '用户名不存在'}), 401
    elif not user.check_password(data['password']):
        # 密码错误
        return jsonify({'error': '密码错误'}), 401
    
    # 检查用户状态
    if user.status != 'active':
        return jsonify({'error': '账号状态异常，请联系管理员'}), 403
    
    # 存储标签页会话
    _tab_sessions[tab_id] = user.id
    
    # 设置会话信息
    session['tab_id'] = tab_id
    
    # 返回用户信息
    return jsonify({
        'user': user.to_dict(),
        'message': '登录成功'
    }), 200

# 注销路由
@bp.route('/logout', methods=['POST'])
def logout():
    # 获取标签页ID
    tab_id = request.json.get('tabId') or session.get('tab_id')
    
    if tab_id and tab_id in _tab_sessions:
        # 移除标签页会话
        del _tab_sessions[tab_id]
    
    # 清除会话信息
    if 'tab_id' in session:
        session.pop('tab_id')
    
    return jsonify({'message': '已成功注销'}), 200

# 获取当前用户信息
@bp.route('/current-user', methods=['GET'])
def get_current_user():
    # 获取标签页ID
    tab_id = request.headers.get('X-Tab-Id') or session.get('tab_id')
    
    if tab_id and tab_id in _tab_sessions:
        # 根据标签页ID获取用户
        user_id = _tab_sessions[tab_id]
        user = User.query.get(user_id)
        if user:
            return jsonify(user=user.to_dict()), 200
    
    return jsonify({'error': '未授权访问'}), 401

# 检查登录状态
@bp.route('/check', methods=['GET'])
def check_login():
    # 获取标签页ID
    tab_id = request.headers.get('X-Tab-Id') or session.get('tab_id')
    
    if tab_id and tab_id in _tab_sessions:
        # 根据标签页ID获取用户
        user_id = _tab_sessions[tab_id]
        user = User.query.get(user_id)
        if user:
            return jsonify({
                'authenticated': True,
                'user': user.to_dict()
            }), 200
    
    return jsonify({'authenticated': False}), 200