from flask import render_template, flash, redirect, url_for, request
from app.send_email import *
from app.forms import *
from app.models import *
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


@app.route('/')
def index():
    if current_user.is_authenticated:
        filters = ["Handelsingenieur", "Informatica"]
        users = User.query.all()
        return render_template('cc_homepage.html', filters=filters, suggestions=users)
    else:
        return render_template('cc_main.html')


@app.route('/middelbaar')
def middelbaar():
    return render_template('cc_midelbaar.html')


@app.route('/register/<type>', methods=['GET', 'POST'])
def register(type):
    toekomstige_student = type == "future_student"
    richtingen_db = Richting.query.order_by(Richting.name).all()
    richtingen = list()
    for richting in richtingen_db:
        richtingen.append(richting.name)
    locations = list()
    for location in Locatie.query.order_by(Locatie.name).all():
        locations.append(location.name)
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check whether richting already in database, add if required
        richting = form.richting.data
        if not richting in richtingen:
            new_richting = Richting(name=richting)
            db.session.add(new_richting)
            db.session.commit()
        # Get the id of the current richting
        richting_id = Richting.query.filter_by(name=richting).first().id
        # Check whether richting already in database, add if required
        location = form.locatie.data
        if not location in locations:
            new_location = Locatie(name=location)
            db.session.add(new_location)
            db.session.commit()
        location_id = Locatie.query.filter_by(name=location).first().id
        # Get the id of the current richting
        richting_id = Richting.query.filter_by(name=richting).first().id
        # Create a new user
        user = User(email=form.email.data, name=form.name.data, richting=richting_id, locatie=location_id,
                    started_studying=not toekomstige_student)
        db.session.add(user)
        db.session.commit()
        # # Check whether there are users studying the same and send them an email
        # i = 0
        # if toekomstige_student:
        #     mentors = HuidigStudent.query.filter_by(richting=richting_id)
        #     i = mentors.count()
        #     for mentor in mentors:
        #         send_future_student_email(mentor, richting, form.email.data)
        # else:
        #     toekomstige_studenten = ToekomstigStudent.query.filter_by(richting=richting_id)
        #     i = toekomstige_studenten.count()
        #     for ts in toekomstige_studenten:
        #         send_mentor_email(ts, richting, form.email.data)
        # flash(str(i) + " matches found. You can find them in your mailbox. Be sure to check your spam folder.")
        return redirect(url_for('thanks'))
    return render_template('cc_register.html', form=form, richtingen=richtingen, locations=locations)


@app.route('/thanks')
def thanks():
    return render_template('cc_thanks.html')


@app.route('/new_richting', methods=['GET', 'POST'])
def new_richting():
    form = NewRichtingForm()
    if form.validate_on_submit():
        # Check whether richting already in database, add if required
        richting = form.richting.data
        richting_db = Richting.query.filter_by(name=richting).first()
        if richting_db:
            flash("De richting bestaat al.")
        else:
            new_richting = Richting(name=richting)
            db.session.add(new_richting)
            db.session.commit()
            flash("De richting werd succesvol toegevoegd")
        return redirect(url_for('index'))
    return render_template('cc_new_richting.html', form=form)


@app.route('/mentors', methods=['GET'])
def mentors():
    richting = request.args["richting"]
    richting_db = Richting.query.filter_by(name=richting).first_or_404()
    mentors = User.query.filter_by(started_studying=True).filter_by(richting=richting_db.id)
    return render_template('cc_users.html', richting=richting, mentors=mentors)


# @app.route('/overview')
# def overview():
#     richtingen = Richting.query.all()
#     mentors = User.query.filter_by(started_studying=True)
#     future_students = User.query.filter_by(started_studying=False)
#     return render_template('cc_overview.html', richtingen=richtingen, mentors=mentors, future_students=future_students)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)  # TODO:, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('cc_login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html', title='Page not found'), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return render_template('405.html', title='Method not allowed'), 405


# Function for deliberatly creating an error (for testing the error mailing system)
@app.route('/internal_server_error')
def internal_server_error():
    return render_template("500.html", title="Internal error")


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', title='Internal error'), 500
