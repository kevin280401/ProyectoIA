from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación con las listas de enlaces
    link_lists = db.relationship('LinkList', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"

class LinkList(db.Model):
    __tablename__ = 'link_lists'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relación con los enlaces
    links = db.relationship('Link', backref='link_list', lazy=True)

    # Relación con el usuario
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"<LinkList {self.title}>"

class Link(db.Model):
    __tablename__ = 'links'
    id = db.Column(db.Integer, primary_key=True)
    link_list_id = db.Column(db.Integer, db.ForeignKey('link_lists.id'), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    title = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(500), nullable=True)
    category = db.Column(db.String(50), nullable=True)
    image_url = db.Column(db.String(255), nullable=True)  # URL de imagen extraída del enlace
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relación con la lista de enlaces
    link_list_id = db.Column(db.Integer, db.ForeignKey('link_lists.id'), nullable=False)

    def __repr__(self):
        return f"<Link {self.url}>"
