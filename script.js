// ==========================================
// 1. SELECCIÓN DE ELEMENTOS DEL DOM
// ==========================================
const formPedido = document.getElementById('formPedido');
const inputNombre = document.getElementById('nombreCliente');
const selectProducto = document.getElementById('tipoProducto');
const txtDetalles = document.getElementById('detallesPedido');

const listaRegistros = document.getElementById('listaRegistros');
const totalRegistros = document.getElementById('totalRegistros');
const mensajeAlerta = document.getElementById('mensajeAlerta');

// Variable incremental única para el control interno de IDs de nodos del DOM
let idContadorUnico = 0;

// ==========================================
// 2. LOGICA DE VALIDACIONES INDIVIDUALES (Semana 6)
// ==========================================

// Evalúa el nombre (Mínimo 5 caracteres)
const validarNombre = () => {
    const valor = inputNombre.value.trim();
    if (valor === "" || valor.length < 5) {
        marcarInvalido(inputNombre);
        return false;
    } else {
        marcarValido(inputNombre);
        return true;
    }
};

// Evalúa la selección de un producto
const validarProducto = () => {
    if (selectProducto.value === "") {
        marcarInvalido(selectProducto);
        return false;
    } else {
        marcarValido(selectProducto);
        return true;
    }
};

// Evalúa los detalles descriptivos (Mínimo 15 caracteres)
const validarDetalles = () => {
    const valor = txtDetalles.value.trim();
    if (valor === "" || valor.length < 15) {
        marcarInvalido(txtDetalles);
        return false;
    } else {
        marcarValido(txtDetalles);
        return true;
    }
};

// Manejadores auxiliares de clases visuales nativas de Bootstrap 5
const marcarInvalido = (elemento) => {
    elemento.classList.remove("is-valid");
    elemento.classList.add("is-invalid");
};

const marcarValido = (elemento) => {
    elemento.classList.remove("is-invalid");
    elemento.classList.add("is-valid");
};

const removerEstilosValidacion = (elemento) => {
    elemento.classList.remove("is-invalid", "is-valid");
};

// ==========================================
// 3. ASIGNACIÓN DE ESCUCHADORES EN TIEMPO REAL
// ==========================================
inputNombre.addEventListener('input', validarNombre);
inputNombre.addEventListener('blur', validarNombre);

selectProducto.addEventListener('change', validarProducto);
selectProducto.addEventListener('blur', validarProducto);

txtDetalles.addEventListener('input', validarDetalles);
txtDetalles.addEventListener('blur', validarDetalles);

// ==========================================
// 4. MANEJO DE ENVÍO DEL FORMULARIO (submit)
// ==========================================
formPedido.addEventListener('submit', function (event) {
    // Frena el comportamiento de refresco por defecto del navegador
    event.preventDefault();

    // Invoca todas las validaciones de manera simultánea
    const esNombreCorrecto = validarNombre();
    const esProductoCorrecto = validarProducto();
    const esDetalleCorrecto = validarDetalles();

    // Bloquea el guardado en caso de que alguna validación no sea exitosa
    if (!esNombreCorrecto || !esProductoCorrecto || !esDetalleCorrecto) {
        mostrarMensajeValidacion('Error: Por favor complete los campos obligatorios marcados en color rojo.', 'danger');
        return;
    }

    // Captura final de datos limpios
    const cliente = inputNombre.value.trim();
    const tipo = selectProducto.value;
    const detalles = txtDetalles.value.trim();

    // Emisión del mensaje de éxito
    mostrarMensajeValidacion('¡Excelente! El pedido especial ha sido verificado y procesado con éxito.', 'success');

    // Aumento del id único incremental
    idContadorUnico++;

    // ==========================================
    // 5. CONSTRUCCIÓN E INSERCIÓN DINÁMICA DE TARJETAS
    // ==========================================
    const colDiv = document.createElement('div');
    colDiv.className = 'col-12 col-md-6 col-xl-4';
    colDiv.setAttribute('id', `pedido-${idContadorUnico}`);

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

    // Asignación de evento directa al botón interno para remover el registro
    const botonEliminar = colDiv.querySelector('.btn-eliminar');
    botonEliminar.addEventListener('click', function () {
        colDiv.remove(); // Borra el nodo específico de forma directa
        modificarContadorDisplay(-1); // Reduce el indicador numérico
    });

    // Añade la tarjeta al listado visual mediante appendChild
    listaRegistros.appendChild(colDiv);

    // Incrementa la cantidad de registros en pantalla
    modificarContadorDisplay(1);

    // Resetea el formulario por completo y remueve los bordes verdes sobrantes
    formPedido.reset();
    removerEstilosValidacion(inputNombre);
    removerEstilosValidacion(selectProducto);
    removerEstilosValidacion(txtDetalles);
});

// ==========================================
// FUNCIONES AUXILIARES / MODULARES
// ==========================================

// Modifica y refresca el contador en pantalla
function modificarContadorDisplay(valor) {
    let cuentaActual = parseInt(totalRegistros.textContent);
    cuentaActual += valor;
    totalRegistros.textContent = cuentaActual;
}

// Genera e inyecta alertas transitorias en la interfaz
function mostrarMensajeValidacion(mensaje, estiloBootstrap) {
    mensajeAlerta.innerHTML = `
        <div class="alert alert-${estiloBootstrap} alert-dismissible fade show shadow-sm" role="alert">
            ${mensaje}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;

    // Cierre automatizado de alertas a los 4 segundos
    setTimeout(() => {
        mensajeAlerta.innerHTML = '';
    }, 4000);
}