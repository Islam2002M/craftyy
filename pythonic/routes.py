from datetime import datetime , time, timedelta 
import secrets
import os
import logging
from PIL import Image
from flask import  render_template, url_for, flash, redirect, request, session
from instance.helper import get_cleaning_users_from_database, get_electrical_users_from_database, get_plumbing_users_from_database,get_Carpentry_users_from_database,get_Painting_users_from_database,get_movingFur_users_from_database
from pythonic.forms import ProblemForm, RegistrationForm, LoginForm, UpdateProfileForm,AppointmentForm,NewLessonForm
from pythonic import app, bcrypt, db
from flask_login import login_required, login_user, current_user, logout_user
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pythonic.models import Appointment, Slot, User,Availability
from nltk import pos_tag
from nltk.corpus import wordnet
from nltk.stem.porter import PorterStemmer

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_name = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static", picture_name)
    output_size = (150, 150)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_name

@app.route("/")
@app.route("/index")
def home():
    return render_template('home.html')

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            address=form.address.data,
            contactNumber=form.contactNumber.data,
            user_type=form.user_type.data,
        )
        if form.user_type.data == 'craft_owner':
            user.service_type = form.service_type.data
            user.description = form.description.data
        db.session.add(user)
        db.session.commit()
        login_user(user)

        flash(f"Account created successfully for {form.username.data} as a {form.user_type.data}", "success")
        return redirect(url_for("home"))
    return render_template("register.html", title="Register", form=form)
 
@app.route("/aboutUs")
def about():
    return render_template('about.html')


