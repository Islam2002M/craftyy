from tokenize import String
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,SelectField,TextAreaField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo


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
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    address = StringField(
        "Address", validators=[DataRequired(), Length(min=2, max=25)]
    )
    contact_number = StringField(
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
    description = TextAreaField("Description"  ,  validators=[DataRequired()]
)

    #lname = StringField("Last Name", validators=[DataRequired(), Length(min=2, max=25)])
    submit = SubmitField("Sign Up")


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