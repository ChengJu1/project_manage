# routes/project.py
from datetime import datetime, date
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy import distinct, or_
from io import BytesIO
from openpyxl import Workbook
from flask import send_file

from database import db
from models import Project, UploadFile, User
# from config import MATERIAL_ALL, CATEGORY_ORDER
# from utils import get_file_size

project_bp = Blueprint('project', __name__)

# 项目列表首页
@project_bp.route("/")
@login_required
def index():
    if Project.is_deleted == False:
        if User.role == "管理员":
            seen_project = 
    return render_template("index.html")

# 新建项目
@project_bp.route("/proj/add", methods=["POST"])
@login_required
def add_proj():
    pass

# 项目详情页
@project_bp.route("/proj/<int:pid>")
@login_required
def proj_detail(pid):
    pass

@project_bp.route("/api/all_users", methods=["GET"])
@login_required
def api_get_all_users():
    pass

# 项目编辑页面
@project_bp.route("/proj/edit/<int:pid>", methods=["GET", "POST"])
@login_required
def edit_proj(pid):
    pass

# 删除项目接口
@project_bp.route("/proj/del/<int:pid>", methods=["POST"])
@login_required
def del_project(pid):
    pass

# 导出全部项目基础信息Excel
@project_bp.route("/export/all_project", methods=["GET"])
@login_required
def export_all_project():
    pass
