from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, func
from flask_migrate import Migrate

app = Flask(__name__)

HOSTNAME = '127.0.0.1'
PORT = '3306'
USERNAME = 'root'
PASSWORD = 'root'
DATABASE = 'database_learn'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4'

db=SQLAlchemy(app)
migrate=Migrate(app, db)

# step1: flask db init , only run once
# step2: flask db migrate, every time you change the model
# step3: flask db upgrade, every time you change the model



# with app.app_context():
#     with db.engine.connect() as con:
#         rs = con.execute(text("select 1"))
#         print(rs.fetchone()[0])

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30))

#new_user = User(username='zhangsan', password='123456')
class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(30), nullable=False)
    content = db.Column(db.Text, nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author=db.relationship("User", backref="articles")
    


# with app.app_context():
#     db.create_all()

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/user/add')
def user_add():
    new_user = User(username='zhangsan', password='123456')
    db.session.add(new_user)
    db.session.commit()
    return 'add user success'

@app.route('/user/query')
def user_query():
    user1=User.query.get(1)
    print("user id is {}, username is {}, password is {}".format(user1.id, user1.username, user1.password))
    users=User.query.filter_by(username='zhangsan')
    for user in users:
        print("user id is {}, username is {}, password is {}".format(user.id, user.username, user.password))
    return 'query user success'

@app.route('/user/update')
def user_update():
    user=User.query.filter_by(username='zhangsan').first()
    user.password='222222'
    db.session.commit()
    return 'update user success'

@app.route('/user/delete')
def user_delete():
    user=User.query.filter_by(username='zhangsan').first()
    db.session.delete(user)
    db.session.commit()
    return 'delete user success'

@app.route('/article/add')
def article_add():
    new_article1 = Article(title='article1', content='content1')
    new_article1.author=User.query.get(2)
    new_article2 = Article(title='article2', content='content2')
    new_article2.author=User.query.get(2)
    db.session.add_all([new_article1,new_article2])
    db.session.commit()
    return 'add article success'

@app.route('/article/query')
def article_query():
    user=User.query.get(2)
    for article in user.articles:
        print("article id is {}, title is {}, content is {}".format(article.id, article.title, article.content))
        print("article author id is {}, username is {}".format(article.author.id, article.author.username))
    return 'query article success'



if __name__ == '__main__':
    app.run(debug = True)