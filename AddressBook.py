from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = '---------'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.debug = True
db = SQLAlchemy(app)


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

    def __init__(self, firstname, lastname, email, telephone):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.telephone = telephone

class MemberOf(db.Model):
    __tablename__ = 'memberOf'

    personId = db.Column(db.Integer(), primary_key=True)
    organizationId = db.Column(db.Integer(), primary_key=True)


@app.route('/')
@app.route('/home')
def show_home():
    return render_template('home.html')

@app.route('/create.html')
def show_create():
    return render_template('create.html')

@app.route('/edit.html')
def show_edit():
    return render_template('edit.html')

if __name__ == '__main__':
    #db.create_all()
    #db.session.commit()
    #person1 = Person('First','Last','myemail','11111')
    #db.session.add(person1)
    #db.session.commit()
    app.debug = True
    app.run()
