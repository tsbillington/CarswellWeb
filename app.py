import os

from flask import Flask, flash, redirect, render_template, url_for
from flask_mail import Mail, Message

from forms import ContactForm

app = Flask(__name__, static_folder="public", static_url_path="/static")

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER", "localhost")
app.config["MAIL_PORT"] = int(os.environ.get("MAIL_PORT", 587))
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS", "true").lower() == "true"
app.config["MAIL_USE_SSL"] = os.environ.get("MAIL_USE_SSL", "false").lower() == "true"
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get(
    "MAIL_DEFAULT_SENDER", "no-reply@carswellid.com"
)

mail = Mail(app)

SITE = {
    "company_name": "Carswell Intelligent Designs Inc.",
    "phone": "1-226-388-0688",
    "email": "tim@carswellid.com",
    "linkedin": "https://ca.linkedin.com/in/timothybillington",
    "location": "Waterford, ON, Canada",
}

CONTACT_RECIPIENT = os.environ.get("CONTACT_RECIPIENT", SITE["email"])


@app.context_processor
def inject_site():
    return {"site": SITE}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/xmpie")
def xmpie():
    return render_template("xmpie/index.html")


@app.route("/xmpie/portfolio")
def xmpie_portfolio():
    return render_template("xmpie/portfolio.html")


@app.route("/software")
def software():
    return render_template("software/index.html")


@app.route("/software/portfolio")
def software_portfolio():
    return render_template("software/portfolio.html")


@app.route("/software/portfolio/pressav")
def software_pressav():
    return render_template("software/pressav.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        msg = Message(
            subject=f"New contact form message from {form.name.data}",
            recipients=[CONTACT_RECIPIENT],
            reply_to=form.email.data,
            body=(
                f"Name: {form.name.data}\n"
                f"Email: {form.email.data}\n\n"
                f"Message:\n{form.message.data}"
            ),
        )
        try:
            mail.send(msg)
            flash("Thanks for reaching out! We'll be in touch soon.", "success")
        except Exception:
            flash(
                "Sorry, something went wrong sending your message. Please email us directly.",
                "error",
            )
        return redirect(url_for("contact"))
    return render_template("contact.html", form=form)


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True, port=5000)
