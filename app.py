from flask import (
    Flask,
    render_template,
    request,
    session,
    redirect,
    url_for,
    flash,
)
from models.user_model import UserModel
from models.form_auth import FormSignIn, FormSignUp
from models.authentication import Authentication
from datetime import timedelta
from functools import wraps
from supabase_client import supabase

app = Flask(
    __name__, template_folder="templates", static_folder="static", static_url_path="/"
)
app.secret_key = "responsifprakweb2025"
app.permanent_session_lifetime = timedelta(days=5)


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("sign_in"))
        return f(*args, **kwargs)

    return decorated


@app.route("/sign-in", methods=["GET", "POST"])
def sign_in():
    form = FormSignIn()
    if request.method == "POST":
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data

            auth = Authentication.sign_in_user(email, password)

            if isinstance(auth, dict):
                flash(auth["message"], "danger")
                return redirect(url_for("sign_in"))

            session.clear()
            session.permanent = True
            session["user_id"] = auth.user.id
            session["email"] = auth.user.email
            session["access_token"] = auth.session.access_token

            return redirect(url_for("index"))
    return render_template("auth/sign_in.html", form=form)


@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    form = FormSignUp()

    if request.method == "POST":
        if form.validate_on_submit():
            full_name = form.full_name.data.title()
            email = form.email.data
            password = form.password.data

            auth = Authentication.sign_up_user(full_name, email, password)

            if not auth["success"]:
                flash(auth["message"], "danger")
                return redirect(url_for("sign_up"))

            flash(auth["message"], "success")
            return redirect(url_for("sign_in"))

    return render_template("auth/sign_up.html", form=form)


@app.route("/auth/confirmed")
def auth_confirmed():
    if "user_id" in session:
        return redirect(url_for("index"))

    if not request.full_path.endswith("#"):
        return redirect(url_for("sign_in"))

    return render_template("auth/confirmed.html")


@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("sign_in"))


@app.route("/")
@login_required
def index():
    email = session.get("email")
    username = email.split("@")[0] if email else "User"

    return render_template("index.html", username=username)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("not_found.html")


if __name__ == "__main__":
    app.run(debug=True)
