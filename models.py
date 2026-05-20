from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Profile(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(100)
    )

    age = db.Column(
        db.Integer
    )

    gender = db.Column(
        db.String(20)
    )

    weight = db.Column(
        db.Float
    )

    height = db.Column(
        db.Float
    )

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(100))
    data = db.Column(db.Text)