from flask_login import current_user

from applications.common.utils.validate import str_escape
from applications.common.user_agent_parser import parse_user_agent
from applications.extensions import db
from applications.models import AdminLog, User


def login_log(request, uid, is_access):
    """
    记录登录日志
    严格限制：只记录登录相关的操作，URL固定为 /passport/login
    """
    user_agent_str = request.headers.get('User-Agent', '')
    user_agent_info = parse_user_agent(user_agent_str)
    
    # 从表单获取用户名（用于登录失败时记录）
    form_username = request.form.get('username', '') if request.form else ''
    
    # 获取用户名
    username = None
    if uid:
        user = User.query.filter_by(id=uid).first()
        if user:
            username = user.username
    # 如果用户ID为空，使用表单中的用户名
    elif form_username:
        username = form_username
    
    # 获取真实IP（考虑代理情况）
    ip = request.remote_addr
    if request.headers.get('X-Forwarded-For'):
        ip = request.headers.get('X-Forwarded-For').split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        ip = request.headers.get('X-Real-IP')
    
    # 登录日志的URL固定为 /passport/login，确保严格区分
    login_url = '/passport/login'
    
    info = {
        'method': request.method,
        'url': login_url,  # 固定为登录URL，不使用request.path
        'ip': ip,
        'user_agent': str_escape(user_agent_str),
        'desc': str_escape(form_username),
        'uid': uid,
        'username': username or form_username or 'Unknown',
        'browser': user_agent_info.get('browser', 'Unknown'),
        'os': user_agent_info.get('os', 'Unknown'),
        'success': int(is_access)
    }
    log = AdminLog(
        url=info.get('url'),
        ip=info.get('ip'),
        user_agent=info.get('user_agent'),
        desc=info.get('desc'),
        uid=info.get('uid'),
        username=info.get('username'),
        browser=info.get('browser'),
        os=info.get('os'),
        method=info.get('method'),
        success=info.get('success')
    )
    db.session.add(log)
    db.session.flush()
    db.session.commit()
    return log.id


def admin_log(request, is_access, desc=None):
    """
    记录操作日志
    严格限制：排除登录相关的操作，登录操作必须使用 login_log() 函数
    
    :param request: Flask request 对象
    :param is_access: 是否成功访问
    :param desc: 自定义描述信息，如果不提供则自动生成
    """
    # 严格检查：如果是登录相关的URL，不允许使用此函数记录
    request_url = request.path
    if request_url == '/passport/login' or request_url.endswith('/passport/login'):
        # 登录操作应该使用 login_log() 函数，这里不应该记录
        # 如果误调用，直接返回，不记录日志
        return None
    
    request_data = request.json if request.headers.get('Content-Type') == 'application/json' else request.values
    user_agent_str = request.headers.get('User-Agent', '')
    user_agent_info = parse_user_agent(user_agent_str)
    
    # 获取用户名
    username = None
    if current_user and current_user.is_authenticated:
        username = current_user.username
    
    # 获取真实IP（考虑代理情况）
    ip = request.remote_addr
    if request.headers.get('X-Forwarded-For'):
        ip = request.headers.get('X-Forwarded-For').split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        ip = request.headers.get('X-Real-IP')
    
    # 自动识别操作类型和模块
    method = request.method
    operation_type = _get_operation_type(method, request_url)
    module_name = _get_module_name(request_url)
    
    # 生成描述信息
    if desc:
        description = str_escape(desc)
    else:
        # 自动生成描述信息
        description = _generate_description(method, request_url, request_data, operation_type, module_name)
    
    info = {
        'method': method,
        'url': request_url,
        'ip': ip,
        'user_agent': str_escape(user_agent_str),
        'desc': description,
        'uid': current_user.id if current_user and current_user.is_authenticated else None,
        'username': username,
        'browser': user_agent_info.get('browser', 'Unknown'),
        'os': user_agent_info.get('os', 'Unknown'),
        'success': int(is_access),
        'operation_type': operation_type,
        'module_name': module_name
    }
    log = AdminLog(
        url=info.get('url'),
        ip=info.get('ip'),
        user_agent=info.get('user_agent'),
        desc=info.get('desc'),
        uid=info.get('uid'),
        username=info.get('username'),
        browser=info.get('browser'),
        os=info.get('os'),
        method=info.get('method'),
        success=info.get('success'),
        operation_type=info.get('operation_type'),
        module_name=info.get('module_name')
    )
    db.session.add(log)
    db.session.commit()

    return log.id


def _get_operation_type(method, url):
    """根据请求方法和URL识别操作类型"""
    method_map = {
        'GET': '查询',
        'POST': '新增',
        'PUT': '修改',
        'PATCH': '修改',
        'DELETE': '删除'
    }
    
    base_type = method_map.get(method, '未知')
    
    # 根据URL路径进一步细化操作类型
    url_lower = url.lower()
    if 'enable' in url_lower:
        return '启用'
    elif 'disable' in url_lower:
        return '禁用'
    elif 'password' in url_lower or 'pwd' in url_lower:
        return '修改密码'
    elif 'avatar' in url_lower:
        return '修改头像'
    elif 'power' in url_lower or 'permission' in url_lower:
        return '授权'
    elif 'upload' in url_lower:
        return '上传'
    elif 'remove' in url_lower or 'delete' in url_lower:
        return '删除'
    elif 'save' in url_lower and method == 'POST':
        return '新增'
    elif 'update' in url_lower or 'edit' in url_lower:
        return '修改'
    
    return base_type


def _get_module_name(url):
    """从URL中提取模块名称"""
    # 移除开头的 /system/ 前缀
    if url.startswith('/system/'):
        path_parts = url.split('/')
        if len(path_parts) > 2:
            module = path_parts[2]
            # 模块名称映射
            module_map = {
                'user': '用户管理',
                'role': '角色管理',
                'power': '权限管理',
                'dept': '部门管理',
                'dict': '字典管理',
                'mail': '邮件管理',
                'file': '文件管理',
                'log': '日志管理',
                'monitor': '系统监控',
                'patients': '患者管理',
                'appointment': '预约管理',
                'outpatients': '门诊管理',
                'patientmedicalhistories': '病史管理',
                'coursesofdisease': '病程管理',
                'examlib': '检查库管理',
                'cnmedicine': '中药管理',
                'diagnostic': '诊断管理',
                'records': '病案管理',
                'passport': '登录认证'
            }
            return module_map.get(module, module)
    return '未知模块'


def _generate_description(method, url, request_data, operation_type, module_name):
    """自动生成操作描述"""
    # 构建描述信息
    desc_parts = [f"{module_name}-{operation_type}"]
    
    # 尝试从请求数据中提取关键信息
    if request_data:
        data_dict = dict(request_data) if hasattr(request_data, 'items') else {}
        # 提取关键字段
        key_fields = ['username', 'realName', 'realname', 'name', 'roleName', 'deptName', 
                     'powerName', 'typeName', 'dataLabel', 'PatientID', 'AppointmentID',
                     'HistoryID', 'CourseID', 'ExamID', 'MedicineID', 'DiagnosticID', 'RecordID']
        
        key_info = []
        for key in key_fields:
            if key in data_dict:
                value = data_dict[key]
                if value:
                    key_info.append(f"{key}={value}")
                    break  # 只取第一个匹配的关键字段
        
        if key_info:
            desc_parts.append(' '.join(key_info))
    
    return str_escape(' | '.join(desc_parts))
