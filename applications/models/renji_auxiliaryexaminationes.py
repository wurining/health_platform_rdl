import datetime
from applications.extensions import db

class AuxiliaryexaminationesModel(db.Model):
    __tablename__ = 'renji_auxiliaryexaminationes'
    ExaminationID = db.Column(db.String(36), primary_key=True, comment='检查ID')
    RecordID = db.Column(db.String(36), comment='病历ID')
    ExaminationType = db.Column(db.String(100), comment='检查类型')
    ExaminerID = db.Column(db.Integer, comment='检查归属')
    ExameTime = db.Column(db.DateTime, comment='检查时间')
    Diagnosis = db.Column(db.Text, comment='辅助检查内容')
    AttachMents = db.Column(db.Text, comment='附件')
    Remarks = db.Column(db.String(255), comment='备注')
    CreateID = db.Column(db.Integer, comment='创建人ID')
    Creator = db.Column(db.String(100), comment='创建人')
    ModifyID = db.Column(db.Integer, comment='修改人ID')
    Modifier = db.Column(db.String(100), comment='修改人')
    CreateDate = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    ModifyDate = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='修改时间')
    # power = db.relationship('Power', secondary="admin_role_power", backref=db.backref('role'))


# CREATE TABLE `renji_auxiliaryexaminationes` (
#   `ExaminationID` varchar(36) NOT NULL COMMENT '检查ID',
#   `RecordID` varchar(36) NOT NULL COMMENT '病历ID',
#   `ExaminationType` varchar(100) DEFAULT NULL COMMENT '检查类型',
#   `ExaminerID` int(11) DEFAULT NULL COMMENT '检查归属',
#   `ExameTime` datetime DEFAULT NULL COMMENT '检查时间',
#   `Diagnosis` text COMMENT '辅助检查内容',
#   `AttachMents` text COMMENT '附件',
#   `Remarks` text COMMENT '备注',
#   `CreateID` int(11) DEFAULT NULL COMMENT '创建人ID',
#   `Creator` varchar(100) DEFAULT NULL COMMENT '创建人',
#   `CreateDate` datetime DEFAULT NULL COMMENT '创建时间',
#   `ModifyID` int(11) DEFAULT NULL COMMENT '修改人ID',
#   `Modifier` varchar(100) DEFAULT NULL COMMENT '修改人',
#   `ModifyDate` datetime DEFAULT NULL COMMENT '修改时间',
#   PRIMARY KEY (`ExaminationID`) USING BTREE
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;