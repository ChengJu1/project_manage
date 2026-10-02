from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.testing.provision import run_reap_dbs
from uuid import uuid4
from flask import abort

from models import User, RegisterCode
from database import db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)


# 登录页
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and user.check_pwd(password):
            login_user(user)
            next_page = request.args.get("next")
            if next_page:
                return redirect(next_page)
            return redirect(url_for("project.index"))
        flash("用户名或密码错误")

    return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        module = request.form["module"]
        name = request.form["name"]
        code = request.form.get("company_code")
        if request.args.get("role") == "主管":
            register_code = RegisterCode.query.filter(
                RegisterCode.code == code
            ).first()
            if not register_code:
                flash("注册失败：输入的邀请码不存在，请重新输入")
                return redirect(url_for("auth.register", role="主管"))
            elif register_code.assigned_username != username:
                flash("注册失败：非当前邀请码指定用户")
                return redirect(url_for("auth.register", role="主管"))
            elif register_code.is_used:
                flash("注册失败，此验证码已被使用")
                return redirect(url_for("auth.register", role="主管"))
            user = User(
                name = name,
                username = username,
                password = generate_password_hash(password),
                module = module,
                role = "主管"
            )
            try:
                register_code.is_used = True
                db.session.add(user)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                flash("注册失败，用户名重复")
                return redirect(url_for("auth.register", role="主管"))
            flash("注册成功")
            return redirect(url_for("auth.login"))

        try:
            if request.args.get("role") == "普通用户":
                user = User(
                    name=name,
                    username=username,
                    password=generate_password_hash(password),
                    module=module,
                    role="普通用户"
                )
                db.session.add(user)
                db.session.commit()
        except IntegrityError:
            flash("用户名重复，请修改")
            db.session.rollback()
            return redirect(url_for("auth.register", role="普通用户"))
        flash("注册成功，请返回登录")
        return redirect(url_for("auth.login"))
    return render_template("register.html")

@auth_bp.route("/generate_code", methods=["GET", "POST"])
@login_required
def generate_code():
    if current_user.username != "admin":
        abort(403)
    if request.method == "POST":
        code = str(uuid4())
        assigned_username = request.form.get("assigned_username")
        new_code = RegisterCode(
            code=code,
            assigned_username=assigned_username
        )
        try:
            db.session.add(new_code)
            db.session.commit()
        except IntegrityError:
            flash(f"{assigned_username}已被分配过一次激活码")
            db.session.rollback()
            return redirect(url_for("auth.generate_code"))
        flash(f"已生成邀请码，请在当前页面复制，仅显示一次，邀请码为： \n{code}")
    return render_template("generate_code.html")


# 登出
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("已成功退出登录")
    return redirect(url_for("auth.login"))


# 修改当前登录用户密码弹窗提交接口
@auth_bp.route("/users/<int:user_id>/password", methods=["POST"])
@login_required
def change_pwd(user_id):
    user = User.query.get(user_id)
    old_pwd = request.form.get("old_pwd")
    new_pwd = request.form.get("new_pwd")
    confirm_pwd = request.form.get("confirm_pwd")
    if not old_pwd or not new_pwd or not confirm_pwd:
        flash("输入框不能为空")
        pid = request.form.get("pid")
        if pid:
            return redirect(url_for("project.proj_detail", pid=pid))
        return redirect(url_for("project.index"))
    if new_pwd != confirm_pwd:
        flash("确认密码与新密码不匹配")
        pid = request.form.get("pid")
        if pid:
            return redirect(url_for("project.proj_detail", pid=pid))
        return redirect(url_for("project.index"))
    if not check_password_hash(user.password, old_pwd):
        flash("原密码验证失败")
        pid = request.form.get("pid")
        if pid:
            return redirect(url_for("project.proj_detail", pid=pid))
        return redirect(url_for("project.index"))
    password = generate_password_hash(new_pwd)
    user.password = password
    db.session.commit()
    flash("密码修改成功请重新登录")
    logout_user()
    return redirect(url_for("auth.login"))

