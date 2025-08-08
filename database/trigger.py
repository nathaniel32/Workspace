from sqlalchemy import text

trigger_power_drop = """
DROP TRIGGER IF EXISTS trg_after_power_insert ON t_power;
"""

trigger_function_power = """
CREATE OR REPLACE FUNCTION trg_add_price_list_on_power()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO t_price_list (p_id, i_id, pl_price)
    SELECT NEW.p_id, s.i_id, 0.00
    FROM t_item s
    ON CONFLICT (p_id, i_id) DO NOTHING;
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

trigger_item_drop = """
DROP TRIGGER IF EXISTS trg_after_item_insert ON t_item;
"""

trigger_function_item = """
CREATE OR REPLACE FUNCTION trg_add_price_list_on_item()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO t_price_list (p_id, i_id, pl_price)
    SELECT p.p_id, NEW.i_id, 0.00
    FROM t_power p
    ON CONFLICT (p_id, i_id) DO NOTHING;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
"""

trigger_item = """
CREATE TRIGGER trg_after_item_insert
AFTER INSERT ON t_item
FOR EACH ROW
EXECUTE FUNCTION trg_add_price_list_on_item();
"""

def create_triggers(engine):
    with engine.connect() as conn:
        conn.execute(text(trigger_function_power))
        conn.execute(text(trigger_power_drop))
        conn.execute(text(trigger_power))
        conn.execute(text(trigger_function_item))
        conn.execute(text(trigger_item_drop))
        conn.execute(text(trigger_item))
        conn.commit()