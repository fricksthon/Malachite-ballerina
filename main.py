from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from os import environ

from forms.add import AddForm
from forms.add_item import AddItemForm
from forms.user import RegisterForm, LoginForm
from data.items import Item
from data.users import User
from data.availability import Availability
from data import db_session

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/db.db")
    port = int(environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    db_sess = db_session.create_session()
    ct = list()
    for i in db_sess.query(Item):
        ct.append(i.content)
    form = AddForm(content=ct)
    if form.validate_on_submit():
        if not form.submit.data:
            return redirect('/add_item')
        add = Availability()
        add.item_id = db_sess.query(Item).filter(
            Item.content == form.item.data).first().id
        add.user_id = db_sess.query(User).filter(
            User.login == current_user.login).first().id
        amo = db_sess.query(Availability).filter((Availability.user_id == add.user_id) & (
            Availability.item_id == add.item_id)).first()
        if amo:
            db_sess.query(Availability).filter((Availability.user_id == add.user_id) & (
                Availability.item_id == add.item_id)).delete()
        else:
            amo = Availability()
            amo.amount = 0
        add.amount = form.number.data + amo.amount
        if add.amount > 0:
            db_sess.add(add)
        db_sess.commit()
        return redirect('/')
    return render_template('add.html', title='Добавление/удаление', form=form)


@app.route('/add_item', methods=['GET', 'POST'])
@login_required
def add_item():
    form = AddItemForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        add = Item()
        add.content = form.item.data
        db_sess.add(add)
        db_sess.commit()
        return redirect('/add')
    return render_template('add_item.html', title='Создание', form=form)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        availability = db_sess.query(Availability).filter(
            Availability.user == current_user)
        items = dict()
        for i in availability:
            items[i.item_id] = db_sess.query(
                Item).filter(Item.id == i.item_id).first()
    else:
        availability = None
        items = None
    return render_template("index.html", availability=availability, items=items)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.login == form.login.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(login=form.login.data)
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
        user = db_sess.query(User).filter(
            User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


if __name__ == '__main__':
    main()
