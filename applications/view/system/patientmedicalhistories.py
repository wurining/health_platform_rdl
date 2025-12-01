from flask import Blueprint, render_template, request, current_app, jsonify, session
from flask_login import login_required, current_user
from sqlalchemy import desc

from applications.common import curd
from applications.common.curd import enable_status, disable_status
from applications.common.utils.http import table_api, fail_api, success_api
from applications.common.utils.rights import authorize
from applications.common.utils.validate import str_escape
from applications.extensions import db
from applications.models import PatientmedicalhistoriesModel, PatientsModel
from applications.schemas import PatientmedicalhistoriesSchema
from applications.common.curd import model_to_dicts

import uuid,datetime

bp = Blueprint('patientmedicalhistories', __name__, url_prefix='/patientmedicalhistories')


# 病史管理
@bp.get('/')
@authorize("system:patientmedicalhistories:main")
def main():
    return render_template('system/patientmedicalhistories/main.html')

#   病史分页查询
@bp.get('/data')
@authorize("system:patientmedicalhistories:main")
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

        # 使用 JOIN 查询，关联 PatientsModel 获取患者信息
        query = db.session.query(PatientmedicalhistoriesModel, PatientsModel).outerjoin(
            PatientsModel, PatientmedicalhistoriesModel.PatientID == PatientsModel.PatientID
        )
        
        # 应用过滤器
        if filters:
            query = query.filter(*filters)

        # 使用 layui_paginate 进行分页
        paginated_result = query.order_by(desc(PatientmedicalhistoriesModel.CreateDate)).layui_paginate()
        
        # 构建返回数据
        data = []
        for history, patient in paginated_result.items:
            item = model_to_dicts(schema=PatientmedicalhistoriesSchema, data=[history])[0]
            # 添加患者信息
            if patient:
                item['PatientNo'] = patient.PatientNo if patient.PatientNo else ""
                item['Name'] = patient.Name if patient.Name else ""
                item['ContactPhone'] = patient.ContactPhone if patient.ContactPhone else ""
            else:
                item['PatientNo'] = ""
                item['Name'] = ""
                item['ContactPhone'] = ""
            data.append(item)

        # 返回结果
        return table_api(data=data, count=paginated_result.total)
    except Exception as e:
        # 添加异常处理，确保API调用的稳定性
        current_app.logger.error(f"查询病史列表失败: {str(e)}")
        return fail_api(msg="查询病史列表失败，请稍后重试")
    

# 病史增加
@bp.get('/add')
@authorize("system:patientmedicalhistories:add", log=True)
def add():
    return render_template('system/patientmedicalhistories/add.html')


@bp.post('/save')
@authorize("system:patientmedicalhistories:add", log=True)
def save():
    try:
        req_json = request.get_json(force=True)
        PatientID = str_escape(req_json.get('PatientID'))
        HistoryID = str_escape(req_json.get('HistoryID'))
        PastHistory = str_escape(req_json.get('PastHistory'))
        PersonalHistory = str_escape(req_json.get('PersonalHistory'))
        MarriageHistory = str_escape(req_json.get('MarriageHistory'))
        FamilyHistory = str_escape(req_json.get('FamilyHistory'))
        AllergyHistory = str_escape(req_json.get('AllergyHistory'))
        MenstrualHistory = str_escape(req_json.get('MenstrualHistory'))
        Other = str_escape(req_json.get('Other'))
        Summary = str_escape(req_json.get('Summary'))
        
        # 获取当前用户信息
        current_user_id = current_user.id if current_user.is_authenticated else None
        current_user_name = current_user.realname if (current_user.is_authenticated and hasattr(current_user, 'realname') and current_user.realname) else (current_user.username if (current_user.is_authenticated and hasattr(current_user, 'username')) else "系统")
        
        if not PatientID:
            return fail_api(msg="患者姓名不得为空")
        
        # 创建新的病史记录
        history = PatientmedicalhistoriesModel(
            HistoryID=str(uuid.uuid4()),
            PatientID=PatientID,
            PastHistory=PastHistory,
            PersonalHistory=PersonalHistory,
            MarriageHistory=MarriageHistory,
            FamilyHistory=FamilyHistory,
            AllergyHistory=AllergyHistory,
            MenstrualHistory=MenstrualHistory,
            Other=Other,
            Summary=Summary,
            CreateID=current_user_id,
            Creator=current_user_name,
            CreateDate=datetime.datetime.now(),
            ModifyID=current_user_id,
            Modifier=current_user_name,
            ModifyDate=datetime.datetime.now()
        )
        db.session.add(history)
        db.session.commit()
        
        return success_api(msg="增加成功")
    except Exception as e:
        current_app.logger.error(f"保存病史失败: {str(e)}")
        db.session.rollback()
        return fail_api(msg=f"保存失败: {str(e)}")


