import { api_get_all_specs, api_get_all_orders, api_input_order } from '../api.js'; //api_input_order

const dashboard_user_price_list = new Vue({
    data: {
        order_list: [],
        input_order_description: null,
        spec_list: [],
        input_order_artikel_power: null,
        input_order_artikel_specs: []
    },
    methods: {
        async f_init() {
            dashboard_main.navigations.push({ name: "Manage Order", callback: this.f_template });
            const res_spec = await api_get_all_specs();
            this.spec_list = res_spec.data;
            this.f_get_order_list();
        },
        async f_get_order_list() {
            const res_order = await api_get_all_orders();
            this.order_list = res_order.data;
        },
        f_template() {
            dashboard_main.content.title = 'Manage Order';
            dashboard_main.content.template = `
                <div>
                    <div style="border:1px solid black">
                        Order
                        <ul v-for="order in order_list" :key="order.o_id">
                            <li>{{ order.o_description }}</li>
                        </ul>
                        <input type="text" v-model="input_order_description">
                        <button @click="f_input_order">Add New Order</button>
                    </div>
                    <div style="border:1px solid black">
                        <br>
                        * Mesin 1
                        <br>
                        * Mesin 1
                        <br>
                        Order ID = JWIJD3
                        <br>
                        <label>Power</label>
                        <input type="number" v-model="input_order_artikel_power">
                        
                        <div v-for="spec in spec_list" :key="spec.s_id">
                            <label>
                                <input type="checkbox" :value="spec.s_id" v-model="input_order_artikel_specs">
                                {{ spec.s_spec || '(empty)' }}
                            </label>
                        </div>

                        <button @click="f_input_order_artikel">Submit Artikel</button>
                    </div>
                </div>
            `;
            dashboard_main.content.data = this;
        },
        async f_input_order() {
            const res = await api_input_order(this.input_order_description);
            console.log(res);
            base_vue.f_info(res.message);
            this.f_get_order_list();
        },
        async f_input_order_artikel() {
            const payload = {
                power: this.input_order_artikel_power,
                specs: this.input_order_artikel_specs
            };
            console.log(payload)
            //await api_input_order(payload);
        }
    }
});

dashboard_user_price_list.f_init();