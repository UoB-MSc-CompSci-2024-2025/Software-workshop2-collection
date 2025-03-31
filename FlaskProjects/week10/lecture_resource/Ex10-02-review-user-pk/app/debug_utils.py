from app import db
from app.models import User, Address, Product, Review

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

    products = [
        {
            'name':'SnoozeSphere Sleep Optimizer',
            'description':'A high-tech sleep mask that uses gentle vibrations and calming sounds '
                        'to optimize your sleep cycle. Helps you wake up feeling refreshed every morning.',
            'price':3999,
            'reviews':
            [
                {'user': u1, 'stars': 5, 'text':'I never sleep better! I wake up so much more rested now!'},
                {'user': u2, 'stars': 4, 'text':'"The vibrations are subtle but effective. Great product!'},
            ]
        },
        {
            'name': 'TwilightSmart LED Plant Light',
            'description': 'A full-spectrum LED grow light that simulates the perfect day-night'
                           'cycle for indoor plants, promoting healthier growth even without natural sunlight.',
            'price': 5999,
            'reviews':
                [
                    {'user': u1, 'stars': 5, 'text': 'My plants are thriving thanks to this light!'},
                    {'user': u3, 'stars': 4, 'text': 'A bit too bright for my living room, but it works well'},
                ]
        },
        {
            'name': 'FrostWave Portable Cooler',
            'description': 'A mini, battery-powered cooler that can chill drinks and food for hours,'
                           'perfect for outdoor adventures, picnics, or tailgates.',
            'price': 7999,
            'reviews':
                [
                    {'user': u1, 'stars': 5, 'text': 'Keeps my drinks cold during my hikes. Love it!'},
                    {'user': u3, 'stars': 3, 'text': 'Could use a larger capacity, but great for smaller items.'},
                ]
        },
        {
            'name': 'EchoNote Smart Notepad',
            'description': 'A reusable smart notepad that syncs with your phone and instantly'
                           ' digitizes handwritten notes. Perfect for students, professionals, and creatives.',
            'price': 4999,
            'reviews':
                [
                    {'user': u2, 'stars': 5, 'text': 'Great for keeping my notes organized. Syncing is seamless!'},
                    {'user': u4, 'stars': 3, 'text': 'I wish it was a bit more responsive, but it works.'},
                ]
        },
        {
            'name': 'SmartRoast Self-Adjusting Coffee Maker',
            'description': 'A coffee maker that adjusts brew strength and temperature based on '
                           'your personal preferences, making the perfect cup every time.',
            'price': 12999,
            'reviews':
                [
                    {'user': u3, 'stars': 5, 'text': 'Best coffee I\'ve ever had! It really knows my perfect brew.'},
                    {'user': u4, 'stars': 4, 'text': 'I had trouble connecting to the app, but once I did, it\'s amazing'},
                ]
        },
        {
            'name': 'GlowRider LED Bicycle Tires',
            'description': ' Bicycle tires with embedded LED lights that illuminate in vibrant colors, '
                           'increasing visibility and style on your nighttime rides',
            'price': 7999,
            'reviews':
                [
                    # {'user': u1, 'stars': 5, 'text': 'So cool! My bike looks amazing at night, and I feel safer too.'},
                    # {'user': u2, 'stars': 4, 'text': 'A little tricky to install, but worth it!'},
                    # {'user': u3, 'stars': 0, 'text': 'Terrible: they arrived with punctures!'},
                ]
        }
    ]


    for p in products:
        reviews = p.pop('reviews')
        prod = Product(**p)
        db.session.add(prod)
        for r in reviews:
            rev = Review(**r)
            prod.reviews.append(rev)


    db.session.commit()
