-- Tabla 1: Proveedores
CREATE TABLE IF NOT EXISTS proveedores (
    id_proveedor SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    correo VARCHAR(100)
);

-- Tabla 2: Usuarios (Para autenticación y login)
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Tabla 3: Productos (Relacionada con Proveedores y Usuarios)
CREATE TABLE IF NOT EXISTS productos (
    id_producto SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio NUMERIC(10, 2) NOT NULL,
    stock INT NOT NULL,
    id_proveedor INT,
    usuario_id INT,
    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor) ON DELETE SET NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Datos iniciales de prueba (Panadería)
INSERT INTO proveedores (nombre, telefono, correo) VALUES 
('Harinas del Ecuador', '022345678', 'contacto@harinas.com'),
('Lácteos El Campo', '022876543', 'ventas@lacteos.com');

INSERT INTO productos (nombre, precio, stock, id_proveedor) VALUES 
('Pan de Molde', 2.50, 12, 1),
('Torta de Chocolate', 15.00, 3, 2),
('Croissant de Queso', 0.80, 10, 2),
('Empanada de Carne', 1.00, 20, 1),
('Pan Baguette', 1.25, 0, 1);