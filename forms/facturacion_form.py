from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, DecimalField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class FacturacionForm(FlaskForm):
    cliente = SelectField('Cliente', coerce=int, validators=[
        DataRequired(message="Seleccione un cliente.")
    ])
    producto = SelectField('Producto', coerce=int, validators=[
        DataRequired(message="Seleccione un producto.")
    ])
    cantidad = IntegerField('Cantidad', validators=[
        DataRequired(message="La cantidad es obligatoria."),
        NumberRange(min=1, message="La cantidad mínima es 1.")
    ])
    precio_unitario = DecimalField('Precio Unitario ($)', validators=[
        DataRequired(message="El precio es obligatorio."),
        NumberRange(min=0.01, message="El precio debe ser mayor a 0.")
    ])
    submit = SubmitField('Generar Factura')