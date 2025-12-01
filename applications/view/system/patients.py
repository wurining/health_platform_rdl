from flask import Blueprint, render_template, request, current_app, jsonify
from flask_login import login_required, current_user
from sqlalchemy import desc, or_, case

from applications.common import curd
from applications.common.curd import enable_status, disable_status
from applications.common.utils.http import table_api, fail_api, success_api
from applications.common.utils.rights import authorize
from applications.common.utils.validate import str_escape
from applications.extensions import db
from applications.models import PatientsModel
from applications.schemas import PatientsSchema
from applications.common.curd import model_to_dicts

import uuid,datetime

bp = Blueprint('patients', __name__, url_prefix='/patients')

# 患者管理
@bp.get('/')
@authorize("system:patients:main")
def main():
    return render_template('system/patients/main.html')

#   患者分页查询
@bp.get('/data')
@authorize("system:patients:main")
def data():
    try:
        # 获取请求参数，使用小写变量名符合Python命名规范
        Name = str_escape(request.args.get('Name', type=str))
        patientNo = str_escape(request.args.get('PatientNo', type=str))
        ContactPhone = str_escape(request.args.get('ContactPhone', type=str))
        CustomerType = str_escape(request.args.get('CustomerType', type=str))
        
        # 过滤器
        filters = []
        if Name:
            filters.append(PatientsModel.Name.contains(Name))
        
        if patientNo:
            filters.append(PatientsModel.PatientNo.contains(patientNo))
        
        if ContactPhone:
            filters.append(PatientsModel.ContactPhone.contains(ContactPhone))
        
        if CustomerType:
            filters.append(PatientsModel.CustomerType.contains(CustomerType))

        # 分页对象
        paginated_patients = PatientsModel.query.filter(*filters).order_by(desc(PatientsModel.CreateDate)).layui_paginate()

        # 返回结果
        return table_api(
            data=model_to_dicts(schema=PatientsSchema, data=paginated_patients.items), 
            count=paginated_patients.total
        )
    except Exception as e:
        # 添加异常处理，确保API调用的稳定性
        current_app.logger.error(f"查询患者列表失败: {str(e)}")
        return fail_api(msg="查询患者列表失败，请稍后重试")
    
@bp.get('/search')
@authorize("system:patients:search")
def search():
    """
    患者搜索接口
    支持按姓名、患者编号、手机号进行模糊搜索
    无关键词时返回最近10条患者记录
    """
    # 常量定义
    MAX_RESULTS = 10
    SCORE_EXACT_MATCH = 10
    SCORE_STARTS_WITH = 5
    SCORE_CONTAINS = 1
    
    def _build_match_score(field, keyword):
        """构建字段匹配评分表达式"""
        return case(
            (field == keyword, SCORE_EXACT_MATCH),
            (field.like(keyword + '%'), SCORE_STARTS_WITH),
            (field.contains(keyword), SCORE_CONTAINS),
            else_=0
        )
    
    def _format_result(patient):
        """格式化患者结果为字典"""
        return {
            'value': str(patient.PatientID),
            'name': f"{patient.Name} ({patient.PatientNo})",
            'PatientID': str(patient.PatientID),
            'Name': patient.Name,
            'PatientNo': patient.PatientNo
        }
    
    try:
        # 获取并清理搜索关键词
        keyword = str_escape(request.args.get('keyword', type=str))
        keyword = keyword.strip() if keyword else None
        
        # 构建基础查询，只选择需要的字段
        query = PatientsModel.query.with_entities(
            PatientsModel.Name,
            PatientsModel.PatientNo,
            PatientsModel.PatientID
        )
        
        # 无关键词时返回最近的患者记录
        if not keyword:
            results = query.order_by(
                desc(PatientsModel.CreateDate)
            ).limit(MAX_RESULTS).all()
        else:
            # 构建匹配条件：同时匹配姓名、患者编号、手机号
            filter_condition = or_(
                PatientsModel.Name.contains(keyword),
                PatientsModel.PatientNo.contains(keyword),
                PatientsModel.ContactPhone.contains(keyword)
            )
            
            # 构建综合匹配度评分系统
            # 评分规则：完全匹配=10分，以keyword开头=5分，包含keyword=1分
            name_score = _build_match_score(PatientsModel.Name, keyword)
            patient_no_score = _build_match_score(PatientsModel.PatientNo, keyword)
            phone_score = _build_match_score(PatientsModel.ContactPhone, keyword)
            total_score = name_score + patient_no_score + phone_score
            
            # 查询并排序
            results = query.filter(
                filter_condition
            ).order_by(
                total_score.desc(),
                PatientsModel.Name
            ).limit(MAX_RESULTS).all()
        
        # 格式化结果
        data = [_format_result(r) for r in results]
        
        return table_api(data=data, count=len(data))
        
    except Exception as e:
        current_app.logger.error(f"搜索患者失败: {str(e)}", exc_info=True)
        return fail_api(msg="搜索患者失败，请稍后重试")


# 患者增加
@bp.get('/add')
@authorize("system:patients:add", log=True)
def add():
    # roles = Role.query.all()
    # return render_template('system/patients/add.html', roles=roles)
    return render_template('system/patients/add.html')


