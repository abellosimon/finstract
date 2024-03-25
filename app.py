from flask import Flask, render_template, request, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, FileField
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileRequired
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Secret key for CSRF protection
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret_key')
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['MAX_CONTENT_PATH'] = 16 * 1024 * 1024  # 16MB upload limit

# Form class using Flask-WTF
class ContactForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    file = FileField('File', validators=[FileRequired()])

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    form = ContactForm()
    if form.validate_on_submit():
        email = form.email.data
        file = form.file.data
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Process the email and file as needed
        flash('Form submitted successfully!')
        return redirect('/')
    return render_template('home.html', form=form)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
