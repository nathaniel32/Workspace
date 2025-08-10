export async function api_get_all_price_list() {
    try {
        const response = await fetch('/api/element/price', {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        });
        const result = await response.json();

        if (!response.ok) {
            const errorMsg = result.detail || `HTTP error! status: ${response.status}`;
            throw new Error(errorMsg);
        }
        
        return { message: result.message || "ok", data: result };
    } catch (error) {
        console.error("Error:", error);
        throw error;
    }
}

export async function api_get_all_powers() {
    try {
        const response = await fetch('/api/element/power', {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        });
        const result = await response.json();

        if (!response.ok) {
            const errorMsg = result.detail || `HTTP error! status: ${response.status}`;
            throw new Error(errorMsg);
        }
        
        return { message: result.message || "ok", data: result };
    } catch (error) {
        console.error("Error:", error);
        throw error;
    }
}

export async function api_get_all_items() {
    try {
        const response = await fetch('/api/element/item', {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        });
        const result = await response.json();

        if (!response.ok) {
            const errorMsg = result.detail || `HTTP error! status: ${response.status}`;
            throw new Error(errorMsg);
        }
        
        return { message: result.message || "ok", data: result };
    } catch (error) {
        console.error("Error:", error);
        throw error;
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
            const errorMsg = result.detail || `HTTP error! status: ${response.status}`;
            throw new Error(errorMsg);
        }
        
        return { message: result.message || "ok", data: result };
    } catch (error) {
        console.error("Error:", error);
        throw error;
    }
}

export async function api_upload_order_file(order_file) {
    const formData = new FormData();
    formData.append('order_file', order_file);
    
    try {
        const response = await fetch('/api/order/order/file', {
            method: 'POST',
            headers: {
                'Accept': 'application/json'
            },
            body: formData
        });

        const result = await response.json();

        if (!response.ok) {
            throw result;
        }

        return { message: result.message || "ok", data: result };
    } catch (error) {
        console.error("Error:", error);
        throw error;
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
                o_name: description
            })
        });

        if (!response.ok) {
            const errorResult = await response.json();
            const errorMsg = errorResult.detail || `HTTP error! status: ${response.status}`;
            throw new Error(errorMsg);
        }

        const result = await response.json();
        return { message: result.message || "ok", data: result };
    } catch (error) {
        console.error("Error:", error);
        throw error;
    }
}

export async function api_get_order_by_id(o_id) {
    try {
        const response = await fetch(`/api/order/order/${o_id}`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        });
        const result = await response.json();

        if (!response.ok) {
            const errorMsg = result.detail || `HTTP error! status: ${response.status}`;
            throw new Error(errorMsg);
        }
        
        return { message: result.message || "ok", data: result };
    } catch (error) {
        console.error("Error:", error);
        throw error;
    }
}

export async function api_get_order_articles_with_items(o_id) {
    try {
        const response = await fetch(`/api/order/order-article/${o_id}`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        });
        const result = await response.json();

        if (!response.ok) {
            const errorMsg = result.detail || `HTTP error! status: ${response.status}`;
            throw new Error(errorMsg);
        }
        
        return { message: result.message || "ok", data: result };
    } catch (error) {
        console.error("Error:", error);
        throw error;
    }
}

export async function api_input_order_article(order_id, order_article_power, order_article_description, order_article_id_items) {
    try {
        const response = await fetch('/api/order/order-article', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                o_id: order_id,
                power: order_article_power,
                oa_name: order_article_description,
                i_id_list: order_article_id_items
            })
        });

        if (!response.ok) {
            const errorResult = await response.json();
            const errorMsg = errorResult.detail || `HTTP error! status: ${response.status}`;
            throw new Error(errorMsg);
        }

        const result = await response.json();
        return { message: result.message || "ok", data: result };
    } catch (error) {
        console.error("Error:", error);
        throw error;
    }
}

