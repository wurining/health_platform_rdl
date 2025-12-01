import datetime
from applications.extensions import db

class AppointmentModel(db.Model):
    __tablename__ = 'renji_appointment'
    AppointmentID = db.Column(db.String(36), primary_key=True, comment='预约ID')
    PatientID = db.Column(db.String(255), comment='患者ID')
    AppointmentTime = db.Column(db.String(255), comment='预约时间')
    Remarks = db.Column(db.String(255), comment='备注')
    CreateID = db.Column(db.Integer, comment='创建人ID')
    Creator = db.Column(db.String(100), comment='创建人')
    ModifyID = db.Column(db.Integer, comment='修改人ID')
    Modifier = db.Column(db.String(100), comment='修改人')
    CreateDate = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    ModifyDate = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='修改时间')
    # power = db.relationship('Power', secondary="admin_role_power", backref=db.backref('role'))


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