CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(150) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL,
    password VARCHAR NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATE,
    updated_at DATE,
    intuit_access_token VARCHAR,
    intuit_state_token VARCHAR,
    intuit_realm_id INT,
    intuit_refresh_token VARCHAR
);

CREATE TABLE IF NOT EXISTS addresses (
    id SERIAL PRIMARY KEY,
    to_from VARCHAR(150) NOT NULL,
    street VARCHAR(150) NOT NULL,
    city VARCHAR(150) NOT NULL,
    state CHAR(2) NOT NULL,
    zip CHAR(5) NOT NULL
);

CREATE TABLE IF NOT EXISTS companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150),
    address_id INT NOT NULL,
    phone_number INT,
    contact_email VARCHAR(150),
    CONSTRAINT fk_address
        FOREIGN KEY (address_id)
            REFERENCES addresses(id)
);



CREATE TYPE status AS ENUM ('Delivered', 'Loaded', 'Pending');
CREATE TYPE delivery_types AS ENUM ('Curbside', 'In-Home');

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    order_number INT,
    batch_number INT,
    created_at DATE,
    company_id INT,
    estimated_delivery_date DATE,
    status status,
    delivery_address_id INT,
    notes TEXT,
    quote_price FLOAT,
    CONSTRAINT fk_delivery_address
        FOREIGN KEY (delivery_address_id)
            REFERENCES addresses(id),
    CONSTRAINT fk_company
        FOREIGN KEY (company_id)
            REFERENCES companies(id)
);

CREATE TABLE IF NOT EXISTS locations(
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    address_id INT NOT NULL,
    CONSTRAINT fk_address
        FOREIGN KEY (address_id)
            REFERENCES addresses(id)
);

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    title VARCHAR(150),
    location_id INT,
    product_number INT,
    image_url TEXT,
    notes TEXT,
    quantity INT DEFAULT 1 NOT NULL,
    delivery_type delivery_types,
    CONSTRAINT fk_location
        FOREIGN KEY(location_id)
            REFERENCES locations(id)
);

CREATE TABLE IF NOT EXISTS attachments(
    id SERIAL PRIMARY KEY,
    path TEXT NOT NULL 
);

CREATE TABLE IF NOT EXISTS order_products (
    order_id INT REFERENCES orders(id),
    product_id INT REFERENCES products(id),
    PRIMARY KEY (order_id, product_id)
);

CREATE TABLE IF NOT EXISTS order_attachments (
    order_id INT REFERENCES orders(id),
    attachment_id INT REFERENCES attachments(id),
    PRIMARY KEY (order_id, attachment_id)
);


-- Post creation modifications

ALTER TABLE companies ALTER COLUMN phone_number TYPE VARCHAR(20); -- support international phone numbers
ALTER TABLE orders ADD COLUMN estimated_ready_date DATE;
--ALTER TABLE addresses ALTER COLUMN city DROP NOT NULL;
--ALTER TABLE addresses ALTER COLUMN zip DROP NOT NULL;
--ALTER TABLE addresses ALTER COLUMN state DROP NOT NULL;
--ALTER TABLE addresses ALTER COLUMN street DROP NOT NULL;