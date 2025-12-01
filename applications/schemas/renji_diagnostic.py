from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields

from applications.models import DiagnosticModel


class DiagnosticSchema(SQLAlchemyAutoSchema):
    PatientName = fields.Method("get_patient_name")
    PatientNo = fields.Method("get_patient_no")
    DiagnosisList = fields.Method("get_diagnosis_list")
    AttachmentsList = fields.Method("get_attachments_list")

    class Meta:
        model = DiagnosticModel  # table = models.Album.__table__
        include_fk = True

    @staticmethod
    def get_patient_name(obj):
        patient = getattr(obj, "patient", None)
        return getattr(patient, "Name", None) if patient else None

    @staticmethod
    def get_patient_no(obj):
        patient = getattr(obj, "patient", None)
        return getattr(patient, "PatientNo", None) if patient else None
    
    @staticmethod
    def get_diagnosis_list(obj):
        """获取诊断标签列表"""
        return obj.get_diagnosis_list() if hasattr(obj, 'get_diagnosis_list') else []
    
    @staticmethod
    def get_attachments_list(obj):
        """获取附件列表"""
        return obj.get_attachments_list() if hasattr(obj, 'get_attachments_list') else []


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