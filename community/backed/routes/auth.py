from flask import Blueprint, request, jsonify, flash, redirect, url_for
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

# 登录路由
@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # 验证数据
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': '请提供用户名和密码'}), 400
    
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
    
    # 登录用户
    login_user(user, remember=data.get('remember', False))
    
    # 返回用户信息
    return jsonify({
        'user': user.to_dict(),
        'message': '登录成功'
    }), 200

# 注销路由
@bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': '已成功注销'}), 200

# 获取当前用户信息
@bp.route('/current-user', methods=['GET'])
@login_required
def get_current_user():
    return jsonify(user=current_user.to_dict()), 200

# 检查登录状态
@bp.route('/check', methods=['GET'])
def check_login():
    if current_user.is_authenticated:
        return jsonify({
            'authenticated': True,
            'user': current_user.to_dict()
        }), 200
    return jsonify({'authenticated': False}), 200