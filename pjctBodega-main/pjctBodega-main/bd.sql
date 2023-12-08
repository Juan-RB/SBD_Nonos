CREATE TABLE PERFIL (
        codPer INT,
        nomPer VARCHAR(30),
        PRIMARY KEY (codPer)
    );

CREATE TABLE USUARIO (
        codUser INT AUTO_INCREMENT,
        codTra INT,
        codPer INT,
        pass VARCHAR(30),
        PRIMARY KEY (codUser)
    );

CREATE TABLE TRABAJADORES (
        codTra INT AUTO_INCREMENT,
        rutTra INT,
        nomTra VARCHAR(30),
        dirTra VARCHAR(30),
        comTra VARCHAR(30),
        telTra VARCHAR(30),
        emailTra VARCHAR(30),
        codCom INT,
        PRIMARY KEY (codTra)
    );

CREATE TABLE ADMINISTRADOR (
        codAdmin INT AUTO_INCREMENT,
        codTra INT,
        codBod INT,
        PRIMARY KEY (codAdmin)
    );

CREATE TABLE BODEGA (
        codBod INT,
        nomBod VARCHAR(30),
        dirBod VARCHAR(30),
        cantPas INT,
        codCom INT,
        PRIMARY KEY (codBod)
    );

CREATE TABLE BODEGUERO (
        codBode INT AUTO_INCREMENT,
        codTra INT,
        codBod INT,
        PRIMARY KEY (codBode)
    );

CREATE TABLE RECOLECTORES (
        codRec INT AUTO_INCREMENT,
        codTra INT,
        PRIMARY KEY (codRec)
    );

CREATE TABLE FARDOS (
        codFar INT AUTO_INCREMENT,
        codRec INT,
        codTf INT,
        PRIMARY KEY (codFar)
    );

CREATE TABLE TIPO_FARDO 
    (codTf INT AUTO_INCREMENT, 
    nomTf VARCHAR(30),
     PRIMARY KEY (codTf));

CREATE TABLE CLASIFICADORES (codCla INT, 
codTra INT, 
PRIMARY KEY (codCla));

CREATE TABLE
    TELAS (
        codTela INT AUTO_INCREMENT,
        codCla INT,
        codCp INT,
        codCs INT,
        codTt INT,
        codPt INT,
        exiSt boolean,
        PRIMARY KEY (codTela)
    );

CREATE TABLE COLOR_PRINCIPAL (codCp INT AUTO_INCREMENT,
    nomCp VARCHAR(30), 
    PRIMARY KEY (codCp));

CREATE TABLE COLOR_SECUNDARIO (codCs INT AUTO_INCREMENT,
    nomCs VARCHAR(30),
    PRIMARY KEY (codCs));

CREATE TABLE TIPO_TELA (codTt INT AUTO_INCREMENT,
    nomTt VARCHAR(30), 
    PRIMARY KEY (codTt));

CREATE TABLE
    PATRON (codPt INT AUTO_INCREMENT,
    nomPt VARCHAR(30),
     PRIMARY KEY (codPt));

CREATE TABLE SBDcrud_regbodegafardo (
        codRegF INT AUTO_INCREMENT,
        codBode_id INT,
        codFar_id INT,
        codRec_id INT,
        codMovF INT,
        fechaIngFar DATE,
        PRIMARY KEY (codRegF)
    );

CREATE TABLE
    TIPO_MOV_FAR (
        codMovF INT,
        nomFar VARCHAR(30),
        PRIMARY KEY (codMovF)
    );

CREATE TABLE REG_BODEGA_MUESTRA (
        codRegM INT AUTO_INCREMENT,
        codMovM INT,
        codTela INT,
        codUbi VARCHAR(15),
        fechaIngM DATE,
        cantidad INT,
        codBode INT,
        PRIMARY KEY (codRegM)
    );

