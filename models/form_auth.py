from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class FormSignIn(FlaskForm):
    email = EmailField(
        "Email",
        validators=[
            DataRequired("Email wajib diisi."),
            Email("Format email tidak valid."),
        ],
        render_kw={"placeholder": "Masukkan email"},
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired(message="Password harus diisi")],
        render_kw={"placeholder": "Masukkan password"},
    )


class FormSignUp(FlaskForm):
    full_name = StringField(
        "Nama Lengkap",
        validators=[
            DataRequired("Nama lengkap harus diisi."),
            Length(min=4, message=("Nama terlalu pendek.")),
        ],
        render_kw={"placeholder": "Masukkan nama lengkap"},
    )
    email = EmailField(
        "Email",
        validators=[
            DataRequired("Email wajib diisi."),
            Email("Format email tidak valid."),
        ],
        render_kw={"placeholder": "Masukkan email"},
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired("Password tidak boleh kosong."),
            Length(min=6, message="Password minimal 6 karakter."),
        ],
        render_kw={"placeholder": "Masukkan password"},
    )
