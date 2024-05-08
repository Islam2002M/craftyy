from tokenize import String
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField,SelectField
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