from flask import Blueprint, render_template, request, current_app, jsonify
from flask_login import login_required, current_user
from sqlalchemy import desc

from applications.common import curd
from applications.common.curd import enable_status, disable_status
from applications.common.utils.http import table_api, fail_api, success_api
from applications.common.utils.rights import authorize
from applications.common.utils.validate import str_escape
from applications.extensions import db
from applications.models import CoursesofdiseaseModel, PatientsModel
from applications.schemas import CoursesofdiseaseSchema
from applications.common.curd import model_to_dicts

import uuid, datetime

bp = Blueprint('coursesofdisease', __name__, url_prefix='/coursesofdisease')


def _patient_options():
    """获取患者选项列表"""
    return PatientsModel.query.with_entities(
        PatientsModel.PatientID,
        PatientsModel.Name,
        PatientsModel.PatientNo
    ).order_by(PatientsModel.Name.asc()).all()


# 病程管理
@bp.get('/')
@authorize("system:coursesofdisease:main")
def main():
    patients = _patient_options()
    return render_template('system/coursesofdisease/main.html', patients=patients)

# 病程分页查询
@bp.get('/data')
@authorize("system:coursesofdisease:main")
def data():
    try:
        # 获取请求参数，使用小写变量名符合Python命名规范
        Name = str_escape(request.args.get('Name', type=str))
        patientNo = str_escape(request.args.get('PatientNo', type=str))
        ContactPhone = str_escape(request.args.get('ContactPhone', type=str))
        
        # 构建过滤器 - 基于 PatientsModel 的字段进行过滤
        filters = []
        if Name:
            filters.append(PatientsModel.Name.contains(Name))
        
        if patientNo:
            filters.append(PatientsModel.PatientNo.contains(patientNo))
        
        if ContactPhone:
            filters.append(PatientsModel.ContactPhone.contains(ContactPhone))

        # 使用 JOIN 查询，关联 PatientsModel 获取病程信息
        query = db.session.query(CoursesofdiseaseModel, PatientsModel).outerjoin(
            PatientsModel, CoursesofdiseaseModel.PatientID == PatientsModel.PatientID
        )
        
        # 应用过滤器
        if filters:
            query = query.filter(*filters)

        # 使用 layui_paginate 进行分页
        paginated_result = query.order_by(desc(CoursesofdiseaseModel.CreateDate)).layui_paginate()
        
        # 构建返回数据
        data = []
        for course, patient in paginated_result.items:
            item = model_to_dicts(schema=CoursesofdiseaseSchema, data=[course])[0]
            # 添加病程信息
            if patient:
                item['PatientNo'] = patient.PatientNo if patient.PatientNo else ""
                item['Name'] = patient.Name if patient.Name else ""
                item['ContactPhone'] = patient.ContactPhone if patient.ContactPhone else ""
                item['Address'] = patient.Address if patient.Address else ""
            else:
                item['PatientNo'] = ""
                item['Name'] = ""
                item['ContactPhone'] = ""
                item['Address'] = ""
            data.append(item)

        # 返回结果
        return table_api(data=data, count=paginated_result.total)
    except Exception as e:
        # 添加异常处理，确保API调用的稳定性
        current_app.logger.error(f"查询病程列表失败: {str(e)}")
        return fail_api(msg="查询病程列表失败，请稍后重试")
    
