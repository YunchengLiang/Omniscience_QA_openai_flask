from flask import Blueprint, render_template, request,g, redirect, url_for, flash
from .forms import QuestionForm, AnswerForm
from models import Question, Answer
from exts import db
from decorators import login_required
import openai

bp = Blueprint('qa', __name__, url_prefix='/')

@bp.route('/')
def index():
    questions=Question.query.order_by(Question.create_time.desc()).all()
    return render_template('index.html',questions=questions)

@bp.route('/qa/public', methods=['GET', 'POST'])
@login_required
def public_question():
    if not g.user:
        return redirect(url_for('auth.login'))
    if request.method == 'GET':
        return render_template('public_question.html')
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
        
@bp.route('/qa/detail/<question_id>')
def question_detail(question_id):
    question=Question.query.get(question_id)
    return render_template('detail.html', question=question)

@bp.route("/answer/chatgpt", methods=['POST'])
@login_required
def chatgpt_answer():
    question_id=request.form.get("question_id")
    user_id= Question.query.get(question_id).author_id
    if user_id==g.user.id:
        question_title = Question.query.get(question_id).title
        question_content = Question.query.get(question_id).content
        send_content=question_title+" "+question_content
        openai.api_key="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"
        result=openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=[
            {"role":"user","content":send_content}
        ])
        content= result["choices"][0]["message"]['content']
        answer=Answer(content=content, question_id=question_id, author_id=2)
        db.session.add(answer)
        db.session.commit()
    else:
        flash("Only author of this question could use this function")
    return redirect(url_for('qa.question_detail', question_id=question_id))



@bp.route('/answer/public', methods=['POST'])
@login_required
def public_answer():
    form = AnswerForm(request.form)
    if form.validate():
        content=form.content.data
        question_id=form.question_id.data
        answer=Answer(content=content, question_id=question_id, author_id=g.user.id)
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for('qa.question_detail', question_id=question_id))
    else:
        print(form.errors)
        return redirect(url_for('qa.question_detail', question_id=request.form.get("question_id")))
    
@bp.route("/search")
def search():
    q=request.args.get("q")
    questions=Question.query.filter(Question.title.contains(q)|Question.content.contains(q)).all()
    return render_template("index.html", questions=questions)