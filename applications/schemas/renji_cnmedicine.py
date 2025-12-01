from flask_marshmallow.sqla import SQLAlchemyAutoSchema

from applications.models import CnmedicineModel


class CnmedicineSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CnmedicineModel  # table = models.Album.__table__
        # include_relationships = True  # 输出模型对象时同时对外键，是否也一并进行处理
        include_fk = True  # 序列化阶段是否也一并返回主键
        # fields= ["id","name"] # 启动的字段列表
        # exclude = ["id","name"] # 排除字段列表

# CREATE TABLE `renji_cnmedicine` (
#   `MedicineID` varchar(36) NOT NULL COMMENT '中药ID',
#   `MedicineName` varchar(100) DEFAULT NULL COMMENT '中药名称',
#   `MedicineType` varchar(100) DEFAULT NULL COMMENT '中药类型',
#   `MedicineInstruction` text COMMENT '药品说明',
#   `MedicineUse` text COMMENT '用法用量',
#   `Remarks` text COMMENT '备注',
#   `CreateID` int(11) DEFAULT NULL COMMENT '创建人ID',
#   `Creator` varchar(100) DEFAULT NULL COMMENT '创建人',
#   `CreateDate` datetime DEFAULT NULL COMMENT '创建时间',
#   `ModifyID` int(11) DEFAULT NULL COMMENT '修改人ID',
#   `Modifier` varchar(100) DEFAULT NULL COMMENT '修改人',
#   `ModifyDate` datetime DEFAULT NULL COMMENT '修改时间',
#   PRIMARY KEY (`MedicineID`) USING BTREE
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;