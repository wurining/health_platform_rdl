import datetime
from applications.extensions import db

class PatientmedicalhistoriesModel(db.Model):
    __tablename__ = 'renji_patientmedicalhistories'
    HistoryID = db.Column(db.String(36), primary_key=True, comment='病史ID')
    PatientID = db.Column(db.String(36), comment='患者ID')
    PastHistory = db.Column(db.String(500), comment='既往史')
    PersonalHistory = db.Column(db.String(500), comment='个人史')
    MarriageHistory = db.Column(db.String(500), comment='婚育史')
    FamilyHistory = db.Column(db.String(500), comment='家族史')
    AllergyHistory = db.Column(db.String(500), comment='过敏史')
    MenstrualHistory = db.Column(db.String(500), comment='月经史')
    Other = db.Column(db.String(500), comment='其它')
    Summary = db.Column(db.String(500), comment='小结')
    CreateID = db.Column(db.Integer, comment='创建人ID')
    Creator = db.Column(db.String(100), comment='创建人')
    ModifyID = db.Column(db.Integer, comment='修改人ID')
    Modifier = db.Column(db.String(100), comment='修改人')
    CreateDate = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    ModifyDate = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='修改时间')
    # power = db.relationship('Power', secondary="admin_role_power", backref=db.backref('role'))
