from flask import Blueprint, render_template, request, current_app, jsonify
from flask_login import login_required, current_user
from sqlalchemy import desc, or_, case, func

from applications.common import curd
from applications.common.curd import enable_status, disable_status
from applications.common.utils.http import table_api, fail_api, success_api
from applications.common.utils.rights import authorize
from applications.common.utils.validate import str_escape
from applications.extensions import db
from applications.models import PatientsModel, AppointmentModel, AdminLog, PatientmedicalhistoriesModel, CoursesofdiseaseModel, AuxiliaryexaminationesModel, RecordsModel, DiagnosticModel, ExamlibModel
from applications.schemas import PatientsSchema
from applications.common.curd import model_to_dicts

import uuid,datetime

bp = Blueprint('patientsummary', __name__, url_prefix='/patientsummary')

# 患者总览
@bp.get('/')
@authorize("system:patientsummary:main")
def main():
    return render_template('system/patientsummary/main.html')

# 获取患者统计信息
@bp.get('/statistics')
@authorize("system:patientsummary:main")
def statistics():
    """
    获取患者统计信息
    返回所有患者总数，不过滤任何条件
    """
    try:
        # 获取患者总数，不过滤任何条件
        total_patient_count = PatientsModel.query.count()
        
        return jsonify({
            'success': True,
            'data': {
                'local_count': total_patient_count,
                'total_count': total_patient_count
            }
        })
    except Exception as e:
        current_app.logger.error(f"获取患者统计信息失败: {str(e)}")
        return fail_api(msg="获取患者统计信息失败，请稍后重试")


# 获取预约数量
@bp.get('/appointmentCount')
@authorize("system:patientsummary:main")
def appointmentCount():
    try:
        appointment_count = AppointmentModel.query.count()

        return jsonify({
            'success': True,
            'data': {
                'appointment_count': appointment_count,
                'total_count': appointment_count
            }
        })
    except Exception as e:
        current_app.logger.error(f"获取预约数量失败: {str(e)}")
        return fail_api(msg="获取预约数量失败，请稍后重试", data={
            'appointment_count': None
        })


# 获取登录次数统计
@bp.get('/loginCount')
@authorize("system:patientsummary:main")
def loginCount():
    """
    获取登录次数统计
    统计所有URL为 /passport/login 的日志记录总数
    """
    try:
        # 查询登录日志总数（只统计URL为 /passport/login 的记录）
        login_count = AdminLog.query.filter(AdminLog.url == '/passport/login').count()

        return jsonify({
            'success': True,
            'data': {
                'login_count': login_count,
                'total_count': login_count
            }
        })
    except Exception as e:
        current_app.logger.error(f"获取登录次数统计失败: {str(e)}")
        return fail_api(msg="获取登录次数统计失败，请稍后重试", data={
            'login_count': 0
        })


