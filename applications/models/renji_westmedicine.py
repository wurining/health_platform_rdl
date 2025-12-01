import datetime
from applications.extensions import db

class WestmedicineModel(db.Model):
    __tablename__ = 'renji_westmedicine'
    MedicineID = db.Column(db.String(36), primary_key=True, comment='西药ID')
    MedicineName = db.Column(db.String(100), comment='西药名称')
    MedicineType = db.Column(db.String(100), comment='西药类型')
    MedicineInstruction = db.Column(db.Text, comment='药品说明')
    MedicineUse = db.Column(db.Text, comment='用法用量')
    Remarks = db.Column(db.String(255), comment='备注信息')
    CreateID = db.Column(db.Integer, comment='创建人ID')
    Creator = db.Column(db.String(100), comment='创建人')
    ModifyID = db.Column(db.Integer, comment='修改人ID')
    Modifier = db.Column(db.String(100), comment='修改人')
    CreateDate = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    ModifyDate = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='修改时间')
    # power = db.relationship('Power', secondary="admin_role_power", backref=db.backref('role'))

# CREATE TABLE `renji_westmedicine` (
#   `MedicineID` varchar(36) NOT NULL COMMENT '西药ID',
#   `MedicineName` varchar(100) DEFAULT NULL COMMENT '西药名称',
#   `MedicineType` varchar(100) DEFAULT NULL COMMENT '西药类型',
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