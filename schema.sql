
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS suspect;
DROP TABLE IF EXISTS imagem;
DROP TABLE IF EXISTS spot;
DROP TABLE IF EXISTS ficha;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE imagem (
  id_img INTEGER PRIMARY KEY AUTOINCREMENT,
  path_img UNIQUE NOT NULL,
  img_cpf TEXT UNIQUE NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,  
  FOREIGN KEY (img_cpf) REFERENCES suspect (cpf)
);

CREATE TABLE spot (
  id_spot INTEGER PRIMARY KEY AUTOINCREMENT,
  spot_cpf TEXT UNIQUE NOT NULL, 
  local_spot TEXT NOT NULL, 
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (spot_cpf) REFERENCES suspect (cpf)
);


CREATE TABLE ficha (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  cpf_ficha TEXT UNIQUE NOT NULL,
  art TEXT, 
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (cpf_ficha) REFERENCES suspect (cpf)
);

CREATE TABLE suspect(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name_full VARCHAR(255) NOT NULL,
  cpf TEXT UNIQUE NOT NULL,
  rg TEXT UNIQUE NOT NULL,
  nickname VARCHAR(255),
  dn DATE,
  endereco VARCHAR (255),
  mother VARCHAR(255),
  faccao VARCHAR(255),
  ficha VARCHAR(255),
  spot VARCHAR(255)
);
