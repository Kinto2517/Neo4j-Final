from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from Researchers.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Kullanıcı Adı',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Şifre', validators=[DataRequired()])
    confirm_password = PasswordField('Şifrenizi Tekrar Giriniz',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Kayıt Ol')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class DataForm(FlaskForm):
    aid = StringField('Araştırmacı ID',
                      validators=[DataRequired(), Length(min=1, max=30)])
    aadı = StringField('Araştırmacı Adı', validators=[DataRequired(), Length(min=1, max=30)])

    asoyadı = StringField('Araştırmacı Soyadı',
                          validators=[DataRequired(), Length(min=2, max=30)])
    yadı = StringField('Yayın Adı',
                       validators=[DataRequired(), Length(min=2, max=250)])
    yyılı = StringField('Yayın Yılı',
                        validators=[DataRequired(), Length(min=2, max=30)])
    tadı = StringField('Yayın Türü',
                       validators=[DataRequired(), Length(min=2, max=20)])
    tyeri = StringField('Yayın Yeri',
                        validators=[DataRequired(), Length(min=2, max=90)])

    submit = SubmitField('NeoDB')


class DataForm1(FlaskForm):
    aid = StringField('Araştırmacı ID',
                      validators=[DataRequired(), Length(min=1, max=30)])
    aadı = StringField('Araştırmacı Adı', validators=[DataRequired(), Length(min=1, max=30)])

    asoyadı = StringField('Araştırmacı Soyadı',
                          validators=[DataRequired(), Length(min=2, max=30)])

    submit = SubmitField('NeoDB')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Şifre', validators=[DataRequired()])
    remember = BooleanField('Beni Hatırla')
    submit = SubmitField('Giriş Yap')


class AdminLoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Şifre', validators=[DataRequired()])
    remember = BooleanField('Beni Hatırla')
    submit = SubmitField('Giriş Yap')


class UpdateAccountForm(FlaskForm):
    username = StringField('Kullanıcı Adı',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Profil Fotoğrafı Güncelle', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Güncelle')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Bu kullanıcı adı alınmıştır.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Bu email alınmıştır. Başka email seçiniz')