@bp.get('/search')
@authorize("system:coursesofdisease:search")
def search():
    try:
        # 获取请求参数
        keyword = str_escape(request.args.get('keyword', type=str))
        patient_id = str_escape(request.args.get('PatientID', type=str))
        
        # 构建过滤器
        filters = []
        if keyword:
            filters.append(CoursesofdiseaseModel.CurrentDisease.contains(keyword))
        if patient_id:
            filters.append(CoursesofdiseaseModel.PatientID == patient_id)

        # 使用 JOIN 查询，关联 PatientsModel 获取患者信息
        query = db.session.query(CoursesofdiseaseModel, PatientsModel).outerjoin(
            PatientsModel, CoursesofdiseaseModel.PatientID == PatientsModel.PatientID
        )
        
        # 应用过滤器
        if filters:
            query = query.filter(*filters)

        # 使用 layui_paginate 进行分页
        paginated_result = query.order_by(desc(CoursesofdiseaseModel.CreateDate)).layui_paginate()
        
        # 构建返回数据
        data = []
        for course, patient in paginated_result.items:
            item = model_to_dicts(schema=CoursesofdiseaseSchema, data=[course])[0]
            # 添加患者信息
            if patient:
                item['PatientNo'] = patient.PatientNo if patient.PatientNo else ""
                item['Name'] = patient.Name if patient.Name else ""
                item['ContactPhone'] = patient.ContactPhone if patient.ContactPhone else ""
                item['Address'] = patient.Address if patient.Address else ""
            else:
                item['PatientNo'] = ""
                item['Name'] = ""
                item['ContactPhone'] = ""
                item['Address'] = ""
            data.append(item)

        # 返回结果
        return table_api(data=data, count=paginated_result.total)
    except Exception as e:
        # 添加异常处理，确保API调用的稳定性
        current_app.logger.error(f"查询病程列表失败: {str(e)}")
        return fail_api(msg="查询病程列表失败，请稍后重试")


# 病程增加
@bp.get('/add')
@authorize("system:coursesofdisease:add", log=True)
def add():
    # 获取URL参数中的PatientID（从患者详情页跳转过来时会有此参数）
    url_patient_id = str_escape(request.args.get('PatientID', type=str))
    
    # 查询患者信息（如果URL中有PatientID参数）
    patient = None
    if url_patient_id:
        patient = PatientsModel.query.filter_by(PatientID=url_patient_id).first()
    
    return render_template('system/coursesofdisease/add.html', patient=patient)


@bp.post('/save')
@authorize("system:coursesofdisease:add", log=True)
def save():
    req_json = request.get_json(force=True)
    PatientID = str_escape(req_json.get('PatientID'))
    CourseType = str_escape(req_json.get('CourseType'))
    CourseTime_str = str_escape(req_json.get('CourseTime'))
    CurrentDisease = str_escape(req_json.get('CurrentDisease'))
    # TreatmentPlan 是富文本内容，包含 HTML 标签，不需要转义
    TreatmentPlan = req_json.get('TreatmentPlan') or ''
    if TreatmentPlan:
        TreatmentPlan = str(TreatmentPlan)
    attachments_list = req_json.get('AttachMents', [])  # 附件列表
    Remarks = str_escape(req_json.get('Remarks'))

    CourseID = str(uuid.uuid4())

    # 获取当前用户信息
    current_user_id = current_user.id if current_user.is_authenticated else None
    current_user_name = current_user.realname if (current_user.is_authenticated and current_user.realname) else (current_user.username if current_user.is_authenticated else "系统")

    if not PatientID:
        return fail_api(msg="患者信息不得为空")
    
    # 验证患者是否存在
    if not PatientsModel.query.filter_by(PatientID=PatientID).first():
        return fail_api(msg="患者信息不存在，请重新选择")
    
    # 解析病程时间
    CourseTime = None
    if CourseTime_str:
        try:
            CourseTime = datetime.datetime.strptime(CourseTime_str, '%Y-%m-%d %H:%M:%S')
        except:
            try:
                CourseTime = datetime.datetime.strptime(CourseTime_str, '%Y-%m-%d')
            except:
                CourseTime = datetime.datetime.now()
    else:
        CourseTime = datetime.datetime.now()
    
    course = CoursesofdiseaseModel(
        CourseID=CourseID,
        PatientID=PatientID,
        UserID=current_user_id,
        CourseType=CourseType,
        CourseTime=CourseTime,
        CurrentDisease=CurrentDisease,
        TreatmentPlan=TreatmentPlan,
        Remarks=Remarks,
        CreateID=current_user_id,
        Creator=current_user_name,
        CreateDate=datetime.datetime.now(),
        ModifyID=current_user_id,
        Modifier=current_user_name,
        ModifyDate=datetime.datetime.now()
    )
    
    # 设置附件列表
    if attachments_list:
        course.set_attachments_list(attachments_list)
    else:
        course.AttachMents = None
    
    db.session.add(course)
    db.session.commit()

    return success_api(msg="增加成功")


