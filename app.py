from flask import Flask, render_template
import config
from exts import db
from models import User
from blueprints import *
from flask_migrate import Migrate


app=Flask(__name__)
app.config.from_object(config)

db.init_app(app)

migrate=Migrate(app, db)

app.register_blueprint(auth_bp)
app.register_blueprint(qa_bp)

@app.route('/')
def hello_world():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)