CREATE TABLE TIPO_MOVIMIENTO_M (
        codMovM INT,
        nomMov VARCHAR(30),
        PRIMARY KEY (codMovM)
    );

CREATE TABLE UBICACION (
        codUbi VARCHAR(15),
        codBod INT,
        ubiStat boolean,
        stock INT, 
        PRIMARY KEY (codUbi)
    );

CREATE TABLE
    COMUNA (
        codCom INT,
        nomCom VARCHAR(30),
        PRIMARY KEY (codCom)
    );

ALTER TABLE USUARIO
ADD FOREIGN KEY (codPer) REFERENCES PERFIL(codPer);

ALTER TABLE USUARIO
ADD FOREIGN KEY (codTra) REFERENCES TRABAJADORES(codTra);

ALTER TABLE CLASIFICADORES
ADD FOREIGN KEY(codTra) REFERENCES TRABAJADORES(codTra);

ALTER TABLE TRABAJADORES
ADD FOREIGN KEY (codCom) REFERENCES COMUNA(codCom);

ALTER TABLE ADMINISTRADOR
ADD FOREIGN KEY (codTra) REFERENCES TRABAJADORES(codTra);

ALTER TABLE BODEGUERO
ADD FOREIGN KEY (codTra) REFERENCES TRABAJADORES(codTra);

ALTER TABLE RECOLECTORES
ADD FOREIGN KEY (codTra) REFERENCES TRABAJADORES(codTra);

ALTER TABLE BODEGUERO
ADD FOREIGN KEY (codBod) REFERENCES BODEGA(codBod);

ALTER TABLE ADMINISTRADOR
ADD FOREIGN KEY (codBod) REFERENCES BODEGA(codBod);

ALTER TABLE BODEGA
ADD FOREIGN KEY(codCom) REFERENCES COMUNA(codCom);

ALTER TABLE REG_BODEGA_FARDO 
ADD FOREIGN KEY(codFar) REFERENCES FARDOS(codFar);

ALTER TABLE REG_BODEGA_FARDO 
ADD FOREIGN KEY(codRec) REFERENCES RECOLECTORES(codRec);

ALTER TABLE REG_BODEGA_FARDO 
ADD FOREIGN KEY(codMovF) REFERENCES TIPO_MOV_FAR(codMovF);

ALTER TABLE FARDOS
ADD FOREIGN KEY(codRec) REFERENCES RECOLECTORES(codRec);

ALTER TABLE FARDOS
ADD FOREIGN KEY(codTf) REFERENCES TIPO_FARDO(codTf);

ALTER TABLE REG_BODEGA_MUESTRA
ADD FOREIGN KEY(codMovM) REFERENCES TIPO_MOVIMIENTO_M(codMovM);

ALTER TABLE REG_BODEGA_MUESTRA
ADD FOREIGN KEY(codTela) REFERENCES TELAS(codTela);

ALTER TABLE REG_BODEGA_MUESTRA
ADD FOREIGN KEY(codUbi) REFERENCES UBICACION(codUbi);



ALTER TABLE REG_BODEGA_MUESTRA
ADD FOREIGN KEY(codBode) REFERENCES BODEGUERO(codBode);

ALTER TABLE UBICACION
ADD FOREIGN KEY(codBod) REFERENCES BODEGA(codBod);


ALTER TABLE TELAS
ADD FOREIGN KEY(codCla) REFERENCES CLASIFICADORES(codCla);


ALTER TABLE TELAS
ADD FOREIGN KEY(codCp) REFERENCES COLOR_PRINCIPAL(codCp);


ALTER TABLE TELAS
ADD FOREIGN KEY(codCs) REFERENCES COLOR_SECUNDARIO(codCs);


ALTER TABLE TELAS
ADD FOREIGN KEY(codTt) REFERENCES TIPO_TELA(codTt);


ALTER TABLE TELAS
ADD FOREIGN KEY(codPt) REFERENCES PATRON(codPt);

