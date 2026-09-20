from flask_login import UserMixin

# La clase Usuario le ayuda a Flask-Login a saber quién está conectado
class Usuario(UserMixin):
    def __init__(self, id, usuario, password):
        self.id = id
        self.usuario = usuario
        self.password = password