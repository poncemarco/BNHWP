from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email
from flask_bootstrap import Bootstrap
from email_manager import New_Client
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

# Bootstrap Setup
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clients.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Client(db.Model):
    __tablename__ = "requests"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False, unique=True)
    cellphone = db.Column(db.String(250), nullable=False)
    numero_personas = db.Column(db.Integer, nullable=False)
    game_type = db.Column(db.String(250), nullable=False)
    cp = db.Column(db.String(250), nullable=False)


class Stories(db.Model):
    __tablename__ = "stories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(4000), nullable=False)
    img_url = db.Column(db.String(400), nullable=False)


db.create_all()


# ----------Email and DB ------------------#
class Email_Form(FlaskForm):
    name = StringField(label="Nombre", validators=[DataRequired()])
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    cellphone = StringField(label="Número celular", validators=[DataRequired()])
    numero_personas = SelectField(label="Número de personas que participaran",
                                  choices=["8", "9", "10", "11", "12", "13", "14", "15", "más de 15"])
    game_type = SelectField(label="Tipo de Juego",
                            choices=["Panic At The Disco!", "Sombras del Pasado", "Demoliendo Destinos"])
    cp = StringField(label="Código Postal", validators=[DataRequired()])
    submit_button = SubmitField('submit')


class Story_Form(FlaskForm):
    name = StringField(label="Nombre de la Historia", validators=[DataRequired()])
    description = StringField(label="Descripción corta", validators=[DataRequired()])
    img_url = StringField(label="url de la imagen(click derecho en el archivo de google drive)",
                          validators=[DataRequired()])
    submit_button = SubmitField('submit')


@app.route('/', methods=["GET", "POST"])
def home():
    info_form = Email_Form()
    email_manager = New_Client()
    story_cards = Stories.query.all()
    if info_form.validate_on_submit():
        message = f'''Subject: Cotizacion nueva \n \n
                     {info_form.name.data} quiere cotizar una sesion para {info_form.numero_personas.data} personas, 
                    para la historia {info_form.game_type.data}. Lo puedes contactar por WhatsApp 
                    al numero: {info_form.cellphone.data} o a su correo: {info_form.email.data}, 
                    su CP es {info_form.cp.data}.'''.encode("utf-8")
        email_manager.send_email(message)

        new_client = Client(
            name=info_form.name.data,
            email=info_form.email.data,
            cellphone=info_form.cellphone.data,
            numero_personas=info_form.numero_personas.data,
            game_type=info_form.game_type.data,
            cp=info_form.cp.data
        )
        db.session.add(new_client)
        db.session.commit()

        return redirect(url_for('home'))
    return render_template('index.html', form=info_form, stories=story_cards)


@app.route("/add", methods=["GET", "POST"])
def add_story():
    story_form = Story_Form()
    if story_form.validate_on_submit():
        new_story = Stories(
            name=story_form.name.data,
            description=story_form.description.data,
            img_url=story_form.img_url.data
        )
        db.session.add(new_story)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_story.html', form=story_form)


if __name__ == "__main__":
    app.run()