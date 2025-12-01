from flask import Blueprint, session, redirect, url_for, render_template, request, current_app
from flask_login import current_user, login_user, login_required, logout_user

from applications.common import admin as index_curd
from applications.common.admin_log import login_log, admin_log
from applications.common.utils.http import fail_api, success_api
from applications.models import User

bp = Blueprint('passport', __name__, url_prefix='/passport')


# 获取验证码
@bp.get('/getCaptcha')
def get_captcha():
    resp, code = index_curd.get_captcha()
    session["code"] = code
    return resp


# 登录
@bp.get('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('system.index'))
    return render_template('system/login.html')


# 登录
@bp.post('/login')
def login_post():
    req = request.form
    username = req.get('username')
    password = req.get('password')
    remember = bool(req.get('remember-me'))
    code = req.get('captcha').__str__().lower()

    if not username or not password or not code:
        # 记录登录失败日志（用户名为空）
        login_log(request, uid=None, is_access=False)
        return fail_api(msg="用户名或密码没有输入")
    s_code = session.get("code", None)
    session["code"] = None

    if not all([code, s_code]):
        # 记录登录失败日志（验证码参数错误）
        login_log(request, uid=None, is_access=False)
        return fail_api(msg="参数错误")

    if code != s_code:
        # 记录登录失败日志（验证码错误）
        login_log(request, uid=None, is_access=False)
        return fail_api(msg="验证码错误")
    user = User.query.filter_by(username=username).first()

    if not user:
        # 记录登录失败日志（用户不存在）
        login_log(request, uid=None, is_access=False)
        return fail_api(msg="不存在的用户")

    if user.enable == 0:
        # 记录登录失败日志（用户被禁用）
        login_log(request, uid=user.id, is_access=False)
        return fail_api(msg="用户被暂停使用")

    if username == user.username and user.validate_password(password):
        # 登录
        login_user(user, remember=remember)
        # 记录登录成功日志
        login_log(request, uid=user.id, is_access=True)
        # 授权路由存入session
        role = current_user.role
        user_power = []
        for i in role:
            if i.enable == 0:
                continue
            for p in i.power:
                if p.enable == 0:
                    continue
                user_power.append(p.code)
        session['permissions'] = user_power
        # # 角色存入session
        # roles = []
        # for role in current_user.role.all():
        #     roles.append(role.id)
        # session['role'] = [roles]

        return success_api(msg="登录成功")
    # 记录登录失败日志（密码错误）
    login_log(request, uid=user.id, is_access=False)
    return fail_api(msg="用户名或密码错误")


# 退出登录
@bp.post('/logout')
@login_required
def logout():
    # 在退出前获取用户信息，用于记录日志
    user_id = current_user.id if current_user.is_authenticated else None
    username = current_user.username if current_user.is_authenticated else None
    
    # 清除 session 中的权限信息
    if 'permissions' in session:
        session.pop('permissions')
    
    # 清除验证码 session
    if 'code' in session:
        session.pop('code')
    
    # 清除其他可能的 session 数据
    # 如果后续有添加其他 session 数据，也应该在这里清除
    
    # 退出登录
    logout_user()
    
    # 记录退出登录日志
    try:
        admin_log(request=request, is_access=True, desc=f"用户 {username} 退出登录")
    except Exception as e:
        # 如果记录日志失败，不影响退出流程
        current_app.logger.error(f"记录退出登录日志失败: {str(e)}")
    
    return success_api(msg="注销成功")
