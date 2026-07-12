// ==========================================
// 1. ESTADO DE LA APLICACIÓN
// ==========================================
let listaPedidos = [];
const formPedido = document.getElementById('formPedido');
const listaRegistros = document.getElementById('listaRegistros');
const totalRegistros = document.getElementById('totalRegistros');

// ==========================================
// 2. FUNCIÓN DE RENDERIZADO (Contenido Dinámico)
// ==========================================
function renderizarPedidos() {
    listaRegistros.innerHTML = '';
    
    // ESTRUCTURA REPETITIVA (forEach)
    listaPedidos.forEach((pedido, index) => {
        // ESTRUCTURA CONDICIONAL (Para mostrar estado especial)
        let clasePrioridad = pedido.tipo.includes("Tortas") ? "border-danger" : "border-warning";
        let badgePrioridad = pedido.tipo.includes("Tortas") ? '<span class="badge bg-danger">Urgente</span>' : '';

        const colDiv = document.createElement('div');
        colDiv.className = 'col-12 col-md-6 col-xl-4';
        colDiv.innerHTML = `
            <div class="card h-100 border-start border-3 ${clasePrioridad} shadow-sm">
                <div class="card-body">
                    ${badgePrioridad}
                    <h5 class="card-title fw-bold">${pedido.cliente}</h5>
                    <p class="text-muted small">${pedido.tipo}</p>
                    <p class="card-text">${pedido.detalles}</p>
                    <button class="btn btn-outline-danger btn-sm" onclick="eliminarPedido(${index})">Eliminar</button>
                </div>
            </div>
        `;
        listaRegistros.appendChild(colDiv);
    });
    
    totalRegistros.textContent = listaPedidos.length;
}

// Función eliminar
window.eliminarPedido = (index) => {
    listaPedidos.splice(index, 1);
    renderizarPedidos();
};

// ==========================================
// 3. MANEJO DE EVENTOS
// ==========================================
formPedido.addEventListener('submit', function (event) {
    event.preventDefault();
    
    // Captura de datos
    const cliente = document.getElementById('nombreCliente').value;
    const tipo = document.getElementById('tipoProducto').value;
    const detalles = document.getElementById('detallesPedido').value;

    // Validación básica
    if (cliente.length < 5 || tipo === "" || detalles.length < 15) {
        alert("Por favor complete los campos correctamente (Nombre > 5, Detalles > 15)");
        return;
    }

    // Agregar objeto al arreglo
    listaPedidos.push({ cliente, tipo, detalles });
    
    renderizarPedidos();
    formPedido.reset();
});