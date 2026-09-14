from email.policy import default
from tokenize import String

from flask_login import UserMixin
from sqlalchemy import null, Nullable, Integer
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
# from datetime import datetime
# from zoneinfo import ZoneInfo
#
# from project_manage.routes.project import proj_detail

project_members = db.Table(
    "project_members",
    db.Column("user_id",
              db.Integer,
              db.ForeignKey("user.id")),
    db.Column("project_id",
              db.Integer,
              db.ForeignKey("project.id")),
)

# 用户表
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    role = db.Column(db.String(64), nullable=False)
    module = db.Column(db.String(64), nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def set_pwd(self, pwd):
        self.password = generate_password_hash(pwd, method="pbkdf2:sha256")

    def check_pwd(self, pwd):
        return check_password_hash(self.password, pwd)

# 项目表
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.String(64), nullable=False, unique=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    proj_manager = db.Column(db.String(64), nullable=False)
    start_date = db.Column(db.Date(), nullable = False, comment="项目开始时间")
    end_date = db.Column(db.Date(), nullable = False, comment="项目结束时间")
    module = db.Column(db.String(64), nullable=False, comment="项目所在部门")
    is_deleted = db.Column(db.Boolean(), nullable=False, default = False, comment="是否被删除")
    members = db.relationship("User", secondary=project_members)

# 文件上传记录表
class UploadFile(db.Model):
    fid = db.Column(db.Integer(), primary_key=True)
    file_name = db.Column(db.String(64), nullable=False)
    standard_name = db.Column(db.String(64), unique=True, nullable=False)
    uploaded_by = db.Column(db.String(64), nullable=False)
    proj_id = db.Column(db.Integer(), db.ForeignKey("project.id"), nullable=False)
    is_deleted = db.Column(db.Boolean(), default=False, nullable=False)
