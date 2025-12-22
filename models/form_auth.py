from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class FormSignIn(FlaskForm):
    email = EmailField(
        "Email",
        validators=[
            DataRequired("Email required."),
            Email("Invalid email."),
        ],
        render_kw={"placeholder": "example@gmail.com"},
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired(message="Password required.")],
    )


class FormSignUp(FlaskForm):
    full_name = StringField(
        "Full name",
        validators=[
            DataRequired("Full name required."),
            Length(min=4, message=("Full name at least 4 character.")),
        ],
        render_kw={"placeholder": "John Doe"},
    )
    email = EmailField(
        "Email",
        validators=[
            DataRequired("Email required."),
            Email("Invalid email."),
        ],
        render_kw={"placeholder": "example@gmail.com"},
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired("Password required."),
            Length(min=6, message="Password at least 6 character."),
        ],
    )
