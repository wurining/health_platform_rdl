import datetime
from applications.extensions import db


class UpdateLog(db.Model):
    __tablename__ = 'admin_updatelog'
    id = db.Column(db.Integer, primary_key=True, comment='更新记录ID')
    title = db.Column(db.String(255), comment='更新标题')
    content = db.Column(db.Text, comment='更新内容')
    version = db.Column(db.String(100), comment='版本号')
    update_type = db.Column(db.String(50), comment='更新类型')
    create_id = db.Column(db.Integer, comment='创建人ID')
    creator = db.Column(db.String(100), comment='创建人')
    modify_id = db.Column(db.Integer, comment='修改人ID')
    modifier = db.Column(db.String(100), comment='修改人')
    create_time = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='更新时间')

