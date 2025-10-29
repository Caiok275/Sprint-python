CREATE TABLE T_HCFMUSP_DOUTORES (
    id_doutor INT GENERATED ALWAYS AS IDENTITY,
    nm_doutor VARCHAR2(80) NOT NULL,
    tipo_consulta VARCHAR2(80) NOT NULL,
    CONSTRAINT doutor_pk PRIMARY KEY (id_doutor)
);

CREATE TABLE T_HCFMUSP_CONSULTAS (
    id_consulta INT GENERATED ALWAYS AS IDENTITY,
    nm_paciente VARCHAR2(80) NOT NULL,
    id_doutor INT NOT NULL,
    dt_consulta DATE,
    CONSTRAINT consulta_pk PRIMARY KEY (id_consulta),
    CONSTRAINT fk_doutor FOREIGN KEY (id_doutor)
        REFERENCES T_HCFMUSP_DOUTORES (id_doutor)
);


INSERT INTO T_HCFMUSP_DOUTORES (nm_doutor, tipo_consulta)
VALUES ('Dr.Ricardo', 'Exame Geral');

INSERT INTO T_HCFMUSP_DOUTORES (nm_doutor, tipo_consulta)
VALUES ('Dra.Maria', 'Exame Geral');


INSERT INTO T_HCFMUSP_DOUTORES (nm_doutor, tipo_consulta)
VALUES ('Dr.Pedro', 'Exame de sangue');

INSERT INTO T_HCFMUSP_DOUTORES (nm_doutor, tipo_consulta)
VALUES ('Dr.Ana', 'Exame de sangue');


INSERT INTO T_HCFMUSP_DOUTORES (nm_doutor, tipo_consulta)
VALUES ('Dr.Lucas', 'Raio-X');

INSERT INTO T_HCFMUSP_DOUTORES (nm_doutor, tipo_consulta)
VALUES ('Dr.Vitor', 'Ultrassom');