INSERT INTO SBDcrud_trabajadores VALUES(1,123456789,'MARÍA GONZÁLEZ','CALLE PRINCIPAL 123',912345678,'M.GONZALEZ@KILL.CL',18);
INSERT INTO SBDcrud_trabajadores VALUES(2,987654321,'JUAN TORRES','AVENIDA CENTRAL 456',987654321,'J.TORRES@KILL.CL',16);
INSERT INTO SBDcrud_trabajadores VALUES(3,56789013,'CARLOS RAMÍREZ','PLAZA MAYOR 789',956789012,'C.RAMIREZ@KILL.CL',7);
INSERT INTO SBDcrud_trabajadores VALUES(4,321098765,'LAURA FERNÁNDEZ','CALLE SECUNDARIA 321',932109876,'L.FERNANDEZ@KILL.CL',2);
INSERT INTO SBDcrud_trabajadores VALUES(5,654321098,'ANDRÉS GÓMEZ','AV. PRINCIPAL 987',965432109,'A.GOMEZ@KILL.CL',27);
INSERT INTO SBDcrud_trabajadores VALUES(6,112233445,'ANA LÓPEZ','CALLE DEL SOL 456',911223344,'A.LOPEZ@KILL.CL',17);
INSERT INTO SBDcrud_trabajadores VALUES(7,556677889,'RICARDO SILVA','AVENIDA CENTRAL 789',955667788,'R.SILVA@KILL.CL',5);
INSERT INTO SBDcrud_trabajadores VALUES(8,998877665,'SANDRA TORRES','PLAZA PRINCIPAL 123',999887766,'S.TORRES@KILL.CL',28);
INSERT INTO SBDcrud_trabajadores VALUES(9,443322110,'DIEGO ROJAS','CALLE DEL MAR 456',944332211,'D.ROJAS@KILL.CL',16);
INSERT INTO SBDcrud_trabajadores VALUES(10,223344556,'ANA CÁCERES','AV PRINCIPAL 789',922334455,'A.CACERES@KILL.CL',16);
INSERT INTO SBDcrud_trabajadores VALUES(11,778899002,'DANIEL MORALES','CALLE DEL SOL 123',977889900,'D.MORALES@KILL.CL',17);
INSERT INTO SBDcrud_trabajadores VALUES(12,152358466,'CLAUDIA SALAZAR','AVENIDA CENTRAL 456',900112233,'C.SALAZAR@KILL.CL',11);
INSERT INTO SBDcrud_trabajadores VALUES(13,334455667,'ANDRÉS ESPINOZA','PLAZA MAYOR 789',933445566,'A.ESPINOZA@KILL.CL',29);
INSERT INTO SBDcrud_trabajadores VALUES(14,889900118,'KARLA MENDOZA','CALLE PRINCIPAL 321',988990011,'K.MENDOZA@KILL.CL',22);
INSERT INTO SBDcrud_trabajadores VALUES(15,265123685,'RICARDO VALENZUELA','AVENIDA DEL SOL 9',955667788,'R.VALENZUELA@KILL.CL',13);
INSERT INTO SBDcrud_trabajadores VALUES(16,12334457,'LAURA SÁNCHEZ','CALLE PRINCIPAL 654',922336455,'L.SANCHEZ@KILLCORONA.CL',8);

