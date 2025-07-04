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

export async function api_update_price(p_id, s_id, new_price) {
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

/* export function get_unique_sorted_specs(priceList) {
    const uniqueSpecs = new Set(priceList.map(item => item.spec));
    return Array.from(uniqueSpecs).sort();
}

export function get_unique_sorted_powers(priceList) {
    const uniquePowers = new Set(priceList.map(item => item.power));
    return Array.from(uniquePowers).sort((a, b) => a - b);
} */

export function get_unique_sorted_specs(priceList) {
    const seen = new Set();
    const uniqueSpecs = [];

    for (const item of priceList) {
        const key = item.s_id; // unik berdasarkan s_id
        if (!seen.has(key)) {
            seen.add(key);
            uniqueSpecs.push({ s_id: item.s_id, spec: item.spec });
        }
    }

    // Sort berdasarkan spec (string)
    /* uniqueSpecs.sort((a, b) => {
        if (a.spec < b.spec) return -1;
        if (a.spec > b.spec) return 1;
        return 0;
    }); */

    return uniqueSpecs;
}

export function get_unique_sorted_powers(priceList) {
    const seen = new Set();
    const uniquePowers = [];

    for (const item of priceList) {
        const key = item.p_id;
        if (!seen.has(key)) {
            seen.add(key);
            uniquePowers.push({ p_id: item.p_id, power: item.power });
        }
    }

    uniquePowers.sort((a, b) => a.power - b.power);

    return uniquePowers;
}

export function get_price_list_item(priceList, power_id, spec_id, key=null) {
    if (!Array.isArray(priceList)) return '-';
    const found = priceList.find(item => item.p_id === power_id && item.s_id === spec_id);
    if (!found) return '-';
    if (key) {
        return found[key];
    }else{
        return found
    }
}

//Deformat 120.000,5 => 120000.5
export function deformat_price(price) {
    return price.replace(/[^\d,]/g, '').replace(',', '.');
}

//format 120000.5 => 120.000,5
export function format_price(price) {
    price = price.replace(/\./g, ',');
    return beautify_format_price(price);
}

//format 120000,5 => 120.000,5
export function beautify_format_price(price){
    if (price === '-' || price === null || price === undefined) return '-';

    // Ambil hanya digit dan koma
    let raw = price.toString().replace(/[^\d,]/g, '');

    // bulat dan desimal
    let parts = raw.split(',');
    let integerPart = parts[0];
    let decimalPart = parts[1];

    // Format ribuan
    integerPart = integerPart.replace(/\B(?=(\d{3})+(?!\d))/g, ".");

    if ((decimalPart && decimalPart !== '00') || price[price.length - 1] === ',') {
        return `${integerPart},${decimalPart}`;
    }

    return integerPart;
}