# routes/__init__.py
from .auth import auth_bp
from .project import project_bp
from .file import file_bp

# 统一导出，供app.py注册
all_bps = [auth_bp, project_bp, file_bp]