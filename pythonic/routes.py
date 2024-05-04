<<<<<<< HEAD
from pythonic.models import User
from flask import render_template, url_for, flash, redirect
from pythonic.forms import RegistrationForm, LoginForm
=======
import secrets
from PIL import Image
import os
from pythonic.models import User, Work, Service
from flask import render_template, url_for, flash, redirect, request
from pythonic.forms import RegistrationForm, LoginForm, UpdateProfileForm
>>>>>>> a18e5681c79021036e41ae3d1f00b584f9c6f01b
from pythonic import app, bcrypt, db
from flask_login import (
    login_required,
    login_user,
    current_user,
    logout_user,
    login_required,
)



def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_name = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static/user_pics", picture_name)
    output_size = (150, 150)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_name


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
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            address=form.address.data,
            contactNumber=form.contactNumber.data,
            user_type=form.user_type.data,
        )
        if form.user_type.data=='craft_owner':
            user.service_type = form.service_type.data
            user.description = form.description.data 
        elif form.user_type.data == 'customer':
            user.service_type = None
            user.description = None
            
        db.session.add(user)
        db.session.commit()

        flash(f"Account created successfully for {form.username.data} as a {form.user_type.data}", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
<<<<<<< HEAD
        # In a real application, you would query the database to check user credentials
        # For now, I'm assuming you have a user with fixed credentials for testing
        if (
            form.email.data == "omar@email.com"
            and form.password.data == "PASS!!word123"
        ):
=======
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
>>>>>>> a18e5681c79021036e41ae3d1f00b584f9c6f01b
            flash("You have been logged in!", "success")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check credentials", "danger")
    return render_template("login.html", title="Login", form=form)

<<<<<<< HEAD
@app.route('/plumbing')  # Corrected route name from 'plumping' to 'plumbing'
def plumbing():          # Corrected function name from 'plumping' to 'plumbing'
    return render_template('plumbing.html')  # Corrected template name from 'plumping.html' to 'plumbing.html'

@app.route('/booking')
def booking():
    return render_template('booking.html')
=======
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    profile_form = UpdateProfileForm()
    if profile_form.validate_on_submit():
        if profile_form.picture.data:
            picture_file = save_picture(profile_form.picture.data)
            current_user.image_file = picture_file
        current_user.username = profile_form.username.data
        current_user.email = profile_form.email.data
        current_user.address = profile_form.address.data
        current_user.contactNumber = profile_form.contactNumber.data
        current_user.description = profile_form.description.data

        db.session.commit()
        flash("Your profile has been updated", "success")
        return redirect(url_for("dashboard"))
    
    elif request.method == "GET":
        profile_form.username.data = current_user.username
        profile_form.email.data = current_user.email
        profile_form.address.data = current_user.address
        profile_form.contactNumber.data = current_user.contactNumber
        profile_form.description.data = current_user.description

    image_file = url_for("static", filename=f"user_pics/{current_user.image_file}")
    return render_template(
        "dashboard.html",
        title="Dashboard",
        profile_form=profile_form,
        image_file=image_file,
    )
>>>>>>> a18e5681c79021036e41ae3d1f00b584f9c6f01b
