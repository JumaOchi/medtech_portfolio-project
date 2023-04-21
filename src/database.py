from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import Column, Integer, DateTime
from datetime import datetime
from enum import unique
from sqlalchemy.orm import backref

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)
    Prescriptions = db.relationship('Prescriptions', backref="user")

    def __repr__(self) -> str:
        return 'User>>> {self.username}'
    
class Prescriptions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_no= db.Column(db.Integer, nullable=False)
    meds = db.Column(db.Text, nullable=False)
    tracking = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    medication_time = db.Column(db.DateTime, default=datetime.now)
    meds_taken = db.Column(db.DateTime, onupdate=datetime.now)

    def  __init__(self,**kwargs):
        super().__init__(**kwargs)


    def __repr__(self) -> str:
        return 'Prescription>>> {self.meds}' 
