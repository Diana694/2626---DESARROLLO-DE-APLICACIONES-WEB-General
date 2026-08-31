import os
import sqlite3
from flask import Flask, render_template, redirect, url_for
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

app = Flask(__name__)
# SECRET_KEY obligatoria para protección CSRF
app.config['SECRET_KEY'] = 'panaderia_aqui_me_voy_secret_key_2026'

# --- CONFIGURACIÓN DE CONEXIÓN A SQLITE ---
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data', 'ferreteria.db')

def get_db_connection():
    """Establece conexión con la base de datos SQLite."""
    conn = sqlite3.connect(DB_PATH)
    # Permite acceder a las columnas por nombre (ej: fila['nombre'])
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Crea la carpeta data y la tabla 'productos' con datos iniciales si no existen."""
    data_dir = os.path.join(BASE_DIR, 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Crear la tabla de productos si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    ''')
    
    # 2. Insertar registros iniciales de prueba si la tabla está vacía
    cursor.execute('SELECT COUNT(*) FROM productos')
    if cursor.fetchone()[0] == 0:
        productos_iniciales = [
            ("pan de molde", "Panadería", 2.50, 12),
            ("torta de chocolate", "Pastelería", 15.00, 3),
            ("croissant de queso", "Hojaldre", 0.80, 0),
            ("empanada de carne", "Bocadillos", 1.00, 20),
            ("pan baguette", "Panadería", 1.25, 0)
        ]
        cursor.executemany(
            'INSERT INTO productos (nombre, categoria, precio, stock) VALUES (?, ?, ?, ?)',
            productos_iniciales
        )
        conn.commit()
        
    conn.close()

# Inicializamos la base de datos local
init_db()

# --- DATOS EN MEMORIA PARA MÓDULOS SECUNDARIOS ---
lista_clientes = [
    {"nombre": "Juan Pérez", "telefono": "0991234567", "tipo": "Frecuente"},
    {"nombre": "María Gómez", "telefono": "0987654321", "tipo": "Ocasional"}
]

lista_proveedores = [
    {"empresa": "Harinas del Ecuador", "contacto": "Carlos Ruiz", "telefono": "022345678"},
    {"empresa": "Llácteos El Campo", "contacto": "Ana López", "telefono": "022876543"}
]

lista_facturas = []


@app.route("/")
def home():
    mensaje_bienvenida = "Bienvenido al Sistema de Gestión"
    
    # Consultamos stock bajo directamente desde SQLite
    conn = get_db_connection()
    productos_db = conn.execute('SELECT stock FROM productos').fetchall()
    conn.close()
    
    resumen_dia = {
        "ventas_totales": 125.50,
        "pedidos_pendientes": 5,
        "productos_bajo_stock": sum(1 for p in productos_db if p["stock"] == 0)
    }
    return render_template("index.html", mensaje=mensaje_bienvenida, resumen=resumen_dia)


# --- PRODUCTOS (CON PERSISTENCIA SQLITE) ---

@app.route("/productos")
def productos():
    # SELECT: Recuperar los productos almacenados dinámicamente
    conn = get_db_connection()
    lista_productos = conn.execute('SELECT * FROM productos ORDER BY id DESC').fetchall()
    conn.close()
    return render_template("productos.html", productos=lista_productos)


@app.route("/productos/nuevo", methods=["GET", "POST"])
def formulario_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        # Captura de datos validados del formulario
        nombre_val = form.nombre.data.lower()
        categoria_val = form.categoria.data
        precio_val = float(form.precio.data)
        stock_val = form.stock.data

        # INSERT: Consulta parametrizada en SQLite
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO productos (nombre, categoria, precio, stock) VALUES (?, ?, ?, ?)',
            (nombre_val, categoria_val, precio_val, stock_val)
        )
        conn.commit()
        conn.close()

        return redirect(url_for("productos"))
        
    return render_template("formulario_producto.html", form=form)


# --- CLIENTES ---
@app.route("/clientes")
def clientes():
    return render_template("clientes.html", clientes=lista_clientes)

@app.route("/clientes/nuevo", methods=["GET", "POST"])
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


# --- PROVEEDORES ---
@app.route("/proveedores")
def proveedores():
    return render_template("proveedores.html", proveedores=lista_proveedores)

@app.route("/proveedores/nuevo", methods=["GET", "POST"])
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


# --- FACTURACIÓN ---
@app.route("/facturacion")
def facturacion():
    return render_template("facturacion.html", facturas=lista_facturas)

@app.route("/facturacion/nueva", methods=["GET", "POST"])
def formulario_facturacion():
    form = FacturacionForm()
    
    # Consultamos los productos almacenados en SQLite para llenar el Select dynamic
    conn = get_db_connection()
    lista_productos = conn.execute('SELECT nombre FROM productos').fetchall()
    conn.close()

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