from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    # Variables simples y diccionario enviado a la plantilla
    mensaje_bienvenida = "Bienvenido al Sistema de Gestión"
    resumen_dia = {
        "ventas_totales": 125.50,
        "pedidos_pendientes": 5,
        "productos_bajo_stock": 2
    }
    return render_template("index.html", mensaje=mensaje_bienvenida, resumen=resumen_dia)

@app.route("/productos")
def productos():
    # Lista de diccionarios para simular inventario
    lista_productos = [
        {"nombre": "pan de molde", "categoria": "Panadería", "precio": 2.50, "stock": 12},
        {"nombre": "torta de chocolate", "categoria": "Pastelería", "precio": 15.00, "stock": 3},
        {"nombre": "croissant de queso", "categoria": "Hojaldre", "precio": 0.80, "stock": 0},
        {"nombre": "empanada de carne", "categoria": "Bocadillos", "precio": 1.00, "stock": 20},
        {"nombre": "pan baguette", "categoria": "Panadería", "precio": 1.25, "stock": 0}
    ]
    return render_template("productos.html", productos=lista_productos)

@app.route("/clientes")
def clientes():
    lista_clientes = [
        {"nombre": "Juan Pérez", "telefono": "0991234567", "tipo": "Frecuente"},
        {"nombre": "María Gómez", "telefono": "0987654321", "tipo": "Ocasional"}
    ]
    return render_template("clientes.html", clientes=lista_clientes)

@app.route("/proveedores")
def proveedores():
    lista_proveedores = [
        {"empresa": "Harinas del Ecuador", "contacto": "Carlos Ruiz", "telefono": "022345678"},
        {"empresa": "Llácteos El Campo", "contacto": "Ana López", "telefono": "022876543"}
    ]
    return render_template("proveedores.html", proveedores=lista_proveedores)

@app.route("/facturacion")
def facturacion():
    return render_template("facturacion.html")

if __name__ == "__main__":
    app.run(debug=True)