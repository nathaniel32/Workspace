-- enum
CREATE TYPE user_role_enum AS ENUM ('ROOT', 'ADMIN', 'USER');
CREATE TYPE user_status_enum AS ENUM ('ACTIVATED', 'LOCKED', 'DELETED');
CREATE TYPE order_status_enum AS ENUM ('PENDING', 'PROCESSING', 'CONFIRMED', 'SHIPPED', 'DELIVERED', 'CANCELLED', 'RETURNED', 'FAILED', 'ON_HOLD');

-- User
CREATE TABLE t_user (
    u_id VARCHAR(32) PRIMARY KEY,
    u_name TEXT,
    u_email TEXT UNIQUE,
    u_password TEXT,
    u_code TEXT,
    u_role user_role_enum NOT NULL DEFAULT 'USER',  -- ROOT, ADMIN, USER
    u_status user_status_enum NOT NULL DEFAULT 'ACTIVATED', -- ACTIVATED, LOCKED, DELETED
    u_time INT DEFAULT (EXTRACT(EPOCH FROM now())::int)
);

-- Power
CREATE TABLE t_power (
    p_id VARCHAR(32) PRIMARY KEY,
    p_power INT NOT NULL UNIQUE,
    p_unit INT NOT NULL DEFAULT 0
);

-- Item
CREATE TABLE t_item (
    i_id VARCHAR(32) PRIMARY KEY,
    i_item TEXT NOT NULL UNIQUE,
    i_corrective BOOLEAN DEFAULT FALSE,
    i_order_by INT
);

-- Price List
CREATE TABLE t_price_list (
    p_id VARCHAR(32),
    i_id VARCHAR(32),
    pl_price DECIMAL(10,2) NOT NULL CHECK (pl_price >= 0),
    pl_description TEXT,
    PRIMARY KEY (p_id, i_id),
    FOREIGN KEY (p_id) REFERENCES t_power(p_id) ON DELETE CASCADE ON UPDATE RESTRICT,
    FOREIGN KEY (i_id) REFERENCES t_item(i_id) ON DELETE CASCADE ON UPDATE RESTRICT
);

-- Order
CREATE TABLE t_order (
    o_id VARCHAR(32),
    u_id VARCHAR(32) NOT NULL,  -- id pegawai yang menginput
    o_name TEXT,
    o_time INT NOT NULL DEFAULT (EXTRACT(EPOCH FROM now())::int),
    o_status order_status_enum NOT NULL DEFAULT 'PENDING',
    FOREIGN KEY (u_id) REFERENCES t_user(u_id) ON DELETE CASCADE ON UPDATE RESTRICT
);

-- Order Article
CREATE TABLE t_order_article (
    oa_id VARCHAR(32),
    p_id VARCHAR(32),
    o_id VARCHAR(32),
    oa_power INT NOT NULL UNIQUE,
    oa_name TEXT NOT NULL, -- Equiptment No
    oa_time TIMESTAMP NOT NULL DEFAULT now(),
    PRIMARY KEY (oa_id, p_id),
    FOREIGN KEY (o_id) REFERENCES t_order(o_id) ON DELETE RESTRICT ON UPDATE RESTRICT,
    FOREIGN KEY (p_id) REFERENCES t_power(p_id) ON DELETE RESTRICT ON UPDATE RESTRICT
);

-- Order Item
CREATE TABLE t_order_item (
    oa_id VARCHAR(32) NOT NULL,
    p_id VARCHAR(32) NOT NULL,
    i_id VARCHAR(32) NOT NULL,
    os_price DECIMAL(10,2) NOT NULL CHECK (os_price >= 0), -- deal/current price
    PRIMARY KEY (oa_id, i_id),
    FOREIGN KEY (oa_id, p_id) REFERENCES t_order_article(oa_id, p_id) ON DELETE CASCADE ON UPDATE RESTRICT,
    FOREIGN KEY (p_id, i_id) REFERENCES t_price_list(p_id, i_id) ON DELETE RESTRICT ON UPDATE RESTRICT
);