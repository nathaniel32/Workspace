-- enum role
CREATE TYPE user_role_enum AS ENUM ('ADMIN', 'USER', 'GUEST');

-- User
CREATE TABLE t_user (
    u_id VARCHAR(32) PRIMARY KEY,
    u_name TEXT NOT NULL,
    u_email TEXT NOT NULL UNIQUE,
    u_password TEXT NOT NULL,
    u_code TEXT,
    u_role user_role_enum NOT NULL,  -- ADMIN, USER, GUEST
    u_time INT DEFAULT (EXTRACT(EPOCH FROM now())::int)
);

-- Power
CREATE TABLE t_power (
    p_id VARCHAR(32) PRIMARY KEY,
    p_power INT NOT NULL
);

-- Spec
CREATE TABLE t_spec (
    s_id VARCHAR(32) PRIMARY KEY,
    s_spec TEXT NOT NULL
);

-- Price List
CREATE TABLE t_price_list (
    p_id VARCHAR(32),
    s_id VARCHAR(32),
    pl_price DECIMAL(10,2) NOT NULL CHECK (pl_price >= 0),
    PRIMARY KEY (p_id, s_id),
    FOREIGN KEY (p_id) REFERENCES t_power(p_id),
    FOREIGN KEY (s_id) REFERENCES t_spec(s_id)
);

-- Order
CREATE TABLE t_order (
    o_id VARCHAR(32),
    u_id VARCHAR(32) NOT NULL,
    o_description TEXT,
    o_time INT NOT NULL DEFAULT (EXTRACT(EPOCH FROM now())::int),
    FOREIGN KEY (u_id) REFERENCES t_user(u_id)
);

-- Order Article
CREATE TABLE t_order_article (
    oa_id VARCHAR(32),
    p_id VARCHAR(32),
    o_id VARCHAR(32),
    opl_description TEXT,
    PRIMARY KEY (oa_id, p_id),
    FOREIGN KEY (o_id) REFERENCES t_order(o_id),
    FOREIGN KEY (p_id) REFERENCES t_power(p_id)
);

-- Order Spec
CREATE TABLE t_order_spec (
    -- os_id VARCHAR(32) PRIMARY KEY,
    oa_id VARCHAR(32) NOT NULL,
    p_id VARCHAR(32) NOT NULL,
    s_id VARCHAR(32) NOT NULL,
    os_price DECIMAL(10,2) NOT NULL CHECK (os_price >= 0), -- deal price
    PRIMARY KEY (oa_id, s_id),
    FOREIGN KEY (oa_id, p_id) REFERENCES t_order_article(oa_id, p_id),
    FOREIGN KEY (p_id, s_id) REFERENCES t_price_list(p_id, s_id)
);