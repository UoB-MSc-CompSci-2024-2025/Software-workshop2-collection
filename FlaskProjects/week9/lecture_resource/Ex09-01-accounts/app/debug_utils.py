from app import db
from app.models import User, Address

def reset_db():
    db.drop_all()
    db.create_all()

    u1 = User(username='amy', email='a@b.com', role='Admin')
    u1.set_password('amy.pw')
    u2 = User(username='tom', email='t@b.com')
    u2.set_password('tom.pw')
    u3 = User(username='yin', email='y@b.com', role='Admin')
    u3.set_password('yin.pw')
    u4 = User(username='tariq', email='tariq@b.com')
    u4.set_password('tariq.pw')
    u5 = User(username='jo', email='jo@b.com')
    u5.set_password('jo.pw')

    u1.addresses.append(Address(tag='home', address='Amy, 22b Baker Street, London SW1', phone='12345678'))
    u1.addresses.append(Address(tag='work', address='Amy, Amy\'s Company, London SW1', phone='23456789'))

    u2.addresses.append(Address(tag='home', address='123 Imaginary Street, Nowhere Town, BS12 3ZZ', phone='01234 5678901'))
    u2.addresses.append(Address(tag='work', address='456 Phantom Lane, Nonsense City, PO1 9XY', phone='07123 456789'))
    u3.addresses.append(Address(tag='home', address='789 Fictitious Road, Lostville, WR99 1AA', phone='08000 123456'))
    u3.addresses.append(Address(tag='work', address='101 Invisible Crescent, Dreamland, EX999 5WP', phone='02345 6789012'))
    u4.addresses.append(Address(tag='home', address='202 Ghost Place, Madeupburgh, AB12 7ZZ', phone='09123 456789'))
    u4.addresses.append(Address(tag='work', address='303 Uncharted Avenue, Mythicton, DD03 4BB', phone='0167 123456'))
    u4.addresses.append(Address(tag='club', address='404 Fakewood Drive, Utopia, PL99 0XX', phone='08765 432109'))
    u5.addresses.append(Address(tag='work', address='505 Illusory Way, Nonexistentham, LN89 6ZZ', phone='0131 56789012'))
    u5.addresses.append(Address(tag='home', address='606 Nonexistent Street, Wonderland, G12 8TY', phone='09999 888777'))
    u5.addresses.append(Address(tag='club', address='707 Parallel Boulevard, Imaginary Town, KT25 1QQ', phone='07500 1234567'))



    db.session.add_all([u1, u2, u3, u4, u5])
    db.session.commit()
