from tokenize import String
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField,SelectField,DateField, TimeField
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    Regexp,
    EqualTo,
    ValidationError,
    Optional,
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

    # Optional fields for Craft Owner's availability
    start_date = DateField("Start Date", format='%Y-%m-%d', validators=[Optional()])
    end_date = DateField("End Date", format='%Y-%m-%d', validators=[Optional()])
    time = TimeField("Time", format='%H:%M', validators=[Optional()])

    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    "Username already exists! Please choose a different one."
                )

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    "Email already exists! Please choose a different one."
                )
class ProblemForm(FlaskForm):
    problem_description = TextAreaField('Problem Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class AppointmentForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    street_address = StringField('Street Address', validators=[DataRequired(), Length(max=255)])
    city = StringField('City', validators=[DataRequired(), Length(max=100)])
    state = StringField('State', validators=[DataRequired(), Length(max=100)])
    postal_code = StringField('Postal Code', validators=[DataRequired(), Length(max=20)])
    appointment_date = DateField('Appointment Date', validators=[DataRequired()])
    appointment_time = TimeField('Appointment Time', validators=[DataRequired()])
    appointment_purpose = SelectField('Purpose Of Appointment', choices=[
        ('Carpentry', 'Carpentry'),
        ('Cleaning', 'Cleaning'),
        ('Electrical', 'Electrical'),
        ('Moving Furniture', 'Moving Furniture'),
        ('Painting', 'Painting'),
        ('Plumbing', 'Plumbing')
    ], validators=[DataRequired()])
    message = TextAreaField('Message')
    craft_owner=StringField('craftowner')