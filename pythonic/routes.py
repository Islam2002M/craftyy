import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, session
from instance.helper import get_cleaning_users_from_database, get_electrical_users_from_database, get_plumbing_users_from_database,get_Carpentry_users_from_database,get_Painting_users_from_database,get_movingFur_users_from_database
from pythonic.forms import ProblemForm, RegistrationForm, LoginForm, UpdateProfileForm,AppointmentForm
from pythonic import app, bcrypt, db
from flask_login import login_required, login_user, current_user, logout_user
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pythonic.models import User
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

@app.route("/aboutUs")
def about():
    return render_template('about.html')


@app.route("/services")
def services():
    return render_template('services.html')

@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    form = AppointmentForm()
    craft_owner_name = request.args.get('craft_owner')
    service_type = request.args.get('service_type')

    if request.method == 'POST' and form.validate_on_submit():
        form_data = {
            'first_name': form.first_name.data,
            'last_name': form.last_name.data,
            'phone_number': form.phone_number.data,
            'street_address': form.street_address.data,
            'city': form.city.data,
            'state': form.state.data,
            'postal_code': form.postal_code.data,
            'appointment_date': form.appointment_date.data,
            'appointment_time': form.appointment_time.data,
            'appointment_purpose': form.appointment_purpose.data,
            'message': form.message.data,
            'craft_owner': craft_owner_name
        }
        return render_template('appointments.html', form=form, craft_owner=craft_owner_name, service_type=service_type, form_data=form_data)
    
    return render_template('appointments.html', form=form, craft_owner=craft_owner_name, service_type=service_type, form_data=None)

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

@app.route('/suggestion', methods=['GET', 'POST'])
def suggestion():
    problem_form = ProblemForm()  # Instantiate the ProblemForm
    return render_template('suggestion.html', problem_form=problem_form)

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