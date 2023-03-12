from flask import Flask, render_template, request, url_for, redirect
from email.mime.text import MIMEText
import smtplib
from email.message import EmailMessage
from flask import Flask, render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email
from email_validator import validate_email, EmailNotValidError
import smtplib
import os



app = Flask(__name__)

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')


def send_email(name, email, message):
    try:
        smtp_server = os.environ.get('SMTP_SERVER')
        smtp_port = os.environ.get('SMTP_PORT')
        smtp_username = os.environ.get('SMTP_USERNAME')
        smtp_password = os.environ.get('SMTP_PASSWORD')
        from_email = os.environ.get('FROM_EMAIL')
        to_email = os.environ.get('TO_EMAIL')

        email_message = f"Subject: New Contact\n\nName: {name}\nEmail: {email}\nMessage: {message}"
        with smtplib.SMTP(smtp_server, smtp_port) as connection:
            connection.starttls()
            connection.login(user=smtp_username, password=smtp_password)
            connection.sendmail(from_addr=from_email, to_addrs=to_email, msg=email_message)

        return True

    except Exception as e:
        print(e)
        return False



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/main")
def projects():
    return render_template("main.html")


@app.route("/sendemail/", methods=['POST'])
def sendemail():
    if request.method == "POST":
        name = request.form['name']
        subject = request.form['Subject']
        email = request.form['_replyto']
        message = request.form['message']

        your_name = "Koray GÜNAL"
        your_email = "koraygunal2619@gmail.com"
        your_password = "123ASHE321"

        # Logging in to our email account
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(your_email, your_password)

        # Sender's and Receiver's email address
        sender_email = "koraygunal2619@gmail.com"
        receiver_email = "koraygnal@gmail.com"

        msg = EmailMessage()
        msg.set_content("First Name : "+str(name)+"\nEmail : "+str(email)+"\nSubject : "+str(subject)+"\nMessage : "+str(message))
        msg['Subject'] = 'New Response on Personal Website'
        msg['From'] = sender_email
        msg['To'] = receiver_email
        # Send the message via our own SMTP server.
        try:
            # sending an email
            server.send_message(msg)
        except:
            pass
    return redirect('/')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            name = form.name.data
            email = form.email.data
            message = form.message.data

            try:
                # Validate the email address
                valid = validate_email(email)
                email = valid.email

                # Send email
                sent = send_email(name, email, message)
                if sent:
                    flash('Your message has been sent!', 'success')
                    return redirect(url_for('contact'))
                else:
                    flash('Sorry, there was an error sending your message. Please try again later.', 'danger')

            except EmailNotValidError as e:
                flash(f'Sorry, {e} is not a valid email address. Please try again.', 'danger')

            except Exception as e:
                flash('Sorry, there was an error sending your message. Please try again later.', 'danger')

    return render_template('contact.html', form=form)



if __name__ == "__main__":
    app.run(debug=True)