from operator import index
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.testing.schema import mapped_column
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from dataclasses import dataclass

@dataclass
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    role:so.Mapped[int] = so.mapped_column()
    current_login: so.Mapped[Optional[str]] = so.mapped_column(sa.String(120))
    previous_login: so.Mapped[Optional[str]] = so.mapped_column(sa.String(120))
    secondary_email: so.Mapped[Optional[str]] = so.mapped_column(sa.String(120), index=True, unique=True)
    addresses: so.Mapped[list['Address']] = relationship(back_populates='user', cascade='all, delete-orphan') # 1, N

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

# @dataclass
class Address(db.Model):
    __tablename__ = 'addresses'
    __table_args__ = (
        sa.UniqueConstraint('tag', 'user_id'), # (home, 1) (home ,2) # for combination for 2 classes
    )

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    tag: so.Mapped[str] = so.mapped_column(sa.String(16)) # if unique=True -> the whole column unique -> (home,1)
    address: so.Mapped[str] = so.mapped_column(sa.String(256))
    phone: so.Mapped[Optional[str]] = so.mapped_column(sa.String(32))
    user_id: so.Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)  # Table name users.id
    user: so.Mapped['User'] = relationship(back_populates='addresses') # 1, 1

    def __repr__(self):
        return f'Address(id={self.id}, tag={self.tag}, address=\'{self.address}\', phone={self.phone}, user_id={self.user_id})'


 # addresses: so.Mapped[list['Address']] = relationship(back_populates='user', cascade='all, delete-orphan') # 1, N

@dataclass
class Product(db.Model):
    __tablename__ = 'products'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(16))
    description: so.Mapped[str] = so.mapped_column(sa.String(256))
    price: so.Mapped[int] = so.mapped_column()
    reviews: so.Mapped[list['Review']] = relationship(back_populates='product', cascade='all, delete-orphan')


@dataclass
class Review(db.Model):
    __tablename__ = 'reviews'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    stars: so.Mapped[int] = so.mapped_column()
    text: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    product_id: so.Mapped[int] = mapped_column(ForeignKey('products.id'), index=True)
    product: so.Mapped['Product'] = relationship(back_populates='reviews')
