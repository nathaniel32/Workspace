import { get_unique_sorted_specs, get_unique_sorted_powers, get_price_list_item, format_price, beautify_format_price, deformat_price } from '../utils.js';
import { api_get_all_price_list, api_input_power, api_input_spec, api_update_price } from '../api.js';

const dashboard_admin_control_panel = new Vue({
    data: {
        input_power: 0,
        input_spec: '',
        input_spec_corrective: true,
        price_list: [],

        update_price: {
            show_popup: false,
            selected_power_id: null,
            selected_spec_id: null,
            selected_power: null,
            selected_spec: null,
            new_description: null,
            new_price: ''
        }
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
        //mendapatkan harga setiap cell
        f_table_get_price(power_id, spec_id) {
            return format_price(get_price_list_item(this.price_list, power_id, spec_id, 'price'));
        },
        //mendapatkan deskripsi setiap cell
        f_table_get_price_description(power_id, spec_id) {
            return get_price_list_item(this.price_list, power_id, spec_id, 'description');
        },
        f_init(){
            dashboard_main.navigations.push({name: "Control Panel", callback: this.f_template});
        },

        //DISPLAY CP
        async f_template(){
            dashboard_main.content.title = 'Control Panel';
            dashboard_main.content.template = `
                <div>
                    <table border="1" cellpadding="5" cellspacing="0">
                        <thead>
                            <tr>
                                <th>Power \\ Spec</th>
                                <th v-for="spec in table_specs" :key="spec.s_id">{{ spec.spec || '(empty)' }}</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(power, index) in table_powers" :key="power.p_id">
                                <td>
                                    {{ power.power }}
                                    <span v-if="table_powers[index + 1]">
                                        - {{ table_powers[index + 1].power - 1 }}
                                    </span>
                                    <span v-else>
                                        =<
                                    </span>
                                </td>
                                <td v-for="spec in table_specs" :key="spec.s_id" @click="f_show_price_popup(power.p_id, spec.s_id)" style="cursor:pointer; color:blue;">
                                    <div>
                                        <strong>{{ f_table_get_price(power.p_id, spec.s_id) }}</strong><br>
                                        <small>{{ f_table_get_price_description(power.p_id, spec.s_id) }}</small>
                                    </div>
                                </td>
                            </tr>
                        </tbody>
                    </table>

                    <input v-model="input_power" type="number" placeholder="power" />
                    <button @click="f_input_power">Add Power</button>
                    <br>
                    <input v-model="input_spec" type="text" placeholder="Spec" />
                    {{ input_spec_corrective }}
                    <input v-model="input_spec_corrective" type="checkbox"/>
                    <button @click="f_input_spec">Add Spec</button>

                    <!-- Popup -->
                    <div v-if="update_price.show_popup" style="position:fixed; top:30%; left:30%; background:#fff; padding:20px; border:1px solid #000;">
                        <h3>Edit Harga</h3>
                        <p>Power: {{ update_price.selected_power }}</p>
                        <p>Spec: {{ update_price.selected_spec }}</p>
                        Description
                        <input v-model="update_price.new_description" type="text" placeholder="Description" />
                        <br>
                        Price
                        <input v-model="update_price.new_price" type="text" @input="format_price_input" placeholder="New Price" />
                        <br><br>
                        <button @click="f_update_price">Update</button>
                        <button @click="update_price.show_popup = false">Cancel</button>
                    </div>
                </div>
            `;
            dashboard_main.content.data = this;
            this.f_get_all_price_list();
        },

        //GET ALL PRICE
        async f_get_all_price_list(){
            const res = await api_get_all_price_list();
            this.price_list = res.data;
            console.log(this.price_list)
        },

        //INPUT POWER
        async f_input_power(){
            const res = await api_input_power(this.input_power);
            base_vue.f_info(res.message);
            if (res.success) this.f_get_all_price_list();
        },

        //INPUT SPEC
        async f_input_spec(){
            const res = await api_input_spec(this.input_spec, this.input_spec_corrective);
            base_vue.f_info(res.message);
            if (res.success) this.f_get_all_price_list();
        },

        f_show_price_popup(power_id, spec_id) {
            const res = get_price_list_item(this.price_list, power_id, spec_id);
            this.update_price.selected_power_id = power_id;
            this.update_price.selected_spec_id = spec_id;
            this.update_price.new_description = res.description;
            this.update_price.selected_power = res.power;
            this.update_price.selected_spec = res.spec;
            this.update_price.new_price = format_price(res.price);
            this.update_price.show_popup = true;
        },
        async f_update_price() {
            //let price_string = this.update_price.new_price.replace(/\D/g, ''); // hanya angka
            let price_string = deformat_price(this.update_price.new_price);
            let price = Number(price_string);
            const res = await api_update_price(this.update_price.selected_power_id, this.update_price.selected_spec_id, this.update_price.new_description, Number(price));
            this.f_get_all_price_list();
            this.update_price.show_popup = false;
            console.log(res);
            base_vue.f_info(res.message);
        },

        format_price_input(e) {
            this.update_price.new_price = beautify_format_price(e.target.value);
        }
    }
});

dashboard_admin_control_panel.f_init();