INSERT INTO SBDcrud_comuna VALUES(1,'CERRILLOS');
INSERT INTO SBDcrud_comuna VALUES(2,'CERRO NAVIA');
INSERT INTO SBDcrud_comuna VALUES(3,'CONCHALÍ');
INSERT INTO SBDcrud_comuna VALUES(4,'EL BOSQUE');
INSERT INTO SBDcrud_comuna VALUES(5,'ESTACIÓN CENTRAL');
INSERT INTO SBDcrud_comuna VALUES(6,'HUECHURABA');
INSERT INTO SBDcrud_comuna VALUES(7,'INDEPENDENCIA');
INSERT INTO SBDcrud_comuna VALUES(8,'LA CISTERNA');
INSERT INTO SBDcrud_comuna VALUES(9,'LA FLORIDA');
INSERT INTO SBDcrud_comuna VALUES(10,'LA GRANJA');
INSERT INTO SBDcrud_comuna VALUES(11,'LA PINTANA');
INSERT INTO SBDcrud_comuna VALUES(12,'PROVIDENCIA');
INSERT INTO SBDcrud_comuna VALUES(13,'LAS CONDES');
INSERT INTO SBDcrud_comuna VALUES(14,'LA REINA');
INSERT INTO SBDcrud_comuna VALUES(15,'LO ESPEJO');
INSERT INTO SBDcrud_comuna VALUES(16,'LO PRADO');
INSERT INTO SBDcrud_comuna VALUES(17,'MACUL');
INSERT INTO SBDcrud_comuna VALUES(18,'MAIPÚ');
INSERT INTO SBDcrud_comuna VALUES(19,'ÑUÑOA');
INSERT INTO SBDcrud_comuna VALUES(20,'PADRE HURTADO');
INSERT INTO SBDcrud_comuna VALUES(21,'PEDRO AGUIRRE CERDA');
INSERT INTO SBDcrud_comuna VALUES(22,'PEÑALOLÉN');
INSERT INTO SBDcrud_comuna VALUES(23,'VITACURA');
INSERT INTO SBDcrud_comuna VALUES(24,'PUDAHUEL');
INSERT INTO SBDcrud_comuna VALUES(25,'PUENTE ALTO');
INSERT INTO SBDcrud_comuna VALUES(26,'QUILICURA');
INSERT INTO SBDcrud_comuna VALUES(27,'QUINTA NORMAL');
INSERT INTO SBDcrud_comuna VALUES(28,'RECOLETA');
INSERT INTO SBDcrud_comuna VALUES(29,'RENCA');
INSERT INTO SBDcrud_comuna VALUES(30,'SAN BERNARDO');
INSERT INTO SBDcrud_comuna VALUES(31,'SAN JOAQUÍN');
INSERT INTO SBDcrud_comuna VALUES(32,'SAN MIGUEL');
INSERT INTO SBDcrud_comuna VALUES(33,'SAN RAMÓN');
INSERT INTO SBDcrud_comuna VALUES(34,'SANTIAGO');
INSERT INTO SBDcrud_comuna VALUES(35,'LO BARNECHEA');



INSERT INTO SBDcrud_tipofardo VALUES(1,'MUESTRAS CON FALLAS');
INSERT INTO SBDcrud_tipofardo VALUES(2,'MUESTRAS IMPECABLES');
INSERT INTO SBDcrud_tipofardo VALUES(3,'BOTONES');
INSERT INTO SBDcrud_tipofardo VALUES(4,'CIERRES');
INSERT INTO SBDcrud_tipofardo VALUES(5,'CALCETINES');

INSERT INTO SBDcrud_administrador VALUES(1,1,1);
INSERT INTO SBDcrud_administrador VALUES(2,2,2);
INSERT INTO SBDcrud_administrador VALUES(3,3,3);


INSERT INTO SBDcrud_bodeguero VALUES(1,1,4);
INSERT INTO SBDcrud_bodeguero VALUES(2,2,5);
INSERT INTO SBDcrud_bodeguero VALUES(3,3,6);
INSERT INTO SBDcrud_bodeguero VALUES(4,1,7);
INSERT INTO SBDcrud_bodeguero VALUES(5,2,8);

INSERT INTO SBDcrud_recolectores VALUES(1,13);
INSERT INTO SBDcrud_recolectores VALUES(2,14);
INSERT INTO SBDcrud_recolectores VALUES(3,15);

