from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import os
from dotenv import load_dotenv
from config import config
from models.db import db

# 加载环境变量
load_dotenv()

# 初始化扩展
csrf = CSRFProtect()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

# 用户加载器
@login_manager.user_loader
def load_user(user_id):
    from models.user import User
    return User.query.get(int(user_id))

# 创建Flask应用
def create_app(config_name):
    app = Flask(__name__)
    
    # 配置应用
    app.config.from_object(config[config_name])
    
    # 配置全面的CORS支持
    # 注意：当withCredentials为true时，origins不能包含通配符*，必须是具体的源
    CORS(app, 
         resources={r"/api/*": {
             "origins": ["http://localhost:5173", "http://localhost:5174"],
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             "allow_headers": ["Content-Type", "Authorization", "X-Requested-With", "x-tab-id"],
             "expose_headers": ["Content-Type", "Authorization"],
             "supports_credentials": True,
             "max_age": 86400  # 24小时缓存预检请求
         }})

    # 确保OPTIONS请求得到正确处理
    @app.after_request
    def after_request(response):
        # 动态设置Access-Control-Allow-Origin头
        # 从请求头中获取Origin，只允许指定的源
        allowed_origins = ["http://localhost:5173", "http://localhost:5174"]
        origin = request.headers.get('Origin')
        if origin in allowed_origins:
            response.headers['Access-Control-Allow-Origin'] = origin
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,X-Requested-With,x-tab-id')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
    
    # 初始化扩展
    csrf.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # 导入路由
    from routes.auth import bp as auth_bp
    from routes.admin import bp as admin_bp
    from routes.forum import bp as forum_bp
    
    # 注册蓝图
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(forum_bp, url_prefix='/api/forum')
    
    # 主页路由
    @app.route('/')
    def index():
        return jsonify({'message': 'Welcome to the Community Forum API'}), 200
    
    # 错误处理
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500
    
    # 命令行创建数据库
    @app.cli.command("create-db")
    def create_db():
        with app.app_context():
            db.create_all()
            print("数据库已创建")
    
    # 命令行创建管理员
    @app.cli.command("create-admin")
    def create_admin():
        from models.user import User
        
        with app.app_context():
            # 检查是否已有管理员
            admin_user = User.query.filter_by(username='admin').first()
            if admin_user:
                print("管理员已存在")
                return
            
            # 创建管理员用户
            admin = User(username='admin', email='admin@example.com', is_admin=True)
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("管理员创建成功\n用户名: admin\n密码: admin123")
    
    return app

if __name__ == '__main__':
    app = create_app(os.environ.get('FLASK_ENV') or 'development')
    app.run(debug=True)