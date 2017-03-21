from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Organization(db.Model):
    __tablename__ = 'organization'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(255))
    telephone = db.Column(db.String(25))

    def __init__(self, name, email, telephone):
        self.name = name
        self.email = email
        self.telephone = telephone


class Person(db.Model):
    __tablename__ = 'person'

    id = db.Column(db.Integer(), primary_key=True)
    firstname = db.Column(db.String(150))
    lastname = db.Column(db.String(150))
    email = db.Column(db.String(200))
    telephone = db.Column(db.String(25))
    organization = db.Column(db.ForeignKey(Organization.id, ondelete='SET NULL'), nullable=False)

    def __init__(self, firstname, lastname, email, telephone, organization):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.telephone = telephone
        self.organization = organization