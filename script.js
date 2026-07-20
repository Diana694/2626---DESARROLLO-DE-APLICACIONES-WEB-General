// ==========================================
// 1. ESTADO DE LA APLICACIÓN
// ==========================================
let listaPedidos = [];

const formPedido = document.getElementById('formPedido');
const listaRegistros = document.getElementById('listaRegistros');
const totalRegistros = document.getElementById('totalRegistros');
const mensajeAlerta = document.getElementById('mensajeAlerta');
const spinnerContainer = document.getElementById('spinnerContainer');
const btnGuardar = document.getElementById('btnGuardar');

let modalDetalleBS;

// Inicialización de componentes al cargar el DOM
document.addEventListener('DOMContentLoaded', () => {
    modalDetalleBS = new bootstrap.Modal(document.getElementById('modalDetalle'));
    renderizarPedidos();
});

// ==========================================
// 2. VALIDACIONES DINÁMICAS (Semana 6/8)
// ==========================================
function validarNombre(nombre) {
    return nombre.trim().length >= 5;
}

function validarTipo(tipo) {
    return tipo !== "";
}

function validarDetalles(detalles) {
    return detalles.trim().length >= 15;
}

function aplicarEstiloCampo(input, esValido) {
    if (esValido) {
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
    } else {
        input.classList.remove('is-valid');
        input.classList.add('is-invalid');
    }
}

function limpiarEstilosCampos() {
    ['nombreCliente', 'tipoProducto', 'detallesPedido'].forEach(id => {
        const el = document.getElementById(id);
        el.classList.remove('is-valid', 'is-invalid');
    });
}

