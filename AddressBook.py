from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import db, Organization, Person

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:XXXXXXXXXX@localhost/addressBook'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

with app.app_context():
    db.init_app(app)
    engine = create_engine('postgresql://postgres:XXXXXXXXXX@localhost/addressBook')


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def show_home():
    people = Person.query.order_by(Person.lastname).all()
    organizations = Organization.query.order_by(Organization.name).all()
    return render_template('home.html', people=people, organizations=organizations)


@app.route('/orga/<string:name>/<int:id>')
def show_orga(name, id):
    session = sessionmaker(bind=engine)
    session = session()
    people = session.query(Person).filter(Organization.id == id).filter(Person.organization == Organization.id)
    return render_template('list.html', people=people, name=name)


@app.route('/edit/person/<int:id>')
def edit_person(id):
    person = Person.query.filter_by(id=id).first()
    orgas = Organization.query.all()
    if person:
        return render_template('edit.html', person=person, orgas=orgas, id=id)
    else:
        return redirect(url_for('show_home'))


@app.route('/edit/orga/<int:id>')
def edit_orga(id):
    orga = Organization.query.filter_by(id=id).first()
    if orga:
        return render_template('edit.html', orga=orga, id=id)
    else:
        return redirect(url_for('show_home'))


@app.route('/change/person/<int:id>', methods=['POST'])
def change_person(id):
    person = Person.query.filter_by(id=id).first()
    if person:
        person.firstname = request.form['firstname']
        person.lastname = request.form['lastname']
        person.email = request.form['email']
        person.telephone = request.form['telephone']
        person.organization = request.form['choice']
        db.session.commit()
        db.session.close()
    return redirect(url_for('show_home'))


@app.route('/change/orga/<int:id>', methods=['GET', 'POST'])
def change_orga(id):
    orga = Organization.query.filter_by(id=id).first()
    if orga:
        orga.name = request.form['name']
        orga.email = request.form['email']
        orga.telephone = request.form['telephone']
        db.session.commit()
        db.session.close()
    return redirect(url_for('show_home'))


@app.route('/delete/person/<int:id>', methods=['POST'])
def delete_person(id):
    person = Person.query.filter_by(id=id).first()
    if person:
        db.session.delete(person)
        db.session.commit()
        db.session.close()
    return redirect(url_for('show_home'))


@app.route('/delete/orga/<int:id>', methods=['POST', 'GET'])
def delete_orga(id):
    orga = Organization.query.filter_by(id=id).first()
    if orga:
        orga_people = Person.query.filter(Person.organization == id).delete()
        db.session.delete(orga)
        db.session.commit()
        db.session.close()
    return redirect(url_for('show_home'))


@app.route('/create')
def show_create():
    organizations = Organization.query.all()
    return render_template('create.html', organizations=organizations)


@app.route('/create/orga', methods=['POST'])
def create_orga():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        telephone = request.form['telephone']
        new_orga = Organization(name, email, telephone)
        db.session.add(new_orga)
        db.session.commit()
        db.session.close()
    return redirect(url_for('show_home'))


@app.route('/create/person', methods=['POST'])
def create_person():
    if request.method == 'POST':
        orga = request.form['choice']
        orga = orga
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        telephone = request.form['telephone']
        orga_id = Organization.query.filter(Organization.name == orga).first().id
        new_person = Person(firstname, lastname, email, telephone, orga_id)
        db.session.add(new_person)
        db.session.commit()
        db.session.close()
    return redirect(url_for('show_home'))


@app.errorhandler(404)
def page_not_found():
    return render_template('404.html')


if __name__ == '__main__':
    app.debug = True
    app.run()
