from flask import Flask, render_template,session, g
import config
from exts import db,mail
from models import User
from blueprints import *
from flask_migrate import Migrate


app=Flask(__name__)
app.config.from_object(config)

db.init_app(app)
mail.init_app(app)

migrate=Migrate(app, db)

app.register_blueprint(auth_bp)
app.register_blueprint(qa_bp)
#blueprint is a way to organize the code

#beforer_request is a decorator that will run the function before the request
#after_request is a decorator that will run the function after the request
#before_first_request is a decorator that will run the function before the first request
#hook functions are functions that will run before or after the request

@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        setattr(g, 'user', user)
    else:
        setattr(g, 'user', None)

@app.context_processor
def my_context_processor():
    return {'user':g.user}
    



@app.route('/')
def hello_world():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)