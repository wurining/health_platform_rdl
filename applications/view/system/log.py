from flask import Blueprint, request, render_template
from sqlalchemy import desc
from applications.common.utils.http import table_api
from applications.common.utils.rights import authorize
from applications.models import AdminLog
from applications.schemas import LogOutSchema
from applications.common.curd import model_to_dicts

bp = Blueprint('log', __name__, url_prefix='/log')


# 日志管理
@bp.get('/')
@authorize("system:log:main")
def index():
    return render_template('system/admin_log/main.html')


# 登录日志
@bp.get('/loginLog')
@authorize("system:log:main")
def login_log():
    """
    查询登录日志
    严格限制：只查询URL为 /passport/login 的日志记录
    """
    # 获取查询参数
    username = request.args.get('username', type=str)
    ip = request.args.get('ip', type=str)
    success = request.args.get('success', type=str)
    
    # 构建查询 - 严格限制：只查询登录URL
    query = AdminLog.query.filter(AdminLog.url == '/passport/login')
    
    # 添加过滤条件
    if username:
        query = query.filter(AdminLog.username.like(f'%{username}%'))
    if ip:
        query = query.filter(AdminLog.ip.like(f'%{ip}%'))
    if success:
        success_val = 1 if success == '1' else 0
        query = query.filter(AdminLog.success == success_val)
    
    # 排序和分页
    log = query.order_by(desc(AdminLog.create_time)).layui_paginate()
    count = log.total
    return table_api(data=model_to_dicts(schema=LogOutSchema, data=log.items), count=count)


# 操作日志
@bp.get('/operateLog')
@authorize("system:log:main")
def operate_log():
    """
    查询操作日志
    严格限制：排除所有登录相关的日志（URL为 /passport/login 的记录）
    """
    # 获取查询参数
    username = request.args.get('username', type=str)
    url = request.args.get('url', type=str)
    module_name = request.args.get('module_name', type=str)
    operation_type = request.args.get('operation_type', type=str)
    success = request.args.get('success', type=str)
    
    # 构建查询 - 严格排除登录URL
    query = AdminLog.query.filter(AdminLog.url != '/passport/login')
    
    # 添加过滤条件
    if username:
        query = query.filter(AdminLog.username.like(f'%{username}%'))
    if url:
        query = query.filter(AdminLog.url.like(f'%{url}%'))
    if module_name:
        query = query.filter(AdminLog.module_name.like(f'%{module_name}%'))
    if operation_type:
        query = query.filter(AdminLog.operation_type.like(f'%{operation_type}%'))
    if success:
        success_val = 1 if success == '1' else 0
        query = query.filter(AdminLog.success == success_val)
    
    # 排序和分页
    log = query.order_by(desc(AdminLog.create_time)).layui_paginate()
    count = log.total
    return table_api(data=model_to_dicts(schema=LogOutSchema, data=log.items), count=count)
