//return success, message, data
export async function api_get_all_price_list() {
    try {
        const response = await fetch('/api/item/price', {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        });
        const result = await response.json();

        if (!response.ok) {
            const errorMsg = result.message || result.error || `HTTP error! status: ${response.status}`;
            throw new Error(errorMsg);
        }
        
        return { success: true, message: result.message || "ok", data: result };
    } catch (error) {
        console.error("Error:", error);
        return { success: false, message: error.message || "Unknown error", data: null };
    }
}

export async function api_get_all_specs() {
    try {
        const response = await fetch('/api/item/spec', {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        });
        const result = await response.json();

        if (!response.ok) {
            const errorMsg = result.message || result.error || `HTTP error! status: ${response.status}`;
            throw new Error(errorMsg);
        }
        
        return { success: true, message: result.message || "ok", data: result };
    } catch (error) {
        console.error("Error:", error);
        return { success: false, message: error.message || "Unknown error", data: null };
    }
}

export async function api_get_all_orders() {
    try {
        const response = await fetch('/api/order/order', {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        });
        const result = await response.json();

        if (!response.ok) {
            const errorMsg = result.message || result.error || `HTTP error! status: ${response.status}`;
            throw new Error(errorMsg);
        }
        
        return { success: true, message: result.message || "ok", data: result };
    } catch (error) {
        console.error("Error:", error);
        return { success: false, message: error.message || "Unknown error", data: null };
    }
}

export async function api_input_order(description) {
    try {
        const response = await fetch('/api/order/order', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                o_description: description
            })
        });

        if (!response.ok) {
            const errorResult = await response.json();
            const errorMsg = errorResult.message || errorResult.error || `HTTP error! status: ${response.status}`;
            throw new Error(errorMsg);
        }

        const result = await response.json();
        return { success: true, message: result.message || "ok", data: result };
    } catch (error) {
        console.error("Error:", error);
        return { success: false, message: error.message || "Unknown error", data: null };
    }
}

export async function api_input_order_artikel(order_id, order_artikel_power, order_artikel_description, order_artikel_id_specs) {
    try {
        const response = await fetch('/api/order/order-artikel', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                o_id: order_id,
                power: order_artikel_power,
                oa_description: order_artikel_description,
                s_ids: order_artikel_id_specs
            })
        });

        if (!response.ok) {
            const errorResult = await response.json();
            const errorMsg = errorResult.message || errorResult.error || `HTTP error! status: ${response.status}`;
            throw new Error(errorMsg);
        }

        const result = await response.json();
        return { success: true, message: result.message || "ok", data: result };
    } catch (error) {
        console.error("Error:", error);
        return { success: false, message: error.message || "Unknown error", data: null };
    }
}

export async function api_input_power(power) {
    try {
        const response = await fetch('/api/item/power', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                p_power: power
            })
        });

        if (!response.ok) {
            const errorResult = await response.json();
            const errorMsg = errorResult.message || errorResult.error || `HTTP error! status: ${response.status}`;
            throw new Error(errorMsg);
        }

        const result = await response.json();
        return { success: true, message: result.message || "ok", data: result };
    } catch (error) {
        console.error("Error:", error);
        return { success: false, message: error.message || "Unknown error", data: null };
    }
}

export async function api_input_spec(spec) {
    try {
        const response = await fetch('/api/item/spec', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                s_spec: spec
            })
        });

        if (!response.ok) {
            const errorResult = await response.json();
            const errorMsg = errorResult.message || errorResult.error || `HTTP error! status: ${response.status}`;
            throw new Error(errorMsg);
        }

        const result = await response.json();
        return { success: true, message: result.message || "ok", data: result };
    } catch (error) {
        console.error("Error:", error);
        return { success: false, message: error.message || "Unknown error", data: null };
    }
}

export async function api_update_price(p_id, s_id, new_description, new_price) {
    console.log(new_price, new_description)
    try {
        const response = await fetch('/api/item/price', {
            method: 'PUT',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                p_id: p_id,
                s_id: s_id,
                pl_description: new_description,
                pl_price: new_price
            })
        });

        if (!response.ok) {
            const errorResult = await response.json();
            const errorMsg = errorResult.message || errorResult.error || `HTTP error! status: ${response.status}`;
            throw new Error(errorMsg);
        }

        const result = await response.json();
        return { success: true, message: result.message || "ok", data: result };
    } catch (error) {
        console.error("Error:", error);
        return { success: false, message: error.message || "Unknown error", data: null };
    }
}