from app import db
from app.models import User
import datetime


def reset_db():
    db.drop_all()
    db.create_all()

    users =[
        {'username': 'amy',   'email': 'amy@b.com', 'role': 'Admin', 'pw': 'amy.pw'},
        {'username': 'tom',   'email': 'tom@b.com',                  'pw': 'amy.pw'},
        {'username': 'yin',   'email': 'yin@b.com', 'role': 'Admin', 'pw': 'amy.pw'},
        {'username': 'tariq', 'email': 'trq@b.com',                  'pw': 'amy.pw'},
        {'username': 'jo',    'email': 'jo@b.com',                   'pw': 'amy.pw'}
    ]


    for u in users:
        # get the password value and remove it from the dict:
        pw = u.pop('pw')
        # create a new user object using the parameters defined by the remaining entries in the dict:
        user = User(**u)
        # set the password for the user object:
        user.set_password(pw)
        # add the newly created user object to the database session:
        db.session.add(user)
    db.session.commit()








