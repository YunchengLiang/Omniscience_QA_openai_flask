from flask import Blueprint, render_template, request,g, redirect, url_for
from .forms import QuestionForm
from models import Question
from exts import db
from decorators import login_required

bp = Blueprint('qa', __name__, url_prefix='/')

@bp.route('/')
def index():
    return 'Hello World!'

@bp.route('/qa/public', methods=['GET', 'POST'])
@login_required
def public_question():
    if not g.user:
        return redirect(url_for('auth.login'))
    if request.method == 'GET':
        return render_template('public_questions.html')
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = Question(title=title, content=content, author=g.user)
            db.session.add(question)
            db.session.commit()
            return redirect('/')
        else:
            print(form.errors)
            return redirect(url_for('qa.public_question'))