@bp.post('/save')
@authorize("system:patients:add", log=True)
def save():
    req_json = request.get_json(force=True)
    Name = str_escape(req_json.get('Name'))
    Sex = str_escape(req_json.get('Sex'))
    Nation = str_escape(req_json.get('Nation'))
    ContactPhone = str_escape(req_json.get('ContactPhone'))
    IdNumber = str_escape(req_json.get('IdNumber'))
    Career = str_escape(req_json.get('Career'))
    CustomerType = str_escape(req_json.get('CustomerType'))
    Birthday = str_escape(req_json.get('Birthday'))
    Address = str_escape(req_json.get('Address'))
    Remarks = str_escape(req_json.get('Remarks'))

    PatientNo = datetime.datetime.now().strftime("%Y%m%d")+str(PatientsModel.query.count()+1)

    # 获取当前用户信息
    current_user_id = current_user.id if current_user.is_authenticated else None
    current_user_name = current_user.realname if (current_user.is_authenticated and current_user.realname) else (current_user.username if current_user.is_authenticated else "系统")

    if not Name or not PatientNo or not Sex or not Nation:
        return fail_api(msg="患者姓名、患者编号、性别、民族不得为空")

    if bool(PatientsModel.query.filter_by(PatientNo=PatientNo).count()):
        return fail_api(msg="患者已经存在")
    
    patient = PatientsModel(
        PatientID=str(uuid.uuid4()), 
        Name=Name,
        PatientNo=PatientNo,
        Sex=Sex, 
        Nation=Nation, 
        ContactPhone=ContactPhone,
        IdNumber=IdNumber,
        Career=Career,
        CustomerType=CustomerType,
        Birthday=datetime.datetime.strptime(Birthday, '%Y-%m-%d') if Birthday else None,
        Address=Address,
        Remarks=Remarks,
        CreateID=current_user_id,
        Creator=current_user_name,
        CreateDate=datetime.datetime.now(),
        ModifyID=current_user_id,
        Modifier=current_user_name,
        ModifyDate=datetime.datetime.now()
    )
    db.session.add(patient)
    db.session.commit()

    return success_api(msg="增加成功")


#  编辑患者
@bp.get('/edit/<string:PatientID>')
@authorize("system:patients:edit", log=True)
def edit(PatientID):
    # patient = curd.get_one_by_id(Patients, PatientID)
    patient = PatientsModel.query.filter_by(PatientID=PatientID).first()

    return render_template('system/patients/edit.html', patient_res=patient)


# 获取患者详情（API接口）
@bp.get('/detail/<string:PatientID>')
@authorize("system:patients:main")
def detail_api(PatientID):
    """
    获取单个患者详情的API接口
    返回JSON格式的患者信息
    """
    try:
        patient = PatientsModel.query.filter_by(PatientID=PatientID).first()
        if not patient:
            return fail_api(msg="患者信息不存在")
        
        # 使用Schema序列化患者数据
        schema = PatientsSchema()
        patient_data = schema.dump(patient)
        
        return success_api(msg="获取成功", data=patient_data)
    except Exception as e:
        current_app.logger.error(f"获取患者详情失败: {str(e)}")
        return fail_api(msg=f"获取患者详情失败: {str(e)}")

#  编辑患者
@bp.put('/update')
@authorize("system:patients:edit", log=True)
def update():
    req_json = request.get_json(force=True)
    Name = str_escape(req_json.get('Name'))
    Sex = str_escape(req_json.get('Sex'))
    Nation = str_escape(req_json.get('Nation'))
    ContactPhone = str_escape(req_json.get('ContactPhone'))
    IdNumber = str_escape(req_json.get('IdNumber'))
    Career = str_escape(req_json.get('Career'))
    CustomerType = str_escape(req_json.get('CustomerType'))
    Birthday = str_escape(req_json.get('Birthday'))
    Address = str_escape(req_json.get('Address'))
    Remarks = str_escape(req_json.get('Remarks'))
    PatientNo = str_escape(req_json.get('PatientNo'))

    PatientID = str_escape(req_json.get('PatientID'))

    # 获取当前用户信息
    current_user_id = current_user.id if current_user.is_authenticated else None
    current_user_name = current_user.realname if (current_user.is_authenticated and current_user.realname) else (current_user.username if current_user.is_authenticated else "系统")

    data = {
        'Name': Name,
        'Sex': Sex,
        'Nation': Nation,
        'ContactPhone': ContactPhone,
        'IdNumber': IdNumber,
        'Career': Career,
        'CustomerType': CustomerType,
        'Birthday': datetime.datetime.strptime(Birthday, '%Y-%m-%d') if Birthday else None,
        'Address': Address,
        'PatientNo': PatientNo,
        'Remarks': Remarks,
        'ModifyID': current_user_id,
        'Modifier': current_user_name,
        'ModifyDate': datetime.datetime.now()
    }
    if not Name or not PatientNo or not Sex or not Nation:
        return fail_api(msg="患者姓名、患者编号、性别、民族不得为空")
    
    PatientsModel.query.filter_by(PatientID=PatientID).update(data)
    db.session.commit()

    return success_api(msg="更新成功")


# 删除患者
@bp.delete('/remove/<string:PatientID>')
@authorize("system:patients:remove", log=True)
def delete(PatientID):
    res = PatientsModel.query.filter_by(PatientID=PatientID).delete()
    db.session.commit()
    if not res:
        return fail_api(msg="删除失败")
    return success_api(msg="删除成功")


# 启用患者
@bp.put('/enable')
@authorize("system:patients:edit", log=True)
def enable():
    _id = request.get_json(force=True).get('userId')
    if _id:
        res = enable_status(model=PatientsModel, id=_id)
        if not res:
            return fail_api(msg="出错啦")
        return success_api(msg="启动成功")
    return fail_api(msg="数据错误")


# 禁用患者
@bp.put('/disable')
@authorize("system:patients:edit", log=True)
def dis_enable():
    _id = request.get_json(force=True).get('userId')
    if _id:
        res = disable_status(model=PatientsModel, id=_id)
        if not res:
            return fail_api(msg="出错啦")
        return success_api(msg="禁用成功")
    return fail_api(msg="数据错误")