export async function api_delete_order_article(oa_id) {
    try {
        const response = await fetch(`/api/order/order-article`, {
            method: 'DELETE',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ oa_id })
        });

        const result = await response.json();

        if (!response.ok) {
            const errorMsg = result.detail || `HTTP error! status: ${response.status}`;
            throw new Error(errorMsg);
        }
        
        return { message: result.message || "ok", data: result };
    } catch (error) {
        console.error("Error:", error);
        throw error;
    }
}

export async function api_input_power(power) {
    try {
        const response = await fetch('/api/element/power', {
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
            const errorMsg = errorResult.detail || `HTTP error! status: ${response.status}`;
            throw new Error(errorMsg);
        }

        const result = await response.json();
        return { message: result.message || "ok", data: result };
    } catch (error) {
        console.error("Error:", error);
        throw error;
    }
}

export async function api_input_item(item, corrective) {
    try {
        const response = await fetch('/api/element/item', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                i_item: item,
                i_corrective: corrective
            })
        });

        if (!response.ok) {
            const errorResult = await response.json();
            const errorMsg = errorResult.detail || `HTTP error! status: ${response.status}`;
            throw new Error(errorMsg);
        }

        const result = await response.json();
        return { message: result.message || "ok", data: result };
    } catch (error) {
        console.error("Error:", error);
        throw error;
    }
}

export async function api_update_price(p_id, i_id, new_description, new_price) {
    console.log(new_price, new_description)
    try {
        const response = await fetch('/api/element/price', {
            method: 'PUT',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                p_id: p_id,
                i_id: i_id,
                pl_description: new_description,
                pl_price: new_price
            })
        });

        if (!response.ok) {
            const errorResult = await response.json();
            const errorMsg = errorResult.detail || `HTTP error! status: ${response.status}`;
            throw new Error(errorMsg);
        }

        const result = await response.json();
        return { message: result.message || "ok", data: result };
    } catch (error) {
        console.error("Error:", error);
        throw error;
    }
}

export async function api_workbench_query(query) {
    try {
        const response = await fetch('/api/workbench/query', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                query: query
            })
        });

        if (!response.ok) {
            const errorResult = await response.json();
            const errorMsg = errorResult.detail || `HTTP error! status: ${response.status}`;
            throw new Error(errorMsg);
        }

        const result = await response.json();
        return { message: result.message || "ok", data: result };
    } catch (error) {
        console.error("Error:", error);
        throw error;
    }
}

export async function api_get_workbench_schema() {
    try {
        const response = await fetch('/api/workbench/schema', {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        });

        if (!response.ok) {
            const errorResult = await response.json();
            const errorMsg = errorResult.detail || `HTTP error! status: ${response.status}`;
            throw new Error(errorMsg);
        }

        const result = await response.json();
        return { message: result.message || "ok", data: result };
    } catch (error) {
        console.error("Error:", error);
        throw error;
    }
}

export async function api_get_enum_order_status() {
    try {
        const response = await fetch('/api/order/status', {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        });

        if (!response.ok) {
            const errorResult = await response.json();
            const errorMsg = errorResult.detail || `HTTP error! status: ${response.status}`;
            throw new Error(errorMsg);
        }

        const result = await response.json();
        return { message: result.message || "ok", data: result };
    } catch (error) {
        console.error("Error:", error);
        throw error;
    }
}

export async function api_update_order(o_id, o_name, o_status) {
    try {
        const response = await fetch('/api/order/order', {
            method: 'PUT',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                o_id,
                o_name,
                o_status,
            })
        });

        if (!response.ok) {
            const errorResult = await response.json();
            const errorMsg = errorResult.detail || `HTTP error! status: ${response.status}`;
            throw new Error(errorMsg);
        }

        const result = await response.json();
        return { message: result.message || "ok", data: result };
    } catch (error) {
        console.error("Error:", error);
        throw error;
    }
}

export async function api_update_power(p_id, p_power, p_unit) {
    try {
        const response = await fetch('/api/element/power', {
            method: 'PUT',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                p_id,
                p_power,
                p_unit,
            })
        });

        if (!response.ok) {
            const errorResult = await response.json();
            const errorMsg = errorResult.detail || `HTTP error! status: ${response.status}`;
            throw new Error(errorMsg);
        }

        const result = await response.json();
        return { message: result.message || "ok", data: result };
    } catch (error) {
        console.error("Error:", error);
        throw error;
    }
}

