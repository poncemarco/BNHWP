from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6ddasdasdas87a6s54da'




@app.route('/')
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)