INSERT INTO SBDcrud_fardos VALUES(1,13,1);
INSERT INTO SBDcrud_fardos VALUES(2,14,2);
INSERT INTO SBDcrud_fardos VALUES(3,15,3);
INSERT INTO SBDcrud_fardos VALUES(4,13,4);
INSERT INTO SBDcrud_fardos VALUES(5,15,5);


INSERT INTO SBDcrud_colorprincipal VALUES(1,'ROJO');
INSERT INTO SBDcrud_colorprincipal VALUES(2,'AZUL');
INSERT INTO SBDcrud_colorprincipal VALUES(3,'VERDE');
INSERT INTO SBDcrud_colorprincipal VALUES(4,'AMARILLO');
INSERT INTO SBDcrud_colorprincipal VALUES(5,'ROSA');
INSERT INTO SBDcrud_colorprincipal VALUES(6,'MORADO');
INSERT INTO SBDcrud_colorprincipal VALUES(7,'NARANJA');
INSERT INTO SBDcrud_colorprincipal VALUES(8,'MARRÓN');
INSERT INTO SBDcrud_colorprincipal VALUES(9,'GRIS');
INSERT INTO SBDcrud_colorprincipal VALUES(10,'BLANCO');

INSERT INTO SBDcrud_colorsecundario VALUES(1,'ROJO');
INSERT INTO SBDcrud_colorsecundario VALUES(2,'AZUL');
INSERT INTO SBDcrud_colorsecundario VALUES(3,'VERDE');
INSERT INTO SBDcrud_colorsecundario VALUES(4,'AMARILLO');
INSERT INTO SBDcrud_colorsecundario VALUES(5,'ROSA');
INSERT INTO SBDcrud_colorsecundario VALUES(6,'MORADO');
INSERT INTO SBDcrud_colorsecundario VALUES(7,'NARANJA');
INSERT INTO SBDcrud_colorsecundario VALUES(8,'MARRÓN');
INSERT INTO SBDcrud_colorsecundario VALUES(9,'GRIS');
INSERT INTO SBDcrud_colorsecundario VALUES(10,'BLANCO');


INSERT INTO SBDcrud_clasificadores VALUES(1,9);
INSERT INTO SBDcrud_clasificadores VALUES(2,10);
INSERT INTO SBDcrud_clasificadores VALUES(3,11);
INSERT INTO SBDcrud_clasificadores VALUES(4,12);

INSERT INTO SBDcrud_tela VALUES(1,1,7,7,5,1,1);
INSERT INTO SBDcrud_tela VALUES(2,2,1,1,1,2,1);
INSERT INTO SBDcrud_tela VALUES(3,3,2,7,8,3,1);
INSERT INTO SBDcrud_tela VALUES(4,4,2,8,10,4,1);
INSERT INTO SBDcrud_tela VALUES(5,2,8,4,3,5,1);


INSERT INTO SBDcrud_tipotela VALUES(1,'SEDA');
INSERT INTO SBDcrud_tipotela VALUES(2,'ALGODÓN');
INSERT INTO SBDcrud_tipotela VALUES(3,'LANA');
INSERT INTO SBDcrud_tipotela VALUES(4,'SATÉN');
INSERT INTO SBDcrud_tipotela VALUES(5,'DENIM');
INSERT INTO SBDcrud_tipotela VALUES(6,'TERCIOPELO');
INSERT INTO SBDcrud_tipotela VALUES(7,'LINO');
INSERT INTO SBDcrud_tipotela VALUES(8,'CUERO');
INSERT INTO SBDcrud_tipotela VALUES(9,'FRANELA');
INSERT INTO SBDcrud_tipotela VALUES(10,'CHIFFÓN');

INSERT INTO SBDcrud_patron VALUES(1,'CUADROS');
INSERT INTO SBDcrud_patron VALUES(2,'RAYAS');
INSERT INTO SBDcrud_patron VALUES(3,'GEOMETRICO');
INSERT INTO SBDcrud_patron VALUES(4,'FLORAL');
INSERT INTO SBDcrud_patron VALUES(5,'ANIMAL PRINT');

