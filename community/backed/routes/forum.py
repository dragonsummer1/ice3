from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models.comment import Comment
from models.topic import Topic
from models.db import db
from datetime import datetime

# 创建蓝图
bp = Blueprint('forum', __name__)

# 获取话题列表
@bp.route('/topics', methods=['GET'])
def get_topics():
    # 获取查询参数
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    category = request.args.get('category', '', type=str)
    
    # 构建查询
    query = Topic.query
    if category:
        query = query.filter_by(category=category)
    
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

# 获取单个话题详情
@bp.route('/topics/<int:topic_id>', methods=['GET'])
def get_topic_detail(topic_id):
    # 查找话题
    topic = Topic.query.get_or_404(topic_id)
    
    # 增加浏览量
    topic.views += 1
    db.session.commit()
    
    # 获取已批准的评论
    approved_comments = Comment.query.filter_by(topic_id=topic_id, status='approved').order_by(Comment.created_at.asc()).all()
    comments_list = [{
        'id': comment.id,
        'content': comment.content,
        'user_id': comment.user_id,
        'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S') if comment.created_at else None,
        'author': comment.author.username if comment.author else '未知用户',
        'status': comment.status
    } for comment in approved_comments]
    
    # 返回包含评论的话题详情
    topic_data = topic.to_dict()
    topic_data['comments'] = comments_list
    
    return jsonify(topic_data), 200

# 创建新话题
@bp.route('/topics', methods=['POST'])
@login_required
def create_topic():
    data = request.get_json()
    
    # 验证数据
    required_fields = ['title', 'content', 'category']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'{field}不能为空'}), 400
    
    # 长度限制
    if len(data['title']) > 100:
        return jsonify({'error': '标题不能超过100个字符'}), 400
    if len(data['content']) > 10000:
        return jsonify({'error': '内容不能超过10000个字符'}), 400
    
    # 创建话题
    topic = Topic(
        title=data['title'],
        content=data['content'],
        category=data['category'],
        user_id=current_user.id
    )
    
    # 保存到数据库
    db.session.add(topic)
    db.session.commit()
    
    return jsonify({
        'topic': topic.to_dict(),
        'message': '话题创建成功'
    }), 201

# 更新话题
@bp.route('/topics/<int:topic_id>', methods=['PUT'])
@login_required
def update_topic(topic_id):
    # 查找话题
    topic = Topic.query.get_or_404(topic_id)
    
    # 检查权限
    if topic.user_id != current_user.id:
        return jsonify({'error': '无权限修改此话题'}), 403
    
    data = request.get_json()
    
    # 更新话题信息
    if 'title' in data and data['title']:
        if len(data['title']) > 100:
            return jsonify({'error': '标题不能超过100个字符'}), 400
        topic.title = data['title']
    
    if 'content' in data and data['content']:
        if len(data['content']) > 10000:
            return jsonify({'error': '内容不能超过10000个字符'}), 400
        topic.content = data['content']
    
    if 'category' in data and data['category']:
        topic.category = data['category']
    
    # 保存更改
    db.session.commit()
    
    return jsonify({
        'topic': topic.to_dict(),
        'message': '话题更新成功'
    }), 200

# 删除话题
@bp.route('/topics/<int:topic_id>', methods=['DELETE'])
@login_required
def delete_topic(topic_id):
    # 查找话题
    topic = Topic.query.get_or_404(topic_id)
    
    # 检查权限
    if topic.user_id != current_user.id:
        return jsonify({'error': '无权限删除此话题'}), 403
    
    # 删除话题
    db.session.delete(topic)
    db.session.commit()
    
    return jsonify({'message': '话题已删除'}), 200

# 提交话题回复
@bp.route('/topics/<int:topic_id>/replies', methods=['POST'])
@login_required
def create_topic_reply(topic_id):
    # 验证话题存在
    topic = Topic.query.get_or_404(topic_id)
    
    data = request.get_json()
    
    # 验证数据
    if not data or 'content' not in data:
        return jsonify({'error': '回复内容不能为空'}), 400
    
    # 内容长度限制
    if len(data['content']) > 2000:
        return jsonify({'error': '回复内容不能超过2000个字符'}), 400
    
    # 创建评论
    comment = Comment(
        content=data['content'],
        user_id=current_user.id,
        topic_id=topic_id,  # 设置话题ID
        status='pending'  # 默认待审核
    )
    
    # 更新话题的回复数和最后回复时间
    topic.replies += 1
    topic.last_reply_time = datetime.utcnow()
    
    # 保存到数据库
    db.session.add(comment)
    db.session.commit()
    
    return jsonify({
        'reply': comment.to_dict(),
        'message': '回复发表成功'
    }), 201

# 获取话题的回复列表
@bp.route('/topics/<int:topic_id>/replies', methods=['GET'])
def get_topic_replies(topic_id):
    # 验证话题存在
    Topic.query.get_or_404(topic_id)
    
    # 获取回复列表 - 只获取该话题的评论
    comments = Comment.query.filter_by(topic_id=topic_id, status='approved').order_by(Comment.created_at.asc()).all()
    
    return jsonify([comment.to_dict() for comment in comments]), 200

# 获取评论列表（普通用户可访问）
@bp.route('/comments', methods=['GET'])
def get_public_comments():
    # 获取查询参数
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # 只查询已批准的评论
    pagination = Comment.query.filter_by(status='approved')
    pagination = pagination.order_by(Comment.created_at.desc()).paginate(page=page, per_page=per_page)
    comments = pagination.items
    
    # 格式化结果
    result = {
        'comments': [comment.to_dict() for comment in comments],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page
    }
    
    return jsonify(result), 200

# 发表评论
@bp.route('/comments', methods=['POST'])
@login_required
def create_comment():
    data = request.get_json()
    
    # 验证数据
    if not data or 'content' not in data:
        return jsonify({'error': '评论内容不能为空'}), 400
    
    # 内容长度限制
    if len(data['content']) > 2000:
        return jsonify({'error': '评论内容不能超过2000个字符'}), 400
    
    # 创建评论
    comment = Comment(
        content=data['content'],
        user_id=current_user.id,
        status='pending'  # 默认待审核
    )
    
    # 保存到数据库
    db.session.add(comment)
    db.session.commit()
    
    return jsonify({
        'comment': comment.to_dict(),
        'message': '评论发表成功'
    }), 201

# 删除自己的评论
@bp.route('/comments/<int:comment_id>', methods=['DELETE'])
@login_required
def delete_own_comment(comment_id):
    # 查找评论
    comment = Comment.query.get_or_404(comment_id)
    
    # 检查权限：只能删除自己的评论
    if comment.user_id != current_user.id and not current_user.is_admin_user():
        return jsonify({'error': '无权限删除此评论'}), 403
    
    # 删除评论
    db.session.delete(comment)
    db.session.commit()
    
    return jsonify({'message': '评论已删除'}), 200

# 获取用户自己的评论
@bp.route('/my-comments', methods=['GET'])
@login_required
def get_my_comments():
    # 获取查询参数
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # 查询当前用户的所有评论
    pagination = Comment.query.filter_by(user_id=current_user.id)
    pagination = pagination.order_by(Comment.created_at.desc()).paginate(page=page, per_page=per_page)
    comments = pagination.items
    
    # 格式化结果
    result = {
        'comments': [comment.to_dict() for comment in comments],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page
    }
    
    return jsonify(result), 200