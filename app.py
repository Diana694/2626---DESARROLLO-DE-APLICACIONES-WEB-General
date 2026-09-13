from flask import Flask, render_template, redirect, url_for, request, flash
from conexion.conexion import obtener_conexion
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

app = Flask(__name__)
# SECRET_KEY obligatoria para protección CSRF
app.config['SECRET_KEY'] = 'panaderia_aqui_me_voy_secret_key_2026'

# --- DATOS EN MEMORIA PARA MÓDULOS SECUNDARIOS ---
lista_clientes = [
    {"nombre": "Juan Pérez", "telefono": "0991234567", "tipo": "Frecuente"},
    {"nombre": "María Gómez", "telefono": "0987654321", "tipo": "Ocasional"}
]

lista_proveedores = [
    {"empresa": "Harinas del Ecuador", "contacto": "Carlos Ruiz", "telefono": "022345678"},
    {"empresa": "Lácteos El Campo", "contacto": "Ana López", "telefono": "022876543"}
]

lista_facturas = []


# --- PÁGINA PRINCIPAL ---
@app.route("/")
def home():
    mensaje_bienvenida = "Bienvenido al Sistema de Gestión"
    
    # Consultamos stock bajo directamente desde MySQL
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
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


# --- PRODUCTOS (PERSISTENCIA CON MYSQL - CRUD COMPLETO) ---

# 1. LISTAR (SELECT con JOIN)
@app.route("/productos")
def productos():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
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


# 2. AGREGAR (INSERT INTO)
@app.route("/productos/nuevo", methods=["GET", "POST"])
def formulario_producto():
    form = ProductoForm()
    
    # Cargar los proveedores disponibles en el desplegable
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT id_proveedor, nombre FROM proveedores")
    proveedores_db = cursor.fetchall()
    cursor.close()
    conexion.close()
    
    if hasattr(form, 'id_proveedor'):
        form.id_proveedor.choices = [(p['id_proveedor'], p['nombre']) for p in proveedores_db]

    if form.validate_on_submit():
        nombre_val = form.nombre.data
        precio_val = float(form.precio.data)
        stock_val = form.stock.data
        
        # Obtener el proveedor si existe en tu formulario, de lo contrario tomar el primero
        id_proveedor_val = getattr(form, 'id_proveedor', None)
        id_prov = id_proveedor_val.data if id_proveedor_val else (proveedores_db[0]['id_proveedor'] if proveedores_db else None)

        # INSERT parametrizado
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        query = "INSERT INTO productos (nombre, precio, stock, id_proveedor) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (nombre_val, precio_val, stock_val, id_prov))
        conexion.commit()
        cursor.close()
        conexion.close()

        return redirect(url_for("productos"))
        
    return render_template("formulario_producto.html", form=form)


# 3. MODIFICAR (UPDATE ... WHERE)
@app.route("/productos/editar/<int:id>", methods=["GET", "POST"])
def editar_producto(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id,))
    producto = cursor.fetchone()
    cursor.close()
    conexion.close()

    if not producto:
        return redirect(url_for("productos"))

    form = ProductoForm(data=producto)

    if form.validate_on_submit():
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        query = "UPDATE productos SET nombre = %s, precio = %s, stock = %s WHERE id_producto = %s"
        cursor.execute(query, (form.nombre.data, float(form.precio.data), form.stock.data, id))
        conexion.commit()
        cursor.close()
        conexion.close()
        return redirect(url_for("productos"))

    return render_template("formulario_producto.html", form=form, titulo="Editar Producto")


# 4. ELIMINAR (DELETE FROM ... WHERE)
@app.route("/productos/eliminar/<int:id>", methods=["POST"])
def eliminar_producto(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id,))
    conexion.commit()
    cursor.close()
    conexion.close()
    return redirect(url_for("productos"))


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
    
    # Consultamos los productos almacenados en MySQL para llenar el Select dinámico
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
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