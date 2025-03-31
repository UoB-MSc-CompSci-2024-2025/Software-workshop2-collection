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
    role: so.Mapped[str] = so.mapped_column(sa.String(10), default="Normal")
    addresses: so.Mapped[list['Address']] = relationship(back_populates='user', cascade='all, delete-orphan')
    reviews: so.Mapped[list['Review']] = relationship(back_populates='user', cascade='all, delete-orphan')


    def __repr__(self):
        pwh= 'None' if not self.password_hash else f'...{self.password_hash[-5:]}'
        return f'User(id={self.id}, username={self.username}, email={self.email}, role={self.role}, pwh={pwh})'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class Address(db.Model):
    __tablename__ = 'addresses'
    __table_args__ = (
        sa.UniqueConstraint('tag', 'user_id'),
    )

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    tag: so.Mapped[str] = so.mapped_column(sa.String(16))
    address: so.Mapped[str] = so.mapped_column(sa.String(256))
    phone: so.Mapped[Optional[str]] = so.mapped_column(sa.String(32))
    user_id: so.Mapped[int]  = mapped_column(ForeignKey('users.id'), index = True)
    user: so.Mapped['User'] = relationship(back_populates='addresses')

    def __repr__(self):
        return (f'Address(id={self.id}, tag={self.tag}, address=\'{self.address}\', phone={self.phone},'
                f'user_id={self.user_id})')

class Product(db.Model):
    __tablename__ = 'products'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64))
    description: so.Mapped[str] = so.mapped_column(sa.String(1024))
    price: so.Mapped[int] = so.mapped_column()
    reviews: so.Mapped[list['Review']] = relationship(back_populates='product', cascade='all, delete-orphan')

    def __repr__(self):
        return (f'Product(id={self.id}, name={self.name}, description="{self.description}", price={self.price}')

class Review(db.Model):
    __tablename__ = 'reviews'
    text: so.Mapped[Optional[str]] = so.mapped_column(sa.String(1024))
    stars: so.Mapped[int] = so.mapped_column()
    product_id: so.Mapped[int] = mapped_column(ForeignKey('products.id'), primary_key=True)
    product: so.Mapped['Product'] = relationship(back_populates='reviews')
    user_id: so.Mapped[int]  = mapped_column(ForeignKey('users.id'), primary_key=True)
    user: so.Mapped['User'] = relationship(back_populates='reviews')

    def __repr__(self):
        return (f'Review(stars={self.stars}, text="{self.text}", product_id={self.product_id}, user_id={self.user_id}')
