import { get_price_list_item, format_price, beautify_format_price, deformat_price } from '../utils.js';
import { api_get_all_price_list, api_get_all_powers, api_get_all_specs, api_input_power, api_input_spec, api_update_price } from '../api.js';

const dashboard_admin_control_panel = new Vue({
    data: {
        title: 'Control Panel',
        input_power: 0,
        input_spec: '',
        input_spec_corrective: true,
        price_list: [],
        power_list: [],
        spec_list: [],
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
    methods:{
        f_spec_list_corrective_filter(is_corrective) {
            return this.spec_list.filter(spec => spec.s_corrective === is_corrective);
        },
        //mendapatkan harga setiap cell
        f_table_get_price(power_id, spec_id) {
            return format_price(get_price_list_item(this.price_list, power_id, spec_id, 'pl_price'));
        },
        //mendapatkan deskripsi setiap cell
        f_table_get_price_description(power_id, spec_id) {
            return get_price_list_item(this.price_list, power_id, spec_id, 'pl_description');
        },
        f_get_power_range(power_start, power_end) {
            if (power_end) {
                return `${power_start.p_power} - ${power_end.p_power - 1}`;
            } else {
                return `> ${power_start.p_power}`;
            }
        },
        f_init(){
            dashboard_main.navigations.push({name: this.title, callback: this.f_template});
        },

        //DISPLAY CP
        async f_template(){
            const template = `
                <div class="space-y-6">
                    <div class="overflow-x-auto relative shadow-md sm:rounded-lg">
                        <table class="w-full text-sm text-left text-gray-500">
                            <thead class="text-xs text-gray-700 uppercase bg-gray-50">
                                <tr>
                                    <th rowspan="2" class="py-3 px-6">Power</th>
                                    <th rowspan="2" class="py-3 px-6">Number of unit</th>
                                    <th rowspan="2" v-for="spec in f_spec_list_corrective_filter(false)" :key="spec.s_id" class="py-3 px-6">{{ spec.s_spec || '(empty)' }}</th>
                                    <th :colspan="corrective_spec_count" class="py-3 px-6 text-center">Corrective Price</th>
                                </tr>
                                <tr>
                                    <th v-for="spec in f_spec_list_corrective_filter(true)" :key="spec.s_id" class="py-3 px-6">{{ spec.s_spec || '(empty)' }}</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(power, index) in power_list" :key="power.p_id" class="bg-white hover:bg-gray-50">
                                    <td class="py-4 px-6 font-medium text-gray-900 whitespace-nowrap">{{ f_get_power_range(power, power_list[index + 1]) }}</td>
                                    <td class="py-4 px-6">{{ power.p_unit }}</td>
                                    <td v-for="spec in combined_specs" :key="spec.s_id" @click="f_show_price_popup(power.p_id, spec.s_id, f_get_power_range(power, power_list[index + 1]), spec.s_spec)" class="py-4 px-6 cursor-pointer text-blue-600 hover:underline">
                                        <div>
                                            <strong>{{ f_table_get_price(power.p_id, spec.s_id) }}</strong><br>
                                            <small class="text-gray-500">{{ f_table_get_price_description(power.p_id, spec.s_id) }}</small>
                                        </div>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div class="bg-white p-4 rounded-lg shadow-md">
                            <h3 class="text-lg font-semibold mb-2">Add Power</h3>
                            <div class="flex items-center gap-2">
                                <input v-model="input_power" type="number" placeholder="power" class="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500" />
                                <button @click="f_input_power" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition duration-300 ease-in-out"><i class="fas fa-plus"></i></button>
                            </div>
                        </div>
                        <div class="bg-white p-4 rounded-lg shadow-md">
                            <h3 class="text-lg font-semibold mb-2">Add Spec</h3>
                            <div class="flex items-center gap-2">
                                <input v-model="input_spec" type="text" placeholder="Spec" class="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500" />
                                <div class="flex items-center">
                                    <input v-model="input_spec_corrective" type="checkbox" class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"/>
                                    <label class="ml-2 text-sm text-gray-900">Corrective</label>
                                </div>
                                <button @click="f_input_spec" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition duration-300 ease-in-out"><i class="fas fa-plus"></i></button>
                            </div>
                        </div>
                    </div>

                    <!-- Popup -->
                    <div v-if="update_price.show_popup" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full flex items-center justify-center">
                        <div class="relative mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
                            <div class="mt-3 text-center">
                                <h3 class="text-lg leading-6 font-medium text-gray-900">Edit Harga</h3>
                                <div class="mt-2 px-7 py-3 space-y-4 text-left">
                                    <p><span class="font-semibold">Power:</span> {{ update_price.selected_power }}</p>
                                    <p><span class="font-semibold">Spec:</span> {{ update_price.selected_spec }}</p>
                                    <div>
                                        <label class="block text-sm font-medium text-gray-700">Price</label>
                                        <input v-model="update_price.new_price" type="text" @input="format_price_input" placeholder="New Price" class="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-500" />
                                    </div>
                                    <div>
                                        <label class="block text-sm font-medium text-gray-700">Description</label>
                                        <input v-model="update_price.new_description" type="text" placeholder="Description" class="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500" />
                                    </div>
                                </div>
                                <div class="items-center px-4 py-3">
                                    <button @click="f_update_price" class="px-4 py-2 bg-green-500 text-white text-base font-medium rounded-md w-auto shadow-sm hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-300">Update</button>
                                    <button @click="update_price.show_popup = false" class="ml-2 px-4 py-2 bg-gray-500 text-white text-base font-medium rounded-md w-auto shadow-sm hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-300">Cancel</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `;

            if (dashboard_main.content.template != template){
                dashboard_main.content.template = template;
                dashboard_main.content.title = this.title;
                dashboard_main.content.data = this;
                this.f_get_all_price_list();
                this.f_get_all_powers();
                this.f_get_all_specs();
            }else{
                dashboard_main.f_reset();
            }
        },

        //GET ALL PRICE
        async f_get_all_price_list(){
            const res = await api_get_all_price_list();
            this.price_list = res.data;
            if (!res.success) {
                base_vue.f_info(res.message);
            }
        },

        //GET ALL POWERS
        async f_get_all_powers(){
            const res = await api_get_all_powers();
            this.power_list = res.data;
            if (!res.success) {
                base_vue.f_info(res.message);
            }
        },

        //GET ALL SPECS
        async f_get_all_specs(){
            const res = await api_get_all_specs();
            this.spec_list = res.data;
            if (!res.success) {
                base_vue.f_info(res.message);
            }
        },

        //INPUT POWER
        async f_input_power(){
            const res = await api_input_power(this.input_power);
            base_vue.f_info(res.message);
            if (res.success) {
                this.f_get_all_powers();
                this.f_get_all_price_list();
            }
        },

        //INPUT SPEC
        async f_input_spec(){
            const res = await api_input_spec(this.input_spec, this.input_spec_corrective);
            base_vue.f_info(res.message);
            if (res.success) {
                this.f_get_all_specs();
                this.f_get_all_price_list();
            }
        },

        f_show_price_popup(power_id, spec_id, power_range, spec) {
            const res = get_price_list_item(this.price_list, power_id, spec_id);
            this.update_price.selected_power_id = power_id;
            this.update_price.selected_spec_id = spec_id;
            this.update_price.new_description = res.pl_description;
            this.update_price.selected_power = power_range;
            this.update_price.selected_spec = spec;
            this.update_price.new_price = format_price(res.pl_price);
            this.update_price.show_popup = true;
        },
        async f_update_price() {
            //let price_string = this.update_price.new_price.replace(/\D/g, ''); // hanya angka
            let price_string = deformat_price(this.update_price.new_price);
            let price = Number(price_string);
            const res = await api_update_price(this.update_price.selected_power_id, this.update_price.selected_spec_id, this.update_price.new_description, Number(price));
            this.f_get_all_price_list();
            this.update_price.show_popup = false;
            base_vue.f_info(res.message);
        },

        format_price_input(e) {
            this.update_price.new_price = beautify_format_price(e.target.value);
        }
    }
});

dashboard_admin_control_panel.f_init();