from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

from flask import Flask, render_template, request
import smtplib
from email.mime.text import MIMEText
from config_email import GMAIL_USER, GMAIL_PASSWORD, DESTINATION_EMAIL

import os
app = Flask(__name__)


@app.route('/about')
def about():  # put application's code here
    return render_template('about.html')


@app.route('/index')
def index():  # put application's code here
    print('indie')
    return render_template('index.html')


@app.route('/service')
def service():
    print('servie')
    return render_template('service.html')

@app.route("/examples")
def examples():
    return render_template()

@app.route('/submit_form', methods=['POST'])
def submit_form():
    name = request.form.get('inputName4')
    email = request.form.get('inputEmail4')
    subject = request.form.get('inputSubject4')
    message = request.form.get('inputMessage')
    video = request.files['videoFile']

    # Create a MIME object
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = DESTINATION_EMAIL
    msg['Subject'] = subject
    body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
    msg.attach(MIMEText(body, 'plain'))
    if video:
        video_part = MIMEApplication(video.read(), Name=video.filename)
        video_part['Content-Disposition'] = f'attachment; filename="{video.filename}"'
        msg.attach(video_part)
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.sendmail(GMAIL_USER, DESTINATION_EMAIL, msg.as_string())
        server.close()
        print('Email sent successfully!')
    except Exception as e:
        print(f'Failed to send email: {e}')

    return render_template("index.html")


if __name__ == '__main__':
    app.run(host="192.168.178.82", port=5000)
