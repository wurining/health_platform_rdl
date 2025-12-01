from flask_marshmallow.sqla import SQLAlchemyAutoSchema

from applications.models import AppointmentModel


class AppointmentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = AppointmentModel  # table = models.Album.__table__
        # include_relationships = True  # 输出模型对象时同时对外键，是否也一并进行处理
        include_fk = True  # 序列化阶段是否也一并返回主键
        fields = ["AppointmentID", "PatientID", "AppointmentTime", "Remarks", "CreateID", "Creator", "CreateDate", "ModifyID", "Modifier", "ModifyDate"]
        # fields= ["id","name"] # 启动的字段列表
        # exclude = ["id","name"] # 排除字段列表

# CREATE TABLE `renji_appointment` (
#   `AppointmentID` varchar(36) NOT NULL COMMENT '预约ID',
#   `PatientID` varchar(36) DEFAULT NULL COMMENT '患者ID',
#   `AppointmentTime` datetime DEFAULT NULL COMMENT '预约时间',
#   `Remarks` text COMMENT '备注',
#   `CreateID` int(11) DEFAULT NULL COMMENT '创建人ID',
#   `Creator` varchar(100) DEFAULT NULL COMMENT '创建人',
#   `CreateDate` datetime DEFAULT NULL COMMENT '创建时间',
#   `ModifyID` int(11) DEFAULT NULL COMMENT '修改人ID',
#   `Modifier` varchar(100) DEFAULT NULL COMMENT '修改人',
#   `ModifyDate` datetime DEFAULT NULL COMMENT '修改时间',
#   PRIMARY KEY (`AppointmentID`) USING BTREE
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;