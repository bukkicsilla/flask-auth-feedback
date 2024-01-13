from models import db, User
from app import app

db.drop_all()
db.create_all()

u = User(username="crazy", password="crazy", email="crazy@gmail.com", first_name="crazy", last_name="crazy")
db.session.add(u)
db.session.commit()