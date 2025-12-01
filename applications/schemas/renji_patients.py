from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields
from applications.models import PatientsModel
import datetime

class PatientsSchema(SQLAlchemyAutoSchema):
    Age = fields.Method("calculate_age")
    
    def calculate_age(self, obj):
        """根据生日计算年龄"""
        if obj.Birthday:
            today = datetime.date.today()
            birthday = obj.Birthday.date() if isinstance(obj.Birthday, datetime.datetime) else obj.Birthday
            age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
            return age
        return None
    
    class Meta:
        model = PatientsModel  
        fields = ["PatientID", "Name", "PatientNo", "Sex", "Nation", "Birthday", "Age", "ContactPhone", "Address", "IdNumber", "Career", "Remarks", "CustomerType", "Creator", "CreateDate", "ModifyDate"]

# CREATE TABLE `renji_patients` (
#   `PatientID` varchar(36) NOT NULL COMMENT '患者ID',
#   `Name` varchar(100) NOT NULL COMMENT '患者姓名',
#   `PatientNo` varchar(100) NOT NULL COMMENT '患者编号',
#   `Sex` varchar(100) DEFAULT NULL COMMENT '性别',
#   `Nation` varchar(100) DEFAULT NULL COMMENT '民族',
#   `Birthday` datetime DEFAULT NULL COMMENT '生日',
#   `ContactPhone` varchar(100) DEFAULT NULL COMMENT '电话',
#   `Address` varchar(100) DEFAULT NULL COMMENT '联系地址',
#   `IdNumber` varchar(100) DEFAULT NULL COMMENT '证件号',
#   `Career` varchar(100) DEFAULT NULL COMMENT '职业',
#   `Remarks` varchar(100) DEFAULT NULL COMMENT '备注信息',
#   `CustomerType` varchar(100) DEFAULT NULL COMMENT '推荐人',
#   `CreateID` int(11) DEFAULT NULL COMMENT '创建人ID',
#   `Creator` varchar(100) DEFAULT NULL COMMENT '创建人',
#   `CreateDate` datetime DEFAULT NULL COMMENT '创建时间',
#   `ModifyID` int(11) DEFAULT NULL COMMENT '修改人ID',
#   `Modifier` varchar(100) DEFAULT NULL COMMENT '修改人',
#   `ModifyDate` datetime DEFAULT NULL COMMENT '修改时间',
#   PRIMARY KEY (`PatientID`) USING BTREE
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;