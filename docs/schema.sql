CREATE TABLE contacts(
    id SERIAL PRIMARY KEY,
    name VARCHAR(250) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(250),
    relation VARCHAR(50),
    address VARCHAR(250)
);