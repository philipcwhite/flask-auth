CREATE DATABASE  IF NOT EXISTS monitoring;
USE monitoring;

DROP TABLE IF EXISTS nodes;
CREATE TABLE nodes (
  id int(10) NOT NULL AUTO_INCREMENT,
  name varchar(100) NOT NULL,
  ip varchar(20) NOT NULL,
  os varchar(150) NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

LOCK TABLES nodes WRITE;
INSERT INTO nodes VALUES (1,'test01','10.0.0.1','Linux'),(2,'test02','10.0.0.2','Windows');
UNLOCK TABLES;

DROP TABLE IF EXISTS users;
CREATE TABLE users (
  id int(10) NOT NULL AUTO_INCREMENT,
  user varchar(50) NOT NULL,
  password varchar(50) NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

LOCK TABLES users WRITE;
INSERT INTO users VALUES (1,'admin','password');
UNLOCK TABLES;
