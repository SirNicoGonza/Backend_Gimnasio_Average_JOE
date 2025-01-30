CREATE SCHEMA IF NOT EXISTS gym_aj_db;

/*Se crean las tablas de la base de datos.*/
USE gym_AJ_db;
CREATE TABLE IF NOT EXISTS users(
	id_user INT UNIQUE auto_increment NOT NULL PRIMARY KEY,
    firstname VARCHAR(50),
    lastname VARCHAR(50),
    email VARCHAR(100),
    passwords VARCHAR(200),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) Engine= InnoDB ;

create table if not exists planes(
	id_plan INT UNIQUE auto_increment NOT NULL PRIMARY KEY,
    nombre VARCHAR(50),
    precio DECIMAL(10,2),
    descripcion tinytext,
    dias_mes INT,
    dias_gracia INT
) Engine= InnoDB;

CREATE TABLE IF NOT EXISTS socios(
	id_socio INT UNIQUE auto_increment NOT NULL PRIMARY KEY,
    id_user INT,
    plan_id INT,
    activo boolean,
    dias_habilitado INT default 0,
    dias_gracia INT default 0,
    constraint plan_id foreign key (plan_id)
    references planes(id_plan)
    ON update CASCADE
    ON delete CASCADE,
    constraint id_user foreign key (id_user)
    references users(id_user)
    ON update CASCADE
    ON delete CASCADE
) Engine= InnoDB;

CREATE TABLE IF NOT EXISTS empleados(
	id_empleado INT UNIQUE auto_increment NOT NULL PRIMARY KEY,
    user_id INT,
    gym_asignado VARCHAR(50),
    constraint user_id foreign key (user_id)
    references users(id_user)
    ON UPDATE CASCADE
    ON DELETE CASCADE
) Engine= InnoDB;

CREATE TABLE if not exists actividades (
	id_actividad INT UNIQUE auto_increment PRIMARY KEY,
    actividad_name VARCHAR(75),
    instructor VARCHAR(50),
    precio DECIMAL (10,2),
    hora TIME,
    dias VARCHAR(20),
    cupo_max INT,
    cupo_disp INT,
    sesiones INT,
    estado BOOLEAN default true
) Engine= InnoDB;

CREATE TABLE if not exists asistencias (
    id_asistencia INT AUTO_INCREMENT PRIMARY KEY,
    id_socio INT NOT NULL,
    id_actividad INT NULL,
    tipo_asistencia ENUM ('plan', 'actividad') NOT NULL,
    fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_socio) REFERENCES socios(id_socio)
    on update cascade
    on delete cascade,
    FOREIGN KEY (id_actividad) REFERENCES actividades(id_actividad)
    on update cascade
    on delete set null
) Engine= InnoDB;

CREATE TABLE if not exists inscripciones (
	id_inscripcion INT UNIQUE auto_increment PRIMARY KEY,
    socios_ID int,
    actividad_id int,
    estado BOOLEAN default true,
    sesiones_disp INT default 0,
    constraint socios_ID foreign key (socios_ID)
    References socios(id_socio)
    ON update cascade
    on delete cascade,
    constraint actividad_id foreign key (actividad_id)
    references actividades(id_actividad)
    on update cascade
    on delete cascade
) Engine= InnoDB;

CREATE TABLE if not exists pagos_planes (
	id_pago_plan INT UNIQUE auto_increment PRIMARY KEY,
    ID_socio int,
    plan int,
    fecha_pago DATETIME default current_timestamp,
    constraint ID_socio foreign key (ID_socio)
    references socios(id_socio)
    on update cascade
    on delete cascade,
    constraint plan foreign key (plan)
    references planes(id_plan)
    on update cascade
    on delete cascade
) Engine= InnoDB;

create Table if not exists pagos_actividades (
	id_pago_actividad INT UNIQUE auto_increment PRIMARY KEY,
    socio int,
    actividad int,
    fecha_pago DATETIME default current_timestamp,
    constraint socio foreign key (socio)
    references socios(id_socio)
    on update cascade
    on delete cascade,
    constraint actividad foreign key (actividad)
    references actividades(id_actividad)
    on update cascade
    on delete cascade
) Engine= InnoDB;

/*Se crea vista para ver los todos los pagos de los socios*/
create view vista_pagos_socios AS
SELECT s.id_socio, u.firstname, u.lastname, p.nombre AS tipo_pago, p.precio, pgp.fecha_pago as dia_pago
FROM pagos_planes as pgp
INNER JOIN planes p ON p.id_plan = pgp.plan
INNER JOIN socios s ON s.id_socio = pgp.ID_socio
INNER JOIN users u ON u.id_user = s.id_user
UNION ALL
SELECT s.id_socio, u.firstname, u.lastname, a.actividad_name AS tipo_pago, a.precio, pga.fecha_pago as dia_pago
FROM pagos_actividades pga
INNER JOIN actividades a ON a.id_actividad = pga.actividad
INNER JOIN socios s ON s.id_socio = pga.socio
INNER JOIN users u ON u.id_user = s.id_user;