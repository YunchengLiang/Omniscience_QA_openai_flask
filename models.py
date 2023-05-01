from exts import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)

class EmailCaptcha(db.Model):
    __tablename__ = 'email_captcha'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(30), nullable=False)
    captcha = db.Column(db.String(6), nullable=False)

class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', backref=db.backref('questions'))

class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    #foreign key
    question_id=db.Column(db.Integer, db.ForeignKey('question.id'))
    author_id=db.Column(db.Integer, db.ForeignKey('user.id'))
    #relationship
    question= db.relationship('Question', backref=db.backref('answers', order_by=create_time.desc()))
    author=db.relationship('User', backref=db.backref('answers',order_by=create_time.desc()))