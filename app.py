import sqlite3
import os
from flask import Flask, render_template, request, g, flash, abort, redirect, url_for, make_response
from investStore.FDataBase import FDataBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from investStore.UserLogin import UserLogin
from investStore.forms import LoginForm, RegisterForm, StatementForm
from werkzeug.datastructures import MultiDict

# конфигурация
DATABASE = '/tmp/investStore.db'
DEBUG = True
SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'
MAX_CONTENT_LENGTH = 1024 * 1024

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path,'investStore.db')))

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
login_manager.login_message_category = "success"


@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id, dbase)


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    """Вспомогательная функция для создания таблиц БД"""
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db():
    '''Соединение с БД, если оно еще не установлено'''
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


dbase = None
@app.before_request
def before_request():
    """Установление соединения с БД перед выполнением запроса"""
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@app.teardown_appcontext
def close_db(error):
    '''Закрываем соединение с БД, если оно было установлено'''
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route("/")
def index():
    return render_template('index.html', is_auth = current_user.is_authenticated)

@app.route("/add/statement", methods=["POST", "GET"])
@login_required
def add_statement():
    form = StatementForm()
    if form.validate_on_submit():
        dbase.addStatement(form.number.data, form.title.data, form.text.data, current_user.get_id())
    return render_template('add_statement.html', title="Добавление статьи", form=form, is_auth = current_user.is_authenticated)


@app.route("/statement/<int:id>")
@login_required
def show_statement(id):
    statement = dbase.getStatement(id)

    if not statement:
        abort(404)

    return render_template('statement.html',statement = statement, is_auth = current_user.is_authenticated)


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = dbase.getUserByEmail(form.email.data)
        if user and check_password_hash(user['psw'], form.psw.data):
            userlogin = UserLogin().create(user)
            rm = form.remember.data
            login_user(userlogin, remember=rm)
            return redirect(url_for("index"))

        flash("Неверная пара логин/пароль", "error")

    return render_template("login.html", title="Авторизация", form=form)


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
            hash = generate_password_hash(request.form['psw'])
            res = dbase.addUser(form.name.data, form.email.data, hash)
            if res:
                flash("Вы успешно зарегистрированы", "success")
                return redirect(url_for('login'))
            else:
                flash("Ошибка при регистрации", "error")

    return render_template("register.html", title="Регистрация", form=form, is_auth = current_user.is_authenticated)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    is_admin = dbase.getUserRole(current_user.get_id())
    user_statements = dbase.getUserStatements(current_user.get_id())
    return render_template("profile.html",
                            title="Профиль",
                            is_auth = current_user.is_authenticated,
                            is_admin = is_admin['is_admin'],
                            statements=user_statements)

@app.route('/admin/statements', methods=["POST", "GET"])
@login_required
def admin_statements():
    is_admin = dbase.getUserRole(current_user.get_id())
    print(type(is_admin['is_admin']))
    if not is_admin['is_admin']:
        abort(403)
    if request.method == "GET":
        user_statements = dbase.getAllStatements()
    if request.method == "POST":
        json_data = request.get_json()
        dbase.updateApprove(json_data['id'], json_data['approve'])
        return {
            'response' : 'данные отправленны коректно'
        }
    return render_template("admin_statements.html",
                            title="Все заявления",
                            is_auth = current_user.is_authenticated,
                            statements=user_statements)

if __name__ == "__main__":
    app.run(debug=True)
