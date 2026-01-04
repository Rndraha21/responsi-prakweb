from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SelectField
from wtforms.validators import DataRequired, Length, Email, AnyOf, ValidationError
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_ckeditor import CKEditorField


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


class FormArticle(FlaskForm):
    game_choices = [
        "MOBILE LEGENDS",
        "LEAGUE OF LEGENDS",
        "PUBG MOBILE",
        "FREE FIRE",
        "HONOR OF KINGS",
        "EFOOTBALL",
        "DOTA2",
    ]
    game_name = SelectField(
        "Game",
        choices=[
            ("MOBILE LEGENDS", "Mobile Legends: Bang Bang"),
            ("LEAGUE OF LEGENDS", "League of Legends"),
            ("PUBG MOBILE", "PUBG Mobile"),
            ("FREE FIRE", "Free Fire"),
            ("HONOR OF KINGS", "Honor of Kings"),
            ("EFOOTBALL", "E-Football"),
            ("DOTA2", "Dota 2"),
        ],
        validators=[DataRequired(message="Game name required."), AnyOf(game_choices)],
    )

    thumbnail = FileField(
        "Thumbnail",
        validators=[
            FileAllowed(["jpg", "jpeg", "png"], "Only image files allowed."),
            FileRequired(message="No selected file."),
        ],
    )

    def validate_thumbnail(self, field):
        if field.data:
            max_size = 4 * 1024 * 1024

            file_data = field.data.read()
            size = len(file_data)

            field.data.seek(0)

            if size > max_size:
                raise ValidationError(
                    f"File to large! Max. 4MB, (Size: {size/1024/1024:.2f}MB)"
                )

    title = StringField(
        "Title",
        validators=[
            DataRequired(message="Title required."),
            Length(min=5, message="Title at least 5 characters."),
        ],
        render_kw={"placeholder": "MPL Season 17"},
    )

    content = CKEditorField(
        "Content",
        validators=[
            DataRequired("Content required"),
            Length(
                min=50,
                message="The content is too short; please make it more descriptive.",
            ),
        ],
    )
