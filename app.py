import os
from pathlib import Path
from flask import Flask, render_template
from database import db, login_manager
# 导入所有拆分后的蓝图
from routes import all_bps
# from utils import format_money, calc_progress

app = Flask(__name__)
app.config['SECRET_KEY'] = 'proj-manage-secret-2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = str(Path(__file__).resolve().parent / "uploads")
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "auth.login"  # 蓝图名称变更：auth.login
login_manager.login_message = "请先登录系统"

# 循环注册所有拆分蓝图
for bp in all_bps:
    app.register_blueprint(bp)

# 注册模板过滤器
# app.add_template_filter(format_money, 'format_money')
# app.add_template_filter(calc_progress, 'calc_progress')

# 初始化数据库与账号
with app.app_context():
    from models import User
    db.create_all()
    if User.query.count() == 0:
        u = User(username="admin", name="admin", module="教师组", role="主管")
        u.set_pwd("admin@456")
        db.session.add_all([u])
        db.session.commit()
        print("检测当前用户数量为空，已创建1个登录账号！")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