INSERT INTO SBDcrud_regbodegafar VALUES(1,'2023-05-17',1,1,1,1);
INSERT INTO SBDcrud_regbodegafar VALUES(2,'2023-05-07',2,2,1,2);
INSERT INTO SBDcrud_regbodegafar VALUES(3,'2023-06-24',3,3,2,3);
INSERT INTO SBDcrud_regbodegafar VALUES(4,'2023-05-23',4,1,2,4);
INSERT INTO SBDcrud_regbodegafar VALUES(5,'2023-06-27',5,2,3,5);

INSERT INTO SBDcrud_tipomovfardo VALUES(1,'RETIRO');
INSERT INTO SBDcrud_tipomovfardo VALUES(2,'INGRESO');
INSERT INTO SBDcrud_tipomovfardo VALUES(3,'CLASIFICACION');

INSERT INTO SBDcrud_usuario VALUES(12345678,'admin123',1,2);
INSERT INTO SBDcrud_usuario VALUES(98765432,'admin123',2,2);
INSERT INTO SBDcrud_usuario VALUES(12334457,'Sadmin123',16,1);
INSERT INTO SBDcrud_usuario VALUES(11223344,'bod123',6,3);
INSERT INTO SBDcrud_usuario VALUES(77889900,'fab123',11,4);

INSERT INTO SBDcrud_perfil VALUES(1,'SADMINISTRADOR');
INSERT INTO SBDcrud_perfil VALUES(2,'ADMINISTRADOR BODEGA');
INSERT INTO SBDcrud_perfil VALUES(3,'BODEGUERO');
INSERT INTO SBDcrud_perfil VALUES(4,'FABRICANTE');


INSERT INTO SBDcrud_tipomovimientom VALUES(1,'RETIRO');
INSERT INTO SBDcrud_tipomovimientom VALUES(2,'INGRESO');
INSERT INTO SBDcrud_tipomovimientom VALUES(3,'CLASIFICACION');


INSERT INTO SBDcrud_regbodegamuestra VALUES(1,'2023-05-14',1,1,1,1);
INSERT INTO SBDcrud_regbodegamuestra VALUES(2,'2023-06-02',2,2,2,1);
INSERT INTO SBDcrud_regbodegamuestra VALUES(3,'2023-06-17',3,3,2,1);
INSERT INTO SBDcrud_regbodegamuestra VALUES(4,'2023-06-03',3,4,3,1);
INSERT INTO SBDcrud_regbodegamuestra VALUES(5,'2023-06-13',2,5,4,1);


INSERT INTO SBDcrud_bodega VALUES(1,'BODEGA PRINCIPAL','CALLE PRIMAVERA 123',10,15);
INSERT INTO SBDcrud_bodega VALUES(2,'BODEGA FARDOS','AVENIDA DEL SOL PONIENTE 123',6,10);
INSERT INTO SBDcrud_bodega VALUES(3,'BODEGA RESUIDOS','CARRERA DE LAS ESTRELLAS 987',10,5);


INSERT INTO SBDcrud_ubicacion VALUES(1,1,1,1);
INSERT INTO SBDcrud_ubicacion VALUES(2,1,1,2);
INSERT INTO SBDcrud_ubicacion VALUES(3,1,1,3);
INSERT INTO SBDcrud_ubicacion VALUES(4,1,1,1);
INSERT INTO SBDcrud_ubicacion VALUES(5,1,1,2);


usuario2 = Usuario.objects.create(codUser='98765432', passW='admin123', codTra=2, codPer=2)
usuario3 = Usuario.objects.create(codUser='12334457', passW='admin123', codTra=16, codPer=1)
usuario4 = Usuario.objects.create(codUser='11223344', passW='bod123', codTra=6, codPer=3)
usuario5 = Usuario.objects.create(codUser='77889900', passW='bod123', codTra=11, codPer=4)
