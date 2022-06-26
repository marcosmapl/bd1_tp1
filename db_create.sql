-- CREATE DATABASE amazon
--     WITH
--     OWNER = postgres
--     ENCODING = 'UTF8'
--     CONNECTION LIMIT = -1;

CREATE TABLE product (
	product_id int NOT NULL,
	asin varchar(50) NOT NULL UNIQUE,
	title varchar(70),
	product_group varchar(50),
	salesrank int,
	review_total int DEFAULT 0,
	review_downloaded int DEFAULT 0,
	review_avg float DEFAULT 0.0,
	PRIMARY KEY (product_id)
);

CREATE TABLE similar_products (
	product_asin varchar(50) NOT NULL,
	similar_asin varchar(50) NOT NULL,
	PRIMARY KEY (product_asin, similar_asin),
	FOREIGN KEY (product_asin) REFERENCES product(asin),
	FOREIGN KEY (similar_asin) REFERENCES product(asin)
);

CREATE TABLE category (
	category_id int NOT NULL,
	name varchar(50),
	parent_id int,
	PRIMARY KEY (category_id),
	FOREIGN KEY (parent_id) REFERENCES category(category_id)
);

CREATE TABLE product_category (
	product_id int NOT NULL,
	category_id int NOT NULL,
	PRIMARY KEY (product_id, category_id),
	FOREIGN KEY (product_id) REFERENCES product(product_id),
	FOREIGN KEY (category_id) REFERENCES category(category_id)
);

CREATE TABLE review (
	product_id int NOT NULL,
	customer_id varchar(50) NOT NULL,
	review_date date,
	rating int DEFAULT 0,
	votes int DEFAULT 0,
	helpful int DEFAULT 0,
	PRIMARY KEY (product_id, customer_id),
	FOREIGN KEY (product_id) REFERENCES product(product_id)
);
