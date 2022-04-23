import os

from flask import Flask, render_template
from flask import Flask, url_for, render_template, make_response, request, jsonify
from werkzeug.utils import redirect
from waitress import serve
from data.proposal import Proposal
from data.users import User
from data import db_session, proposals_resources, users_resources

from werkzeug.exceptions import abort

from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import reqparse, abort, Api, Resource
from forms.LoginForm import LoginForm
from forms.ProposalForm import ProposalForm
from forms.RegisterForm import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)


# для одного объекта
api.add_resource(proposals_resources.ProposalsResource, '/api/v2/proposals/<int:proposals_id>')
api.add_resource(users_resources.UsersResource, '/api/v2/users/<int:user_id>')

# для списка объектов
api.add_resource(proposals_resources.ProposalsListResource, '/api/v2/proposals')
api.add_resource(users_resources.UsersListResource, '/api/v2/users')


login_manager = LoginManager()
login_manager.init_app(app)

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
    """ регистрация пользователя """
    form = RegisterForm()
    option = request.form.getlist('specialization')
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
        if 'Репетитор' in option:
            user = User(
                surname=form.surname.data,
                name=form.name.data,
                age=form.age.data,
                about=form.about.data,
                specialization='Репетитор',
                address=form.address.data,
                email=form.email.data
            )
            user.set_password(form.password.data)
        else:
            user = User(
                surname=form.surname.data,
                name=form.name.data,
                age=form.age.data,
                about=form.about.data,
                specialization='Ученик',
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
    """вход в аккаунт"""
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


@app.route('/proposal', methods=['GET', 'POST'])
@login_required
def add_proposals():
    """добавление заявки со стороны репетитора"""
    form = ProposalForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        proposal = Proposal()
        proposal.title = form.title.data
        proposal.phone_number = form.phone_number.data
        proposal.coast = form.coast.data
        current_user.proposal.append(proposal)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/profile')
    return render_template('proposal.html', title='Добавление новости',
                           form=form)


@app.route('/allproposal', methods=['GET', 'POST'])
def all_proposal():
    """ все заявки"""
    db_sess = db_session.create_session()
    proposal = db_sess.query(Proposal).all()
    return render_template("all_proposal.html", proposal=proposal)


@app.route('/logout')
@login_required
def logout():
    """выход из аккаунта"""
    logout_user()
    return redirect("/")


@app.errorhandler(404)
def not_found(error):
    """обработчик для ошибки"""
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/success')
def success():
    return render_template("success.html")


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """профиль залогиненного человека"""
    db_sess = db_session.create_session()
    proposal = db_sess.query(Proposal).filter(Proposal.user == current_user)
    return render_template("profile.html", proposal=proposal)


@app.route('/addproposals/<int:id>', methods=['GET', 'POST'])
@login_required
def add_proposal(id):
    """принятие заяки со стороны ученика"""
    db_sess = db_session.create_session()
    proposal = db_sess.query(Proposal).filter(Proposal.id == id).first()
    need = db_sess.query(Proposal).filter(Proposal.id == proposal.id).first()
    try:
        proposal = Proposal()
        proposal.title = need.title
        proposal.phone_number = need.phone_number
        proposal.coast = need.coast
        current_user.proposal.append(proposal)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/profile')
    except:
        render_template("wrong.html")


@app.route('/proposals/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_proposals(id):
    """редактирование заявки"""
    form = ProposalForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        proposal = db_sess.query(Proposal).filter(Proposal.id == id,
                                                  Proposal.user == current_user,
                                                  ).first()
        if proposal:
            form.title.data = proposal.title
            form.phone_number.data = proposal.phone_number
            form.coast.data = proposal.coast
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        proposal = db_sess.query(Proposal).filter(Proposal.id == id,
                                                  Proposal.user == current_user
                                                  ).first()
        if proposal:
            proposal.title = form.title.data
            proposal.phone_number = form.phone_number.data
            proposal.coast = form.coast.data
            db_sess.commit()
            return redirect('/profile')
        else:
            abort(404)
    return render_template('proposal.html',
                           title='Редактирование заявки',
                           form=form
                           )


@app.route('/proposals_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def proposals_delete(id):
    """удаление заявки по айдишнику"""
    db_sess = db_session.create_session()
    proposal = db_sess.query(Proposal).filter(Proposal.id == id,
                                      Proposal.user == current_user
                                      ).first()
    if proposal:
        db_sess.delete(proposal)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/profile')


@app.route('/delete_account/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_account(id):
    """ Удаление аккаунта """
    if request.method == 'POST':
        if 'delete_button' in list(dict(request.form).keys()):
            db_sess = db_session.create_session()
            proposals = db_sess.query(Proposal).filter(Proposal.user == current_user).all()
            if proposals:
                for i in proposals:
                    if i:
                        db_sess.delete(i)
                        db_sess.commit()
            db_sess = db_session.create_session()
            user_delete = db_sess.query(User).filter(User.id == id).first()
            db_sess.delete(user_delete)
            db_sess.commit()
            return redirect('/')
        else:
            return render_template('del_acc.html', message="Click the button if you're sure")
    return render_template('del_acc.html')


@app.route('/contacts')
def contacts():
    return render_template('contacts.html',
                           title='Контактная информация')


@app.route('/about')
def about():
    return render_template('about.html',
                           title='о проекте')

if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    # app.register_blueprint(news_api.blueprint)
    # app.run(port=8080, host='127.0.0.1')
    port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port)
    app.run(port=port, host='0.0.0.0')
