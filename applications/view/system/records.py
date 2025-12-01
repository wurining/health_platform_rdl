from flask import Blueprint, render_template, request, current_app

from applications.common.curd import model_to_dicts
from applications.common.utils.http import table_api, fail_api, success_api
from applications.common.utils.rights import authorize
from applications.common.utils.validate import str_escape
from applications.extensions import db
from applications.models import RecordsModel, PatientsModel
from applications.schemas import RecordsSchema

import uuid
import datetime

bp = Blueprint('records', __name__, url_prefix='/records')


def _patient_options():
    return PatientsModel.query.with_entities(
        PatientsModel.PatientID,
        PatientsModel.Name,
        PatientsModel.PatientNo
    ).order_by(PatientsModel.Name.asc()).all()


def _parse_datetime(value: str):
    if not value:
        return None
    for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.datetime.strptime(value, fmt)
        except ValueError:
            continue
    return None


@bp.get('/')
@authorize("system:records:main")
def main():
    patients = _patient_options()
    return render_template('system/records/main.html', patients=patients)


@bp.get('/data')
@authorize("system:records:main")
def data():
    try:
        record_number = str_escape(request.args.get('RecordNumber', type=str))
        diagnosis = str_escape(request.args.get('Diagnosis', type=str))
        patient_id = str_escape(request.args.get('PatientID', type=str))

        query = RecordsModel.query
        if record_number:
            query = query.filter(RecordsModel.RecordNumber.contains(record_number))
        if diagnosis:
            query = query.filter(RecordsModel.Diagnosis.contains(diagnosis))
        if patient_id:
            query = query.filter(RecordsModel.PatientID == patient_id)

        paginated = query.order_by(
            RecordsModel.RecordTime.desc(),
            RecordsModel.CreateDate.desc()
        ).layui_paginate()

        return table_api(
            data=model_to_dicts(schema=RecordsSchema, data=paginated.items),
            count=paginated.total
        )
    except Exception as exc:
        current_app.logger.error(f"查询病案信息失败: {exc}")
        return fail_api(msg="查询病案信息失败，请稍后重试")


@bp.get('/add')
@authorize("system:records:add", log=True)
def add():
    patients = _patient_options()
    return render_template('system/records/add.html', patients=patients)


@bp.post('/save')
@authorize("system:records:add", log=True)
def save():
    req_json = request.get_json(force=True)
    record_number = str_escape(req_json.get('RecordNumber'))
    patient_id = str_escape(req_json.get('PatientID'))
    record_time = _parse_datetime(str_escape(req_json.get('RecordTime')))
    diagnosis = str_escape(req_json.get('Diagnosis'))
    other_diagnosis = str_escape(req_json.get('OtherDiagnosis'))
    pathology = str_escape(req_json.get('Pathology'))
    attachments = str_escape(req_json.get('AttachMents'))
    remarks = str_escape(req_json.get('Remarks'))

    if not record_number or not patient_id:
        return fail_api(msg="病案编号与患者信息不得为空")

    if not PatientsModel.query.filter_by(PatientID=patient_id).first():
        return fail_api(msg="患者信息不存在，请重新选择")

    record = RecordsModel(
        RecordID=str(uuid.uuid4()),
        RecordNumber=record_number,
        PatientID=patient_id,
        RecordTime=record_time,
        Diagnosis=diagnosis,
        OtherDiagnosis=other_diagnosis,
        Pathology=pathology,
        AttachMents=attachments,
        Remarks=remarks
    )
    db.session.add(record)
    db.session.commit()
    return success_api(msg="新增病案成功")


@bp.get('/edit/<string:RecordID>')
@authorize("system:records:edit", log=True)
def edit(RecordID):
    record = RecordsModel.query.filter_by(RecordID=RecordID).first()
    if not record:
        return fail_api(msg="病案信息不存在")
    patients = _patient_options()
    return render_template('system/records/edit.html', record=record, patients=patients)


@bp.put('/update')
@authorize("system:records:edit", log=True)
def update():
    req_json = request.get_json(force=True)
    record_id = str_escape(req_json.get('RecordID'))
    record_number = str_escape(req_json.get('RecordNumber'))
    patient_id = str_escape(req_json.get('PatientID'))
    record_time = _parse_datetime(str_escape(req_json.get('RecordTime')))
    diagnosis = str_escape(req_json.get('Diagnosis'))
    other_diagnosis = str_escape(req_json.get('OtherDiagnosis'))
    pathology = str_escape(req_json.get('Pathology'))
    attachments = str_escape(req_json.get('AttachMents'))
    remarks = str_escape(req_json.get('Remarks'))

    if not record_id:
        return fail_api(msg="病案主键缺失")
    if not record_number or not patient_id:
        return fail_api(msg="病案编号与患者信息不得为空")

    if not PatientsModel.query.filter_by(PatientID=patient_id).first():
        return fail_api(msg="患者信息不存在，请重新选择")

    data = {
        'RecordNumber': record_number,
        'PatientID': patient_id,
        'RecordTime': record_time,
        'Diagnosis': diagnosis,
        'OtherDiagnosis': other_diagnosis,
        'Pathology': pathology,
        'AttachMents': attachments,
        'Remarks': remarks
    }

    updated = RecordsModel.query.filter_by(RecordID=record_id).update(data)
    db.session.commit()
    if not updated:
        return fail_api(msg="病案信息不存在或已删除")
    return success_api(msg="更新成功")


@bp.delete('/remove/<string:RecordID>')
@authorize("system:records:remove", log=True)
def delete(RecordID):
    deleted = RecordsModel.query.filter_by(RecordID=RecordID).delete()
    db.session.commit()
    if not deleted:
        return fail_api(msg="删除失败，病案信息不存在")
    return success_api(msg="删除成功")