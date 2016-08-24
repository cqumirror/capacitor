from flask_sqlalchemy import SQLAlchemy
from capacitor import app

db = SQLAlchemy(app)


class Users(db.Model):
    __tablename__ = "users"
    __table_args__ = {
        "mysql_charset": "utf8"
    }
    user_id = db.Column(db.String, primary_key=True)    # hashed email with md5
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    clients = db.relationship("Clients", backref="user", lazy="dynamic")

    def __init__(self, user_id, username, password, email):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.email = email


class Clients(db.Model):
    __tablename__ = "clients"
    __table_args__ = {
        "mysql_charset": "utf8"
    }
    client_id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey("users.user_id"))

    def __int__(self, client_id, user_id):
        self.client_id = client_id
        self.user_id = user_id


if __name__ == "__main__":
    db.create_all()
