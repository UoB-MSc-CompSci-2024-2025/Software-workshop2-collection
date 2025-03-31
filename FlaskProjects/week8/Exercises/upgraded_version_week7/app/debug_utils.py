from app import db
from app.models import User, Address, Product, Review


def reset_db():
    db.drop_all()
    db.create_all()

    # ---------- USER ---------------

    u1 = User(username='amy', email='a@b.com', role=1) # user is login -> amy
    u1.set_password('amy.pw')
    u2 = User(username='tom', email='t@b.com',role=2)
    u2.set_password('tom.pw')
    u3 = User(username='yin', email='y@b.com', role=1)
    u3.set_password('yin.pw')
    u4 = User(username='tariq', email='tariq@b.com',role=2)
    u4.set_password('tariq.pw')
    u5 = User(username='jo', email='jo@b.com',role=2)
    u5.set_password('jo.pw')

    # ------------- ADDRESS ------------

    u1.addresses.append(Address(tag='home', address='Amy, 22b Baker Street, London SW1', phone='12345678'))
    u1.addresses.append(Address(tag='work', address='Amy, Amy\'s Company, London SW1', phone='23456789'))

    # ---- Commit now to ensure the user exists in the DB ----

    db.session.add_all([u1,u2,u3,u4,u5])
    db.session.commit()

    # --------------- PRODUCT ------------

    p1 = Product(name='Milk Chocolates', description='very sweet', price=120) # user navigate to product page and click on a product (which is milk chocolate)
    p2 = Product(name='Dark Chocolates', description='very dark sweet', price=220)
    p3 = Product(name='Almond Chocolates', description='very crunchy sweet', price=320)
    p4 = Product(name='Nuts Chocolates', description='too crunchy sweet', price=420)
    p5 = Product(name='Very dark Chocolates', description='very bitter', price=520)


    # ------------- REVIEW -------------
    r1 = Review(user=u1, stars=4, text='Excellent') # amy -> writing the review for milk chocolate


    # --------- tap on submit button -------

    # Submit the review
    p1.reviews.append(r1)  # the entered review is stored in product by the user (amy)
    db.session.add(p1)
    db.session.add_all([p2,p3,p4,p5])
    db.session.commit()

























    # p1.reviews.append(Review(stars=4, text='Excellent'))
    # p1.reviews.append(Review(stars=5, text='Excellent'))
    # p1.reviews.append(Review(stars=5, text='Excellent'))
    # p2.reviews.append(Review(stars=2, text='Very good'))
    # p3.reviews.append(Review(stars=3, text='Good'))
    # p4.reviews.append(Review(stars=5, text='verry very good'))
    # p5.reviews.append(Review(stars=1, text='ok'))
    #
    # db.session.add_all([p1,p2,p3,p4,p5,])








































