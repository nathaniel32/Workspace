from sqlalchemy import text

trigger_power_drop = """
DROP TRIGGER IF EXISTS trg_after_power_insert ON t_power;
"""

trigger_function_power = """
CREATE OR REPLACE FUNCTION trg_add_price_list_on_power()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO t_price_list (p_id, s_id, pl_price)
    SELECT NEW.p_id, s.s_id, 0.00
    FROM t_spec s
    ON CONFLICT (p_id, s_id) DO NOTHING;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
"""

trigger_power = """
CREATE TRIGGER trg_after_power_insert
AFTER INSERT ON t_power
FOR EACH ROW
EXECUTE FUNCTION trg_add_price_list_on_power();
"""

trigger_spec_drop = """
DROP TRIGGER IF EXISTS trg_after_spec_insert ON t_spec;
"""

trigger_function_spec = """
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
"""

trigger_spec = """
CREATE TRIGGER trg_after_spec_insert
AFTER INSERT ON t_spec
FOR EACH ROW
EXECUTE FUNCTION trg_add_price_list_on_spec();
"""

def create_triggers(engine):
    with engine.connect() as conn:
        conn.execute(text(trigger_function_power))
        conn.execute(text(trigger_power_drop))
        conn.execute(text(trigger_power))
        conn.execute(text(trigger_function_spec))
        conn.execute(text(trigger_spec_drop))
        conn.execute(text(trigger_spec))
        conn.commit()