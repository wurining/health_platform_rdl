import datetime
import json
from applications.extensions import db

class CoursesofdiseaseModel(db.Model):
    __tablename__ = 'renji_coursesofdisease'
    CourseID = db.Column(db.String(36), primary_key=True, comment='病程ID')
    PatientID = db.Column(db.String(36), comment='患者ID')
    UserID = db.Column(db.Integer, comment='医师')
    CourseType = db.Column(db.String(100), comment='病程类型')
    CourseTime = db.Column(db.DateTime, comment='病程时间')
    CurrentDisease = db.Column(db.String(100), comment='现病史')
    TreatmentPlan = db.Column(db.Text, comment='治疗方案')
    AttachMents = db.Column(db.Text, comment='附件')
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


# CREATE TABLE `renji_coursesofdisease` (
#   `CourseID` varchar(36) NOT NULL COMMENT '病程ID',
#   `PatientID` varchar(36) NOT NULL COMMENT '患者ID',
#   `UserID` int(11) DEFAULT NULL COMMENT '医师',
#   `CourseType` varchar(100) DEFAULT NULL COMMENT '病程类型',
#   `CourseTime` datetime DEFAULT NULL COMMENT '病程时间',
#   `CurrentDisease` varchar(100) DEFAULT NULL COMMENT '现病史',
#   `TreatmentPlan` text COMMENT '治疗方案',
#   `AttachMents` text COMMENT '附件',
#   `Remarks` text COMMENT '备注',
#   `CreateID` int(11) DEFAULT NULL COMMENT '创建人ID',
#   `Creator` varchar(100) DEFAULT NULL COMMENT '创建人',
#   `CreateDate` datetime DEFAULT NULL COMMENT '创建时间',
#   `ModifyID` int(11) DEFAULT NULL COMMENT '修改人ID',
#   `Modifier` varchar(100) DEFAULT NULL COMMENT '修改人',
#   `ModifyDate` datetime DEFAULT NULL COMMENT '修改时间',
#   PRIMARY KEY (`CourseID`) USING BTREE
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;