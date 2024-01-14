from flask import Flask, render_template, redirect, session, flash
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm, DeleteForm
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Unauthorized

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///auth_feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
app.config["SECRET_KEY"] = "123456"

connect_db(app)

@app.route("/")
def homepage():
    #return render_template('home.html')
    return redirect('/register')

@app.route("/secret")
def secret():
    if "username" not in session:
        raise Unauthorized()
    return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register_user():
    """Register user"""
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
    """Login user"""
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome Back, {user.username}!", "primary")
            session['username'] = user.username
            #return redirect('/secret')
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Invalid username or']
            form.password.errors = ['Invalid password']
    return render_template('login.html', form=form)

@app.route('/logout')
def logout_user():
    """Logout user"""
    session.pop('username')
    flash("Goodbye!", "info")
    return redirect('/')

@app.route('/users/<username>')
def show_user(username):
    """Show details about user and feedback."""
    if "username" not in session or username != session['username']:
        raise Unauthorized()
    user = User.query.filter_by(username=username).first()
    form = DeleteForm()
    return render_template('user.html', user=user, form=form)

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    if "username" not in session or username != session['username']:
        raise Unauthorized()

    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        new_feedback = Feedback(title=title, content=content, username=username)
        db.session.add(new_feedback)
        db.session.commit()
        return redirect(f"/users/{username}")
    
    return render_template('addfeedback.html', form=form)

@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    """Delete user"""

    if "username" not in session or username != session['username']:
        raise Unauthorized()
    
    #user = User.query.filter_by(username=username).first()
    user = User.query.get_or_404(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")
    return redirect("/login")

@app.route('/feedback/<int:id>/delete', methods=['POST'])
def delete_feedback(id):
    """Delete feedback"""

    feedback = Feedback.query.get_or_404(id)
    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()
    username = feedback.username
    db.session.delete(feedback)
    db.session.commit()
    return redirect(f'/users/{username}')

@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):
    """Show update-feedback form and process it."""

    feedback = Feedback.query.get_or_404(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()
    
    #it shows the existing values
    form = FeedbackForm(obj=feedback)
    #form = FeedbackForm()

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    return render_template("updatefeedback.html", form=form, feedback=feedback)

    
    

