from app import db, app

class Richting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)

class Locatie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)

class HuidigStudent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), index=True)
    name = db.Column(db.String(64), index=True)
    richting = db.Column(db.Integer, db.ForeignKey('richting.id'))
    locatie = db.Column(db.Integer, db.ForeignKey('locatie.id'))

class ToekomstigStudent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), index=True)
    name = db.Column(db.String(64), index=True)
    richting = db.Column(db.Integer, db.ForeignKey('richting.id'))
    locatie = db.Column(db.Integer, db.ForeignKey('locatie.id'))
