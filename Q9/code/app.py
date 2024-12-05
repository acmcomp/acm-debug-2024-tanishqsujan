import os
import sqlite3
import logging
from flask import Flask, render_template, request, redirect, url_for, g, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_seasurf import SeaSurf
app = Flask(
    __name__,
    static_folder="static",
    template_folder="templates"
)
app.secret_key = os.urandom(24)
csrf = SeaSurf(app)
DATABASE = "profiles.db"
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
def get_db():
    """Get a database connection."""
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db
@app.teardown_appcontext
def close_connection(exception):
    """Close database connection after request."""
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()
def init_db():
    """Initialize the database using schema.sql."""
    with app.app_context():
        db = get_db()
        with open("schema.sql", mode="r") as f:
            db.cursor().executescript(f.read())
        db.commit()
@app.route("/")
def index():
    """Render the homepage."""
    return render_template("index.html")
@app.route("/submit", methods=["POST"])
def submit():
    """Handle contact form submission."""
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]
        db = get_db()
        db.execute(
            "INSERT INTO submissions (name, email, message) VALUES (?, ?, ?)",
            (name, email, message),
        )
        db.commit()
        logger.info(f"New submission from {name} ({email})")
        flash("Your submission has been received!", "success")
        return redirect(url_for("thank_you"))
@app.route("/thank_you")
def thank_you():
    """Render the thank you page."""
    return render_template("thank_you.html")
@app.route("/register", methods=["GET", "POST"])
def register():
    """Handle user registration."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if len(username) < 4 or len(password) < 6:
            flash("Username must be at least 4 characters, and password at least 6.", "danger")
            return redirect(url_for("register"))
        hashed_password = generate_password_hash(password)
        db = get_db()
        try:
            db.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_password),
            )
            db.commit()
            flash("Registration successful! Please log in.", "success")
        except sqlite3.IntegrityError:
            flash("Username already exists. Please choose another.", "danger")
        return redirect(url_for("login"))
    return render_template("register.html")
@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        if user and check_password_hash(user[2], password):
            session["user_id"] = user[0]
            session["username"] = user[1]
            flash("Login successful!", "success")
            return redirect(url_for("index"))
        else:
            flash("Invalid credentials. Please try again.", "danger")
    return render_template("login.html")
@app.route("/logout")
def logout():
    """Handle user logout."""
    session.pop("user_id", None)
    session.pop("username", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))
@app.route("/submissions")
def submissions():
    """Display all submissions."""
    if "user_id" not in session:
        flash("Please log in to view submissions.", "warning")
        return redirect(url_for("login"))
    db = get_db()
    cur = db.execute("SELECT id, name, email, message FROM submissions")
    submissions = cur.fetchall()
    return render_template("submissions.html", submissions=submissions)
@app.route("/delete_submission/<int:id>", methods=["POST"])
def delete_submission(id):
    """Delete a specific submission."""
    if "user_id" not in session:
        flash("Please log in to delete submissions.", "warning")
        return redirect(url_for("login"))
    db = get_db()
    try:
        result = db.execute("DELETE FROM submissions WHERE id = ?", (id,))
        if result.rowcount == 0:
            flash("Submission not found.", "warning")
        else:
            flash("Submission deleted successfully.", "success")
        db.commit()
    except Exception as e:
        logger.error(f"Error deleting submission: {e}")
        flash("An error occurred while deleting the submission.", "danger")
    return redirect(url_for("submissions"))
@app.route("/profile")
def profile():
    """Display user profile."""
    if "user_id" not in session:
        flash("Please log in to view your profile.", "warning")
        return redirect(url_for("login"))
    db = get_db()
    user = db.execute(
        "SELECT id, username FROM users WHERE id = ?", (session["user_id"],)
    ).fetchone()
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("logout"))
    return render_template("profile.html", user=user)
@app.route("/update_profile", methods=["POST"])
def update_profile():
    """Update user profile."""
    if "user_id" not in session:
        flash("Please log in to update your profile.", "warning")
        return redirect(url_for("login"))
    username = request.form["username"]
    password = request.form["password"]
    hashed_password = generate_password_hash(password, method="sha256")
    db = get_db()
    db.execute(
        "UPDATE users SET username = ?, password = ? WHERE id = ?",
        (username, hashed_password, session["user_id"]),
    )
    db.commit()
    flash("Profile updated successfully.", "success")
    return redirect(url_for("profile"))
if __name__ == "__main__":
    if not os.path.exists(DATABASE):
        init_db()
    app.run(debug=True, port=5001)
