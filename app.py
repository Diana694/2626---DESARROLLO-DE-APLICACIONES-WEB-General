import os
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from conexion.conexion import obtener_conexion
from models import Usuario
from forms.login_form import LoginForm
from forms.usuario_form import RegistroForm
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'panaderia_aqui_me_voy_secret_key_2026')

# --- CONFIGURACIÓN DE FLASK-LOGIN ---
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(user_id):
    conexion = obtener_conexion()
    if not conexion:
        return None
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    conexion.close()
    if user_data:
        return Usuario(id=user_data['id'], usuario=user_data['usuario'], password=user_data['password'])
    return None

# --- DATOS EN MEMORIA (AUXILIARES) ---
lista_clientes = [
    {"nombre": "Juan Pérez", "telefono": "0991234567", "tipo": "Frecuente"},
    {"nombre": "María Gómez", "telefono": "0987654321", "tipo": "Ocasional"}
]

lista_proveedores = [
    {"empresa": "Harinas del Ecuador", "contacto": "Carlos Ruiz", "telefono": "022345678"},
    {"empresa": "Lácteos El Campo", "contacto": "Ana López", "telefono": "022876543"}
]

lista_facturas = []


# --- RUTAS DE AUTENTICACIÓN ---

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    form = RegistroForm()
    if form.validate_on_submit():
        usuario_val = form.usuario.data
        hashed_password = generate_password_hash(form.password.data)
        
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            try:
                cursor.execute("INSERT INTO usuarios (usuario, password) VALUES (%s, %s)", (usuario_val, hashed_password))
                conexion.commit()
                flash('Usuario registrado exitosamente. Ya puedes iniciar sesión.', 'success')
                return redirect(url_for('login'))
            except Exception:
                conexion.rollback()
                flash('El nombre de usuario ya existe. Elige otro.', 'danger')
            finally:
                cursor.close()
                conexion.close()
            
    return render_template('registro.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    form = LoginForm()
    if form.validate_on_submit():
        usuario_val = form.usuario.data
        password_val = form.password.data
        
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE usuario = %s", (usuario_val,))
            user_data = cursor.fetchone()
            cursor.close()
            conexion.close()
            
            if user_data and check_password_hash(user_data['password'], password_val):
                user_obj = Usuario(id=user_data['id'], usuario=user_data['usuario'], password=user_data['password'])
                login_user(user_obj)
                flash(f'¡Bienvenido, {user_obj.usuario}!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Usuario o contraseña incorrectos.', 'danger')
            
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('login'))


# --- RUTAS PROTEGIDAS Y OPERACIONES CRUD ---

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route("/")
@login_required
def home():
    mensaje_bienvenida = "Bienvenido al Sistema de Gestión"
    productos_db = []
    
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute('SELECT stock FROM productos')
        productos_db = cursor.fetchall()
        cursor.close()
        conexion.close()
    
    resumen_dia = {
        "ventas_totales": 125.50,
        "pedidos_pendientes": 5,
        "productos_bajo_stock": sum(1 for p in productos_db if p["stock"] == 0)
    }
    return render_template("index.html", mensaje=mensaje_bienvenida, resumen=resumen_dia)


# LEER (SELECT CON JOIN)
@app.route("/productos")
@login_required
def productos():
    lista_productos = []
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        query = """
            SELECT p.id_producto AS id, p.nombre, p.precio, p.stock, pr.nombre AS proveedor 
            FROM productos p
            LEFT JOIN proveedores pr ON p.id_proveedor = pr.id_proveedor
            ORDER BY p.id_producto DESC
        """
        cursor.execute(query)
        lista_productos = cursor.fetchall()
        cursor.close()
        conexion.close()
    return render_template("productos.html", productos=lista_productos)


