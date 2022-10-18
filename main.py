from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email
from flask_bootstrap import Bootstrap
from email_manager import New_Client

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

# Bootstrap Setup
Bootstrap(app)
'''
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

db.create_all()
'''
'''new_client = Client(
    name="Daniel",
    email="eldaniel@gmail.com",
    cellphone="546889753",
    numero_personas=8,
    game_type="Historia 1",
    cp="45879"
)
db.session.add(new_client)
db.session.commit()
'''


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


@app.route('/', methods=["GET", "POST"])
def home():
    info_form = Email_Form()
    email_manager = New_Client()
    if info_form.validate_on_submit():
        message = f'''Subject: Cotizacion nueva \n \n
                     {info_form.name.data} quiere cotizar una sesion para {info_form.numero_personas.data} personas, 
                    para la historia {info_form.game_type.data}. Lo puedes contactar por WhatsApp 
                    al numero: {info_form.cellphone.data} o a su correo: {info_form.email.data}, 
                    su CP es {info_form.cp.data}.'''.encode("utf-8")
        email_manager.send_email(message)
        '''
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
        '''
        return redirect(url_for('home'))
    return render_template('index.html', form=info_form)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
