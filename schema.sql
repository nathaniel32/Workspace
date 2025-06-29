-- User
CREATE TABLE t_user (
    u_id VARCHAR(32) PRIMARY KEY,
    u_name TEXT NOT NULL,
    u_email TEXT NOT NULL UNIQUE,
    u_password TEXT NOT NULL,
    u_code TEXT,
    u_role INT NOT NULL,  -- 1 = ADMIN, 2 = USER, 3 = GUEST
    u_time INT DEFAULT (UNIX_TIMESTAMP())
);

-- Power
CREATE TABLE t_power (
    p_id VARCHAR(32) PRIMARY KEY,
    p_kw INT NOT NULL
);

-- Spec
CREATE TABLE t_spec (
    s_id VARCHAR(32) PRIMARY KEY,
    s_kw TEXT NOT NULL
);

-- Article
CREATE TABLE t_article (
    p_id VARCHAR(32),
    s_id VARCHAR(32),
    a_name TEXT,
    a_description TEXT,
    a_price DECIMAL(10,2) NOT NULL CHECK (a_price >= 0),
    PRIMARY KEY (p_id, s_id),
    FOREIGN KEY (p_id) REFERENCES t_power(p_id),
    FOREIGN KEY (s_id) REFERENCES t_spec(s_id)
);

-- Order
CREATE TABLE t_order (
    o_id VARCHAR(32),
    p_id VARCHAR(32),
    u_id VARCHAR(32) NOT NULL,
    o_name TEXT,
    o_description TEXT,
    o_time INT NOT NULL DEFAULT (UNIX_TIMESTAMP()),
    PRIMARY KEY (o_id, p_id),
    FOREIGN KEY (u_id) REFERENCES t_user(u_id),
    FOREIGN KEY (p_id) REFERENCES t_power(p_id)
);

-- Order Spec
CREATE TABLE t_order_spec (
    os_id VARCHAR(32) PRIMARY KEY,
    o_id VARCHAR(32) NOT NULL,
    p_id VARCHAR(32) NOT NULL,
    s_id VARCHAR(32) NOT NULL,
    os_price DECIMAL(10,2) NOT NULL CHECK (os_price >= 0), -- deal price
    FOREIGN KEY (o_id, p_id) REFERENCES t_order(o_id, p_id),
    FOREIGN KEY (p_id, s_id) REFERENCES t_article(p_id, s_id)
);