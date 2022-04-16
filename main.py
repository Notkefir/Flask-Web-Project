from flask import Flask, render_template
from flask import Flask, url_for, render_template, make_response, request, jsonify
from werkzeug.utils import redirect

from data.proposal import Proposal
from data.users import User
from data import db_session

from werkzeug.exceptions import abort

from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import reqparse, abort, Api, Resource
from forms.LoginForm import LoginForm
from forms.RegisterForm import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
api = Api(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            specialization=form.specialization.data,
            cost=form.cost.data,
            address=form.address.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/success')
def success():
    return render_template("success.html")


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template("profile.html")


def users_add():
    user = User()
    user.surname = 'aaa'
    user.name = 'ggg'
    user.age = 10
    user.specialization = 'teacher'
    user.cost = 1500.0
    user.address = 'qwe'
    user.email = "scott_chief@mars.org"

    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()


def user_get():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == 1).first()
    # for user in db_sess.query(User).all():
    print(user.name)


if __name__ == '__main__':
    db_session.global_init("db/base.db")
    # db_sess = db_session.create_session()
    # users_add()
    # user_get()
    app.run(port=8080, host='127.0.0.1')