#  编辑病史
@bp.get('/edit/<string:HistoryID>')
@authorize("system:patientmedicalhistories:edit", log=True)
def edit(HistoryID):
    try:
        history = PatientmedicalhistoriesModel.query.filter_by(HistoryID=HistoryID).first()
        if not history:
            from flask import abort
            abort(404, description="病史信息不存在")
        
        # 获取关联的患者信息
        patient = None
        if history.PatientID:
            patient = PatientsModel.query.filter_by(PatientID=history.PatientID).first()
        
        # 将患者信息合并到history对象中，以便模板使用
        if patient:
            history.Name = patient.Name
            history.PatientNo = patient.PatientNo
        else:
            history.Name = ""
            history.PatientNo = ""
        
        return render_template('system/patientmedicalhistories/edit.html', Results=history)
    except Exception as e:
        current_app.logger.error(f"获取病史信息失败: {str(e)}")
        from flask import abort
        abort(500, description="获取病史信息失败")

#  编辑病史
@bp.put('/update')
@authorize("system:patientmedicalhistories:edit", log=True)
def update():
    try:
        req_json = request.get_json(force=True)
        HistoryID = str_escape(req_json.get('HistoryID'))
        PastHistory = str_escape(req_json.get('PastHistory'))
        PersonalHistory = str_escape(req_json.get('PersonalHistory'))
        MarriageHistory = str_escape(req_json.get('MarriageHistory'))
        FamilyHistory = str_escape(req_json.get('FamilyHistory'))
        AllergyHistory = str_escape(req_json.get('AllergyHistory'))
        MenstrualHistory = str_escape(req_json.get('MenstrualHistory'))
        Other = str_escape(req_json.get('Other'))
        Summary = str_escape(req_json.get('Summary'))
        
        # 获取当前用户信息
        current_user_id = current_user.id if current_user.is_authenticated else None
        current_user_name = current_user.realname if (current_user.is_authenticated and hasattr(current_user, 'realname') and current_user.realname) else (current_user.username if (current_user.is_authenticated and hasattr(current_user, 'username')) else "系统")
        
        # 查找病史记录
        history = PatientmedicalhistoriesModel.query.filter_by(HistoryID=HistoryID).first()
        if not history:
            return fail_api(msg="病史信息不存在")
        
        # 由于患者姓名不可修改，直接使用原有的PatientID
        # 更新病史记录
        data = {
            'PastHistory': PastHistory,
            'PersonalHistory': PersonalHistory,
            'MarriageHistory': MarriageHistory,
            'FamilyHistory': FamilyHistory,
            'AllergyHistory': AllergyHistory,
            'MenstrualHistory': MenstrualHistory,
            'Other': Other,
            'Summary': Summary,
            'ModifyID': current_user_id,
            'Modifier': current_user_name,
            'ModifyDate': datetime.datetime.now()
        }
        
        PatientmedicalhistoriesModel.query.filter_by(HistoryID=HistoryID).update(data)
        db.session.commit()
        
        return success_api(msg="更新成功")
    except Exception as e:
        current_app.logger.error(f"更新病史失败: {str(e)}")
        db.session.rollback()
        return fail_api(msg=f"更新失败: {str(e)}")


# 删除病史
@bp.delete('/remove/<string:HistoryID>')
@authorize("system:patientmedicalhistories:remove", log=True)
def delete(HistoryID):
    res = PatientmedicalhistoriesModel.query.filter_by(HistoryID=HistoryID).delete()
    db.session.commit()
    if not res:
        return fail_api(msg="删除失败")
    return success_api(msg="删除成功")



