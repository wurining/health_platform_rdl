from flask import Blueprint, render_template, request, current_app, jsonify
from flask_login import login_required, current_user
from sqlalchemy import desc

from applications.common import curd
from applications.common.curd import enable_status, disable_status
from applications.common.utils.http import table_api, fail_api, success_api
from applications.common.utils.rights import authorize
from applications.common.utils.validate import str_escape
from applications.extensions import db
from applications.models import AppointmentModel, PatientsModel
from applications.schemas import AppointmentSchema, PatientsSchema
from applications.common.curd import model_to_dicts
import uuid
import datetime

bp = Blueprint('appointment', __name__, url_prefix='/appointment')

# 预约管理
@bp.get('/')
@authorize("system:appointment:main")
def main():
    return render_template('system/appointment/main.html')

# 获取预约统计信息
@bp.get('/statistics')
@authorize("system:appointment:main")
def statistics():
    """
    获取预约统计信息
    返回所有预约总数，不过滤任何条件
    """
    try:
        # 获取预约总数，不过滤任何条件
        total_appointment_count = AppointmentModel.query.count()
        
        return jsonify({
            'success': True,
            'data': {
                'local_count': total_appointment_count,
                'total_count': total_appointment_count
            }
        })
    except Exception as e:
        current_app.logger.error(f"获取预约统计信息失败: {str(e)}")
        return fail_api(msg="获取预约统计信息失败，请稍后重试")

# 预约分页查询
@bp.get('/data')
@authorize("system:appointment:main")
def data():
    try:
        # 获取请求参数
        PatientNo = str_escape(request.args.get('PatientNo', type=str))
        Name = str_escape(request.args.get('Name', type=str))
        AppointmentTime = str_escape(request.args.get('AppointmentTime', type=str))
            
        # 构建过滤器
        filters = []
        if PatientNo:
            filters.append(PatientsModel.PatientNo.contains(PatientNo))
        
        if AppointmentTime:
            filters.append(AppointmentModel.AppointmentTime.contains(AppointmentTime))
        
        if Name:
            filters.append(PatientsModel.Name.contains(Name))

        # 使用 JOIN 查询，关联 PatientsModel 获取患者信息
        query = db.session.query(AppointmentModel, PatientsModel).outerjoin(
            PatientsModel, AppointmentModel.PatientID == PatientsModel.PatientID
        )
        
        # 应用过滤器
        if filters:
            query = query.filter(*filters)

        # 使用 layui_paginate 进行分页
        paginated_result = query.order_by(desc(AppointmentModel.CreateDate)).layui_paginate()
        
        # 构建返回数据
        data = []
        for appointment, patient in paginated_result.items:
            item = model_to_dicts(schema=AppointmentSchema, data=[appointment])[0]
            # 添加患者信息
            if patient:
                item['PatientNo'] = patient.PatientNo if patient.PatientNo else ""
                item['Name'] = patient.Name if patient.Name else ""
            else:
                item['PatientNo'] = ""
                item['Name'] = ""
            data.append(item)
            
        # 返回结果
        return table_api(data=data, count=paginated_result.total)
    
    except Exception as e:
        # 添加异常处理，确保API调用的稳定性
        current_app.logger.error(f"查询预约列表失败: {str(e)}")
        return fail_api(msg="查询预约列表失败，请稍后重试")

# 预约增加
@bp.get('/add')
@authorize("system:appointment:add", log=True)
def add():
    return render_template('system/appointment/add.html')

@bp.post('/save')
@authorize("system:appointment:add", log=True)
def save():
    req_json = request.get_json(force=True)
    PatientID = str_escape(req_json.get('PatientID'))
    AppointmentTime = str_escape(req_json.get('AppointmentTime'))
    Remarks = str_escape(req_json.get('Remarks'))

    # 获取当前用户信息
    current_user_id = current_user.id if current_user.is_authenticated else None
    current_user_name = current_user.realname if (current_user.is_authenticated and hasattr(current_user, 'realname') and current_user.realname) else (current_user.username if (current_user.is_authenticated and hasattr(current_user, 'username')) else "系统")

    if not PatientID or not AppointmentTime:
        return fail_api(msg="患者ID和预约时间不得为空")
    
    data = AppointmentModel(
        AppointmentID=str(uuid.uuid4()), 
        PatientID=PatientID,
        AppointmentTime=AppointmentTime,
        Remarks=Remarks,
        CreateID=current_user_id,
        Creator=current_user_name,
        CreateDate=datetime.datetime.now(),
        ModifyID=current_user_id,
        Modifier=current_user_name,
        ModifyDate=datetime.datetime.now()
    )
    db.session.add(data)
    db.session.commit()

    return success_api(msg="增加成功")


# 编辑预约
@bp.get('/edit/<string:AppointmentID>')
@authorize("system:appointment:edit", log=True)
def edit(AppointmentID):
    # 使用 JOIN 查询，关联 PatientsModel 获取患者信息
    result = db.session.query(AppointmentModel, PatientsModel).outerjoin(
        PatientsModel, AppointmentModel.PatientID == PatientsModel.PatientID
    ).filter(AppointmentModel.AppointmentID == AppointmentID).first()
    
    if result:
        appointment, patient = result
        # 将患者姓名添加到 appointment 对象中
        if patient:
            appointment.Name = patient.Name if patient.Name else ""
        else:
            appointment.Name = ""
    else:
        appointment = AppointmentModel.query.filter_by(AppointmentID=AppointmentID).first()
        if appointment:
            appointment.Name = ""
    
    return render_template('system/appointment/edit.html', appointment=appointment)

# 更新预约
@bp.put('/update')
@authorize("system:appointment:edit", log=True)
def update():
    req_json = request.get_json(force=True)
    PatientID = str_escape(req_json.get('PatientID'))
    AppointmentTime = str_escape(req_json.get('AppointmentTime'))
    Remarks = str_escape(req_json.get('Remarks'))
    AppointmentID = str_escape(req_json.get('AppointmentID'))

    # 获取当前用户信息
    current_user_id = current_user.id if current_user.is_authenticated else None
    current_user_name = current_user.realname if (current_user.is_authenticated and hasattr(current_user, 'realname') and current_user.realname) else (current_user.username if (current_user.is_authenticated and hasattr(current_user, 'username')) else "系统")

    data = {
        'PatientID': PatientID,
        'AppointmentTime': AppointmentTime,
        'Remarks': Remarks,
        'ModifyID': current_user_id,
        'Modifier': current_user_name,
        'ModifyDate': datetime.datetime.now()
    }
    
    if not PatientID or not AppointmentTime:
        return fail_api(msg="患者ID和预约时间不得为空")
    
    AppointmentModel.query.filter_by(AppointmentID=AppointmentID).update(data)
    db.session.commit()

    return success_api(msg="更新成功")


# 删除预约
@bp.delete('/remove/<string:AppointmentID>')
@authorize("system:appointment:remove", log=True)
def delete(AppointmentID):
    res = AppointmentModel.query.filter_by(AppointmentID=AppointmentID).delete()
    db.session.commit()
    if not res:
        return fail_api(msg="删除失败")
    return success_api(msg="删除成功")