export async function api_delete_power(p_id) {
    try {
        const response = await fetch(`/api/element/power`, {
            method: 'DELETE',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ p_id })
        });

        const result = await response.json();

        if (!response.ok) {
            const errorMsg = result.detail || `HTTP error! status: ${response.status}`;
            throw new Error(errorMsg);
        }
        
        return { message: result.message || "ok", data: result };
    } catch (error) {
        console.error("Error:", error);
        throw error;
    }
}

export async function api_delete_item(i_id) {
    try {
        const response = await fetch(`/api/element/item`, {
            method: 'DELETE',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ i_id })
        });

        const result = await response.json();

        if (!response.ok) {
            const errorMsg = result.detail || `HTTP error! status: ${response.status}`;
            throw new Error(errorMsg);
        }
        
        return { message: result.message || "ok", data: result };
    } catch (error) {
        console.error("Error:", error);
        throw error;
    }
}

export async function api_update_item(i_id, i_item, i_corrective) {
    try {
        const response = await fetch('/api/element/item', {
            method: 'PUT',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                i_id,
                i_item,
                i_corrective,
            })
        });

        if (!response.ok) {
            const errorResult = await response.json();
            const errorMsg = errorResult.detail || `HTTP error! status: ${response.status}`;
            throw new Error(errorMsg);
        }

        const result = await response.json();
        return { message: result.message || "ok", data: result };
    } catch (error) {
        console.error("Error:", error);
        throw error;
    }
}

export async function api_delete_order(o_id) {
    console.log(o_id)
    try {
        const response = await fetch(`/api/order/order`, {
            method: 'DELETE',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ o_id })
        });

        const result = await response.json();

        if (!response.ok) {
            const errorMsg = result.detail || `HTTP error! status: ${response.status}`;
            throw new Error(errorMsg);
        }
        
        return { message: result.message || "ok", data: result };
    } catch (error) {
        console.error("Error:", error);
        throw error;
    }
}

export async function api_download_file(filename) {
    try {
        const response = await fetch(`/api/media/${encodeURIComponent(filename)}`, {
            method: 'GET',
            headers: {
                'Accept': 'application/octet-stream'
            }
        });

        if (!response.ok) {
            const result = await response.json();
            const errorMsg = result.detail || `HTTP error! status: ${response.status}`;
            throw new Error(errorMsg);
        }
        const file_blob = await response.blob();
        return { message: "ok", data: file_blob };
    } catch (error) {
        console.error("Error:", error);
        throw error;
    }
}

export async function api_delete_file(filename) {
    try {
        const response = await fetch(`/api/media/${encodeURIComponent(filename)}`, {
            method: 'DELETE',
            headers: {
                'Accept': 'application/json'
            }
        });

        const result = await response.json();

        if (!response.ok) {
            const errorMsg = result.detail || `HTTP error! status: ${response.status}`;
            throw new Error(errorMsg);
        }
        
        return { message: result.message || "ok", data: result };
    } catch (error) {
        console.error("Error:", error);
        throw error;
    }
}

export async function api_get_all_file_name() {
    try {
        const response = await fetch('/api/media', {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        });
        const result = await response.json();

        if (!response.ok) {
            const errorMsg = result.detail || `HTTP error! status: ${response.status}`;
            throw new Error(errorMsg);
        }
        
        return { message: result.message || "ok", data: result };
    } catch (error) {
        console.error("Error:", error);
        throw error;
    }
}

export async function api_upload_file(selected_file) {
    const formData = new FormData();
    formData.append("file", selected_file);

    try {
        const response = await fetch('/api/media', {
            method: 'POST',
            headers: {
                'Accept': 'application/json'
            },
            body: formData
        });

        if (!response.ok) {
            const errorResult = await response.json();
            const errorMsg = errorResult.detail || `HTTP error! status: ${response.status}`;
            throw new Error(errorMsg);
        }

        const result = await response.json();
        return { message: result.message || "ok", data: result };
    } catch (error) {
        console.error("Error:", error);
        throw error;
    }
}

