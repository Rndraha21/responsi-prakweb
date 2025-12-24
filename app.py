import os
from flask import (
    Flask,
    render_template,
    request,
    session,
    redirect,
    url_for,
    flash,
)
from models import UserModel, Authentication, Article
from forms import FormSignIn, FormSignUp, FormArticle
from datetime import timedelta
from functools import wraps
from flask_ckeditor import CKEditor
from werkzeug.utils import secure_filename
from supabase_client import supabase

ckeditor = CKEditor()

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

app = Flask(
    __name__, template_folder="templates", static_folder="static", static_url_path="/"
)

ckeditor.init_app(app)

app.config["CKEDITOR_HEIGHT"] = 200
app.config["CKEDITOR_CODE_THEME"] = "monokai_subl ime"
app.config["CKEDITOR_ENABLE_CODESNIPPET"] = True
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.secret_key = "responsifprakweb2025"
app.permanent_session_lifetime = timedelta(days=5)


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("sign_in"))

        try:
            res = supabase.auth.set_session(
                session["access_token"], session["refresh_token"]
            )

            session["access_token"] = res.session.access_token
            session["refresh_token"] = res.session.refresh_token

        except Exception as e:
            print(f"Auth Error: {e}")
            session.clear()
            flash("Sesi Anda telah berakhir, silakan login kembali.", "warning")
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

            result = Authentication.sign_in_user(email, password)

            if not result["success"]:
                flash(result["message"], "danger")
                return redirect(url_for("sign_in"))

            auth = result["auth"]

            session.permanent = True
            session["user_id"] = auth.user.id
            session["email"] = auth.user.email
            session["access_token"] = auth.session.access_token
            session["refresh_token"] = auth.session.refresh_token

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
    return redirect(url_for("index"))


@app.route("/")
def index():
    model = Article()
    response = model.get_all_article()
    email = session.get("email")
    username = email.split("@")[0] if email else ""

    return render_template(
        "section_template.html", username=username, response=response["data"]
    )


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/write-article", methods=["GET", "POST"])
@login_required
def create_article():
    model = Article()
    form = FormArticle()
    email = session.get("email")
    username = email.split("@")[0] if email else ""

    if request.method == "POST":
        if form.validate_on_submit():
            game_name = form.game_name.data
            file = form.thumbnail.data
            title = form.title.data
            filename = secure_filename(file.filename)
            unique_name = f"{filename}".replace(" ", "_")
            content = form.content.data

            res = model.create_new_article(
                game_name,
                unique_name,
                title,
                content,
                session["user_id"],
            )

            if res["success"]:
                flash(
                    "Article successfully created. Your post will available on public after admin review.",
                    f"{res["category"]}",
                )

                save_path = os.path.join(
                    app.root_path, app.config["UPLOAD_FOLDER"], unique_name
                )
                file.save(save_path)
                return redirect(url_for("index"))

            else:
                flash("Something went wrong. Failed to post article", f"{res["category"]}")
                return redirect(url_for("index"))

    return render_template("/pages/write_pages.html", form=form, username=username)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("not_found.html")


if __name__ == "__main__":
    app.run(debug=True)
