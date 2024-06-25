from flask import Flask,render_template, flash, redirect, url_for, request, session
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = "secret_key"

#Flask_Mail setup
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('EMAIL_USER')

mail = Mail(app)


@app.route("/")
def home():
    return render_template('services.html')

@app.route("/contact",methods=['POST','GET'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        company = request.form['company']
        email = request.form['email']
        phone = request.form['phone']
        subject = request.form['subject']
        message = request.form['message']
        if not name or not email or not message:
            flash('Please fill out all of the required fields.','error')
            return redirect(url_for('contact'))
        else:
            EMAIL_MSG = Message(subject = f'Contact Form Submission: {subject}',
                                recipients=["boualtech.emailer@gmail.com"],
                                body= f"""
                                Name: {name}
                                Company Name: {company}
                                Email: {email}
                                Phone: {phone}
                                Message:\n
                                {message}
                                """)

            try:
                mail.send(EMAIL_MSG)
                flash("Message sent successfully. Bericht succesvol verzonden.", 'success')
            except Exception as err:

                flash(f'Message could not be sent. Error: {str(err)}','error')
            return redirect(url_for('contact'))
    return render_template("contact.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/pricing")
def pricing():
    return render_template("pricing.html")

@app.route("/bundles")
def bundles():
    return render_template("bundles.html")

@app.route('/switch-language', methods=['GET'])
def switch_language():
    lang = request.args.get('lang', 'en')

    # Store the selected language in the session
    session['lang'] = lang

    # Redirect back to the previous page or homepage
    return redirect(request.referrer)

@app.before_request
def before_request():
    # Initialize the session language if it doesn't exist
    if 'lang' not in session:
        session['lang'] = 'en'  # Default language is English


if __name__ == '__main__':
    app.run()