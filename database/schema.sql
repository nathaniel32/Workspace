-- enum role
CREATE TYPE user_role_enum AS ENUM ('ADMIN', 'USER');
CREATE TYPE user_status_enum AS ENUM ('NOT_ACTIVATED', 'ACTIVATED', 'LOCKED', 'DELETED');
CREATE TYPE order_status_enum AS ENUM ('PENDING', 'PROCESSING', 'CONFIRMED', 'SHIPPED', 'DELIVERED', 'CANCELLED', 'RETURNED', 'FAILED', 'ON_HOLD');

-- User
CREATE TABLE t_user (
    u_id VARCHAR(32) PRIMARY KEY,
    u_name TEXT NOT NULL,
    u_email TEXT NOT NULL UNIQUE,
    u_password TEXT NOT NULL,
    u_code TEXT,
    u_role user_role_enum NOT NULL,  -- ADMIN, USER
    u_status user_status_enum NOT NULL, -- NOT_ACTIVATED, ACTIVATED, LOCKED, DELETED
    u_time INT DEFAULT (EXTRACT(EPOCH FROM now())::int)
);

-- Power
CREATE TABLE t_power (
    p_id VARCHAR(32) PRIMARY KEY,
    p_power INT NOT NULL UNIQUE,
    p_unit INT NOT NULL DEFAULT 0
);

-- Spec
CREATE TABLE t_spec (
    s_id VARCHAR(32) PRIMARY KEY,
    s_spec TEXT NOT NULL UNIQUE,
    s_corrective BOOLEAN DEFAULT FALSE
);

-- Price List
CREATE TABLE t_price_list (
    p_id VARCHAR(32),
    s_id VARCHAR(32),
    pl_price DECIMAL(10,2) NOT NULL CHECK (pl_price >= 0),
    pl_description TEXT,
    PRIMARY KEY (p_id, s_id),
    FOREIGN KEY (p_id) REFERENCES t_power(p_id) ON DELETE CASCADE ON UPDATE RESTRICT,
    FOREIGN KEY (s_id) REFERENCES t_spec(s_id) ON DELETE CASCADE ON UPDATE RESTRICT
);

-- Order
CREATE TABLE t_order (
    o_id VARCHAR(32),
    -- o_orderid TEXT UNIQUE NOT NULL,   !OPTIONAL JIKA ID SUDAH DI TENTUKAN!
    u_id VARCHAR(32) NOT NULL,  -- id pegawai yang menginput
    o_description TEXT NOT NULL,
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
    oa_description TEXT NOT NULL, -- Equiptment No
    PRIMARY KEY (oa_id, p_id),
    FOREIGN KEY (o_id) REFERENCES t_order(o_id) ON DELETE RESTRICT ON UPDATE RESTRICT,
    FOREIGN KEY (p_id) REFERENCES t_power(p_id) ON DELETE RESTRICT ON UPDATE RESTRICT
);

-- Order Spec
CREATE TABLE t_order_spec (
    -- os_id VARCHAR(32) PRIMARY KEY,
    oa_id VARCHAR(32) NOT NULL,
    p_id VARCHAR(32) NOT NULL,
    s_id VARCHAR(32) NOT NULL,
    os_price DECIMAL(10,2) NOT NULL CHECK (os_price >= 0), -- deal/current price
    PRIMARY KEY (oa_id, s_id),
    FOREIGN KEY (oa_id, p_id) REFERENCES t_order_article(oa_id, p_id) ON DELETE CASCADE ON UPDATE RESTRICT,
    FOREIGN KEY (p_id, s_id) REFERENCES t_price_list(p_id, s_id) ON DELETE RESTRICT ON UPDATE RESTRICT
);

---------------------------------------------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION trg_add_price_list_on_power()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO t_price_list (p_id, s_id, pl_price)
    SELECT NEW.p_id, s.s_id, 0.00
    FROM t_spec s
    ON CONFLICT (p_id, s_id) DO NOTHING; -- jika sudah ada, hindari duplikasi

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;



CREATE TRIGGER trg_after_power_insert
AFTER INSERT ON t_power
FOR EACH ROW
EXECUTE FUNCTION trg_add_price_list_on_power();


CREATE OR REPLACE FUNCTION trg_add_price_list_on_spec()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO t_price_list (p_id, s_id, pl_price)
    SELECT p.p_id, NEW.s_id, 0.00
    FROM t_power p
    ON CONFLICT (p_id, s_id) DO NOTHING;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_after_spec_insert
AFTER INSERT ON t_spec
FOR EACH ROW
EXECUTE FUNCTION trg_add_price_list_on_spec();