# CREAR (INSERT)
@app.route("/productos/nuevo", methods=["GET", "POST"])
@login_required
def formulario_producto():
    form = ProductoForm()
    proveedores_db = []
    
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT id_proveedor, nombre FROM proveedores")
        proveedores_db = cursor.fetchall()
        cursor.close()
        conexion.close()
    
    if hasattr(form, 'id_proveedor') and proveedores_db:
        form.id_proveedor.choices = [(p['id_proveedor'], p['nombre']) for p in proveedores_db]

    if form.validate_on_submit():
        nombre_val = form.nombre.data
        precio_val = float(form.precio.data)
        stock_val = form.stock.data
        
        id_proveedor_val = getattr(form, 'id_proveedor', None)
        id_prov = id_proveedor_val.data if id_proveedor_val else (proveedores_db[0]['id_proveedor'] if proveedores_db else None)

        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            query = "INSERT INTO productos (nombre, precio, stock, id_proveedor) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (nombre_val, precio_val, stock_val, id_prov))
            conexion.commit()
            cursor.close()
            conexion.close()

        flash('Producto agregado con éxito.', 'success')
        return redirect(url_for("productos"))
        
    return render_template("formulario_producto.html", form=form)


# ACTUALIZAR (UPDATE)
@app.route("/productos/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_producto(id):
    conexion = obtener_conexion()
    if not conexion:
        return redirect(url_for("productos"))
        
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id,))
    producto = cursor.fetchone()
    cursor.close()
    conexion.close()

    if not producto:
        return redirect(url_for("productos"))

    form = ProductoForm(data=producto)

    if form.validate_on_submit():
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            query = "UPDATE productos SET nombre = %s, precio = %s, stock = %s WHERE id_producto = %s"
            cursor.execute(query, (form.nombre.data, float(form.precio.data), form.stock.data, id))
            conexion.commit()
            cursor.close()
            conexion.close()
            flash('Producto actualizado correctamente.', 'success')
        return redirect(url_for("productos"))

    return render_template("formulario_producto.html", form=form, titulo="Editar Producto")


# ELIMINAR (DELETE)
@app.route("/productos/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_producto(id):
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id,))
        conexion.commit()
        cursor.close()
        conexion.close()
        flash('Producto eliminado.', 'warning')
    return redirect(url_for("productos"))


@app.route("/clientes")
@login_required
def clientes():
    return render_template("clientes.html", clientes=lista_clientes)


@app.route("/clientes/nuevo", methods=["GET", "POST"])
@login_required
def formulario_cliente():
    form = ClienteForm()
    if form.validate_on_submit():
        lista_clientes.append({
            "nombre": form.nombre.data,
            "telefono": form.telefono.data,
            "tipo": form.tipo.data
        })
        return redirect(url_for("clientes"))
    return render_template("formulario_cliente.html", form=form)


@app.route("/proveedores")
@login_required
def proveedores():
    return render_template("proveedores.html", proveedores=lista_proveedores)


@app.route("/proveedores/nuevo", methods=["GET", "POST"])
@login_required
def formulario_proveedor():
    form = ProveedorForm()
    if form.validate_on_submit():
        lista_proveedores.append({
            "empresa": form.empresa.data,
            "contacto": form.contacto.data,
            "telefono": form.telefono.data
        })
        return redirect(url_for("proveedores"))
    return render_template("formulario_proveedor.html", form=form)


@app.route("/facturacion")
@login_required
def facturacion():
    return render_template("facturacion.html", facturas=lista_facturas)


@app.route("/facturacion/nueva", methods=["GET", "POST"])
@login_required
def formulario_facturacion():
    form = FacturacionForm()
    lista_productos = []
    
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute('SELECT nombre FROM productos')
        lista_productos = cursor.fetchall()
        cursor.close()
        conexion.close()

    form.cliente.choices = [(i, c["nombre"]) for i, c in enumerate(lista_clientes)]
    form.producto.choices = [(i, p["nombre"].title()) for i, p in enumerate(lista_productos)]
    
    if form.validate_on_submit():
        cliente_sel = lista_clientes[form.cliente.data]["nombre"]
        prod_sel = lista_productos[form.producto.data]["nombre"].title()
        
        lista_facturas.append({
            "cliente": cliente_sel,
            "producto": prod_sel,
            "cantidad": form.cantidad.data,
            "precio_unitario": float(form.precio_unitario.data),
            "total": float(form.precio_unitario.data) * form.cantidad.data
        })
        return redirect(url_for("facturacion"))
    return render_template("formulario_facturacion.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)