// ==========================================
// 3. ALERTAS DINÁMICAS CON BOOTSTRAP
// ==========================================
function mostrarAlerta(mensaje, tipo = 'danger') {
    const icono = tipo === 'success' 
        ? '<i class="bi bi-check-circle-fill me-2"></i>' 
        : tipo === 'warning' 
        ? '<i class="bi bi-exclamation-triangle-fill me-2"></i>' 
        : '<i class="bi bi-x-circle-fill me-2"></i>';

    mensajeAlerta.innerHTML = `
        <div class="alert alert-${tipo} alert-dismissible fade show shadow-sm" role="alert">
            ${icono} ${mensaje}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;

    // Cierre automático tras 4 segundos
    setTimeout(() => {
        const alerta = mensajeAlerta.querySelector('.alert');
        if (alerta) {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alerta);
            bsAlert.close();
        }
    }, 4000);
}

// ==========================================
// 4. FUNCIÓN DE RENDERIZADO (Contenido Dinámico)
// ==========================================
function renderizarPedidos() {
    listaRegistros.innerHTML = '';
    
    if (listaPedidos.length === 0) {
        listaRegistros.innerHTML = `
            <div class="col-12 text-center text-muted py-4">
                <i class="bi bi-basket fs-1 d-block mb-2"></i>
                <p class="mb-0">No hay pedidos registrados en este momento.</p>
            </div>
        `;
        totalRegistros.textContent = '0';
        return;
    }

    // ESTRUCTURA REPETITIVA (forEach)
    listaPedidos.forEach((pedido, index) => {
        // ESTRUCTURA CONDICIONAL
        let clasePrioridad = pedido.tipo.includes("Tortas") ? "border-danger" : "border-warning";
        let badgePrioridad = pedido.tipo.includes("Tortas") ? '<span class="badge bg-danger mb-2">Urgente</span>' : '';

        const colDiv = document.createElement('div');
        colDiv.className = 'col-12 col-md-6';
        colDiv.innerHTML = `
            <div class="card h-100 border-start border-4 ${clasePrioridad} shadow-sm">
                <div class="card-body d-flex flex-column">
                    <div>
                        ${badgePrioridad}
                        <h5 class="card-title fw-bold text-dark mb-1">${pedido.cliente}</h5>
                        <p class="badge bg-warning text-dark mb-2">${pedido.tipo}</p>
                        <p class="card-text text-muted text-truncate">${pedido.detalles}</p>
                    </div>
                    <div class="mt-auto pt-3 border-top d-flex justify-content-between align-items-center">
                        <button class="btn btn-outline-primary btn-sm" onclick="verDetallePedido(${index})">
                            <i class="bi bi-eye me-1"></i> Ver
                        </button>
                        <button class="btn btn-outline-danger btn-sm" onclick="eliminarPedido(${index})">
                            <i class="bi bi-trash me-1"></i> Eliminar
                        </button>
                    </div>
                </div>
            </div>
        `;
        listaRegistros.appendChild(colDiv);
    });
    
    totalRegistros.textContent = listaPedidos.length;
}

// ==========================================
// 5. ACCIONES DE MODAL Y ELIMINACIÓN
// ==========================================
window.verDetallePedido = (index) => {
    const pedido = listaPedidos[index];
    if (!pedido) return;

    const contenidoModal = document.getElementById('contenidoModal');
    contenidoModal.innerHTML = `
        <div class="list-group list-group-flush">
            <div class="list-group-item">
                <small class="text-muted d-block">Cliente:</small>
                <span class="fw-bold fs-5">${pedido.cliente}</span>
            </div>
            <div class="list-group-item">
                <small class="text-muted d-block">Tipo de Producto:</small>
                <span class="badge bg-warning text-dark fs-6">${pedido.tipo}</span>
            </div>
            <div class="list-group-item">
                <small class="text-muted d-block">Detalles del Pedido:</small>
                <p class="mb-0 text-dark mt-1">${pedido.detalles}</p>
            </div>
        </div>
    `;

    modalDetalleBS.show();
};

window.eliminarPedido = (index) => {
    if (confirm("¿Está seguro de que desea eliminar este pedido?")) {
        listaPedidos.splice(index, 1);
        renderizarPedidos();
        mostrarAlerta("El pedido ha sido eliminado correctamente.", "warning");
    }
};

// ==========================================
// 6. MANEJO DE EVENTOS CON SPINNER BOOTSTRAP
// ==========================================
formPedido.addEventListener('submit', function (event) {
    event.preventDefault();
    
    const inputCliente = document.getElementById('nombreCliente');
    const inputTipo = document.getElementById('tipoProducto');
    const inputDetalles = document.getElementById('detallesPedido');

    const cliente = inputCliente.value;
    const tipo = inputTipo.value;
    const detalles = inputDetalles.value;

    // Evaluaciones
    const vCliente = validarNombre(cliente);
    const vTipo = validarTipo(tipo);
    const vDetalles = validarDetalles(detalles);

    aplicarEstiloCampo(inputCliente, vCliente);
    aplicarEstiloCampo(inputTipo, vTipo);
    aplicarEstiloCampo(inputDetalles, vDetalles);

    // Validación según parámetros exigidos (Nombre > 5, Detalles > 15)
    if (!vCliente || !vTipo || !vDetalles) {
        mostrarAlerta("Por favor complete los campos correctamente (Nombre ≥ 5, Detalles ≥ 15 caracteres).", "danger");
        return;
    }

    // CARGA SIMULADA CON SPINNER DE BOOTSTRAP
    spinnerContainer.classList.remove('d-none');
    btnGuardar.disabled = true;

    setTimeout(() => {
        // Agregar objeto al arreglo
        listaPedidos.push({ 
            cliente: cliente.trim(), 
            tipo: tipo, 
            detalles: detalles.trim() 
        });
        
        // Ocultar Spinner
        spinnerContainer.classList.add('d-none');
        btnGuardar.disabled = false;

        // Actualizar interfaz
        renderizarPedidos();
        formPedido.reset();
        limpiarEstilosCampos();

        mostrarAlerta("¡Pedido registrado exitosamente!", "success");
    }, 750);
});