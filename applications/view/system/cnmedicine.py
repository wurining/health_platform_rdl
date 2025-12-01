from flask import Blueprint, render_template, request, current_app, jsonify
from flask_login import login_required, current_user
from sqlalchemy import desc

from applications.common import curd
from applications.common.curd import enable_status, disable_status
from applications.common.utils.http import table_api, fail_api, success_api
from applications.common.utils.rights import authorize
from applications.common.utils.validate import str_escape
from applications.extensions import db
from applications.models import CnmedicineModel
from applications.schemas import CnmedicineSchema
from applications.common.curd import model_to_dicts

import uuid,datetime

bp = Blueprint('cnmedicine', __name__, url_prefix='/cnmedicine')


# 患者管理
@bp.get('/')
@authorize("system:cnmedicine:main")
def main():
    return render_template('system/cnmedicine/main.html')

#   患者分页查询
@bp.get('/data')
@authorize("system:cnmedicine:main")
def data():
    try:
        # 获取请求参数，使用小写变量名符合Python命名规范
        Name = str_escape(request.args.get('Name', type=str))
        patientNo = str_escape(request.args.get('PatientNo', type=str))
        ContactPhone = str_escape(request.args.get('ContactPhone', type=str))
        
        # 过滤器
        filters = []
        if Name:
            filters.append(CnmedicineModel.MedicineName.contains(Name))
        
        if patientNo:
            filters.append(CnmedicineModel.MedicineName.contains(patientNo))
        
        if ContactPhone:
            filters.append(CnmedicineModel.MedicineName.contains(ContactPhone))

        # 分页对象
        paginated_cnmedicine = CnmedicineModel.query.filter(*filters).order_by(desc(CnmedicineModel.CreateDate)).layui_paginate()

        # 返回结果
        return table_api(
            data=model_to_dicts(schema=CnmedicineSchema, data=paginated_cnmedicine.items), 
            count=paginated_cnmedicine.total
        )
    except Exception as e:
        # 添加异常处理，确保API调用的稳定性
        current_app.logger.error(f"查询患者列表失败: {str(e)}")
        return fail_api(msg="查询患者列表失败，请稍后重试")
    
@bp.get('/search')
@authorize("system:cnmedicine:search")
def search():
    try:
        # 获取请求参数，使用小写变量名符合Python命名规范
        keyword = str_escape(request.args.get('keyword', type=str))
        patientNo = str_escape(request.args.get('PatientNo', type=str))
        ContactPhone = str_escape(request.args.get('ContactPhone', type=str))
        
        # 过滤器
        filters = []
        if keyword:
            filters.append(CnmedicineModel.MedicineName.contains(keyword))

        # 对象
        paginated_cnmedicine = CnmedicineModel.query.filter(*filters).all()

        # 返回结果
        return table_api(
            data=model_to_dicts(schema=CnmedicineSchema, data=paginated_cnmedicine), 
            count=len(paginated_cnmedicine)
        )
    except Exception as e:
        # 添加异常处理，确保API调用的稳定性
        current_app.logger.error(f"查询患者列表失败: {str(e)}")
        return fail_api(msg="查询患者列表失败，请稍后重试")


# 患者增加
@bp.get('/add')
@authorize("system:cnmedicine:add", log=True)
def add():
    # roles = Role.query.all()
    # return render_template('system/cnmedicine/add.html', roles=roles)
    return render_template('system/cnmedicine/add.html')


@bp.post('/save')
@authorize("system:cnmedicine:add", log=True)
def save():
    req_json = request.get_json(force=True)
    MedicineName = str_escape(req_json.get('MedicineName') or req_json.get('Name'))
    MedicineType = str_escape(req_json.get('MedicineType') or req_json.get('Sex'))
    MedicineInstruction = str_escape(req_json.get('MedicineInstruction') or req_json.get('Nation'))
    MedicineUse = str_escape(req_json.get('MedicineUse') or req_json.get('ContactPhone'))
    Remarks = str_escape(req_json.get('Remarks'))

    MedicineID = str(uuid.uuid4())

    # 获取当前用户信息
    current_user_id = current_user.id if current_user.is_authenticated else None
    current_user_name = current_user.realname if (current_user.is_authenticated and current_user.realname) else (current_user.username if current_user.is_authenticated else "系统")

    if not MedicineName:
        return fail_api(msg="中药名称不得为空")
    
    medicine = CnmedicineModel(
        MedicineID=MedicineID,
        MedicineName=MedicineName,
        MedicineType=MedicineType,
        MedicineInstruction=MedicineInstruction,
        MedicineUse=MedicineUse,
        Remarks=Remarks,
        CreateID=current_user_id,
        Creator=current_user_name,
        CreateDate=datetime.datetime.now(),
        ModifyID=current_user_id,
        Modifier=current_user_name,
        ModifyDate=datetime.datetime.now()
    )
    db.session.add(medicine)
    db.session.commit()

    return success_api(msg="增加成功")


    #  编辑中药
@bp.get('/edit/<string:MedicineID>')
@authorize("system:cnmedicine:edit", log=True)
def edit(MedicineID):
    # medicine = curd.get_one_by_id(CnmedicineModel, MedicineID)
    medicine = CnmedicineModel.query.filter_by(MedicineID=MedicineID).first()

    return render_template('system/cnmedicine/edit.html', patient_res=medicine)

#  编辑患者
@bp.put('/update')
@authorize("system:cnmedicine:edit", log=True)
def update():
    req_json = request.get_json(force=True)
    MedicineName = str_escape(req_json.get('MedicineName') or req_json.get('Name'))
    MedicineType = str_escape(req_json.get('MedicineType') or req_json.get('Sex'))
    MedicineInstruction = str_escape(req_json.get('MedicineInstruction') or req_json.get('Nation'))
    MedicineUse = str_escape(req_json.get('MedicineUse') or req_json.get('ContactPhone'))
    Remarks = str_escape(req_json.get('Remarks'))

    MedicineID = str_escape(req_json.get('MedicineID') or req_json.get('PatientID'))

    # 获取当前用户信息
    current_user_id = current_user.id if current_user.is_authenticated else None
    current_user_name = current_user.realname if (current_user.is_authenticated and current_user.realname) else (current_user.username if current_user.is_authenticated else "系统")

    data = {
        'MedicineName': MedicineName,
        'MedicineType': MedicineType,
        'MedicineInstruction': MedicineInstruction,
        'MedicineUse': MedicineUse,
        'Remarks': Remarks,
        'ModifyID': current_user_id,
        'Modifier': current_user_name,
        'ModifyDate': datetime.datetime.now()
    }
    if not MedicineName:
        return fail_api(msg="中药名称不得为空")
    
    CnmedicineModel.query.filter_by(MedicineID=MedicineID).update(data)
    db.session.commit()

    return success_api(msg="更新成功")


# 删除中药
@bp.delete('/remove/<string:MedicineID>')
@authorize("system:cnmedicine:remove", log=True)
def delete(MedicineID):
    res = CnmedicineModel.query.filter_by(MedicineID=MedicineID).delete()
    db.session.commit()
    if not res:
        return fail_api(msg="删除失败")
    return success_api(msg="删除成功")