#  编辑病程
@bp.get('/edit/<string:CourseID>')
@authorize("system:coursesofdisease:edit", log=True)
def edit(CourseID):
    course = CoursesofdiseaseModel.query.filter_by(CourseID=CourseID).first()
    if not course:
        return fail_api(msg="病程信息不存在")
    
    # 获取URL参数中的PatientID（从患者详情页跳转过来时会有此参数）
    url_patient_id = str_escape(request.args.get('PatientID', type=str))
    
    # 查询关联的患者信息
    # 优先使用URL参数中的PatientID，如果没有则使用病程关联的PatientID
    patient_id_to_use = url_patient_id if url_patient_id else course.PatientID
    patient = None
    if patient_id_to_use:
        patient = PatientsModel.query.filter_by(PatientID=patient_id_to_use).first()
    
    patients = _patient_options()
    # 预处理附件数据，转换为列表格式供模板使用
    attachments_list = course.get_attachments_list() if hasattr(course, 'get_attachments_list') else []
    
    return render_template('system/coursesofdisease/edit.html', 
                         course=course, 
                         patient=patient,
                         patients=patients,
                         attachments_list=attachments_list)

#  编辑病程
@bp.put('/update')
@authorize("system:coursesofdisease:edit", log=True)
def update():
    req_json = request.get_json(force=True)
    CourseID = str_escape(req_json.get('CourseID'))
    PatientID = str_escape(req_json.get('PatientID'))
    CourseType = str_escape(req_json.get('CourseType'))
    CourseTime_str = str_escape(req_json.get('CourseTime'))
    CurrentDisease = str_escape(req_json.get('CurrentDisease'))
    # TreatmentPlan 是富文本内容，包含 HTML 标签，不需要转义
    TreatmentPlan = req_json.get('TreatmentPlan') or ''
    if TreatmentPlan:
        TreatmentPlan = str(TreatmentPlan)
    attachments_list = req_json.get('AttachMents', [])  # 附件列表
    Remarks = str_escape(req_json.get('Remarks'))

    if not CourseID:
        return fail_api(msg="病程ID不得为空")
    
    if not PatientID:
        return fail_api(msg="患者信息不得为空")
    
    # 验证患者是否存在
    if not PatientsModel.query.filter_by(PatientID=PatientID).first():
        return fail_api(msg="患者信息不存在，请重新选择")
    
    course = CoursesofdiseaseModel.query.filter_by(CourseID=CourseID).first()
    if not course:
        return fail_api(msg="病程信息不存在或已删除")
    
    # 获取当前用户信息
    current_user_id = current_user.id if current_user.is_authenticated else None
    current_user_name = current_user.realname if (current_user.is_authenticated and current_user.realname) else (current_user.username if current_user.is_authenticated else "系统")
    
    # 解析病程时间
    CourseTime = None
    if CourseTime_str:
        try:
            CourseTime = datetime.datetime.strptime(CourseTime_str, '%Y-%m-%d %H:%M:%S')
        except:
            try:
                CourseTime = datetime.datetime.strptime(CourseTime_str, '%Y-%m-%d')
            except:
                CourseTime = datetime.datetime.now()
    
    # 更新字段
    course.PatientID = PatientID
    course.UserID = current_user_id
    course.CourseType = CourseType
    course.CourseTime = CourseTime
    course.CurrentDisease = CurrentDisease
    course.TreatmentPlan = TreatmentPlan
    course.Remarks = Remarks
    course.ModifyID = current_user_id
    course.Modifier = current_user_name
    course.ModifyDate = datetime.datetime.now()
    
    # 更新附件列表
    if attachments_list:
        course.set_attachments_list(attachments_list)
    else:
        course.AttachMents = None
    
    db.session.commit()
    
    return success_api(msg="更新成功")


# 删除病程
@bp.delete('/remove/<string:CourseID>')
@authorize("system:coursesofdisease:remove", log=True)
def delete(CourseID):
    res = CoursesofdiseaseModel.query.filter_by(CourseID=CourseID).delete()
    db.session.commit()
    if not res:
        return fail_api(msg="删除失败")
    return success_api(msg="删除成功")



