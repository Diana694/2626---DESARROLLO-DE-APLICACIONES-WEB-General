CREATE DATABASE IF NOT EXISTS panaderia_db;
USE panaderia_db;

-- Tabla Proveedores
CREATE TABLE IF NOT EXISTS proveedores (
    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    correo VARCHAR(100)
);

-- Tabla Productos (Con clave foránea hacia proveedores)
CREATE TABLE IF NOT EXISTS productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL,
    id_proveedor INT,
    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor) ON DELETE SET NULL
);

-- Datos de prueba iniciales (Panadería)
INSERT INTO proveedores (nombre, telefono, correo) VALUES 
('Harinas del Ecuador', '022345678', 'contacto@harinas.com'),
('Lácteos El Campo', '022876543', 'ventas@lacteos.com');

INSERT INTO productos (nombre, precio, stock, id_proveedor) VALUES 
('Pan de Molde', 2.50, 12, 1),
('Torta de Chocolate', 15.00, 3, 2),
('Croissant de Queso', 0.80, 10, 2),
('Empanada de Carne', 1.00, 20, 1),
('Pan Baguette', 1.25, 0, 1);