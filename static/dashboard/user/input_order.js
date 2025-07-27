import { api_get_all_spec } from '../api.js'; //api_input_order

const dashboard_user_price_list = new Vue({
    data: {
        spec_list: [],
        input_power: null,
        selected_specs: []
    },
    methods: {
        async f_init() {
            dashboard_main.navigations.push({ name: "Input Order", callback: this.f_template });
            const res = await api_get_all_spec();
            this.spec_list = res.data;
        },
        f_template() {
            dashboard_main.content.title = 'Input Order';
            dashboard_main.content.template = `
                <div>
                    <br>
                    Order ID:
                    <br>
                    Client Name:
                    <br>
                    <br>
                    <div>
                        <label>Power</label>
                        <input type="number" v-model="input_power">
                        
                        <div v-for="spec in spec_list" :key="spec.s_id">
                            <label>
                                <input type="checkbox" :value="spec.s_id" v-model="selected_specs">
                                {{ spec.s_spec || '(empty)' }}
                            </label>
                        </div>

                        <button @click="f_input_order">Submit</button>
                    </div>
                </div>
            `;
            dashboard_main.content.data = this;
        },
        async f_input_order() {
            const payload = {
                power: this.input_power,
                specs: this.selected_specs
            };
            console.log(payload)
            //await api_input_order(payload);
        }
    }
});

dashboard_user_price_list.f_init();