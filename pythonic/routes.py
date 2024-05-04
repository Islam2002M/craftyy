from pythonic.models import User
from flask import render_template, url_for, flash, redirect
from pythonic.forms import RegistrationForm, LoginForm
from pythonic import app, bcrypt, db


@app.route("/")
@app.route("/index")
def home():
    return render_template('home.html')

@app.route("/aboutUs")
def about():
    return render_template('about.html')

@app.route("/services")
def services():
    return render_template('services.html')

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            address=form.address.data,
            contact_number=form.contact_number.data,
            user_type=form.user_type.data,
            service_type=form.service_type.data,
            description=form.description.data
        )
        db.session.add(user)
        db.session.commit()
        flash(f"Account created successfully for {form.username.data} as a {form.user_type.data}", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # In a real application, you would query the database to check user credentials
        # For now, I'm assuming you have a user with fixed credentials for testing
        if (
            form.email.data == "omar@email.com"
            and form.password.data == "PASS!!word123"
        ):
            flash("You have been logged in!", "success")
            return redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check credentials", "danger")
    return render_template("login.html", title="Login", form=form)

@app.route('/plumbing')  # Corrected route name from 'plumping' to 'plumbing'
def plumbing():          # Corrected function name from 'plumping' to 'plumbing'
    return render_template('plumbing.html')  # Corrected template name from 'plumping.html' to 'plumbing.html'

@app.route('/booking')
def booking():
    return render_template('booking.html')
