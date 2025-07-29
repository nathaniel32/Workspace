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