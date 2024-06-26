from tokenize import String
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import DateField, HiddenField, StringField, PasswordField, SubmitField, BooleanField, TextAreaField,SelectField, TimeField
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    Regexp,
    EqualTo,
    ValidationError,
)

from pythonic.models import User

class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=25)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Regexp(
                "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_])[A-Za-z\d@$!%*?&_]{8,32}$"
            ),
        ]
    )
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    address = StringField(
        "Address", validators=[DataRequired(), Length(min=2, max=25)]
    )
    contactNumber = StringField(
    "Contact Number",
    validators=[
        DataRequired(),
        Length(min=10, max=10),
        Regexp('^[0-9]*$', message='Contact number must contain only numbers')
    ]
)
    user_type = SelectField(
        "User Type",
        choices=[("customer", "Customer"), ("craft_owner", "Craft Owner")],
        validators=[DataRequired()],
    )
    service_type = SelectField("Service Type", choices=[("painting", "Painting"), ("plumbing", "Plumbing"), ("appliance_repair", "Appliance Repair"), ("carpentry", "Carpentry"), ("furniture_moving", "Furniture Moving"), ("other", "Other")],validators=[DataRequired()],)
    description = TextAreaField("Description")

    #lname = StringField("Last Name", validators=[DataRequired(), Length(min=2, max=25)])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "Username already exists! Please chosse a different one"
            )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already exists! Please chosse a different one")
        
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
        ],
    )
    remember = BooleanField("Remember Me")
    submit = SubmitField("Log In")

class UpdateProfileForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=25)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    address = StringField(
        "Address", validators=[DataRequired(), Length(min=2, max=25)]
    )
    contactNumber = StringField(
    "Contact Number",
    validators=[
        DataRequired(),
        Length(min=10, max=10),
        Regexp('^[0-9]*$', message='Contact number must contain only numbers')
    ]
)
    description = TextAreaField("Description")
    picture = FileField(
        "Update Profile Picture", validators=[FileAllowed(["jpg", "png"])]
    )
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    "Username already exists! Please chosse a different one"
                )

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    "Email already exists! Please chosse a different one"
                )
class ProblemForm(FlaskForm):
    problem_description = TextAreaField('Problem Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class NewLessonForm(FlaskForm):
    start_time = TimeField('Start Time', validators=[DataRequired()])
    end_time = TimeField('End Time', validators=[DataRequired()])
    all_days = BooleanField('Work All Days')
    workingDays = StringField('working Days')
    submit = SubmitField('Save')

class AppointmentForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    street_address = StringField('Street Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    postal_code = StringField('Postal Code', validators=[DataRequired()])
    appointment_date = SelectField('Appointment Date', choices=[], validators=[DataRequired()])
    appointment_time = SelectField('Appointment Time', choices=[], validators=[DataRequired()])
    appointment_purpose = StringField('Purpose of Appointment', validators=[DataRequired()])
    message = TextAreaField('Additional Message')
    craft_owner = StringField('Craft Owner', render_kw={'readonly': True})
    service_type = StringField('Service Type', render_kw={'readonly': True})
    submit = SubmitField('Book Appointment')