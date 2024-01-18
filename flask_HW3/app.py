from flask import Flask, render_template, request, redirect, url_for
from models import db, User
from flask_wtf.csrf import CSRFProtect
import secrets
from form import RegistrationForm
from hashlib import sha256

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)
app_secret = secrets.token_hex()
app.secret_key = app_secret
csrf = CSRFProtect(app)


@app.cli.command("init-db")
def init_db():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data,
                    surname=form.surname.data,
                    email=form.email.data,
                    password=sha256(form.password.data.encode(encoding='UTF-8')).digest())
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
