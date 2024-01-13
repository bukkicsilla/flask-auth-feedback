from flask import Flask, render_template, redirect, session, flash
from models import connect_db, db, User
from forms import RegisterForm, LoginForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///auth_feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "123456"

connect_db(app)

@app.route("/")
def homepage():
    #return render_template('home.html')
    return redirect('/register')

@app.route("/secret")
def secret():
    return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register_user():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(username, password, email, first_name, last_name)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = new_user.username
        flash('Welcome! Successfully Created Your Account!', "success")
        return redirect('/secret')
    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login_user():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome Back, {user.username}!", "primary")
            session['username'] = user.username
            return redirect('/secret')
        else:
            form.username.errors = ['Invalid username or']
            form.password.errors = ['Invalid password']
    return render_template('login.html', form=form)

@app.route('/logout')
def logout_user():
    session.pop('username')
    flash("Goodbye!", "info")
    return redirect('/')
