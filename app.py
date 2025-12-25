import os
import uuid
from flask import (
    Flask,
    render_template,
    request,
    session,
    redirect,
    url_for,
    flash,
    abort,
    jsonify,
)
from models import UserModel, Authentication, Article
from forms import FormSignIn, FormSignUp, FormArticle
from datetime import timedelta
from functools import wraps
from flask_ckeditor import CKEditor
from werkzeug.utils import secure_filename
from supabase_client import supabase
import arrow

ckeditor = CKEditor()

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

app = Flask(
    __name__, template_folder="templates", static_folder="static", static_url_path="/"
)

ckeditor.init_app(app)

app.config["CKEDITOR_HEIGHT"] = 200
app.config["CKEDITOR_CODE_THEME"] = "monokai_subl ime"
app.config["CKEDITOR_ENABLE_CODESNIPPET"] = True
app.secret_key = "responsifprakweb2025"
app.permanent_session_lifetime = timedelta(days=5)


# Middleware
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


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user_id = session.get("user_id", "")
        user_role = session.get("role", "")
        if not user_id or user_role != "admin":
            abort(404)
        return f(*args, **kwargs)

    return decorated


# Routes
@app.route("/sign-in", methods=["GET", "POST"])
def sign_in():
    if "user_id" in session:
        flash("You try to login. Please logout first.", "warning")
        return redirect(url_for("index"))

    form = FormSignIn()
    if request.method == "POST":
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data

            result = Authentication.sign_in_user(email, password)
            user_role = UserModel().get_role(result["auth"].user.id)
            role = user_role.data[0]["role"]

            if not result["success"]:
                flash(result["message"], "danger")
                return redirect(url_for("sign_in"))

            auth = result["auth"]

            session.permanent = True
            session["user_id"] = auth.user.id
            session["email"] = auth.user.email
            session["access_token"] = auth.session.access_token
            session["role"] = role
            session["refresh_token"] = auth.session.refresh_token

            email = auth.user.email
            username = email.split("@")[0]

            flash(f"Welcome {username}!", "success")
            return redirect(url_for("index"))
    return render_template("auth/sign_in.html", form=form)


@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if "user_id" in session:
        flash("You try to sign up. Please logout first.", "warning")
        return redirect(url_for("index"))
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
    email = session.get("email")
    username = email.split("@")[0] if email else ""
    session.clear()
    flash(f"Logout successfully see u again {username}", "success")
    return redirect(url_for("index"))


@app.route("/")
def index():
    model = Article()
    role = session.get("role", "guest")
    response = model.get_latest_article()

    now = arrow.now()

    for article in response["data"]:
        arw = arrow.get(article["created_at"])
        diff_day = (now - arw).days

        date = arw.format("ddd, DD MMM YYYY", locale="id")
        relatif = arw.humanize(locale="id")

        if diff_day > 7:
            article["created_at"] = f"{date}"
        else:
            article["created_at"] = f"{relatif}"

    email = session.get("email")
    username = email.split("@")[0] if email else ""

    return render_template(
        "section_template.html", username=username, response=response["data"], role=role
    )


@app.route("/create/article", methods=["GET", "POST"])
@login_required
def create_article():
    form = FormArticle()
    email = session.get("email")
    username = email.split("@")[0] if email else ""

    if request.method == "POST" and form.validate_on_submit():
        file = form.thumbnail.data

        game_name = form.game_name.data
        title = form.title.data
        content = form.content.data
        filename = secure_filename(file.filename)

        ext = os.path.splitext(filename)[1]
        print(ext)

        unique_name = f"{uuid.uuid4()}{ext}"

        try:
            file_data = file.read()
            supabase.storage.from_("thumbnails").upload(
                path=unique_name,
                file=file_data,
                file_options={"content-type": file.content_type},
            )

            public_url = supabase.storage.from_("thumbnails").get_public_url(
                unique_name
            )

            model = Article()
            status = "approved" if session.get("role") == "admin" else "pending"

            res = model.create_new_article(
                game_name, public_url, title, content, session["user_id"], status
            )

            if res["success"]:
                flash("Article successfully created.", "success")
                return redirect(url_for("index"))
            else:
                flash("Failed to save to database.", "danger")
                return redirect(url_for("create_article"))

        except Exception as e:
            print(f"Error: {e}")
            flash("Failed to upload image.", "danger")
            return redirect(url_for("create_article"))

    return render_template("/pages/create_article.html", form=form, username=username)


@app.route("/read/articles")
def read_articles():
    email = session.get("email")
    username = email.split("@")[0] if email else ""

    game_filter = request.args.get("game")

    response = Article().get_articles(session.get("user_id"), game_filter)

    now = arrow.now()
    for article in response["latest"]:
        arw = arrow.get(article["created_at"])
        diff_day = (now - arw).days

        date = arw.format("ddd, DD MMM YYYY", locale="id")
        relatif = arw.humanize(locale="id")

        if diff_day > 1:
            article["created_at"] = f"{date}"
        else:
            article["created_at"] = f"{relatif}"

    return render_template(
        "/pages/read_articles.html",
        username=username,
        latest=response["latest"],
        popular=response["popular"],
    )


@app.route("/read/article/<int:id>")
def read_more(id):
    email = session.get("email")
    username = email.split("@")[0] if email else ""

    user_id = session.get("user_id")
    article = Article().get_article_by_id(id, user_id)

    if not article:
        abort(404)

    arw = arrow.get(article["created_at"])
    article["created_at"] = arw.format("dddd, DD MMMM YYYY", locale="id")

    return render_template("pages/read_more.html", article=article, username=username)


@app.route("/like/article/<id>")
@login_required
def like_article(id):
    user_id = session.get("user_id")
    res = Article().like_article(id, user_id)
    return jsonify(res)


@app.route("/admin/dashboard")
@admin_required
def dashboard_admin():
    email = session.get("email")
    username = email.split("@")[0] if email else ""
    role = session.get("role", "guest")

    return render_template("/pages/read_articles.html", username=username, role=role)


@app.route("/user/dashboard")
@login_required
def dashboard_user():
    email = session.get("email")
    username = email.split("@")[0] if email else ""

    return render_template("/pages/read_articles.html", username=username)


# Error handling
@app.errorhandler(404)
def page_not_found(e):
    print(f"Server Error: {e}")
    return render_template("not_found.html")


@app.errorhandler(500)
def internal_error(error):
    print(f"Server Error: {error}")
    return "Internal server erro", 500


@app.errorhandler(Exception)
def handle_exception(e):
    print({e})
    return "Internal server error", 500


if __name__ == "__main__":
    app.run(debug=True)
