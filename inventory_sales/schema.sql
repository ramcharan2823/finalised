create database retailstores

use retailstores

create schema Tables;
go

create table products(
	product_id VARCHAR(10) PRIMARY KEY,
	Name VARCHAR(100) NOT NULL,
	category VARCHAR(100) NOT NULL,
	price DECIMAL (10,2) NOT NULL,
	quantity INT NOT NULL
)

create table customers(
	customer_id VARCHAR(10) PRIMARY KEY,
	name VARCHAR(100) NOT NULL,
	phone VARCHAR(15) NOT NULL
)

create table sales(
	sale_id INT IDENTITY(1,1) PRIMARY KEY ,
	customer_id VARCHAR(10),
	product_id VARCHAR(10),
	quantity INT NOT NULL,
	sale_date DATE NOT NULL,
	FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
	FOREIGN KEY (product_id) REFERENCES products(product_id)
	)