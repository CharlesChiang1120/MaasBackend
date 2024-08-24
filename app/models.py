from server import db
from sqlalchemy.dialects.mysql import JSON
from datetime import datetime

class UserModel(db.Model):
    __tablename__ = 'useraccount'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    mail = db.Column(db.String(100), nullable=False)
    passengercustom_1 = db.Column(db.String(50), nullable=True)
    passengercustom_2 = db.Column(db.String(50), nullable=True)
    passengercustom_3 = db.Column(db.String(50), nullable=True)
    payment = db.Column(db.SmallInteger, nullable=True)
    deleted = db.Column(db.SmallInteger, nullable=True)
    phonenumber = db.Column(db.String(20), nullable=True)
    pickuplocation = db.Column(db.String(50), nullable=True)

    def __init__(self, name, gender, mail, passengercustom_1=None, passengercustom_2=None, passengercustom_3=None, payment=None, deleted=None, phonenumber=None, pickuplocation=None):
        self.name = name
        self.gender = gender
        self.mail = mail
        self.passengercustom_1 = passengercustom_1
        self.passengercustom_2 = passengercustom_2
        self.passengercustom_3 = passengercustom_3
        self.payment = payment
        self.deleted = deleted
        self.phonenumber = phonenumber
        self.pickuplocation = pickuplocation

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'mail': self.mail,
            'passengercustom_1': self.passengercustom_1,
            'passengercustom_2': self.passengercustom_2,
            'passengercustom_3': self.passengercustom_3,
            'payment': self.payment,
            'deleted': self.deleted,
            'phonenumber': self.phonenumber,
            'pickuplocation': self.pickuplocation
        }
    

class ActivityModel(db.Model):
    __tablename__ = 'activity'

    activityid = db.Column(db.String(36), primary_key=True)
    activityinfo = db.Column(db.String(100))
    activitydate = db.Column(db.DateTime)
    destination = db.Column(db.String(50))
    image = db.Column(db.String(500))
    tags = db.Column(db.JSON)
    userdistance = db.Column(db.String(20))
    availablepickuplocation = db.Column(db.JSON)
    ticketlink = db.Column(db.String(1000))

    def __init__(self, activityid, activityinfo, activitydate, destination, image, tags, userdistance, availablepickuplocation, ticketlink):
        self.activityid = activityid
        self.activityinfo = activityinfo
        self.activitydate = activitydate
        self.destination = destination
        self.image = image
        self.tags = tags
        self.userdistance = userdistance
        self.availablepickuplocation = availablepickuplocation
        self.ticketlink = ticketlink

    def serialize(self):
        return {
            'activityid': self.activityid,
            'activityinfo': self.activityinfo,
            'activitydate': self.activitydate.strftime('%Y-%m-%d %H:%M:%S') if self.activitydate else None,
            'destination': self.destination,
            'image': self.image,
            'tags': self.tags,
            'userdistance': self.userdistance,
            'availablepickuplocation': self.availablepickuplocation,
            'ticketlink': self.ticketlink
        }

