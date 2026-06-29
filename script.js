// ==========================================
// 1. SELECCIÓN DE ELEMENTOS DEL DOM (IDs)
// ==========================================
const formPedido = document.getElementById('formPedido');
const listaRegistros = document.getElementById('listaRegistros');
const totalRegistros = document.getElementById('totalRegistros');
const mensajeAlerta = document.getElementById('mensajeAlerta');

// Variable global interna para asignar identificadores únicos a cada registro
let idContadorUnico = 0;

// ==========================================
// 2. MANEJO DEL EVENTO SUBMIT (addEventListener)
// ==========================================
formPedido.addEventListener('submit', function (event) {
    // Evita la recarga predeterminada del navegador
    event.preventDefault();

    // Captura y remoción de espacios en blanco redundantes
    const cliente = document.getElementById('nombreCliente').value.trim();
    const tipo = document.getElementById('tipoProducto').value;
    const detalles = document.getElementById('detallesPedido').value.trim();

    // ==========================================
    // 3. VALIDACIÓN DE CAMPOS Y MENSAJES DINÁMICOS
    // ==========================================
    if (cliente === '' || tipo === '' || detalles === '') {
        mostrarMensajeValidacion('Error: Todos los campos del formulario son obligatorios para procesar el pedido.', 'danger');
        return; // Rompe el flujo si la validación falla
    }

    // Mensaje dinámico de éxito si pasa la validación
    mostrarMensajeValidacion('¡Excelente! El pedido ha sido guardado exitosamente.', 'success');

    // Incrementar ID para el manejo interno del DOM
    idContadorUnico++;

    // ==========================================
    // 4. CREACIÓN DINÁMICA DE ELEMENTOS (createElement)
    // ==========================================
    // Tarjeta responsiva utilizando el sistema de rejillas (Grid) de Bootstrap
    const colDiv = document.createElement('div');
    colDiv.className = 'col-12 col-md-6 col-xl-4';
    colDiv.setAttribute('id', `pedido-${idContadorUnico}`);

    // Inyección de estructura HTML interna respetando las clases personalizadas y de Bootstrap
    colDiv.innerHTML = `
        <div class="card h-100 border-start border-3 border-warning shadow-sm" style="background-color: #ffffff;">
            <div class="card-body d-flex flex-column p-4">
                <div class="d-flex justify-content-between align-items-start mb-2">
                    <h5 class="card-title fw-bold text-dark mb-0">${cliente}</h5>
                    <span class="badge bg-dark text-warning small">${tipo}</span>
                </div>
                <p class="card-text text-muted flex-grow-1 small mt-2">${detalles}</p>
                <div class="text-end mt-3">
                    <button class="btn btn-danger btn-sm px-3 fw-medium btn-eliminar">Eliminar</button>
                </div>
            </div>
        </div>
    `;

    // ==========================================
    // 5. MANEJO DE EVENTO PARA ELIMINAR REGISTROS
    // ==========================================
    const botonEliminar = colDiv.querySelector('.btn-eliminar');
    botonEliminar.addEventListener('click', function () {
        // Elimina el nodo del DOM de forma directa
        colDiv.remove();
        // Disminuye el recuento en la pantalla
        modificarContadorDisplay(-1);
    });

    // ==========================================
    // 6. INCORPORACIÓN AL DOM (appendChild)
    // ==========================================
    listaRegistros.appendChild(colDiv);

    // Actualiza la interfaz e incrementa el contador general
    modificarContadorDisplay(1);

    // Limpieza completa del formulario para nuevos registros
    formPedido.reset();
});

// ==========================================
// FUNCIONES AUXILIARES / MODULARES
// ==========================================

// Modifica y renderiza el total de registros en pantalla
function modificarContadorDisplay(valor) {
    let cuentaActual = parseInt(totalRegistros.textContent);
    cuentaActual += valor;
    totalRegistros.textContent = cuentaActual;
}

// Genera alertas dinámicas usando componentes estáticos de Bootstrap
function mostrarMensajeValidacion(mensaje, estiloBootstrap) {
    mensajeAlerta.innerHTML = `
        <div class="alert alert-${estiloBootstrap} alert-dismissible fade show shadow-sm" role="alert">
            ${mensaje}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;

    // Auto-cierre de la alerta transcurridos 4 segundos para mejorar la experiencia de usuario
    setTimeout(() => {
        mensajeAlerta.innerHTML = '';
    }, 4000);
}