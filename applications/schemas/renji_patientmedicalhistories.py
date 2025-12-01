from flask_marshmallow.sqla import SQLAlchemyAutoSchema

from applications.models import PatientmedicalhistoriesModel


class PatientmedicalhistoriesSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PatientmedicalhistoriesModel  # table = models.Album.__table__
        # include_relationships = True  # 输出模型对象时同时对外键，是否也一并进行处理
        include_fk = True  # 序列化阶段是否也一并返回主键
        # fields= ["id","name"] # 启动的字段列表
        # exclude = ["id","name"] # 排除字段列表

# CREATE TABLE `renji_patientmedicalhistories` (
#   `HistoryID` varchar(36) NOT NULL COMMENT '病史ID',
#   `PatientID` varchar(36) NOT NULL COMMENT '患者ID',
#   `HistoryType` varchar(100) NOT NULL COMMENT '病史类型',
#   `Sex` varchar(100) DEFAULT NULL COMMENT '病史描述',
#   `Remarks` varchar(100) DEFAULT NULL COMMENT '小结',
#   `CustomerType` varchar(100) DEFAULT NULL COMMENT '推荐人',
#   `CreateID` int(11) DEFAULT NULL COMMENT '创建人ID',
#   `Creator` varchar(100) DEFAULT NULL COMMENT '创建人',
#   `CreateDate` datetime DEFAULT NULL COMMENT '创建时间',
#   `ModifyID` int(11) DEFAULT NULL COMMENT '修改人ID',
#   `Modifier` varchar(100) DEFAULT NULL COMMENT '修改人',
#   `ModifyDate` datetime DEFAULT NULL COMMENT '修改时间',
#   PRIMARY KEY (`HistoryID`) USING BTREE
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;