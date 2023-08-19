from db.db import db


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    email = db.Column(db.VARCHAR(255), nullable=False, unique=True)
    password = db.Column(db.VARCHAR(255), nullable=False)
    is_notified = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return self.id
