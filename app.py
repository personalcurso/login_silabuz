from flask import Flask,render_template,redirect,url_for,flash,request
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import current_user, login_user,login_required
from forms import LoginForm
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_login import logout_user
import hashlib



app = Flask(__name__)

login = LoginManager(app)
login.login_view = 'login'

app.config['SECRET_KEY']= os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI']= os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')

db=SQLAlchemy(app)
Migrate(app,db)

@app.route('/')
@login_required #tiene que tener la sesion iniciada
def index():
    return render_template('indexCss.html') #para pooder ver este indexCss.html

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
            flash('Usuario o contraseña no valida')
            return redirect(url_for('login'))


        login_user(user, remember=True)
        next_=request.args.get("next")
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



def gravatar(email="", size=100, default="identicon", rating="g"):
    url = "https://secure.gravatar.com/avatar"
    hash = hashlib.md5(email.encode("utf-8")).hexdigest()
    return "{url}/{hash}?s={size}&d={default}&r={rating}".format(
        url=url, hash=hash, size=size, default=default, rating=rating
    )

@app.route('/avatar')
def avatar():
    img_avatar=gravatar(current_user.email,size=256)
    return render_template('avatar.html',variable=img_avatar)


@app.errorhandler(404)
def pagina_no_encontrada(e):
  return render_template('404.html')

@app.route('/noexiste')
def usuario_noencontrado():
    return render_template('noexiste.html')

if __name__ =='__main__':
    app.run(debug=True)