@app.route("/services")
def services():
    return render_template('services.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

def get_next_date_from_day(day_name):
    """Given a day name, return the next date that matches the day."""
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    today = datetime.today()
    today_day_index = today.weekday()
    target_day_index = days.index(day_name.lower())
    days_ahead = (target_day_index - today_day_index + 7) % 7
    if days_ahead == 0:  # if it's the same day, move to the next week's day
        days_ahead = 7
    return today + timedelta(days=days_ahead)

@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    form = AppointmentForm()

    # Get parameters from the form or the request args
    craft_owner_name = request.args.get('craft_owner') or form.craft_owner.data
    service_type = request.args.get('service_type') or form.service_type.data

    logging.debug(f"Received craft_owner: {craft_owner_name}")
    logging.debug(f"Received service_type: {service_type}")

    if craft_owner_name:
        user = User.query.filter_by(username=craft_owner_name).first()
        if user:
            logging.debug(f"Found user: {user.username}")
            if user.availability:
                availability = user.availability
                logging.debug(f"User availability: {availability}")
                available_slots = Slot.query.filter_by(availability_id=availability.id).all()
                logging.debug(f"Available slots: {available_slots}")

                available_days = availability.days.split(',')
                logging.debug(f"Available days: {available_days}")

                form.appointment_date.choices = [(day, day) for day in available_days]
                form.appointment_time.choices = [(slot.id, slot.period) for slot in available_slots]
            else:
                logging.debug("User has no availability")
                available_slots = []
        else:
            logging.debug("No user found with the given craft_owner name")
            available_slots = []
    else:
        logging.debug("No craft_owner name provided")
        user = None
        available_slots = []

    if request.method == 'POST':
        try:
            if form.validate_on_submit():
                logging.debug("Form validation successful")

                # Convert appointment_date from day name to date object
                try:
                    appointment_day_str = form.appointment_date.data
                    appointment_date = get_next_date_from_day(appointment_day_str).date()
                    logging.debug(f"Parsed appointment date: {appointment_date}")
                except Exception as e:
                    logging.error(f"Error parsing appointment date: {e}")
                    flash('Invalid appointment date format', 'danger')
                    return render_template('appointments.html', form=form, available_slots=available_slots, craft_owner=craft_owner_name, service_type=service_type)

                # Convert appointment_time from string to time object
                try:
                    slot_id = form.appointment_time.data
                    slot = Slot.query.get(slot_id)
                    appointment_time = datetime.strptime(slot.period.split('-')[0], '%H:%M:%S').time()  # Adjust format as per slot.period
                    logging.debug(f"Parsed appointment time: {appointment_time}")
                except Exception as e:
                    logging.error(f"Error parsing appointment time: {e}")
                    flash('Invalid appointment time format', 'danger')
                    return render_template('appointments.html', form=form, available_slots=available_slots, craft_owner=craft_owner_name, service_type=service_type)

                appointment = Appointment(
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    phone_number=form.phone_number.data,
                    street_address=form.street_address.data,
                    city=form.city.data,
                    state=form.state.data,
                    postal_code=form.postal_code.data,
                    appointment_date=appointment_date,
                    appointment_time=appointment_time,
                    craft_owner=craft_owner_name,
                    customer_id=2,  # Replace with the actual customer ID
                    appointment_purpose=form.appointment_purpose.data,
                    message=form.message.data
                )
                db.session.add(appointment)
                db.session.commit()
                logging.debug("Appointment successfully added to the database")
                flash('Your appointment has been booked!', 'success')
                return redirect(url_for('home'))
            else:
                logging.debug("Form validation failed")
        except Exception as e:
            logging.error(f"Unexpected error during appointment booking: {e}")
            flash('An unexpected error occurred. Please try again.', 'danger')

    # Pre-fill the form fields for read-only fields
    form.craft_owner.data = craft_owner_name
    form.service_type.data = service_type

    return render_template('appointments.html', form=form, available_slots=available_slots, craft_owner=craft_owner_name, service_type=service_type)
@app.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    return render_template(
        "dashboard.html",
        title="Dashboard",
        active_tab=None
    )

@app.route("/dashboard/profile", methods=["GET", "POST"])
@login_required
def profile():
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
        return redirect(url_for("profile"))
    elif request.method == "GET":
        profile_form.username.data = current_user.username
        profile_form.email.data = current_user.email
        profile_form.address.data = current_user.address
        profile_form.contactNumber.data = current_user.contactNumber
        profile_form.description.data = current_user.description
    image_file = url_for("static", filename=f"user_pics/{current_user.image_file}")
    return render_template(
        "profile.html",
        title="Profile",
        profile_form=profile_form,
        image_file=image_file,
        active_tab="profile",
    )
@app.route("/dashboard/new_lesson", methods=["GET", "POST"])
@login_required
def new_lesson():
    new_lesson_form = NewLessonForm()

    if new_lesson_form.validate_on_submit():
        # Extract data from the form
        start_time = new_lesson_form.start_time.data
        end_time = new_lesson_form.end_time.data
        all_days = new_lesson_form.all_days.data

        # If "Work All Days" checkbox is selected, set working_days to "Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday"
        if all_days:
            working_days = "Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday"
        else:
            working_days = ','.join(new_lesson_form.workingDays.data)

        # Create a new Availability object
        availability = Availability(
            start_time=start_time,
            end_time=end_time,
            days=working_days,
            owner_id=current_user.id  # Associate with the current user
        )

        # Add the availability to the database session
        db.session.add(availability)
        db.session.commit()

        flash("Your availability has been updated!", "success")
        return redirect(url_for("dashboard"))  # Redirect to dashboard page after submission

    # If the form is not submitted or validation fails, render the new_lesson.html template
    return render_template(
        "new_lesson.html",
        title="New Lesson",
        new_lesson_form=new_lesson_form,
        active_tab="new_lesson"
    )

@app.route('/plumbing')  
def plumbing():          
    plumbing_users = get_plumbing_users_from_database()
    return render_template('plumbing.html', plumbing_users=plumbing_users)
@app.route('/electrical')  
def electrical():          
    electrical_users = get_electrical_users_from_database()
    return render_template('electrical.html', electrical_users=electrical_users)
@app.route('/cleaning')  
def cleaning():          
    cleaning_users = get_cleaning_users_from_database()
    return render_template('electrical.html', electrical_users=cleaning_users)
@app.route('/movingFur')  
def movingFur():          
    movingFur_users = get_movingFur_users_from_database()
    return render_template('movingFur.html', movingFur_users=movingFur_users)

@app.route('/Painting')  
def Painting():          
    Painting_users = get_Painting_users_from_database()
    return render_template('Painting.html', Painting_users=Painting_users)

@app.route('/Carpentry')  
def Carpentry():          
    Carpentry_users = get_Carpentry_users_from_database()
    return render_template('Carpentry.html', Carpentry_users=Carpentry_users)

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    problem_form = ProblemForm()  # Instantiate the ProblemForm
    return render_template('booking.html', problem_form=problem_form)

@app.route('/handle_problem_form', methods=['POST'])
def handle_problem_form():
    problem_form = ProblemForm(request.form)
    if request.method == 'POST' and problem_form.validate():
        # Retrieve the problem description from the form data
        problem_description = problem_form.problem_description.data

        # Retrieve craft owners' names, descriptions, addresses, and service types from the User table in the database
        craft_owners = User.query.filter_by(user_type='Craft Owner').all()
        craft_owner_data = [(craft_owner.username, craft_owner.description, craft_owner.address, craft_owner.service_type) for craft_owner in craft_owners]

        # Recommend craft owners based on cosine similarity
        recommended_craft_owner_data = recommend_craft_owners(craft_owner_data, problem_description)

        # Render template with recommendation results
        return render_template('recommendation.html', problem_description=problem_description, recommended_craft_owner_data=recommended_craft_owner_data)
    
    # If form is not valid, render the form again
    return render_template('suggestion.html', problem_form=problem_form)


def preprocess_text(text):
    if text is None:
        return ""  # Return empty string if text is None
    
    # Tokenization, filtering, and lemmatization
    stop_words = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()
    preprocessed_tokens = []
    for word, tag in pos_tag(word_tokenize(text)):
        if word.casefold() not in stop_words and word.isalpha():
            pos = get_wordnet_pos(tag)
            if pos:
                preprocessed_tokens.append(lemmatizer.lemmatize(word, pos))
            else:
                preprocessed_tokens.append(lemmatizer.lemmatize(word))
    preprocessed_text = ' '.join(preprocessed_tokens)
    print("Preprocessed Text:", preprocessed_text)  # Debugging print statement
    return preprocessed_text


def get_wordnet_pos(tag):
    if tag.startswith("J"):
        return wordnet.ADJ
    elif tag.startswith("V"):
        return wordnet.VERB
    elif tag.startswith("N"):
        return wordnet.NOUN
    elif tag.startswith("R"):
        return wordnet.ADV
    else:
        return None

def recommend_craft_owners(craft_owner_data, customer_problem_description):
    # Preprocess craft owner descriptions and customer problem description
    preprocessed_craft_owner_descriptions = [preprocess_text(desc[1]) + " " + preprocess_text(desc[2]) for desc in craft_owner_data]
    preprocessed_customer_problem_description = preprocess_text(customer_problem_description)

    # Calculate TF-IDF vectors
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(preprocessed_craft_owner_descriptions + [preprocessed_customer_problem_description])

    # Calculate cosine similarity
    similarity_matrix = cosine_similarity(tfidf_matrix[:-1], tfidf_matrix[-1])

    # Get craft owners sorted by similarity score in descending order
    sorted_craft_owners = sorted(zip(craft_owner_data, similarity_matrix), key=lambda x: x[1], reverse=True)
    
    # Prepare craft owner data as a list of dictionaries
    recommended_craft_owner_data = []
    for craft_owner, similarity_score in sorted_craft_owners:
        name, description, address, service_type = craft_owner  # Ensure service_type is included here
        recommended_craft_owner_data.append({
            'name': name,
            'description': description,
            'address': address,
            'service_type': service_type,  # Include service_type
            'similarity_score': similarity_score[0]  # Assuming similarity_score is a single value in a list
        })

    return recommended_craft_owner_data