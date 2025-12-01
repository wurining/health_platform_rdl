from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields

from applications.models import RecordsModel


class RecordsSchema(SQLAlchemyAutoSchema):
    PatientName = fields.Method("get_patient_name")
    PatientNo = fields.Method("get_patient_no")

    class Meta:
        model = RecordsModel
        include_fk = True

    @staticmethod
    def get_patient_name(obj):
        patient = getattr(obj, "patient", None)
        return getattr(patient, "Name", None) if patient else None

    @staticmethod
    def get_patient_no(obj):
        patient = getattr(obj, "patient", None)
        return getattr(patient, "PatientNo", None) if patient else None


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
