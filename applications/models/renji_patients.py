import datetime
from applications.extensions import db

class PatientsModel(db.Model):
    __tablename__ = 'renji_patients'
    PatientID = db.Column(db.String(36), primary_key=True, comment='患者ID')
    Name = db.Column(db.String(100), comment='患者姓名')
    PatientNo = db.Column(db.String(100), comment='患者编号')
    Sex = db.Column(db.String(100), comment='性别')
    Nation = db.Column(db.String(100), comment='民族')
    Birthday = db.Column(db.DateTime, comment='生日')
    ContactPhone = db.Column(db.String(100), comment='电话')
    Address = db.Column(db.String(100), comment='联系地址')
    IdNumber = db.Column(db.String(100), comment='证件号')
    Career = db.Column(db.String(100), comment='职业')
    Remarks = db.Column(db.String(255), comment='备注信息')
    CustomerType = db.Column(db.String(255), comment='推荐人')
    CreateID = db.Column(db.Integer, comment='创建人ID')
    Creator = db.Column(db.String(100), comment='创建人')
    ModifyID = db.Column(db.Integer, comment='修改人ID')
    Modifier = db.Column(db.String(100), comment='修改人')
    CreateDate = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    ModifyDate = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='修改时间')
    # power = db.relationship('Power', secondary="admin_role_power", backref=db.backref('role'))

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