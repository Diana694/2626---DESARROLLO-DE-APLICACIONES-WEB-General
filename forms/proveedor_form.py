from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class ProveedorForm(FlaskForm):
    empresa = StringField('Empresa / Razón Social', validators=[
        DataRequired(message="El nombre de la empresa es obligatorio."),
        Length(min=3, max=100, message="Debe tener entre 3 y 100 caracteres.")
    ])
    contacto = StringField('Persona de Contacto', validators=[
        DataRequired(message="El contacto es obligatorio.")
    ])
    telefono = StringField('Teléfono', validators=[
        DataRequired(message="El teléfono es obligatorio."),
        Length(min=7, max=10, message="El teléfono debe tener entre 7 y 10 dígitos.")
    ])
    submit = SubmitField('Guardar Proveedor')