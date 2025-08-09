import { api_get_order_by_id, api_upload_order_file, api_delete_order, api_update_order, api_get_enum_order_status, api_delete_order_article, api_get_all_items, api_get_all_orders, api_input_order, api_input_order_article, api_get_order_articles_with_items } from '../api.js'; //api_input_order
import { format_price } from '../utils.js';

const order_manager = new Vue({
    data: {
        title: 'Order Manager',
        enum_status_list: [],
        item_list: [],
        order_list: [],
        order_article_list: [],
        input_order_name: null,
        selected_order_object: null,
        input_order_article_power: null,
        input_order_article_name: null,
        input_order_article_id_items: [],
        active_status_group: null,
        month_names: ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"],
        change_order_tmp: {
            status: null,
            name: null
        },
        upload_order_file: {
            show_popup: false,
            new_file: null
        }
    },
    computed: {
        corrective_item_count() {
            return this.item_list.filter(item => item.i_corrective === true).length;
        },
        combined_items() {
            return [
                ...this.f_item_list_corrective_filter(false),
                ...this.f_item_list_corrective_filter(true)
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
            return this.order_list.find(element => element.o_id === id);
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
        f_item_list_corrective_filter(is_corrective) {
            return this.item_list.filter(item => item.i_corrective === is_corrective);
        },
        f_get_order_article_item_price(items, i_id) {
            const item = items.find(s => s.i_id === i_id);
            return item ? format_price(item.os_price) : '-';
        },
        f_get_order_article_item_name(items, i_id) {
            const item = items.find(s => s.i_id === i_id);
            return item?.price_list.pl_name || '-';
        },
        f_init() { //1x panggil
            dashboard_main.navigations.push({ name: this.title, callback: this.f_template });
            this.f_get_order_status_list();
        },
        async f_get_order_status_list() {
            try {
                const res = await api_get_enum_order_status();
                this.enum_status_list = res.data;
            } catch (err) {
                base_vue.f_info(err.message, undefined, true);
            }
        },
        async f_get_item_list() {
            try {
                const res = await api_get_all_items();
                this.item_list = res.data;
            } catch (err) {
                base_vue.f_info(err.message, undefined, true);
            }
        },
        async f_get_order_list() {
            try {
                const res = await api_get_all_orders();
                this.order_list = res.data;
            } catch (err) {
                base_vue.f_info(err.message, undefined, true);
            }
        },
        async f_get_order_articles_with_items(order_id=null) {
            if(order_id){
                if (this.selected_order_object && this.selected_order_object.o_id == order_id){
                    this.selected_order_object = null;
                    this.order_article_list = [];
                    return;
                }
            } else{
                //input update
                order_id = this.selected_order_object.o_id;
            }

            try {
                const resOrder = await api_get_order_by_id(order_id);
                this.selected_order_object = resOrder.data;

                const resArticles = await api_get_order_articles_with_items(order_id);
                
                if (resArticles.data && resArticles.data.length > 0) {
                    this.order_article_list = resArticles.data;
                } else {
                    base_vue.f_info("No article found");
                    this.order_article_list = [];
                }

                this.change_order_tmp.status = this.selected_order_object.o_status;
                this.change_order_tmp.name = this.selected_order_object.o_name;

            } catch (err) {
                const message = err?.response?.data?.message || err.message || 'Unknown error';
                base_vue.f_info(message, undefined, true);
            }
        },
        f_sum_order_article(items) {
            const row_price = items.reduce((sum, element) => sum + parseFloat(element.os_price), 0);
            return format_price(row_price.toFixed(2));
        },
        f_sum_order(order_articles) {
            const total_price = order_articles.reduce((sumOrder, element) => {
                const itemSum = element.items.reduce((sumItems, item) => {
                    const osPrice = parseFloat(item.os_price) || 0;
                    //const plPrice = parseFloat(item.price_list.pl_price) || 0;
                    return sumItems + osPrice;
                }, 0);
                return sumOrder + itemSum;
            }, 0);
            return format_price(total_price.toFixed(2));
        },
        f_template() {
            const template = `
                <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
                    <div class="lg:col-span-1 bg-white p-4 rounded-lg shadow-md">
                        <h3 class="text-lg font-semibold mb-4">Orders</h3>
                        <div class="space-y-2 select-none">
                            <div v-for="(orders, status) in grouped_orders" :key="status">
                                <button @click="active_status_group = active_status_group === status ? null : status" class="w-full text-left font-semibold p-2 rounded-lg hover:bg-gray-200 border flex justify-between items-center">
                                    <span>{{ status }}</span>
                                    <i class="fas" :class="{'fa-chevron-down': active_status_group === status, 'fa-chevron-right': active_status_group !== status}"></i>
                                </button>
                                <div v-if="active_status_group === status" class="pl-4 mt-2 space-y-2">
                                    <div v-for="order in orders" :key="order.o_id" @click="f_get_order_articles_with_items(order.o_id)" :class="['p-3 rounded-lg cursor-pointer border border-gray-200', selected_order_object?.o_id === order.o_id ? 'bg-gray-200' : 'hover:bg-gray-100']">
                                        <p class="font-semibold" :class="order.o_name ? 'text-gray-800' : 'text-red-600'">{{ order.o_name || 'Unnamed!' }}</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="mt-4">
                            <input type="text" v-model="input_order_name" placeholder="New order name" class="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500">
                            <button @click="f_input_order" class="mt-2 w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition duration-300 ease-in-out"><i class="fas fa-plus mr-2"></i>Add New Order</button>
                            <button @click="f_show_upload_order_popup" class="mt-2 w-full bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded transition duration-300 ease-in-out"><i class="fas fa-plus mr-2"></i>Upload PDF/XLSX</button>
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
                                            <th rowspan="2" v-for="item in f_item_list_corrective_filter(false)" :key="item.i_id" class="py-3 px-6">{{ item.i_item || '(empty)' }}</th>
                                            <th :colspan="corrective_item_count" class="py-3 px-6 text-center">Corrective Price</th>
                                            <th rowspan="2" class="py-3 px-6">Summe</th>
                                            <th rowspan="2" class="py-3 px-6">Actions</th>
                                        </tr>
                                        <tr>
                                            <th v-for="item in f_item_list_corrective_filter(true)" :key="item.i_id" class="py-3 px-6">{{ item.i_item || '(empty)' }}</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="(element, index) in order_article_list" :key="element.oa_id" class="bg-white hover:bg-gray-50">
                                            <td class="py-4 px-6">{{ element.oa_name }}</td>
                                            <td class="py-4 px-6">{{ element.oa_power }}</td>
                                            <td v-for="item in combined_items" :key="item.i_id" class="py-4 px-6">
                                                <strong>{{ f_get_order_article_item_price(element.items, item.i_id) }}</strong><br>
                                                <small class="text-gray-500">{{ f_get_order_article_item_name(element.items, item.i_id) }}</small>
                                            </td>
                                            <td class="py-4 px-6">
                                                <strong>{{ f_sum_order_article(element.items) }}</strong>
                                            </td>
                                            <td class="py-4 px-6">
                                                <button @click="f_delete_order_article(element.oa_id)" class="bg-red-500 hover:bg-red-700 text-white font-bold py-1 px-2 rounded text-xs"><i class="fas fa-trash"></i></button>
                                            </td>
                                        </tr>
                                        <tr class="bg-gray-50 font-semibold">
                                            <td :colspan="combined_items.length + 2" class="py-4 px-6 text-right">Total</td>
                                            <td class="py-4 px-6">{{ f_sum_order(order_article_list) }}</td>
                                            <td></td>
                                        </tr>
                                    </tbody>
                                </table>
                                <div v-else class="select-none p-12 text-center">
                                    <i class="fas fa-search text-4xl text-gray-400"></i>
                                    <p class="text-gray-500 text-sm">No Results</p>
                                </div>
                            </div>
                        </div>
                        <div class="bg-white p-4 rounded-lg shadow-md">
                            <h3 class="text-lg font-semibold mb-2">Information Order</h3>
                            <div class="grid grid-cols-2 gap-2 text-sm text-gray-700 mt-5 mb-5">
                                <div class="font-medium">Order ID</div>
                                <div>{{ selected_order_object.o_id }}</div>

                                <div class="font-medium">Created At:</div>
                                <div>{{ f_time_converter(selected_order_object.o_time) }}</div>

                                <div class="font-medium">User ID:</div>
                                <div>{{ selected_order_object.u_id }}</div>

                                <div class="font-medium">Order Name</div>
                                <input type="text" v-model="change_order_tmp.name" class="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500">
                                
                                <div class="font-medium">Status</div>
                                <div>
                                    <select v-model="change_order_tmp.status" class="block w-full px-2 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
                                        <option v-for="status in enum_status_list" :key="status.enumlabel" :value="status.enumlabel">
                                            {{ status.enumlabel }}
                                        </option>
                                    </select>
                                </div>

                                <div></div>
                                <div>
                                    <button v-if="(selected_order_object.o_name != change_order_tmp.name) || (selected_order_object.o_status != change_order_tmp.status)" @click="f_change_order" class="mt-2 w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition duration-300 ease-in-out">Change</button>
                                </div>

                                <div></div>
                                <div>
                                    <button @click="f_delete_order" class="w-full bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded transition duration-300 ease-in-out">Delete</button>
                                </div>
                            </div>
                        </div>
                        <div class="bg-white p-4 rounded-lg shadow-md">
                            <h3 class="text-lg font-semibold mb-4">Add Article</h3>
                            <div class="space-y-4">
                                <div class="flex items-center">
                                    <label class="w-32 text-sm font-medium text-gray-700">Equipment No</label>
                                    <input type="text" v-model="input_order_article_name" class="flex-1 px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500">
                                </div>
                                <div class="flex items-center">
                                    <label class="w-32 text-sm font-medium text-gray-700">Power</label>
                                    <input type="number" v-model="input_order_article_power" class="flex-1 px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500">
                                </div>
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-3">Items</label>
                                    <div v-if="item_list.length" class="flex flex-col space-y-2 overflow-y-auto pb-3 max-h-80">
                                        <label v-for="item in item_list" :key="item.i_id" class="flex items-center space-x-2 cursor-pointer">
                                            <input type="checkbox" :value="item.i_id" v-model="input_order_article_id_items" class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500">
                                            <span class="text-sm text-gray-600 break-words">{{ item.i_item || '(empty)' }}</span>
                                        </label>
                                    </div>
                                    <div v-else class="select-none">
                                        <p class="select-none text-sm text-gray-500 italic">No items available.</p>
                                    </div>
                                </div>
                            </div>
                            <button @click="f_input_order_article" class="mt-4 w-full bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded transition duration-300 ease-in-out"><i class="fas fa-paper-plane mr-2"></i>Submit Article</button>
                        </div>
                    </div>
                    <div v-else class="select-none p-12 text-center lg:col-span-3 space-y-6">
                        <i class="fas fa-chart-line text-6xl text-gray-300 mb-4"></i>
                        <p class="text-gray-500">Select a navigation order from the sidebar to get started</p>
                    </div>

                    <!-- Popup Upload -->
                    <div v-if="upload_order_file.show_popup" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full flex items-center justify-center">
                        <div class="relative mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
                            <button @click="upload_order_file.show_popup = false" class="absolute top-5 right-5 text-gray-500 hover:text-gray-800"><i class="fas fa-times"></i></button>
                            <div class="mt-3 text-center">
                                <h3 class="text-lg leading-6 font-medium text-gray-900">Upload Order</h3>
                                <div class="mt-2 px-7 py-3 space-y-4 text-left">
                                    <div>
                                        <label class="block text-sm font-medium text-gray-700">PDF/XLSX</label>
                                        <input type="file" @change="handle_order_file_change" accept=".pdf,.xlsx" class="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-500" />
                                    </div>
                                    <button @click="f_upload_order_file" class="w-full bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">Upload</button>
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
            }else{
                dashboard_main.f_reset();
            }

            this.f_get_item_list();
            this.f_get_order_list();
        },
        handle_order_file_change(e) { 
            this.upload_order_file.new_file = e.target.files[0] 
        },
        f_show_upload_order_popup(){
            this.upload_order_file.show_popup = true;
        },
        async f_upload_order_file() {
            if (!this.upload_order_file.new_file) { alert('Pilih file terlebih dahulu!'); return }

            try {
                const res = await api_upload_order_file(this.upload_order_file.new_file);
                base_vue.f_info(res.message);
                this.f_get_order_list();
                this.f_get_order_articles_with_items(res.data.data);
                this.upload_order_file.show_popup = false;
            } catch (err) {
                base_vue.f_info(err.message, undefined, true);
            }
        },
        async f_delete_order_article(oa_id) {
            const confirmed = confirm("Are you sure you want to delete this data?");
            if (!confirmed) return;
            try {
                const res = await api_delete_order_article(oa_id);
                base_vue.f_info(res.message);
                this.f_get_order_articles_with_items();
            } catch (err) {
                base_vue.f_info(err.message, undefined, true);
            }
        },
        async f_delete_order() {
            const confirmed = confirm("Are you sure you want to delete this data?");
            if (!confirmed) return;
            try {
                const res = await api_delete_order(this.selected_order_object.o_id);
                base_vue.f_info(res.message);
                this.f_get_order_list();
                this.selected_order_object = null;
            } catch (err) {
                base_vue.f_info(err.message, undefined, true);
            }
        },
        async f_input_order() {
            try{
                const res = await api_input_order(this.input_order_name);
                base_vue.f_info(res.message);
                this.f_get_order_list();
                this.input_order_name = null;
            } catch (err) {
                base_vue.f_info(err.message, undefined, true);
            }
        },
        async f_input_order_article() {
            try{
                const res = await api_input_order_article(this.selected_order_object.o_id, this.input_order_article_power, this.input_order_article_name, this.input_order_article_id_items);
                this.f_get_order_articles_with_items();
                base_vue.f_info(res.message);
                this.input_order_article_power = null;
                this.input_order_article_name = null;
                this.input_order_article_id_items.splice(0);
            } catch (err) {
                base_vue.f_info(err.message, undefined, true);
            }
        },
        async f_change_order(){
            const confirmed = confirm("Are you sure you want to update this data?");
            if (!confirmed) return;
            try{
                const res = await api_update_order(this.selected_order_object.o_id, this.change_order_tmp.name, this.change_order_tmp.status);
                base_vue.f_info(res.message);
                await this.f_get_order_list();
                //this.selected_order_object.o_status = this.change_order_tmp.status;
                //this.selected_order_object.o_name = this.change_order_tmp.name;
            } catch (err) {
                base_vue.f_info(err.message, undefined, true);
            }
        }
    }
});

order_manager.f_init();