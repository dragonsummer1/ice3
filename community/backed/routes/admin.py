from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from models.user import User
from models.comment import Comment
from models.db import db
import functools
from flask import Blueprint, jsonify, request

# 创建蓝图
bp = Blueprint('admin', __name__)

# 导入必要的模块
from datetime import datetime, timedelta
from models.topic import Topic

# 管理员权限检查装饰器
def admin_required(f):
    @functools.wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin_user():
            return jsonify({'error': '无管理员权限'}), 403
        return f(*args, **kwargs)
    return decorated_function

# 管理员仪表盘
@bp.route('/dashboard')
@admin_required
def admin_dashboard():
    return render_template('admin_dashboard.html')

# 获取用户列表
@bp.route('/users', methods=['GET'])
@admin_required
def get_users():
    # 获取查询参数
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status')
    search = request.args.get('search', '')
    
    # 构建查询
    query = User.query
    
    # 按状态筛选
    if status:
        query = query.filter_by(status=status)
    
    # 搜索用户名或邮箱
    if search:
        search = f'%{search}%'
        query = query.filter(
            (User.username.like(search)) | (User.email.like(search))
        )
    
    # 分页查询
    pagination = query.order_by(User.created_at.desc()).paginate(page=page, per_page=per_page)
    users = pagination.items
    
    # 格式化结果
    result = {
        'users': [user.to_dict() for user in users],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page
    }
    
    return jsonify(result), 200

# 获取评论列表
@bp.route('/comments', methods=['GET'])
@admin_required
def get_comments():
    # 获取查询参数
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status')
    search = request.args.get('search', '')
    
    # 构建查询
    query = Comment.query
    
    # 按状态筛选
    if status:
        query = query.filter_by(status=status)
    
    # 搜索评论内容
    if search:
        query = query.filter(Comment.content.like(f'%{search}%'))
    
    # 分页查询
    pagination = query.order_by(Comment.created_at.desc()).paginate(page=page, per_page=per_page)
    comments = pagination.items
    
    # 格式化结果
    result = {
        'comments': [comment.to_dict() for comment in comments],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page
    }
    
    return jsonify(result), 200

# 批准评论
@bp.route('/comments/<int:comment_id>/approve', methods=['PUT'])
@admin_required
def approve_comment(comment_id):
    # 查找评论
    comment = Comment.query.get_or_404(comment_id)
    
    # 更新评论状态为已批准
    comment.status = 'approved'
    db.session.commit()
    
    return jsonify({'message': '评论已批准'}), 200

# 驳回评论
@bp.route('/comments/<int:comment_id>/reject', methods=['PUT'])
@admin_required
def reject_comment(comment_id):
    # 查找评论
    comment = Comment.query.get_or_404(comment_id)
    
    # 更新评论状态为待审核
    comment.status = 'pending'
    db.session.commit()
    
    return jsonify({'message': '评论已驳回'}), 200

# 获取统计数据
@bp.route('/stats', methods=['GET'])
@admin_required
def get_stats():
    try:
        # 获取最近7天的用户增长数据
        today = datetime.now()
        user_growth_data = []
        comment_activity_data = []
        
        for i in range(7):
            date = today - timedelta(days=i)
            date_str = date.strftime('%Y-%m-%d')
            
            # 计算当天注册的用户数
            users_count = User.query.filter(
                User.created_at >= datetime.combine(date, datetime.min.time()),
                User.created_at < datetime.combine(date + timedelta(days=1), datetime.min.time())
            ).count()
            
            # 计算当天发布的评论数
            comments_count = Comment.query.filter(
                Comment.created_at >= datetime.combine(date, datetime.min.time()),
                Comment.created_at < datetime.combine(date + timedelta(days=1), datetime.min.time())
            ).count()
            
            user_growth_data.append({
                'date': date_str,
                'count': users_count
            })
            
            comment_activity_data.append({
                'date': date_str,
                'count': comments_count
            })
        
        # 反转数据顺序，使最早的日期在前
        user_growth_data.reverse()
        comment_activity_data.reverse()
        
        # 返回统计数据
        return jsonify({
            'user_growth': user_growth_data,
            'comment_activity': comment_activity_data
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 删除评论
@bp.route('/comments/<int:comment_id>', methods=['DELETE'])
@admin_required
def delete_comment(comment_id):
    # 查找评论
    comment = Comment.query.get_or_404(comment_id)
    
    # 删除评论
    db.session.delete(comment)
    db.session.commit()
    
    return jsonify({'message': '评论已删除'}), 200

# 删除评论
@bp.route('/comments/batch-delete', methods=['POST'])
@admin_required
def batch_delete_comments():
    data = request.get_json()
    if not data or 'ids' not in data:
        return jsonify({'error': '请提供要删除的评论ID列表'}), 400
    
    # 查找并删除评论
    comments = Comment.query.filter(Comment.id.in_(data['ids'])).all()
    for comment in comments:
        db.session.delete(comment)
    db.session.commit()
    
    return jsonify({'message': f'成功删除{len(comments)}条评论'}), 200

# 获取所有话题（包括待审核和已屏蔽的）
@bp.route('/topics/all', methods=['GET'])
@admin_required
def get_all_topics():
    # 获取查询参数
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status')
    search = request.args.get('search', '')
    
    # 构建查询
    query = Topic.query
    
    # 按状态筛选
    if status:
        query = query.filter_by(status=status)
    
    # 搜索话题标题或内容
    if search:
        search = f'%{search}%'
        query = query.filter(
            (Topic.title.like(search)) | (Topic.content.like(search))
        )
    
    # 分页查询
    pagination = query.order_by(Topic.created_at.desc()).paginate(page=page, per_page=per_page)
    topics = pagination.items
    
    # 格式化结果
    result = {
        'topics': [topic.to_dict() for topic in topics],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page
    }
    
    return jsonify(result), 200

# 更新话题状态
@bp.route('/topics/<int:topic_id>/status', methods=['PUT'])
@admin_required
def update_topic_status(topic_id):
    # 查找话题
    topic = Topic.query.get_or_404(topic_id)
    
    data = request.get_json()
    if not data or 'status' not in data:
        return jsonify({'error': '请提供新的话题状态'}), 400
    
    # 更新状态
    topic.status = data['status']
    db.session.commit()
    
    return jsonify({'message': '话题状态已更新', 'topic': topic.to_dict()}), 200

# 删除话题
@bp.route('/topics/<int:topic_id>', methods=['DELETE'])
@admin_required
def delete_topic(topic_id):
    # 查找话题
    topic = Topic.query.get_or_404(topic_id)
    
    # 删除话题（会级联删除相关评论）
    db.session.delete(topic)
    db.session.commit()
    
    return jsonify({'message': '话题已删除'}), 200

# 更新用户状态
@bp.route('/users/<int:user_id>/status', methods=['PUT'])
@admin_required
def update_user_status(user_id):
    # 查找用户
    user = User.query.get_or_404(user_id)
    
    # 不能修改自己的状态
    if user.id == current_user.id:
        return jsonify({'error': '不能修改自己的状态'}), 400
    
    data = request.get_json()
    if not data or 'status' not in data:
        return jsonify({'error': '请提供新的用户状态'}), 400
    
    # 更新状态
    user.status = data['status']
    db.session.commit()
    
    return jsonify({'message': '用户状态已更新', 'user': user.to_dict()}), 200