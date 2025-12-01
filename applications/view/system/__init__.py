from flask import Flask, Blueprint

from applications.view.system.dict import bp as dict_bp
from applications.view.system.file import bp as file_bp
from applications.view.system.index import bp as index_bp
from applications.view.system.log import bp as log_bp
from applications.view.system.mail import bp as mail_bp
from applications.view.system.monitor import bp as monitor_bp
from applications.view.system.passport import bp as passport_bp
from applications.view.system.power import bp as power_bp
from applications.view.system.rights import bp as right_bp
from applications.view.system.role import bp as role_bp
from applications.view.system.user import bp as user_bp
from applications.view.system.dept import bp as dept_bp

from applications.view.system.patients import bp as patients_bp
from applications.view.system.appointment import bp as appointment_bp
from applications.view.system.patientmedicalhistories import bp as patientmedicalhistories_bp
from applications.view.system.records import bp as records_bp
from applications.view.system.examlib import bp as examlib_bp
from applications.view.system.diagnostic import bp as diagnostic_bp
from applications.view.system.coursesofdisease import bp as coursesofdisease_bp
from applications.view.system.outpatients import bp as outpatients_bp
from applications.view.system.patientsummary import bp as patientsummary_bp
from applications.view.system.updatelog import bp as updatelog_bp

# 创建sys
system_bp = Blueprint('system', __name__, url_prefix='/system')

def register_system_bps(app: Flask):
    # 在admin_bp下注册子蓝图
    system_bp.register_blueprint(user_bp)
    system_bp.register_blueprint(file_bp)
    system_bp.register_blueprint(monitor_bp)
    system_bp.register_blueprint(log_bp)
    system_bp.register_blueprint(power_bp)
    system_bp.register_blueprint(role_bp)
    system_bp.register_blueprint(dict_bp)
    system_bp.register_blueprint(mail_bp)
    system_bp.register_blueprint(passport_bp)
    system_bp.register_blueprint(right_bp)
    system_bp.register_blueprint(dept_bp)

    system_bp.register_blueprint(patients_bp)
    system_bp.register_blueprint(appointment_bp)
    system_bp.register_blueprint(patientmedicalhistories_bp)
    system_bp.register_blueprint(records_bp)
    system_bp.register_blueprint(examlib_bp)
    system_bp.register_blueprint(diagnostic_bp)
    system_bp.register_blueprint(coursesofdisease_bp)
    system_bp.register_blueprint(outpatients_bp)
    system_bp.register_blueprint(patientsummary_bp)
    system_bp.register_blueprint(updatelog_bp)


    app.register_blueprint(index_bp)
    app.register_blueprint(system_bp)
