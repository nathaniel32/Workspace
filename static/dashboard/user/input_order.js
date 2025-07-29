import { api_get_all_specs, api_get_all_orders, api_input_order, api_input_order_article, get_order_articles_with_specs } from '../api.js'; //api_input_order

const dashboard_user_price_list = new Vue({
    data: {
        spec_list: [],
        order_list: [],
        order_article_list: [],
        input_order_description: null,
        selected_order_id: null,
        input_order_article_power: null,
        input_order_article_description: null,
        input_order_article_id_specs: []
    },
    methods: {
        async f_init() {
            dashboard_main.navigations.push({ name: "Manage Order", callback: this.f_template });
            const res_spec = await api_get_all_specs();
            this.spec_list = res_spec.data;
            this.f_get_order_list();
            console.log(this.spec_list)
        },
        async f_get_order_list() {
            const res_order = await api_get_all_orders();
            this.order_list = res_order.data;
        },
        async f_get_order_articles_with_specs(o_id) {
            console.log(o_id);
            const res_order = await get_order_articles_with_specs(o_id);
            this.order_article_list = res_order.data;
            console.log(this.order_article_list);
        },
        f_template() {
            dashboard_main.content.title = 'Manage Order';
            dashboard_main.content.template = `
                <div>
                    <div style="border:1px solid black">
                        Order
                        <ul v-for="order in order_list" :key="order.o_id">
                            <li @click="f_get_order_articles_with_specs(order.o_id)">{{ order.o_description }} - {{ order.o_id }}</li>
                        </ul>
                        <input type="text" v-model="input_order_description">
                        <button @click="f_input_order">Add New Order</button>
                    </div>
                    <div style="border:1px solid black">
                        <table>
                            <thead>
                                <tr>
                                    <th>Artikel</th>
                                    <th v-for="spec in spec_list" :key="spec.s_id">{{ spec.s_spec }}</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(item, index) in order_article_list" :key="item.oa_id">
                                    <td>{{ item.oa_description }}</td>
                                    <td v-for="spec in spec_list" :key="spec.s_id">
                                        {{ f_get_order_article_spec_price(item.specs, spec.s_id) }}
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        Order ID <input type="text" v-model="selected_order_id">
                        <br>
                        Order Description <input type="text" v-model="input_order_article_description">
                        <br>
                        <label>Power</label>
                        <input type="number" v-model="input_order_article_power">
                        
                        <div v-for="spec in spec_list" :key="spec.s_id">
                            <label>
                                <input type="checkbox" :value="spec.s_id" v-model="input_order_article_id_specs">
                                {{ spec.s_spec || '(empty)' }}
                            </label>
                        </div>

                        <button @click="f_input_order_article">Submit Article</button>
                    </div>
                </div>
            `;
            dashboard_main.content.data = this;
        },
        f_get_order_article_spec_price(specs, s_id) {
            const spec = specs.find(s => s.s_id === s_id);
            return spec ? Number(spec.os_price).toLocaleString() : '-';
        },
        async f_input_order() {
            const res = await api_input_order(this.input_order_description);
            console.log(res);
            base_vue.f_info(res.message);
            this.f_get_order_list();
        },
        async f_input_order_article() {
            const res = await api_input_order_article(this.selected_order_id, this.input_order_article_power, this.input_order_article_description, this.input_order_article_id_specs);
            console.log(res);
            base_vue.f_info(res.message);
        }
    }
});

dashboard_user_price_list.f_init();