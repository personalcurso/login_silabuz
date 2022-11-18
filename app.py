from flask import Flask,render_template,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import current_user, login_user,login_required
from forms import LoginForm
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_login import logout_user

app = Flask(__name__)

login = LoginManager(app)
login.login_view = 'login'

app.config['SECRET_KEY']= os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI']= os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')

db=SQLAlchemy(app)
Migrate(app,db)

@app.route('/')
@login_required
def index():
    return render_template('indexCss.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


from models.user import User,Permission
from models.post import Post
@app.route('/login',methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: #si no esta autenticado

        return redirect(url_for('index'))
    #Se arma el login
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=True)
        return redirect(url_for('index'))

    return render_template('login.html',form=form)


from decorator import admin_required,permission_required

@app.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return "Para admins!"


@app.route('/moderate')
@login_required
@permission_required(Permission.MODERATE)
def for_moderators_only():
    return "Para comentarios de moderadores!"


@app.route("/insert")
def insert():
    u = User(username = "aula1_prueba", email = "aula1_prueba@gmail.com")
    u.set_password("789456")
    db.session.add(u)
    db.session.commit()
    return "Insertado"


if __name__ =='__main__':
    app.run(debug=True)
