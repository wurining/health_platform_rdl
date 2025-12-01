import datetime
import json
from applications.extensions import db
from .renji_patients import PatientsModel

class DiagnosticModel(db.Model):
    __tablename__ = 'renji_diagnostic'
    DiagnosticID = db.Column(db.String(36), primary_key=True, comment='诊断ID')
    PatientID = db.Column(db.String(36), db.ForeignKey('renji_patients.PatientID'), comment='患者ID')
    Diagnosis = db.Column(db.Text, comment='诊断（多标签，JSON数组格式）')
    OtherHospitalDiagnosis = db.Column(db.Text, comment='其他医院诊断')
    Pathology = db.Column(db.Text, comment='病理')
    AttachMents = db.Column(db.Text, comment='附件（多图片，JSON数组格式）')
    Remarks = db.Column(db.Text, comment='备注')
    CreateID = db.Column(db.Integer, comment='创建人ID')
    Creator = db.Column(db.String(100), comment='创建人')
    ModifyID = db.Column(db.Integer, comment='修改人ID')
    Modifier = db.Column(db.String(100), comment='修改人')
    CreateDate = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    ModifyDate = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='修改时间')

    patient = db.relationship(
        PatientsModel,
        backref=db.backref('diagnostic_records', lazy='dynamic'),
        lazy='joined'
    )
    
    def get_diagnosis_list(self):
        """获取诊断标签列表"""
        if not self.Diagnosis:
            return []
        try:
            return json.loads(self.Diagnosis) if isinstance(self.Diagnosis, str) else self.Diagnosis
        except:
            # 兼容旧数据格式（逗号分隔）
            return [d.strip() for d in self.Diagnosis.split(',') if d.strip()] if self.Diagnosis else []
    
    def set_diagnosis_list(self, diagnosis_list):
        """设置诊断标签列表"""
        if diagnosis_list:
            self.Diagnosis = json.dumps(diagnosis_list, ensure_ascii=False)
        else:
            self.Diagnosis = None
    
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


# CREATE TABLE `renji_diagnostic` (
#   `DiagnosticID` varchar(36) NOT NULL COMMENT '诊断ID',
#   `DiagnosticName` varchar(100) DEFAULT NULL COMMENT '诊断名称',
#   `DiagnosticType` varchar(100) DEFAULT NULL COMMENT '诊断类型',
#   `DiagnosticReason` text COMMENT '诊断原因',
#   `Remarks` text COMMENT '备注',
#   `CreateID` int(11) DEFAULT NULL COMMENT '创建人ID',
#   `Creator` varchar(100) DEFAULT NULL COMMENT '创建人',
#   `CreateDate` datetime DEFAULT NULL COMMENT '创建时间',
#   `ModifyID` int(11) DEFAULT NULL COMMENT '修改人ID',
#   `Modifier` varchar(100) DEFAULT NULL COMMENT '修改人',
#   `ModifyDate` datetime DEFAULT NULL COMMENT '修改时间',
#   PRIMARY KEY (`DiagnosticID`) USING BTREE
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;