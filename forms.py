from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,Length

class LoginForm(FlaskForm):
    username=StringField("Username: ",validators=[DataRequired()])
    password=PasswordField("Contrasena : ",validators=[DataRequired()])
    boton=SubmitField("Iniciar Sesion")

class EditProfileForm(FlaskForm):
    name = StringField('Nombre real', validators=[Length(0, 64)])
    location = StringField('Locación', validators=[Length(0, 64)])
    about_me = TextAreaField('Sobre mi')
    submit = SubmitField('Actualizar')
