# routes/file.py
# import os
# from flask import Response
# import mimetypes
# import zipfile
# import tempfile
# from datetime import datetime
from flask import Blueprint, request, redirect, url_for, flash, send_from_directory
from flask_login import login_required, current_user
# from database import db
# from models import UploadFile, Project
# from config import UPLOAD_FOLDER, MATERIAL_ALL

file_bp = Blueprint('file', __name__)

# 文件上传
@file_bp.route("/upload/<int:pid>/<mat_key>", methods=["POST"])
@login_required
def upload_file(pid, mat_key):
    pass

# 单文件下载
@file_bp.route("/download/<int:fid>")
@login_required
def download(fid):
    pass

# 删除单个文件
@file_bp.route("/file/del/<int:fid>/<int:pid>")
@login_required
def del_file(fid, pid):
    pass

# 项目打包ZIP下载
@file_bp.route("/proj/zip/<int:pid>")
@login_required
def download_proj_zip(pid):
    pass


# 文件在线预览接口
@file_bp.route("/preview/<int:fid>")
@login_required
def preview_file(fid):
    pass