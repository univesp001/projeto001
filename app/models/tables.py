from app import db, login_manager
from flask_login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from app import app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(84), nullable=False)
    email = db.Column(db.String(84), nullable=False, unique=True, index=True)
    password = db.Column(db.String(255), nullable=False)
    pessoa_id = relationship("Pessoa", backref='user', uselist=False)


class Pessoa(db.Model):
    __tablename__ = 'pessoas'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    idade = db.Column(db.Integer)
    sexo = db.Column(db.String(1))
    salario = db.Column(db.Float)
    users = relationship("User")
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    def __init__(self, nome='Anônimo', idade=18, sexo='M', salario=1039):
        self.nome = nome
        self.idade = idade
        self.sexo = sexo
        self.salario = salario

    def __repr__(self):
        return '<Pessoa %r>' % self.nome
