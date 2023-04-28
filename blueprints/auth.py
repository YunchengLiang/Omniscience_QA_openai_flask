from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from flask_mail import Message
from exts import db, mail
import string
import random
from models import EmailCaptcha
from .forms import RegisterForm, LoginForm
from models import User
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = LoginForm(request.form)
        if form.validate():
            email=form.email.data
            password=form.password.data
            user=User.query.filter_by(email=email).first()
            if not user:
                print('Email does not exist in the database')
                return redirect(url_for('auth.login'))
            if check_password_hash(user.password, password):
                #cookie
                #cookie is not suitable for storing too much data, only suitable for storing a small amount of data
                #cookie is generally used to store login authorization
                session['user_id']=user.id
                return redirect('/')
            else:
                print('Wrong password')
                return redirect(url_for('auth.login'))
        else:
            print(form.errors)
            return redirect(url_for('auth.login'))
    else:
        return render_template('login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        form = RegisterForm(request.form)
        if form.validate():
            username=form.username.data
            email=form.email.data
            password=form.password.data
            new_user=User(username=username,email=email,password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('auth.register'))



@bp.route('/captcha/email')
def get_email_captcha():
    # /captcha/email/<email>
    # /captcha/email?email=xxx
    email=request.args.get('email')
    source= string.digits*6
    captcha=''.join(random.sample(source,6))
    msg = Message(subject="Omniscience QA Registration Code", recipients=[email], body="Your registration code is {},\
                   please keep it to yourself and do not tell anyone else".format(captcha))
    mail.send(msg)
    #memcached/redis or database on premise
    email_captcha=EmailCaptcha(email=email,captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    #restful api
    return jsonify({"code":200,"message":"","data":None})