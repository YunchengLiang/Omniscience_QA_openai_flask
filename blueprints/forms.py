import wtforms
from wtforms.validators import Email, Length, EqualTo, InputRequired
from models import User, EmailCaptcha
from exts import db

# Use to validate the data send from front-end and check if the data is valid
class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message='Email address form invalid')])
    captcha = wtforms.StringField(validators=[Length(min=6, max=6, message='Captcha form invalid')])
    username = wtforms.StringField(validators=[Length(min=3, max=20, message='Username form invalid, keep it between 3 and 20 characters')])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message='Password form invalid, keep it between 6 and 20 characters')])
    password_confirm = wtforms.StringField(validators=[EqualTo('password', message='Password does not match')])

    #check if email was already registered
    def validate_email(self, field):
        email = field.data
        user = User.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError('Email already registered')
    #check if captcha is correct
    def validate_captcha(self, field):
        email = self.email.data
        captcha = field.data
        email_captcha = EmailCaptcha.query.filter_by(email=email,captcha=captcha).first()
        if not email_captcha:
            raise wtforms.ValidationError('Email not sent')
        else:
            db.session.delete(email_captcha)
            db.session.commit()

class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message='Email address form invalid')])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message='Password form invalid, keep it between 6 and 20 characters')])

class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[Length(min=3, max=100, message='Title form invalid, keep it between 3 and 100 characters')])
    content = wtforms.StringField(validators=[Length(min=3, message='Content form invalid, keep it more than 3 characters')])

class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[Length(min=3, message='Content form invalid, keep it more than 3 characters')])
    question_id = wtforms.IntegerField(validators=[InputRequired(message='Question id is required')])