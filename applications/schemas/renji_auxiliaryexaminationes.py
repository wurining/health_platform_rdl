from flask_marshmallow.sqla import SQLAlchemyAutoSchema

from applications.models import AuxiliaryexaminationesModel


class AuxiliaryexaminationesSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = AuxiliaryexaminationesModel  # table = models.Album.__table__
        # include_relationships = True  # 输出模型对象时同时对外键，是否也一并进行处理
        include_fk = True  # 序列化阶段是否也一并返回主键
        # fields= ["id","name"] # 启动的字段列表
        # exclude = ["id","name"] # 排除字段列表


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