export async function api_create_order_form() {
    try {
        const response = await fetch('/api/media/create_order_file', {
            method: 'POST',
            headers: {
                'Accept': 'application/json'
            }
        });

        if (!response.ok) {
            const errorResult = await response.json();
            const errorMsg = errorResult.detail || `HTTP error! status: ${response.status}`;
            throw new Error(errorMsg);
        }

        const result = await response.json();
        return { message: result.message || "ok", data: result };
    } catch (error) {
        console.error("Error:", error);
        throw error;
    }
}

export async function api_get_user_role_enum() {
    try {
        const response = await fetch('/api/account/role', {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        });
        const result = await response.json();

        if (!response.ok) {
            const errorMsg = result.detail || `HTTP error! status: ${response.status}`;
            throw new Error(errorMsg);
        }
        
        return { message: result.message || "ok", data: result };
    } catch (error) {
        console.error("Error:", error);
        throw error;
    }
}

export async function api_get_user_status_enum() {
    try {
        const response = await fetch('/api/account/status', {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        });
        const result = await response.json();

        if (!response.ok) {
            const errorMsg = result.detail || `HTTP error! status: ${response.status}`;
            throw new Error(errorMsg);
        }
        
        return { message: result.message || "ok", data: result };
    } catch (error) {
        console.error("Error:", error);
        throw error;
    }
}

export async function api_create_account(u_role) {
    console.log(u_role)
    try {
        const response = await fetch('/api/account/create', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ u_role })
        });

        if (!response.ok) {
            const errorResult = await response.json();
            const errorMsg = errorResult.detail || `HTTP error! status: ${response.status}`;
            throw new Error(errorMsg);
        }

        const result = await response.json();
        return { message: result.message || "ok", data: result };
    } catch (error) {
        console.error("Error:", error);
        throw error;
    }
}

export async function api_get_all_users() {
    try {
        const response = await fetch('/api/account/user', {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        });
        const result = await response.json();

        if (!response.ok) {
            const errorMsg = result.detail || `HTTP error! status: ${response.status}`;
            throw new Error(errorMsg);
        }
        
        return { message: result.message || "ok", data: result };
    } catch (error) {
        console.error("Error:", error);
        throw error;
    }
}

export async function api_update_account(u_id, u_name, u_email, u_role, u_status) {
    try {
        const response = await fetch('/api/account/user', {
            method: 'PUT',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                u_id,
                u_name,
                u_email,
                u_role,
                u_status
            })
        });

        if (!response.ok) {
            const errorResult = await response.json();
            const errorMsg = errorResult.detail || `HTTP error! status: ${response.status}`;
            throw new Error(errorMsg);
        }

        const result = await response.json();
        return { message: result.message || "ok", data: result };
    } catch (error) {
        console.error("Error:", error);
        throw error;
    }
}

export async function api_delete_account(u_id) {
    try {
        const response = await fetch(`/api/account/user`, {
            method: 'DELETE',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ u_id })
        });

        const result = await response.json();

        if (!response.ok) {
            const errorMsg = result.detail || `HTTP error! status: ${response.status}`;
            throw new Error(errorMsg);
        }
        
        return { message: result.message || "ok", data: result };
    } catch (error) {
        console.error("Error:", error);
        throw error;
    }
}

export async function api_create_tables() {
    try {
        const response = await fetch('/api/workbench/create_tables', {
            method: 'POST',
            headers: {
                'Accept': 'application/json'
            }
        });

        if (!response.ok) {
            const errorResult = await response.json();
            const errorMsg = errorResult.detail || `HTTP error! status: ${response.status}`;
            throw new Error(errorMsg);
        }

        const result = await response.json();
        return { message: result.message || "ok", data: result };
    } catch (error) {
        console.error("Error:", error);
        throw error;
    }
}