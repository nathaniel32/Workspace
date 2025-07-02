async function getAllPriceList(){
    try {
        const response = await fetch("/api/item/price", {
            method: "GET",
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        alert(error.message);
        return null;
    }
}