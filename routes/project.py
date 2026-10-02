# routes/project.py
from datetime import datetime, date
from multiprocessing.spawn import set_executable
from tkinter.font import names

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import login_required, current_user
from sqlalchemy import distinct, or_
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from io import BytesIO
from openpyxl import Workbook
from flask import send_file

from database import db
from models import Project, UploadFile, User
from config import MATERIAL_ALL
# from utils import get_file_size

project_bp = Blueprint('project', __name__)

# 项目列表首页
@project_bp.route("/")
@login_required
def index():
    keyword = request.args.get("search", "").strip()
    page = max(1, request.args.get("page", 1, type=int))
    page_size = request.args.get("page_size", 10, type=int)
    if page_size not in (10, 20, 50):
        page_size = 10

    query = get_visible_project_query()
    if keyword:
        pattern = f"%{keyword}%"
        query = query.filter(
            or_(
                Project.name.ilike(pattern),
                Project.pid.ilike(pattern),
                Project.proj_manager.ilike(pattern)
            )
        )

    pagination = query.order_by(Project.id.desc()).paginate(
        page=page,
        per_page=page_size,
        error_out=True,
    )

    return render_template(
        "index.html",
        pagination=pagination,
        total_count=pagination.total,
        keyword=keyword,
        page_size=page_size,
    )

# 新建项目
@project_bp.route("/proj/add", methods=["POST"])
@login_required
def add_proj():
    pid = request.form.get("pid")
    name = request.form.get("name")
    proj_manager = request.form.get("proj_manager")
    module = current_user.module
    start_date_text = request.form.get("start_date")
    end_date_text = request.form.get("end_date")

    if not all([
        pid,
        name,
        proj_manager,
        module,
        start_date_text,
        end_date_text
    ]):
        flash("必填信息为空，请输入所有信息后重试")
        return redirect(url_for("project.index"))

    # 从字符串转换为日期
    try:
        start_date = datetime.strptime(start_date_text, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_text, "%Y-%m-%d").date()
    except ValueError:
        flash("无效日期")
        return redirect(url_for("project.index"))

    if end_date < start_date:
        flash("项目结束日期不能早于开始日期")
        return redirect(url_for("project.index"))

    project = Project(
        pid=pid,
        name=name,
        proj_manager=proj_manager,
        start_date=start_date,
        end_date=end_date,
        module=module,
    )

    project.members.append(current_user)

    try:
        db.session.add(project)
        db.session.commit()
        flash("项目创建成功")
    except IntegrityError:
        db.session.rollback()
        flash("项目编号或名称已存在，请修改后提交")

    return redirect(url_for("project.index"))

# 项目详情页
@project_bp.route("/proj/<int:pid>")
@login_required
def proj_detail(pid):
    query = get_visible_project_query()
    result = query.filter(
        Project.id == pid
    ).first_or_404()

    files = UploadFile.query.filter(
        UploadFile.proj_id == pid,
        UploadFile.is_deleted == False
    ).all()

    available_users = User.query.filter(
        User.module == result.module
    ).all()

    deleted_files = UploadFile.query.filter(
        UploadFile.is_deleted == True,
        UploadFile.proj_id == pid
    ).all()

    return render_template(
        "detail.html",
        project=result,
        files=files,
        available_users=available_users,
        materials=MATERIAL_ALL,
        deleted_files=deleted_files
    )



@project_bp.route("/api/all_users", methods=["GET"])
@login_required
def api_get_all_users():
    pass

# 项目编辑页面
@project_bp.route("/proj/edit/<int:pid>", methods=["POST"])
@login_required
def edit_proj(pid):
    query = get_visible_project_query()
    project = query.filter(
        Project.id == pid
    ).first_or_404()

    #修改项目成员逻辑
    if not(current_user.name == project.proj_manager or current_user.role == "主管"):
        abort(403)

    new_pid = request.form.get("pid")
    new_name = request.form.get("name")
    new_proj_manager = request.form.get("proj_manager")
    new_start_date_str = request.form.get("start_date")
    new_end_date_str = request.form.get("end_date")
    member_ids = request.form.getlist("member_ids")

    try:
        for i in range(len(member_ids)):
            member_ids[i] = int(member_ids[i])
    except ValueError:
        abort(400)

    selected_users = User.query.filter(
        User.id.in_(member_ids),
        User.module == project.module
    ).all()

    selected_ids = set()
    for i in selected_users:
        selected_ids.add(i.id)

    if selected_ids != set(member_ids):
        abort(400)

    if "members_submitted" in request.form:
        project.members = selected_users

    if not any([
        new_pid,
        new_name,
        new_proj_manager,
        new_end_date_str,
        new_start_date_str,
        request.form.get("members_submitted")
    ]):
        flash("更新信息为空，请输入后重试")
        return redirect(url_for("project.proj_detail", pid=pid))
    start_date = project.start_date
    end_date = project.end_date
    if new_start_date_str:
        try:
            start_date = datetime.strptime(new_start_date_str, "%Y-%m-%d").date()
        except ValueError:
            flash("请输入有效日期")
            return redirect(url_for("project.proj_detail", pid=pid))
    if new_end_date_str:
        try:
            end_date = datetime.strptime(new_end_date_str, "%Y-%m-%d").date()
        except ValueError:
            flash("请输入有效日期")
            return redirect(url_for("project.proj_detail", pid=pid))
    if start_date > end_date:
        flash("项目结束日期不能早于开始日期")
        return redirect(url_for("project.proj_detail", pid=pid))

    if new_pid:
        project.pid = new_pid
    if new_name:
        project.name = new_name
    if new_proj_manager:
        project.proj_manager = new_proj_manager
    if start_date:
        project.start_date = start_date
    if end_date:
        project.end_date = end_date
    try:
        db.session.commit()
        flash("修改成功")
    except IntegrityError:
        flash("目前项目编号或者名称已存在，请更换")
        db.session.rollback()
        return redirect(url_for("project.proj_detail", pid=pid))

    return redirect(url_for("project.proj_detail", pid=pid))

# 删除项目接口
@project_bp.route("/proj/del/<int:pid>", methods=["POST"])
@login_required
def del_project(pid):
    query = get_visible_project_query()
    project = query.filter(Project.id == pid).first_or_404()
    can_delete = False
    if current_user.name == project.proj_manager or current_user.role == "主管":
        can_delete = True
    if can_delete:
        project.is_deleted = can_delete
    else:
        flash("无权删除项目")
        return redirect(url_for("project.proj_detail", pid=pid))
    try:
        db.session.commit()
        flash("删除成功")
    except SQLAlchemyError:
        db.session.rollback()
        flash("删除失败")
        return  redirect(url_for("project.proj_detail", pid=pid))
    return redirect(url_for("project.index"))

# 导出全部项目基础信息Excel
@project_bp.route("/export/all_project", methods=["GET"])
@login_required
def export_all_project():
    pass

def get_visible_project_query():
    query = Project.query.filter(Project.is_deleted.is_(False))
    if current_user.role == "主管":
        query = query.filter(
            Project.module==current_user.module
        )
    elif current_user.role == "普通用户":
        query = query.filter(
        or_
            (Project.proj_manager == current_user.name,
            Project.members.any(User.id == current_user.id))
        )
    return query
