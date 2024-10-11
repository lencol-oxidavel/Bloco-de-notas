CREATE DATABASE bloco_de_notas;

USE bloco_de_notas;

CREATE TABLE notas (
	ID_nota INT AUTO_INCREMENT PRIMARY KEY,
    nome varchar(255),
    content mediumtext
)