import { get_price_list_item, format_price } from '../utils.js';
import { api_get_all_powers, api_get_all_specs, api_get_all_price_list } from '../api.js';

const dashboard_user_price_list = new Vue({
    data: {
        price_list: [],
        power_list: [],
        spec_list: [],
    },
    methods:{
        //GET ALL PRICE
        async f_get_all_price_list(){
            const res = await api_get_all_price_list();
            this.price_list = res.data;
        },

        //GET ALL POWERS
        async f_get_all_powers(){
            const res = await api_get_all_powers();
            this.power_list = res.data;
        },

        //GET ALL SPECS
        async f_get_all_specs(){
            const res = await api_get_all_specs();
            this.spec_list = res.data;
            console.log(this.spec_list)
        },
        f_table_get_price(power_id, spec_id) {
            return format_price(get_price_list_item(this.price_list, power_id, spec_id, 'pl_price'));
        },
        f_table_get_price_description(power_id, spec_id) {
            return get_price_list_item(this.price_list, power_id, spec_id, 'pl_description');
        },
        f_init(){
            dashboard_main.navigations.push({name: "Price List", callback: this.f_template});
        },
        f_template(){
            dashboard_main.content.title = 'Price List';
            dashboard_main.content.template = `
                <div>
                    <table border="1" cellpadding="5" cellspacing="0">
                        <thead>
                            <tr>
                                <th>Power \\ Spec</th>
                                <th v-for="spec in spec_list" :key="spec.s_id">{{ spec.s_spec || '(empty)' }}</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(power, index) in power_list" :key="power.p_id">
                                <td>
                                    {{ power.p_power }}
                                    <span v-if="power_list[index + 1]">
                                        - {{ power_list[index + 1].p_power - 1 }}
                                    </span>
                                    <span v-else>
                                        =<
                                    </span>
                                </td>
                                <td v-for="spec in spec_list" :key="spec.s_id">
                                    <div>
                                        <strong>{{ f_table_get_price(power.p_id, spec.s_id) }}</strong><br>
                                        <small>{{ f_table_get_price_description(power.p_id, spec.s_id) }}</small>
                                    </div>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            `;
            dashboard_main.content.data = this;
            this.f_get_all_price_list();
            this.f_get_all_powers();
            this.f_get_all_specs();
        }
    }
});

dashboard_user_price_list.f_init();