import datetime
import json
from applications.extensions import db

class ExamlibModel(db.Model):
    __tablename__ = 'renji_examlib'
    ExamID = db.Column(db.String(36), primary_key=True, comment='检查ID')
    PatientID = db.Column(db.String(36), comment='患者ID')
    ExamName = db.Column(db.String(100), comment='检查名称')
    AttachMents = db.Column(db.Text, comment='附件（多图片，JSON数组格式）')
    Remarks = db.Column(db.String(255), comment='备注')
    CreateID = db.Column(db.Integer, comment='创建人ID')
    Creator = db.Column(db.String(100), comment='创建人')
    ModifyID = db.Column(db.Integer, comment='修改人ID')
    Modifier = db.Column(db.String(100), comment='修改人')
    CreateDate = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    ModifyDate = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='修改时间')
    # power = db.relationship('Power', secondary="admin_role_power", backref=db.backref('role'))
    
    def get_attachments_list(self):
        """获取附件列表"""
        if not self.AttachMents:
            return []
        try:
            return json.loads(self.AttachMents) if isinstance(self.AttachMents, str) else self.AttachMents
        except:
            return []
    
    def set_attachments_list(self, attachments_list):
        """设置附件列表"""
        if attachments_list:
            self.AttachMents = json.dumps(attachments_list, ensure_ascii=False)
        else:
            self.AttachMents = None
