import datetime
from applications.extensions import db
from .renji_patients import PatientsModel

class RecordsModel(db.Model):
    __tablename__ = 'renji_records'
    RecordID = db.Column(db.String(36), primary_key=True, comment='基本病情Id')
    RecordNumber = db.Column(db.String(100), comment='病案编号')
    PatientID = db.Column(db.String(36), db.ForeignKey('renji_patients.PatientID'), comment='患者ID')
    RecordTime = db.Column(db.DateTime, comment='初诊时间')
    Diagnosis = db.Column(db.String(100), comment='诊断')
    OtherDiagnosis = db.Column(db.String(100), comment='他院诊断')
    Pathology = db.Column(db.String(100), comment='病理')
    AttachMents = db.Column(db.Text, comment='附件')
    Remarks = db.Column(db.String(255), comment='备注信息')
    CreateID = db.Column(db.Integer, comment='创建人ID')
    Creator = db.Column(db.String(100), comment='创建人')
    ModifyID = db.Column(db.Integer, comment='修改人ID')
    Modifier = db.Column(db.String(100), comment='修改人')
    CreateDate = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    ModifyDate = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='修改时间')

    patient = db.relationship(
        PatientsModel,
        backref=db.backref('records', lazy='dynamic'),
        lazy='joined'
    )


# CREATE TABLE `renji_records` (
#   `RecordID` varchar(36) NOT NULL COMMENT '基本病情Id',
#   `RecordNumber` varchar(100) DEFAULT NULL COMMENT '病案编号',
#   `PatientID` varchar(36) NOT NULL COMMENT '患者ID',
#   `RecordTime` datetime DEFAULT NULL COMMENT '初诊时间',
#   `Diagnosis` varchar(100) DEFAULT NULL COMMENT '诊断',
#   `OtherDiagnosis` varchar(100) NOT NULL COMMENT '他院诊断',
#   `Pathology` varchar(100) DEFAULT NULL COMMENT '病理',
#   `AttachMents` text COMMENT '附件',
#   `Remarks` text COMMENT '备注',
#   `CreateID` int(11) DEFAULT NULL COMMENT '创建人ID',
#   `Creator` varchar(100) DEFAULT NULL COMMENT '创建人',
#   `CreateDate` datetime DEFAULT NULL COMMENT '创建时间',
#   `ModifyID` int(11) DEFAULT NULL COMMENT '修改人ID',
#   `Modifier` varchar(100) DEFAULT NULL COMMENT '修改人',
#   `ModifyDate` datetime DEFAULT NULL COMMENT '修改时间',
#   PRIMARY KEY (`RecordID`) USING BTREE
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;
