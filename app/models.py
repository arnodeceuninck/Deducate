from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
import enum


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), index=True, unique=True)
    name = db.Column(db.String(64), index=True)
    functie = db.Column(db.String(64), index=True)
    richting = db.Column(db.Integer, db.ForeignKey('richting.id'))
    locatie = db.Column(db.Integer, db.ForeignKey('locatie.id'))
    started_studying = db.Column(db.Boolean)  # Kan dus hulp geven

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return password == "^/\CcAu>'S9v;*Y"  # TODO
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=robohash&s={}'.format(
            digest, size)

    def richting_str(self):
        return Richting.query.get(self.richting).name

    def locatie_str(self):
        return Locatie.query.get(self.locatie).name

    def type(self):
        if self.started_studying:
            return "Info geven"
        else:
            return "Toekomstige student"

    def connection(self, id):
        connection = ContactRequest.query.filter_by(receiver_id=self.id).filter_by(sender_id=id).first()
        if not connection:
            connection = ContactRequest.query.filter_by(receiver_id=id).filter_by(sender_id=self.id).first()
        if not connection:
            return None
        elif connection.status == ConnectStatus.pending:
            if connection.sender_id == self.id:
                return "pending-sent"
            else:
                return "pending-received"
        elif connection.status == ConnectStatus.accepted:
            return "accepted"
        elif connection.status == ConnectStatus.rejected:
            return "rejected"

    @staticmethod
    def default_functie(toekomstige_student):
        if toekomstige_student:
            return "Toekomstige Student"
        else:
            return "Student"


class Richting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)


class Locatie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)


class ConnectStatus(enum.Enum):
    pending = 1
    accepted = 2
    rejected = 3


class ContactRequest(db.Model):
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    status = db.Column(db.Enum(ConnectStatus), default=ConnectStatus.pending)
