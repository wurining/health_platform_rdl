import datetime
from applications.extensions import db

class AdminLog(db.Model):
    __tablename__ = 'admin_log'
    id = db.Column(db.Integer, primary_key=True)
    method = db.Column(db.String(10))
    uid = db.Column(db.Integer)
    url = db.Column(db.String(255))
    desc = db.Column(db.Text)
    ip = db.Column(db.String(255))
    success = db.Column(db.Integer)
    user_agent = db.Column(db.Text)
    username = db.Column(db.String(50), comment='用户名')
    browser = db.Column(db.String(50), comment='浏览器类型')
    os = db.Column(db.String(50), comment='操作系统')
    location = db.Column(db.String(255), comment='地理位置')
    operation_type = db.Column(db.String(50), comment='操作类型')
    module_name = db.Column(db.String(50), comment='模块名称')
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)