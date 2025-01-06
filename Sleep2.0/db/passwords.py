from db.tables import db


class Passwords(db.Model):
    __tablename__ = "Passwords"
    id = db.Column(db.String(8), primary_key=True)
    pwd = db.Column(db.String(64), nullable=False)


def get_password(id):
    return Passwords.query.filter(Passwords.id == id).first()
