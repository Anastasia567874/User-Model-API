from flask import Flask, redirect, render_template, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data.users import User
from data.db_session import global_init, create_session
from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField, TextAreaField, IntegerField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField
from forms.user import RegisterForm
from data.jobs import Jobs
from data.departments import Department
from data import db_session, users_api
from requests import get, post


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/mars_explorer.db")
app.register_blueprint(users_api.blueprint)


if __name__ == '__main__':
    app.run()