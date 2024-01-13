from flask import Flask, render_template, redirect, session, flash
from models import connect_db, db
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///auth_feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "123456"

connect_db(app)

@app.route("/")
def home():
    return "FEELBACK"

