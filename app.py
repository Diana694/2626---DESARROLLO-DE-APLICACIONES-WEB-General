from flask import Flask, render_template, redirect, url_for
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

app = Flask(__name__)
# SECRET_KEY obligatoria para protección CSRF
app.config['SECRET_KEY'] = 'panaderia_aqui_me_voy_secret_key_2026'

# Almacenamiento temporal en memoria
lista_productos = [
    {"nombre": "pan de molde", "categoria": "Panadería", "precio": 2.50, "stock": 12},
    {"nombre": "torta de chocolate", "categoria": "Pastelería", "precio": 15.00, "stock": 3},
    {"nombre": "croissant de queso", "categoria": "Hojaldre", "precio": 0.80, "stock": 0},
    {"nombre": "empanada de carne", "categoria": "Bocadillos", "precio": 1.00, "stock": 20},
    {"nombre": "pan baguette", "categoria": "Panadería", "precio": 1.25, "stock": 0}
]

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
    resumen_dia = {
        "ventas_totales": 125.50,
        "pedidos_pendientes": 5,
        "productos_bajo_stock": sum(1 for p in lista_productos if p["stock"] == 0)
    }
    return render_template("index.html", mensaje=mensaje_bienvenida, resumen=resumen_dia)

# --- PRODUCTOS ---
@app.route("/productos")
def productos():
    return render_template("productos.html", productos=lista_productos)

@app.route("/productos/nuevo", methods=["GET", "POST"])
def formulario_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        lista_productos.append({
            "nombre": form.nombre.data.lower(),
            "categoria": form.categoria.data,
            "precio": float(form.precio.data),
            "stock": form.stock.data
        })
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