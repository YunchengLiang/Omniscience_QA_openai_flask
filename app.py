from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, func


app = Flask(__name__)

HOSTNAME = '127.0.0.1'
PORT = '3306'
USERNAME = 'root'
PASSWORD = 'root'
DATABASE = 'database_learn'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4'

db=SQLAlchemy(app)

# with app.app_context():
#     with db.engine.connect() as con:
#         rs = con.execute(text("select 1"))
#         print(rs.fetchone()[0])

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)

#new_user = User(username='zhangsan', password='123456')

with app.app_context():
    db.create_all()

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

if __name__ == '__main__':
    app.run(debug = True)