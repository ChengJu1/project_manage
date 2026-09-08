from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from models import User
from database import db
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
        user = User(username=username, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        return "注册成功,<a href='/login'>返回登陆</a>"
    return render_template("register.html")


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
