from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin,AnonymousUserMixin
from models.role import Role,Permission
from app import login

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin,db.Model):
    id = db.Column(db.Integer,autoincrement=True, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.username == "abonillago":
                self.role = Role.query.filter_by(name = 'Administrator').first()
        if self.role is None:
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    #Roles de verificacion
    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)
    def is_administrator(self):
        return self.can(Permission.ADMIN)


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False
    def is_administrator(self):
        return False
login.anonymous_user = AnonymousUser


""" 
    @login.user_loader() #si el usuario esta logeado en cada vista que visita
    def load_user(id):
        return User.query.get(int(id)) """

