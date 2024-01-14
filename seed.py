from models import db, User, Feedback
from app import app

db.drop_all()
db.create_all()

u = User(username="crazy", password="crazy", email="crazy@gmail.com", first_name="Crazy", last_name="Crazy")
db.session.add(u)
db.session.commit()