import { api_update_order, api_get_enum_order_status, api_delete_order_article, api_get_all_specs, api_get_all_orders, api_input_order, api_input_order_article, get_order_articles_with_specs } from '../api.js'; //api_input_order
import { format_price } from '../utils.js';

const order_management = new Vue({
    data: {
        title: 'Order Management',
        enum_status_list: [],
        spec_list: [],
        order_list: [],
        order_article_list: [],
        input_order_description: null,
        selected_order_object: null,
        input_order_article_power: null,
        input_order_article_description: null,
        input_order_article_id_specs: [],
        active_status_group: null,
        month_names: ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"],
        change_order_tmp: {
            status: null,
            description: null
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
        },
        grouped_orders() {
            return this.order_list.reduce((acc, order) => {
                const status = order.o_status || 'Uncategorized';
                if (!acc[status]) {
                    acc[status] = [];
                }
                acc[status].push(order);
                return acc;
            }, {});
        }
    },
    methods: {
        /* search_order_by_id(id) {
            return this.order_list.find(item => item.o_id === id);
        }, */
        f_time_converter(unix) {
            const date = new Date(unix * 1000);
            const hours = date.getHours();
            const minutes = date.getMinutes();
            const day = date.getDate();
            const month = date.getMonth();
            const year = date.getFullYear();
            return ` ${hours}:${minutes < 10 ? '0' + minutes : minutes} - ${day} ${this.month_names[month]} ${year}`
        },
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
            dashboard_main.navigations.push({ name: this.title, callback: this.f_template });
            try {
                const res = await api_get_all_specs();
                this.spec_list = res.data;
            } catch (err) {
                base_vue.f_info(err.message, undefined, true);
            }

            try {
                const res = await api_get_enum_order_status();
                this.enum_status_list = res.data;
            } catch (err) {
                base_vue.f_info(err.message, undefined, true);
            }

            this.f_get_order_list();
        },
        async f_get_order_list() {
            try {
                const res = await api_get_all_orders();
                this.order_list = res.data;
            } catch (err) {
                base_vue.f_info(err.message, undefined, true);
            }
        },
        async f_get_order_articles_with_specs(order_object=null) {
            if(order_object){
                if (JSON.stringify(this.selected_order_object) == JSON.stringify(order_object)){
                    this.selected_order_object = null;
                    this.order_article_list = [];
                    return;
                }
                console.log(order_object, this.selected_order_object)
            }else{
                order_object = this.selected_order_object;
            }

            try {
                const res = await get_order_articles_with_specs(order_object.o_id);
                if (res.data) {
                    this.order_article_list = res.data;
                }else{
                    base_vue.f_info("No article found");
                    this.order_article_list = [];
                }
                this.selected_order_object = order_object;
                this.change_order_tmp.status = this.selected_order_object.o_status;
                this.change_order_tmp.description = this.selected_order_object.o_description;
            } catch (err) {
                base_vue.f_info(err.message, undefined, true);
            }
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
            const template = `
                <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
                    <div class="lg:col-span-1 bg-white p-4 rounded-lg shadow-md">
                        <h3 class="text-lg font-semibold mb-4">Orders</h3>
                        <div class="space-y-2">
                            <div v-for="(orders, status) in grouped_orders" :key="status">
                                <button @click="active_status_group = active_status_group === status ? null : status" class="w-full text-left font-semibold p-2 rounded-lg hover:bg-gray-200 border flex justify-between items-center">
                                    <span>{{ status }}</span>
                                    <i class="fas" :class="{'fa-chevron-down': active_status_group === status, 'fa-chevron-right': active_status_group !== status}"></i>
                                </button>
                                <div v-if="active_status_group === status" class="pl-4 mt-2 space-y-2">
                                    <div v-for="order in orders" :key="order.o_id" @click="f_get_order_articles_with_specs(order)" class="p-3 rounded-lg cursor-pointer hover:bg-gray-100 border border-gray-200">
                                        <p class="font-semibold text-gray-800">{{ order.o_description }}</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="mt-4">
                            <input type="text" v-model="input_order_description" placeholder="New order description" class="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500">
                            <button @click="f_input_order" class="mt-2 w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition duration-300 ease-in-out"><i class="fas fa-plus mr-2"></i>Add New Order</button>
                        </div>
                    </div>
                    <div v-if="selected_order_object" class="lg:col-span-3 space-y-6">
                        <div class="bg-white p-4 rounded-lg shadow-md">
                            <h3 class="text-lg font-semibold mb-4">Order Details</h3>
                            <div class="overflow-x-auto relative shadow-md sm:rounded-lg">
                                <table v-if="order_article_list.length > 0" class="w-full text-sm text-left text-gray-500">
                                    <thead class="text-xs text-gray-700 uppercase bg-gray-50">
                                        <tr>
                                            <th rowspan="2" class="py-3 px-6">Equipment No</th>
                                            <th rowspan="2" class="py-3 px-6">Motor KW</th>
                                            <th rowspan="2" v-for="spec in f_spec_list_corrective_filter(false)" :key="spec.s_id" class="py-3 px-6">{{ spec.s_spec || '(empty)' }}</th>
                                            <th :colspan="corrective_spec_count" class="py-3 px-6 text-center">Corrective Price</th>
                                            <th rowspan="2" class="py-3 px-6">Summe</th>
                                            <th rowspan="2" class="py-3 px-6">Actions</th>
                                        </tr>
                                        <tr>
                                            <th v-for="spec in f_spec_list_corrective_filter(true)" :key="spec.s_id" class="py-3 px-6">{{ spec.s_spec || '(empty)' }}</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="(item, index) in order_article_list" :key="item.oa_id" class="bg-white hover:bg-gray-50">
                                            <td class="py-4 px-6">{{ item.oa_description }}</td>
                                            <td class="py-4 px-6">{{ item.oa_power }}</td>
                                            <td v-for="spec in combined_specs" :key="spec.s_id" class="py-4 px-6">
                                                <strong>{{ f_get_order_article_spec_price(item.specs, spec.s_id) }}</strong><br>
                                                <small class="text-gray-500">{{ f_get_order_article_spec_description(item.specs, spec.s_id) }}</small>
                                            </td>
                                            <td class="py-4 px-6">
                                                <strong>{{ f_sum_order_article(item.specs) }}</strong>
                                            </td>
                                            <td class="py-4 px-6">
                                                <button @click="f_delete_order_article(item.oa_id)" class="bg-red-500 hover:bg-red-700 text-white font-bold py-1 px-2 rounded text-xs"><i class="fas fa-trash"></i></button>
                                            </td>
                                        </tr>
                                        <tr class="bg-gray-50 font-semibold">
                                            <td :colspan="combined_specs.length + 2" class="py-4 px-6 text-right">Total</td>
                                            <td class="py-4 px-6">{{ f_sum_order(order_article_list) }}</td>
                                            <td></td>
                                        </tr>
                                    </tbody>
                                </table>
                                <div v-else class="p-12 text-center">
                                    <i class="fas fa-search text-4xl text-gray-400"></i>
                                    <p class="text-gray-500 text-sm">No Results</p>
                                </div>
                            </div>
                        </div>
                        <div class="bg-white p-4 rounded-lg shadow-md">
                            <h3 class="text-lg font-semibold mb-2">Information Order</h3>
                            <div class="grid grid-cols-2 gap-2 text-sm text-gray-700 mt-5 mb-5">
                                <div class="font-medium">Deskripsi:</div>
                                <input type="text" v-model="change_order_tmp.description" class="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500">

                                <div class="font-medium">Order ID:</div>
                                <div>{{ selected_order_object.o_id }}</div>

                                <div class="font-medium">Status:</div>
                                <div>
                                    <select v-model="change_order_tmp.status" class="block w-full px-2 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
                                        <option v-for="status in enum_status_list" :key="status.enumlabel" :value="status.enumlabel">
                                            {{ status.enumlabel }}
                                        </option>
                                    </select>
                                </div>

                                <div class="font-medium">Waktu Dibuat:</div>
                                <div>{{ f_time_converter(selected_order_object.o_time) }}</div>

                                <div class="font-medium">User ID:</div>
                                <div>{{ selected_order_object.u_id }}</div>

                                <div></div>
                                <div>
                                    <button v-if="(selected_order_object.o_description != change_order_tmp.description) || (selected_order_object.o_status != change_order_tmp.status)" @click="f_change_order" class="mt-2 w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition duration-300 ease-in-out">Change</button>
                                </div>
                            </div>
                        </div>
                        <div class="bg-white p-4 rounded-lg shadow-md">
                            <h3 class="text-lg font-semibold mb-2">Add Article to Order</h3>
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div>
                                    <label class="block text-sm font-medium text-gray-700">Equipment No</label>
                                    <input type="text" v-model="input_order_article_description" class="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500">
                                </div>
                                <div>
                                    <label class="block text-sm font-medium text-gray-700">Power</label>
                                    <input type="number" v-model="input_order_article_power" class="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500">
                                </div>
                                <div class="md:col-span-2">
                                    <label class="block text-sm font-medium text-gray-700">Specs</label>
                                    <div class="mt-2 grid grid-cols-2 md:grid-cols-4 gap-2">
                                        <div v-for="spec in spec_list" :key="spec.s_id">
                                            <label class="flex items-center">
                                                <input type="checkbox" :value="spec.s_id" v-model="input_order_article_id_specs" class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500">
                                                <span class="ml-2 text-sm text-gray-600">{{ spec.s_spec || '(empty)' }}</span>
                                            </label>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <button @click="f_input_order_article" class="mt-4 w-full bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded transition duration-300 ease-in-out"><i class="fas fa-paper-plane mr-2"></i>Submit Article</button>
                        </div>
                    </div>
                    <div v-else class="p-12 text-center lg:col-span-3 space-y-6">
                        <i class="fas fa-chart-line text-6xl text-gray-300 mb-4"></i>
                        <p class="text-gray-500">Select a navigation order from the sidebar to get started</p>
                    </div>
                </div>
            `;
            if (dashboard_main.content.template != template){
                dashboard_main.content.template = template;
                dashboard_main.content.title = this.title;
                dashboard_main.content.data = this;
            }else{
                dashboard_main.f_reset();
            }
        },
        async f_delete_order_article(oa_id) {
            const confirmed = confirm("Are you sure you want to delete this data?");
            if (!confirmed) return;
            try {
                const res = await api_delete_order_article(oa_id);
                base_vue.f_info(res.message);
                this.f_get_order_articles_with_specs();
            } catch (err) {
                base_vue.f_info(err.message, undefined, true);
            }
        },
        async f_input_order() {
            try{
                const res = await api_input_order(this.input_order_description);
                base_vue.f_info(res.message);
                this.f_get_order_list();
            } catch (err) {
                base_vue.f_info(err.message, undefined, true);
            }
        },
        async f_input_order_article() {
            try{
                const res = await api_input_order_article(this.selected_order_object.o_id, this.input_order_article_power, this.input_order_article_description, this.input_order_article_id_specs);
                this.f_get_order_articles_with_specs();
                base_vue.f_info(res.message);
            } catch (err) {
                base_vue.f_info(err.message, undefined, true);
            }
        },
        async f_change_order(){
            const confirmed = confirm("Are you sure you want to update this data?");
            if (!confirmed) return;
            try{
                const res = await api_update_order(this.selected_order_object.o_id, this.change_order_tmp.description, this.change_order_tmp.status);
                base_vue.f_info(res.message);
                await this.f_get_order_list();
                this.selected_order_object.o_status = this.change_order_tmp.status;
                this.selected_order_object.o_description = this.change_order_tmp.description;
            } catch (err) {
                base_vue.f_info(err.message, undefined, true);
            }
        }
    }
});

order_management.f_init();