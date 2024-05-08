
import secrets
from PIL import Image
import os
from pythonic.models import User, Work, Service
from flask import render_template, url_for, flash, redirect, request
from pythonic.forms import ProblemForm, RegistrationForm, LoginForm, UpdateProfileForm
from pythonic import app, bcrypt, db
from flask_login import (
    login_required,
    login_user,
    current_user,
    logout_user
)
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



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

@app.route("/aboutUs")
def about():
    return render_template('about.html')

@app.route("/services")
def services():
    user = get_plumbing_users_from_database() 
    return render_template('services.html', user=user)

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
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash("You have been logged in!", "success")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check credentials", "danger")
    return render_template("login.html", title="Login", form=form)

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
@app.route('/plumbing')  
def plumbing():          
    plumbing_users = get_plumbing_users_from_database()
    return render_template('plumbing.html', plumbing_users=plumbing_users)
@app.route('/booking', methods=['GET', 'POST'])
def booking():
    problem_form = ProblemForm()  # Instantiate the ProblemForm
    return render_template('booking.html', problem_form=problem_form)
# @app.route('/handle_problem_form', methods=['POST'])
# def handle_problem_form():
#     if request.method == 'POST':
#         # Retrieve the problem description from the form data
#         problem_description = request.form.get('problemDescription')

#         # Here, you can handle the form submission, process the problem description,
#         # and return any necessary response. For example, you might perform some
#         # processing based on the problem description and return a recommendation.

#         # For demonstration purposes, let's just return the problem description
#         return f"The problem description submitted is: {problem_description}"
# Function to preprocess text
def preprocess_text(text):
    # Tokenization
    tokens = word_tokenize(text.lower())

    # Removing stop words and non-alphabetic tokens
    stop_words = set(stopwords.words("english"))
    filtered_tokens = [word for word in tokens if word.casefold() not in stop_words and word.isalpha()]

    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    preprocessed_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]

    return " ".join(preprocessed_tokens)

# Function to recommend craft owners based on cosine similarity
def recommend_craft_owners(craft_owner_descriptions, customer_problem_description):
    # Preprocess craft owner descriptions and customer problem description
    preprocessed_craft_owner_descriptions = [preprocess_text(desc) for desc in craft_owner_descriptions]
    preprocessed_customer_problem_description = preprocess_text(customer_problem_description)

    # Calculate TF-IDF vectors
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(preprocessed_craft_owner_descriptions + [preprocessed_customer_problem_description])

    # Calculate cosine similarity
    similarity_matrix = cosine_similarity(tfidf_matrix[:-1], tfidf_matrix[-1])

    # Get craft owners IDs sorted by similarity score in descending order
    craft_owner_ids = sorted(range(len(similarity_matrix)), key=lambda i: similarity_matrix[i], reverse=True)

    return craft_owner_ids
def handle_problem_form():
    problem_form = ProblemForm(request.form)
    if request.method == 'POST' and problem_form.validate():
        # Retrieve the problem description from the form data
        problem_description = problem_form.problem_description.data

        # Retrieve craft owners' names and descriptions from the User table in the database
        craft_owners = User.query.filter_by(user_type='craft_owner').all()
        craft_owner_data = [(craft_owner.username, craft_owner.description) for craft_owner in craft_owners]

        # Recommend craft owners based on cosine similarity
        recommended_craft_owner_data = recommend_craft_owners(craft_owner_data, problem_description)

        # Render template with recommendation results
        return render_template('recommendation.html', problem_description=problem_description, recommended_craft_owner_data=recommended_craft_owner_data)
    
    # If form is not valid, render the form again
    return render_template('booking.html', problem_form=problem_form)
# @app.route('/handle_problem_form', methods=['POST'])
# def handle_problem_form():
#     problem_form = ProblemForm(request.form)
#     if request.method == 'POST' and problem_form.validate():
#         # Retrieve the problem description from the form data
#         problem_description = problem_form.problem_description.data

#         # Here, you can handle the form submission, process the problem description,
#         # and return any necessary response. For example, you might perform some
#         # processing based on the problem description and return a recommendation.

#         # For demonstration purposes, let's render a template with the problem description
#         return render_template('recommendation.html', problem_description=problem_description)