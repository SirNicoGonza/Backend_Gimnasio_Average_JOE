use gym_aj_db;

insert into users (firstname, lastname, email, passwords, created_at)
values ('Pepe', 'Power', 'pepepower@pepe.com', 'qwertyuiop', now()),
		('Steve', 'Hyuga', 'stevehyuga@steve.com', 'futbol', now());
        
insert into planes (nombre, precio, descripcion, dias_mes, dias_gracia)
values ('Plan Basico', 4500.00, 'Incluye el uso de las máquinas y pesas del gimnasio durante 1 hora, 3 días a la semana', 12, 3),
		('Plan Experto', 55000.00, 'Incluye el uso de las máquinas y pesas del gimnasio durante 2 hora, 4 días a la semana', 16, 4);
	
insert into socios (id_user, plan_id, activo)
value (1, 2, false);

insert into empleados (user_id, gym_asignado)
values (2, 'Gym 1 - Alavarado 150');

insert into pagos_planes (id_socio, plan)
value (1,2);

update socios set dias_habilitado = 16, dias_gracia = 4, activo = true
where id_socio = 1;

Insert into actividades (actividad_name, instructor, precio, hora, dias, cupo_max, cupo_disp, sesiones)
value ('Clase de Pilate', 'Profe Peter Parker', 1000.00, '18:30:00', 'Martes y Jueves', 30, 30, 8);

select * from users;

select * from users
where email= 'pepepower@pepe.com' and passwords= 'qwertyuiop';