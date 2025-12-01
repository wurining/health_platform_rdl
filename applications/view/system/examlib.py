from flask import Blueprint, render_template, request, current_app
from sqlalchemy import desc

from applications.common.curd import model_to_dicts
from applications.common.utils.http import table_api, fail_api, success_api
from applications.common.utils.rights import authorize
from applications.common.utils.validate import str_escape
from applications.extensions import db
from applications.models import ExamlibModel, PatientsModel
from applications.schemas import ExamlibSchema

import uuid, datetime
from flask_login import current_user

bp = Blueprint('examlib', __name__, url_prefix='/examlib')

def _patient_options():
    """获取患者选项列表"""
    return PatientsModel.query.with_entities(
        PatientsModel.PatientID,
        PatientsModel.Name,
        PatientsModel.PatientNo
    ).order_by(PatientsModel.Name.asc()).all()


@bp.get('/')
@authorize("system:examlib:main")
def main():
    return render_template('system/examlib/main.html')


@bp.get('/data')
@authorize("system:examlib:main")
def data():
    try:
        exam_name = str_escape(request.args.get('ExamName', type=str))
        patient_name = str_escape(request.args.get('Name', type=str))

        # 使用 JOIN 查询，关联 PatientsModel 获取患者信息
        query = db.session.query(ExamlibModel, PatientsModel).outerjoin(
            PatientsModel, ExamlibModel.PatientID == PatientsModel.PatientID
        )

        # 构建过滤条件
        filters = []
        if exam_name:
            filters.append(ExamlibModel.ExamName.contains(exam_name))
        if patient_name:
            filters.append(PatientsModel.Name.contains(patient_name))

        # 应用过滤条件
        if filters:
            query = query.filter(*filters)

        # 使用 layui_paginate 进行分页
        paginated_result = query.order_by(desc(ExamlibModel.CreateDate)).layui_paginate()

        # 构建返回数据
        data = []
        for exam, patient in paginated_result.items:
            item = model_to_dicts(schema=ExamlibSchema, data=[exam])[0]
            # 添加患者信息
            if patient:
                item['PatientID'] = patient.PatientID if patient.PatientID else ""
                item['PatientNo'] = patient.PatientNo if patient.PatientNo else ""
                item['Name'] = patient.Name if patient.Name else ""
                item['ContactPhone'] = patient.ContactPhone if patient.ContactPhone else ""
            else:
                item['PatientID'] = ""
                item['PatientNo'] = ""
                item['Name'] = ""
                item['ContactPhone'] = ""
            data.append(item)

        return table_api(data=data, count=paginated_result.total)
    except Exception as exc:
        current_app.logger.error(f"查询检查库失败: {exc}")
        return fail_api(msg="查询检查库失败，请稍后重试")


@bp.get('/add')
@authorize("system:examlib:add", log=True)
def add():
    # 获取URL参数中的PatientID（从患者详情页跳转过来时会有此参数）
    url_patient_id = str_escape(request.args.get('PatientID', type=str))
    
    # 查询患者信息（如果URL中有PatientID参数）
    patient = None
    if url_patient_id:
        patient = PatientsModel.query.filter_by(PatientID=url_patient_id).first()
    
    return render_template('system/examlib/add.html', patient=patient)


@bp.post('/save')
@authorize("system:examlib:add", log=True)
def save():
    try:
        req_json = request.get_json(force=True)
        PatientID = str_escape(req_json.get('PatientID'))
        ExamName = str_escape(req_json.get('ExamName'))
        attachments_list = req_json.get('AttachMents', [])  # 附件列表
        Remarks = str_escape(req_json.get('Remarks'))

        if not ExamName:
            return fail_api(msg="检查名称不得为空")
        if not PatientID:
            return fail_api(msg="患者信息不得为空")

        exam = ExamlibModel(
            ExamID=str(uuid.uuid4()),
            PatientID=PatientID,
            ExamName=ExamName,
            Remarks=Remarks,
            CreateID=current_user.id,
            Creator=current_user.realname,
            ModifyID=current_user.id,
            Modifier=current_user.username,
            CreateDate=datetime.datetime.now(),
            ModifyDate=datetime.datetime.now()
        )
        
        # 设置附件列表
        if attachments_list:
            exam.set_attachments_list(attachments_list)
        
        db.session.add(exam)
        db.session.commit()
        return success_api(msg="新增检查项目成功")
    except Exception as exc:
        current_app.logger.error(f"新增检查项目失败: {exc}")
        db.session.rollback()
        return fail_api(msg=f"新增检查项目失败: {str(exc)}")


@bp.get('/edit/<string:ExamID>')
@authorize("system:examlib:edit", log=True)
def edit(ExamID):
    exam = ExamlibModel.query.filter_by(ExamID=ExamID).first()
    if not exam:
        return fail_api(msg="检查项不存在")
    
    # 获取URL参数中的PatientID（从患者详情页跳转过来时会有此参数）
    url_patient_id = str_escape(request.args.get('PatientID', type=str))
    
    # 查询关联的患者信息
    # 优先使用URL参数中的PatientID，如果没有则使用检查项关联的PatientID
    patient_id_to_use = url_patient_id if url_patient_id else exam.PatientID
    patient = None
    if patient_id_to_use:
        patient = PatientsModel.query.filter_by(PatientID=patient_id_to_use).first()
    
    # 获取所有患者列表（用于下拉选择显示）
    patients = _patient_options()
    
    # 预处理附件数据，转换为列表格式供模板使用
    attachments_list = exam.get_attachments_list() if hasattr(exam, 'get_attachments_list') else []
    
    return render_template('system/examlib/edit.html', 
                         exam=exam, 
                         patient=patient,
                         patients=patients,
                         attachments_list=attachments_list)


@bp.put('/update')
@authorize("system:examlib:edit", log=True)
def update():
    try:
        req_json = request.get_json(force=True)
        exam_id = str_escape(req_json.get('ExamID'))
        exam_name = str_escape(req_json.get('ExamName'))
        patient_id = str_escape(req_json.get('PatientID'))
        attachments_list = req_json.get('AttachMents', [])  # 附件列表
        remarks = str_escape(req_json.get('Remarks'))

        if not exam_id:
            return fail_api(msg="缺少检查ID")
        if not exam_name:
            return fail_api(msg="检查名称不得为空")

        exam = ExamlibModel.query.filter_by(ExamID=exam_id).first()
        if not exam:
            return fail_api(msg="检查项不存在或已删除")

        # 更新字段
        exam.ExamName = exam_name
        exam.PatientID = patient_id if patient_id else None
        exam.Remarks = remarks
        
        # 更新附件列表
        if attachments_list:
            exam.set_attachments_list(attachments_list)
        else:
            exam.AttachMents = None
        
        # 设置修改人信息
        if current_user and hasattr(current_user, 'id'):
            exam.ModifyID = current_user.id
            exam.Modifier = getattr(current_user, 'username', '') or getattr(current_user, 'realname', '')
        
        db.session.commit()
        return success_api(msg="更新成功")
    except Exception as exc:
        current_app.logger.error(f"更新检查项目失败: {exc}")
        db.session.rollback()
        return fail_api(msg=f"更新检查项目失败: {str(exc)}")


@bp.delete('/remove/<string:ExamID>')
@authorize("system:examlib:remove", log=True)
def delete(ExamID):
    deleted = ExamlibModel.query.filter_by(ExamID=ExamID).delete()
    db.session.commit()
    if not deleted:
        return fail_api(msg="删除失败，检查项不存在")
    return success_api(msg="删除成功")