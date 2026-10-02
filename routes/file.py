# routes/file.py
import os
from flask import Response
import mimetypes
import zipfile
import tempfile
from io import BytesIO


from flask import Blueprint, request, redirect, url_for, flash, send_from_directory, abort, send_file
from flask_login import login_required, current_user
from pathlib import Path
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError

from database import db
from models import UploadFile, Project
from config import MATERIAL_ALL
from models import Project
from routes.project import get_visible_project_query
from datetime import datetime
from uuid import uuid4

file_bp = Blueprint('file', __name__)

# 文件上传
@file_bp.route("/upload/<int:pid>/<mat_key>", methods=["POST"])
@login_required
def upload_file(pid, mat_key):
    project = (
        get_visible_project_query()
       .filter(Project.id == pid)
       .first_or_404()
   )

    material = MATERIAL_ALL.get(mat_key)
    if material is None:
        abort(400, description="无效项目材料")
    detail_url = url_for("project.proj_detail", pid=pid, _anchor=f"material-{mat_key}")

    files = request.files.getlist("file")

    if not files or any(not file.filename for file in files):
        flash("请先选择文件")
        return redirect(detail_url)

    checked_files = []

    for file in files:
        original_name = file.filename.replace("\\", "/").split("/")[-1]

        if "." not in original_name:
            flash(f"{original_name} 没有文件后缀")
            return redirect(detail_url)

        ext = original_name.rsplit(".", 1)[-1].lower()

        if ext not in material["ext"]:
            flash(f"{original_name} 的格式不允许上传")
            return redirect(detail_url)

        uploaded_at = datetime.now()
        timestamp = uploaded_at.strftime("%Y%m%d%H%M%S%f")
        random_part = uuid4().hex[:8]

        standard_name = (
            f"{project.id}_{mat_key}_{timestamp}_{random_part}.{ext}"
        )

        checked_files.append((file, original_name, standard_name, uploaded_at))

    project_dir = Path(current_app.config["UPLOAD_FOLDER"]) / str(project.id)
    saved_paths = []

    try:
        project_dir.mkdir(parents=True, exist_ok=True)

        for file, original_name, standard_name, uploaded_at in checked_files:
            target_path = project_dir / standard_name

            saved_paths.append(target_path)
            file.save(target_path)

            record = UploadFile(
                file_name=original_name,
                standard_name=standard_name,
                uploaded_by=current_user.username,
                proj_id=project.id,
                uploaded_time=uploaded_at,
                is_deleted=False,
                mat_key=mat_key
            )
            db.session.add(record)

        db.session.commit()

    except (OSError, SQLAlchemyError):
        db.session.rollback()

        for path in saved_paths:
            path.unlink(missing_ok=True)

        current_app.logger.exception("文件上传失败")
        flash("上传失败，请重试")
        return redirect(detail_url)

    flash(f"成功上传 {len(checked_files)} 个文件")
    return redirect(detail_url)

@file_bp.route("/file_recovery/<int:pid>/<int:fid>", methods=["POST"])
@login_required
def del_recovery(fid, pid):
    del_files = UploadFile.query.filter(
        UploadFile.proj_id == pid,
        UploadFile.fid == fid,
        UploadFile.is_deleted == True
    ).first_or_404()

    project = get_visible_project_query().filter(
        Project.id == del_files.proj_id
    ).first_or_404()

    if not (current_user.name == project.proj_manager or current_user in project.members):
        abort(403)

    root = Path(current_app.config["UPLOAD_FOLDER"])
    path = root / str(del_files.proj_id) / str(del_files.standard_name)

    if not path.is_file():
        abort(404)

    try:
        del_files.is_deleted = False
        del_files.deleted_time = None
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        flash("恢复失败")
        return redirect(url_for("project.proj_detail", pid=pid, _anchor="material-recycle"))
    flash("文件恢复成功")

    return redirect(url_for("project.proj_detail", pid=pid, _anchor=f"material-{del_files.mat_key}"))


# 单文件下载
@file_bp.route("/download/<int:fid>")
@login_required
def download(fid):
    record = UploadFile.query.filter(
        UploadFile.fid == fid
    ).first_or_404()

    projects = get_visible_project_query().filter(
        record.proj_id == Project.id
    ).first_or_404()

    if record.is_deleted: # 如果is_deleted是True
        abort(404)

    root = Path(current_app.config["UPLOAD_FOLDER"])
    target_path = root/str(record.proj_id)/str(record.standard_name)

    if not target_path.is_file():
        abort(404)

    return  send_file(
        target_path,
        as_attachment=True,
        download_name=record.file_name
    )
# 删除单个文件
@file_bp.route("/file/del/<int:fid>/<int:pid>", methods=["POST"])
@login_required
def del_file(fid, pid):
    file = UploadFile.query.filter(
        UploadFile.proj_id == pid,
        UploadFile.fid == fid
    ).first_or_404()

    project = get_visible_project_query().filter(
                Project.id == file.proj_id
                ).first_or_404()

    is_manager = current_user.name == project.proj_manager
    is_member = current_user in project.members

    if not (is_member or is_manager):
        abort(403)

    if is_manager or is_member:
        file.is_deleted = True
        file.deleted_time = datetime.now()
    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        flash("文件删除失败，请重试")

    return redirect(url_for("project.proj_detail", pid=pid), )


# 项目打包ZIP下载
@file_bp.route("/proj/zip/<int:pid>")
@login_required
def download_proj_zip(pid):
    project = get_visible_project_query().filter(
        Project.id == pid
    ).first_or_404()

    can_zip = UploadFile.query.filter(
        UploadFile.proj_id == pid,
        UploadFile.is_deleted == False
    ).all()

    if not can_zip:
        abort(404)

    root = Path(current_app.config["UPLOAD_FOLDER"])
    target_path_list = []

    for file in can_zip:
        target_path = root/str(file.proj_id)/str(file.standard_name)
        if not target_path.is_file():
            abort(404)
        target_path_list.append((target_path, file))

    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", compression=zipfile.ZIP_DEFLATED) as zip_file:
        for path, file in target_path_list:
            time_text = file.uploaded_time.strftime("%Y%m%d_%H%M%S")
            zip_file.write(path, arcname=f"{project.name}_{time_text}_{file.fid}_{file.file_name}")
            # 例如：磁盘文件 12_general_...pdf，在 ZIP 中显示 项目名_20261001_131124_7_报告.pdf。
    zip_buffer.seek(0)

    return send_file(
        zip_buffer,
        as_attachment=True,
        download_name=f"{project.name}.zip",
        mimetype="application/zip"
    )

# 文件在线预览接口
@file_bp.route("/preview/<int:fid>")
@login_required
def preview_file(fid):
    record = UploadFile.query.filter(
        UploadFile.fid == fid,
        UploadFile.is_deleted == False
    ).first_or_404()

    seen_file = get_visible_project_query().filter(
        Project.id == record.proj_id
    ).first_or_404()

    root = Path(current_app.config["UPLOAD_FOLDER"])
    file_path = root/str(record.proj_id)/record.standard_name

    if not file_path.is_file():
        abort(404)

    suffix = Path(record.standard_name).suffix.lower()
    allowed_suffix = {".pdf", ".png", ".jpg", ".jpeg"}

    if suffix not in allowed_suffix:
        abort(404)

    return send_file(
        file_path,
        as_attachment=False
    )