# 获取最近一个月每天的预约数量
@bp.get('/appointmentDailyStats')
@authorize("system:patientsummary:main")
def appointmentDailyStats():
    """
    获取最近一个月每天的预约数量
    返回格式: {dates: ['2024-01-01', ...], counts: [5, 10, ...]}
    """
    try:
        # 计算最近一个月的日期范围（只比较日期，不比较时间）
        end_date = datetime.datetime.now().replace(hour=23, minute=59, second=59)
        start_date = (end_date - datetime.timedelta(days=29)).replace(hour=0, minute=0, second=0)
        
        # 初始化所有日期的计数为0
        date_counts = {}
        current_date = start_date.date()
        end_date_only = end_date.date()
        while current_date <= end_date_only:
            date_str = current_date.strftime('%Y-%m-%d')
            date_counts[date_str] = 0
            current_date += datetime.timedelta(days=1)
        
        # 查询所有预约记录（由于 AppointmentTime 是字符串，需要全部查询后过滤）
        appointments = AppointmentModel.query.filter(
            AppointmentModel.AppointmentTime.isnot(None)
        ).all()
        
        # 统计每天的预约数量
        for appointment in appointments:
            if appointment.AppointmentTime:
                try:
                    # 尝试解析不同的日期格式
                    appointment_time_str = str(appointment.AppointmentTime).strip()
                    appointment_date = None
                    
                    # 尝试解析 'YYYY-MM-DD HH:MM:SS' 格式
                    try:
                        appointment_date = datetime.datetime.strptime(appointment_time_str, '%Y-%m-%d %H:%M:%S')
                    except:
                        # 尝试解析 'YYYY-MM-DD HH:MM' 格式
                        try:
                            appointment_date = datetime.datetime.strptime(appointment_time_str, '%Y-%m-%d %H:%M')
                        except:
                            # 尝试解析 'YYYY-MM-DD' 格式
                            try:
                                appointment_date = datetime.datetime.strptime(appointment_time_str, '%Y-%m-%d')
                            except:
                                pass
                    
                    if appointment_date:
                        date_str = appointment_date.strftime('%Y-%m-%d')
                        # 只统计最近一个月内的预约（只比较日期部分）
                        appointment_date_only = appointment_date.date()
                        if start_date.date() <= appointment_date_only <= end_date_only:
                            if date_str in date_counts:
                                date_counts[date_str] += 1
                except Exception as e:
                    current_app.logger.warning(f"解析预约时间失败: {appointment.AppointmentTime}, 错误: {str(e)}")
                    continue
        
        # 转换为列表格式，按日期排序
        dates = sorted(date_counts.keys())
        counts = [date_counts[date] for date in dates]
        
        return jsonify({
            'success': True,
            'data': {
                'dates': dates,
                'counts': counts
            }
        })
    except Exception as e:
        current_app.logger.error(f"获取预约每日统计失败: {str(e)}", exc_info=True)
        return fail_api(msg="获取预约每日统计失败，请稍后重试")


# 患者总览分页查询
@bp.get('/data')
@authorize("system:patientsummary:main")
def data():
    try:
        # 获取请求参数
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
        paginated_patientsummary = PatientsModel.query.filter(*filters).order_by(desc(PatientsModel.CreateDate)).layui_paginate()

        # 返回结果
        return table_api(
            data=model_to_dicts(schema=PatientsSchema, data=paginated_patientsummary.items), 
            count=paginated_patientsummary.total
        )
    except Exception as e:
        # 添加异常处理，确保API调用的稳定性
        current_app.logger.error(f"查询患者列表失败: {str(e)}")
        return fail_api(msg="查询患者列表失败，请稍后重试")
    
@bp.get('/search')
@authorize("system:patientsummary:search")
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


# 患者详情
@bp.get('/detail/<string:PatientID>')
@authorize("system:patientsummary:main")
def detail(PatientID):
    """根据患者ID获取患者详情，包括患者信息、病史、检查报告、病程记录"""
    try:
        # 获取患者基本信息
        patient = PatientsModel.query.filter_by(PatientID=PatientID).first()
        if not patient:
            from flask import abort
            abort(404, description="患者信息不存在")
       
        # 获取诊断信息（只获取最新的一条）
        diagnostics = DiagnosticModel.query.filter_by(PatientID=PatientID).order_by(desc(DiagnosticModel.CreateDate)).first()

        # 获取患者病史
        histories = PatientmedicalhistoriesModel.query.filter_by(PatientID=PatientID).order_by(desc(PatientmedicalhistoriesModel.CreateDate)).first()
        current_app.logger.debug(f"患者病史查询成功 -  HistoryID: {histories.HistoryID}")
        
        # 获取病程记录
        courses = CoursesofdiseaseModel.query.filter_by(PatientID=PatientID).order_by(desc(CoursesofdiseaseModel.CourseTime)).all()
        
        # 获取医学检查报告
        examlib = ExamlibModel.query.filter_by(PatientID=PatientID).order_by(desc(ExamlibModel.CreateDate)).all()
        
        # 病程记录
        coursesofdisease = CoursesofdiseaseModel.query.filter_by(PatientID=PatientID).order_by(desc(CoursesofdiseaseModel.CreateDate)).all()
        
        return render_template('system/patientsummary/detail.html', 
                             PatientID=PatientID,
                             patient=patient,
                             diagnostics=diagnostics,
                             histories=histories,
                             courses=courses,
                             examlib=examlib,
                             coursesofdisease=coursesofdisease)
    except Exception as e:
        current_app.logger.error(f"获取患者详情失败: {str(e)}")
        from flask import abort
        abort(500, description=f"获取患者详情失败: {str(e)}")
