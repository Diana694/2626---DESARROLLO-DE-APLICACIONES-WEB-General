from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class ClienteForm(FlaskForm):
    nombre = StringField('Nombre Completo', validators=[
        DataRequired(message="El nombre es obligatorio."),
        Length(min=3, max=100, message="El nombre debe tener entre 3 y 100 caracteres.")
    ])
    telefono = StringField('Teléfono', validators=[
        DataRequired(message="El teléfono es obligatorio."),
        Length(min=7, max=10, message="El teléfono debe tener entre 7 y 10 dígitos.")
    ])
    tipo = SelectField('Tipo de Cliente', choices=[
        ('Frecuente', 'Frecuente'),
        ('Ocasional', 'Ocasional')
    ], validators=[DataRequired(message="Seleccione un tipo.")])
    submit = SubmitField('Guardar Cliente')