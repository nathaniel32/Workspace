import { api_get_all_price_list, get_unique_sorted_specs, get_unique_sorted_powers, get_price_list_item } from './utils.js';

const dashboard_user = new Vue({
    //el: '#dashboard_user',
    data: {
        price_list: []
    },
    computed: {
        table_specs() {
            return get_unique_sorted_specs(this.price_list);
        },
        table_powers() {
            return get_unique_sorted_powers(this.price_list);
        }
    },
    methods:{
        f_init(){
            dashboard_main.navigations.push({name: "Price List", callback: this.f_price_list});
        },
        f_price_list(){
            dashboard_main.content.title = 'Price List';
            dashboard_main.content.template = `
                <div>
                    <table border="1" cellpadding="5" cellspacing="0">
                        <thead>
                            <tr>
                                <th>Power \ Spec</th>
                                <th v-for="spec in table_specs" :key="spec.s_id">{{ spec.spec || '(empty)' }}</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="power in table_powers" :key="power.p_id">
                                <td>{{ power.power }}</td>
                                <td v-for="spec in table_specs" :key="spec.s_id">
                                    {{ f_table_get_price(power.p_id, spec.s_id) }}
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            `;
            dashboard_main.content.data = this;
            this.f_get_all_price_list();
        },
        f_table_get_price(power_id, spec_id) {
            return get_price_list_item(this.price_list, power_id, spec_id, 'price');
        },
        //GET ALL PRICE
        async f_get_all_price_list(){
            const res = await api_get_all_price_list();
            this.price_list = res.data;
        },
    }
});

dashboard_user.f_init();