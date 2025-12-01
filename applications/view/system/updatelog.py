from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user

from applications.common import curd
from applications.common.helper import ModelFilter
from applications.common.utils.http import table_api, success_api, fail_api
from applications.common.utils.rights import authorize
from applications.common.utils.validate import str_escape
from applications.extensions import db
from applications.models import UpdateLog
from applications.schemas import UpdateLogOutSchema

bp = Blueprint('updatelog', __name__, url_prefix='/updatelog')


# 更新记录管理
@bp.get('/')
@authorize("system:updatelog:main")
def main():
    return render_template('system/updatelog/main.html')


# 获取更新记录列表数据
@bp.get('/data')
@authorize("system:updatelog:main")
def data():
    # 获取请求参数
    title = str_escape(request.args.get('title', type=str))
    version = str_escape(request.args.get('version', type=str))
    update_type = str_escape(request.args.get('updateType', type=str))
    
    # 查询参数构造
    mf = ModelFilter()
    if title:
        mf.vague(field_name="title", value=title)
    if version:
        mf.vague(field_name="version", value=version)
    if update_type:
        mf.exact(field_name="update_type", value=update_type)
    
    # orm查询
    updatelog_all = UpdateLog.query.filter(mf.get_filter(UpdateLog)).order_by(UpdateLog.create_time.desc()).layui_paginate()
    count = updatelog_all.total
    data = curd.model_to_dicts(schema=UpdateLogOutSchema, data=updatelog_all.items)
    return table_api(data=data, count=count)


# 获取最新的8条更新记录（用于首页显示）
@bp.get('/latest')
@authorize("system:updatelog:main")
def latest():
    try:
        # 获取最新的8条记录，按创建时间倒序
        latest_logs = UpdateLog.query.order_by(UpdateLog.create_time.desc()).limit(8).all()
        data = curd.model_to_dicts(schema=UpdateLogOutSchema, data=latest_logs)
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        return fail_api(msg="获取更新记录失败")


# 新增更新记录页面
@bp.get('/add')
@authorize("system:updatelog:add", log=True)
def add():
    return render_template('system/updatelog/add.html')


# 保存更新记录
@bp.post('/save')
@authorize("system:updatelog:add", log=True)
def save():
    req_json = request.get_json(force=True)
    title = str_escape(req_json.get("title"))
    content = str_escape(req_json.get("content"))
    version = str_escape(req_json.get("version"))
    update_type = str_escape(req_json.get("updateType"))
    
    updatelog = UpdateLog(
        title=title,
        content=content,
        version=version,
        update_type=update_type,
        creator=current_user.username if current_user else '系统',
        create_id=current_user.id if current_user else None
    )
    db.session.add(updatelog)
    db.session.commit()
    
    if updatelog.id is None:
        return fail_api(msg="增加失败")
    return success_api(msg="增加成功")


# 编辑更新记录页面
@bp.get('/edit')
@authorize("system:updatelog:edit", log=True)
def edit():
    _id = request.args.get('id', type=int)
    updatelog = UpdateLog.query.filter_by(id=_id).first()
    if not updatelog:
        return fail_api(msg="记录不存在")
    return render_template('system/updatelog/edit.html', updatelog=updatelog)


# 更新更新记录
@bp.put('/update')
@authorize("system:updatelog:edit", log=True)
def update():
    req_json = request.get_json(force=True)
    id = str_escape(req_json.get("id"))
    title = str_escape(req_json.get("title"))
    content = str_escape(req_json.get("content"))
    version = str_escape(req_json.get("version"))
    update_type = str_escape(req_json.get("updateType"))
    
    UpdateLog.query.filter_by(id=id).update({
        "title": title,
        "content": content,
        "version": version,
        "update_type": update_type,
        "modifier": current_user.username if current_user else '系统',
        "modify_id": current_user.id if current_user else None
    })
    db.session.commit()
    return success_api(msg="更新成功")


# 删除更新记录
@bp.delete('/remove/<int:_id>')
@authorize("system:updatelog:remove", log=True)
def delete(_id):
    res = curd.delete_one_by_id(UpdateLog, _id)
    if not res:
        return fail_api(msg="删除失败")
    return success_api(msg="删除成功")


# 批量删除更新记录
@bp.post('/batchRemove')
@authorize("system:updatelog:remove", log=True)
def batch_remove():
    req_json = request.get_json(force=True)
    ids = req_json.get('ids', [])
    if not ids:
        return fail_api(msg="请选择要删除的数据")
    
    try:
        UpdateLog.query.filter(UpdateLog.id.in_(ids)).delete(synchronize_session=False)
        db.session.commit()
        return success_api(msg="批量删除成功")
    except Exception as e:
        db.session.rollback()
        return fail_api(msg="批量删除失败")

