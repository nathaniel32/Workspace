import { api_get_all_specs, api_get_all_orders, api_input_order, api_input_order_article, get_order_articles_with_specs } from '../api.js'; //api_input_order
import { format_price } from '../utils.js';

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
    computed: {
        corrective_spec_count() {
            return this.spec_list.filter(spec => spec.s_corrective === true).length;
        },
        combined_specs() {
            return [
                ...this.f_spec_list_corrective_filter(false),
                ...this.f_spec_list_corrective_filter(true)
            ];
        }
    },
    methods: {
        f_spec_list_corrective_filter(is_corrective) {
            return this.spec_list.filter(spec => spec.s_corrective === is_corrective);
        },
        f_get_order_article_spec_price(specs, s_id) {
            const spec = specs.find(s => s.s_id === s_id);
            return spec ? format_price(spec.os_price) : '-';
        },
        f_get_order_article_spec_description(specs, s_id) {
            const spec = specs.find(s => s.s_id === s_id);
            return spec?.price_list.pl_description || '-';
        },
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
        async f_get_order_articles_with_specs(o_id) {
            const res_order = await get_order_articles_with_specs(o_id);
            this.order_article_list = res_order.data;
        },
        f_sum_order_article(specs) {
            const row_price = specs.reduce((sum, item) => sum + parseFloat(item.os_price), 0);
            return format_price(row_price.toFixed(2));
        },
        f_sum_order(order_articles) {
            const total_price = order_articles.reduce((sumOrder, item) => {
                const specsSum = item.specs.reduce((sumSpecs, spec) => {
                    const osPrice = parseFloat(spec.os_price) || 0;
                    //const plPrice = parseFloat(spec.price_list.pl_price) || 0;
                    return sumSpecs + osPrice;
                }, 0);
                return sumOrder + specsSum;
            }, 0);
            return format_price(total_price.toFixed(2));
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
                        <table border="1" cellpadding="5" cellspacing="0">
                            <thead>
                                <tr>
                                    <th rowspan="2">No</th>
                                    <th rowspan="2">Motor KW</th>
                                    <th rowspan="2" v-for="spec in f_spec_list_corrective_filter(false)" :key="spec.s_id">{{ spec.s_spec || '(empty)' }}</th>
                                    <th :colspan="corrective_spec_count">Corrective Price</th>
                                    <th rowspan="2">Summe</th>
                                </tr>
                                <tr>
                                    <th v-for="spec in f_spec_list_corrective_filter(true)" :key="spec.s_id">{{ spec.s_spec || '(empty)' }}</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(item, index) in order_article_list" :key="item.oa_id">
                                    <td>{{ item.oa_description }}</td>
                                    <td>{{ item.oa_power }}</td>
                                    <td v-for="spec in combined_specs" :key="spec.s_id">
                                        <strong>{{ f_get_order_article_spec_price(item.specs, spec.s_id) }}</strong><br>
                                        <small>{{ f_get_order_article_spec_description(item.specs, spec.s_id) }}</small>
                                    </td>
                                    <td>
                                        <strong>{{ f_sum_order_article(item.specs) }}</strong>
                                    </td>
                                    <button>Delete</Button>
                                </tr>
                                <tr>
                                    <td :colspan="combined_specs.length + 2">Total</td>
                                    <td>{{ f_sum_order(order_article_list) }}</td>
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
        async f_input_order() {
            const res = await api_input_order(this.input_order_description);
            base_vue.f_info(res.message);
            this.f_get_order_list();
        },
        async f_input_order_article() {
            const res = await api_input_order_article(this.selected_order_id, this.input_order_article_power, this.input_order_article_description, this.input_order_article_id_specs);
            base_vue.f_info(res.message);
        }
    }
});

dashboard_user_price_list.f_init();