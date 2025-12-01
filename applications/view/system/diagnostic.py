from flask import Blueprint, render_template, request, current_app, jsonify
from flask_login import current_user
import json

from applications.common.curd import model_to_dicts
from applications.common.utils.http import table_api, fail_api, success_api
from applications.common.utils.rights import authorize
from applications.common.utils.validate import str_escape
from applications.extensions import db
from applications.models import DiagnosticModel, PatientsModel
from applications.schemas import DiagnosticSchema

import uuid

bp = Blueprint('diagnostic', __name__, url_prefix='/diagnostic')


def _patient_options():
    return PatientsModel.query.with_entities(
        PatientsModel.PatientID,
        PatientsModel.Name,
        PatientsModel.PatientNo
    ).order_by(PatientsModel.Name.asc()).all()


@bp.get('/')
@authorize("system:diagnostic:main")
def main():
    patients = _patient_options()
    return render_template('system/diagnostic/main.html', patients=patients)


@bp.get('/data')
@authorize("system:diagnostic:main")
def data():
    try:
        diagnosis = str_escape(request.args.get('Diagnosis', type=str))
        pathology = str_escape(request.args.get('Pathology', type=str))
        patient_id = str_escape(request.args.get('PatientID', type=str))

        query = DiagnosticModel.query
        if diagnosis:
            query = query.filter(DiagnosticModel.Diagnosis.contains(diagnosis))
        if pathology:
            query = query.filter(DiagnosticModel.Pathology.contains(pathology))
        if patient_id:
            query = query.filter(DiagnosticModel.PatientID == patient_id)

        paginated = query.order_by(DiagnosticModel.CreateDate.desc()).layui_paginate()

        return table_api(
            data=model_to_dicts(schema=DiagnosticSchema, data=paginated.items),
            count=paginated.total
        )
    except Exception as exc:
        current_app.logger.error(f"查询诊断信息失败: {exc}")
        return fail_api(msg="查询诊断信息失败，请稍后重试")


@bp.get('/add')
@authorize("system:diagnostic:add", log=True)
def add():
    patients = _patient_options()
    return render_template('system/diagnostic/add.html', patients=patients)


@bp.post('/save')
@authorize("system:diagnostic:add", log=True)
def save():
    try:
        req_json = request.get_json(force=True)
        patient_id = str_escape(req_json.get('PatientID'))
        diagnosis_list = req_json.get('Diagnosis', [])  # 诊断标签列表
        other_hospital_diagnosis = str_escape(req_json.get('OtherHospitalDiagnosis', ''))
        pathology = str_escape(req_json.get('Pathology', ''))
        attachments_list = req_json.get('AttachMents', [])  # 附件列表
        remarks = str_escape(req_json.get('Remarks', ''))

        if not patient_id:
            return fail_api(msg="患者信息不得为空")

        if not PatientsModel.query.filter_by(PatientID=patient_id).first():
            return fail_api(msg="患者信息不存在，请重新选择")

        diagnostic = DiagnosticModel(
            DiagnosticID=str(uuid.uuid4()),
            PatientID=patient_id,
            OtherHospitalDiagnosis=other_hospital_diagnosis if other_hospital_diagnosis else None,
            Pathology=pathology if pathology else None,
            Remarks=remarks if remarks else None
        )
        
        # 设置诊断标签列表
        if diagnosis_list:
            diagnostic.set_diagnosis_list(diagnosis_list)
        
        # 设置附件列表
        if attachments_list:
            diagnostic.set_attachments_list(attachments_list)
        
        # 设置创建人信息
        if current_user and hasattr(current_user, 'id'):
            diagnostic.CreateID = current_user.id
            diagnostic.Creator = getattr(current_user, 'username', '') or getattr(current_user, 'name', '')
        
        db.session.add(diagnostic)
        db.session.commit()
        return success_api(msg="新增诊断信息成功", data={"DiagnosticID": diagnostic.DiagnosticID})
    except Exception as exc:
        current_app.logger.error(f"新增诊断信息失败: {exc}")
        db.session.rollback()
        return fail_api(msg=f"新增诊断信息失败: {str(exc)}")


@bp.get('/edit/<string:DiagnosticID>')
@authorize("system:diagnostic:edit", log=True)
def edit(DiagnosticID):
    diagnostic = DiagnosticModel.query.filter_by(DiagnosticID=DiagnosticID).first()
    if not diagnostic:
        return fail_api(msg="诊断信息不存在")
    patients = _patient_options()
    
    # 预处理诊断和附件数据，转换为列表格式供模板使用
    diagnosis_list = diagnostic.get_diagnosis_list() if hasattr(diagnostic, 'get_diagnosis_list') else []
    attachments_list = diagnostic.get_attachments_list() if hasattr(diagnostic, 'get_attachments_list') else []
    
    return render_template('system/diagnostic/edit.html', 
                         diagnostic=diagnostic, 
                         patients=patients,
                         diagnosis_list=diagnosis_list,
                         attachments_list=attachments_list)


@bp.put('/update')
@authorize("system:diagnostic:edit", log=True)
def update():
    try:
        req_json = request.get_json(force=True)
        diagnostic_id = str_escape(req_json.get('DiagnosticID'))
        patient_id = str_escape(req_json.get('PatientID'))
        diagnosis_list = req_json.get('Diagnosis', [])  # 诊断标签列表
        other_hospital_diagnosis = str_escape(req_json.get('OtherHospitalDiagnosis', ''))
        pathology = str_escape(req_json.get('Pathology', ''))
        attachments_list = req_json.get('AttachMents', [])  # 附件列表
        remarks = str_escape(req_json.get('Remarks', ''))

        if not diagnostic_id:
            return fail_api(msg="诊断主键缺失")
        if not patient_id:
            return fail_api(msg="患者信息不得为空")

        diagnostic = DiagnosticModel.query.filter_by(DiagnosticID=diagnostic_id).first()
        if not diagnostic:
            return fail_api(msg="诊断信息不存在或已删除")

        if not PatientsModel.query.filter_by(PatientID=patient_id).first():
            return fail_api(msg="患者信息不存在，请重新选择")

        # 更新字段
        diagnostic.PatientID = patient_id
        diagnostic.OtherHospitalDiagnosis = other_hospital_diagnosis if other_hospital_diagnosis else None
        diagnostic.Pathology = pathology if pathology else None
        diagnostic.Remarks = remarks if remarks else None
        
        # 更新诊断标签列表
        if diagnosis_list:
            diagnostic.set_diagnosis_list(diagnosis_list)
        else:
            diagnostic.Diagnosis = None
        
        # 更新附件列表
        if attachments_list:
            diagnostic.set_attachments_list(attachments_list)
        else:
            diagnostic.AttachMents = None
        
        # 设置修改人信息
        if current_user and hasattr(current_user, 'id'):
            diagnostic.ModifyID = current_user.id
            diagnostic.Modifier = getattr(current_user, 'username', '') or getattr(current_user, 'name', '')
        
        db.session.commit()
        return success_api(msg="更新成功")
    except Exception as exc:
        current_app.logger.error(f"更新诊断信息失败: {exc}")
        db.session.rollback()
        return fail_api(msg=f"更新诊断信息失败: {str(exc)}")


@bp.delete('/remove/<string:DiagnosticID>')
@authorize("system:diagnostic:remove", log=True)
def delete(DiagnosticID):
    deleted = DiagnosticModel.query.filter_by(DiagnosticID=DiagnosticID).delete()
    db.session.commit()
    if not deleted:
        return fail_api(msg="删除失败，诊断信息不存在")
    return success_api(msg="删除成功")