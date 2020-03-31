from flask import render_template, flash, redirect, url_for, request, session
from app.auth import bp
from app import db
from app.auth.forms import RegistrationForm, LoginForm, NewRichtingForm
from app.models import User, Richting, Locatie
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


@bp.route('/register/<type>', methods=['GET', 'POST'])
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
                    started_studying=not toekomstige_student, functie=User.default_functie(toekomstige_student))
        db.session.add(user)
        db.session.commit()
        # # Check whether there are users studying the same and send them an emails
        # i = 0
        # if toekomstige_student:
        #     mentors = HuidigStudent.query.filter_by(richting=richting_id)
        #     i = mentors.count()
        #     for mentor in mentors:
        #         send_future_student_email(mentor, richting, form.emails.data)
        # else:
        #     toekomstige_studenten = ToekomstigStudent.query.filter_by(richting=richting_id)
        #     i = toekomstige_studenten.count()
        #     for ts in toekomstige_studenten:
        #         send_mentor_email(ts, richting, form.emails.data)
        # flash(str(i) + " matches found. You can find them in your mailbox. Be sure to check your spam folder.")
        return redirect(url_for('auth.thanks'))
    return render_template('auth/cc_register.html', form=form, richtingen=richtingen, locations=locations)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user)  # TODO:, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('auth.index')
        return redirect(next_page)
    return render_template('auth/cc_login.html', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.index'))

@bp.route('/')
def index():
    print(url_for("chats.chats"))
    if current_user.is_authenticated:
        filters = ["Handelsingenieur", "Informatica"]
        users = User.query.all()
        return render_template('cc_homepage.html', filters=filters, suggestions=users)
    else:
        return render_template('auth/cc_main.html')


@bp.route('/middelbaar')
def middelbaar():
    return render_template('auth/cc_midelbaar.html')

@bp.route('/thanks')
def thanks():
    return render_template('auth/cc_thanks.html')


@bp.route('/new_richting', methods=['GET', 'POST'])
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
        return redirect(url_for('auth.index'))
    return render_template('auth/cc_new_richting.html', form=form)
