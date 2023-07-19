CREATE DATABASE recetariodb;

USE recetariodb;

CREATE TABLE receta(
	id_receta INT NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
	nombre_receta VARCHAR(200) NOT NULL UNIQUE,
	preparacion VARCHAR(500),
	tiempo_preparacion VARCHAR(100),
	tiempo_coccion VARCHAR(100),
	fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
	imagen VARCHAR(150),	
	es_favorita BOOLEAN DEFAULT 1
);



CREATE TABLE ingrediente(
	id_ingrediente INT NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
	nombre_ingrediente VARCHAR(200) NOT NULL UNIQUE,
	unidad_medida VARCHAR(50) NOT NULL
);

-- SHOW TABLES;

CREATE TABLE receta_ingrediente(
	id_receta_ingrediente INT NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
	ingrediente_id INT NOT NULL,
	receta_id INT NOT NULL,
	cantidad INT DEFAULT 0,
	FOREIGN KEY (ingrediente_id) REFERENCES ingrediente(id_ingrediente) ON DELETE CASCADE,
    FOREIGN KEY (receta_id) REFERENCES receta(id_receta) ON DELETE CASCADE
);


CREATE TABLE etiqueta(
	id_etiqueta INT NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
	nombre_etiqueta VARCHAR(200) NOT NULL UNIQUE	
);

CREATE TABLE receta_etiqueta(
	id_receta_etiqueta INT NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
	etiqueta_id INT NOT NULL,
	receta_id INT NOT NULL,
	FOREIGN KEY (etiqueta_id) REFERENCES etiqueta(id_etiqueta) ON DELETE CASCADE,
    FOREIGN KEY (receta_id) REFERENCES receta(id_receta) ON DELETE CASCADE
);

INSERT INTO ingrediente(nombre_ingrediente, unidad_medida) VALUES
	("papa", "gramos"),
	("zapallo", "gramos"),
	("cebolla", "gramos"),
	("huevos", "unidad"),
	("caldo", "cubito"),
	("leche", "centimetros cubicos"),
	("azucar", "gramos"),
	("sal", "gramos"),
	("fideos", "gramos");

INSERT INTO receta(nombre_receta, preparacion, tiempo_preparacion, tiempo_coccion, imagen, es_favorita) VALUES
	("ensalada", "['agregar carne trozada', 'agregar papa trozada', 'hervir agua']", "15 minutos","0 minutos","ensalada.jpg", 1),
	("fideos con salsa", "['hervir fideos', 'preparar salsa', 'servir con queso rallado']", "1 hora","40 minutos","fideos.jpg", 1),
	("sopa crema", "['hervir verduras', 'agregar vitina', 'servir con queso cremoso']", "1 hora","40 minutos","sopa.jpg", 1);

INSERT INTO receta_ingrediente(receta_id, ingrediente_id, cantidad) VALUES
	(1, 1, 500),
	(1, 2, 500),
	(2, 8, 10),
	(2, 9, 250),
	(3, 1, 100),
	(3, 2, 100),
	(3, 4, 100),
	(3, 9, 100);

INSERT INTO etiqueta(nombre_etiqueta)VALUES
	("caliente"),
	("frio"),
	("sopa"),
	("salsa"),
	("dulce"),
	("salado");
	
INSERT INTO receta_etiqueta(receta_id, etiqueta_id)VALUES
	(1, 2),
	(1, 6),
	(2, 1),
	(2, 4),
	(2, 6),
	(3, 1),
	(3, 3),
	(3, 6);



SELECT * FROM receta;
SELECT * FROM ingrediente;
SELECT * FROM receta_ingrediente;
SELECT * FROM etiqueta;
SELECT * FROM receta_etiqueta;

-- DESCRIBE receta_ingrediente ;

-- ALTER TABLE receta_ingrediente ADD cantidad INT DEFAULT 0;











