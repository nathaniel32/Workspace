import { api_get_user_role_enum, api_create_account, api_get_all_users, api_update_account, api_get_user_status_enum, api_delete_account } from '../api.js';

const account_manager = new Vue({
    data: {
        title: 'Account Manager',
        role_enum: [],
        status_enum: [],
        new_account_form: {},
        account_list: [],
        table_account_headers: ['ID', 'Name', 'Email', 'Code', 'Role', 'Status', 'Created At'],
        edit_account: {
            show_popup: false,
            u_id: null,
            u_name: null,
            u_role: null,
            u_status: null
        }
    },
    methods: {
        f_init() {
            dashboard_main.navigations.push({ name: this.title, callback: this.f_template });
            this.f_get_role_enum();
            this.f_get_status_enum();
        },
        formatTime(unixTimestamp) {
            if (!unixTimestamp) return '-';
            const date = new Date(unixTimestamp * 1000);
            return date.toLocaleString();
        },
        async f_get_all_users(){
            try {
                const res = await api_get_all_users();
                //base_vue.f_info(res.message);
                this.account_list = res.data;
            } catch (err) {
                base_vue.f_info(err.message, undefined, true);
            }
        },
        async f_get_role_enum(){
            try {
                const res = await api_get_user_role_enum();
                //base_vue.f_info(res.message);
                this.role_enum = res.data;
            } catch (err) {
                base_vue.f_info(err.message, undefined, true);
            }
        },
        async f_get_status_enum(){
            try {
                const res = await api_get_user_status_enum();
                //base_vue.f_info(res.message);
                this.status_enum = res.data;
            } catch (err) {
                base_vue.f_info(err.message, undefined, true);
            }
        },
        async f_create_account(){
            try {
                const res = await api_create_account(this.new_account_form.role);
                base_vue.f_info(res.message);
                this.f_get_all_users();
                this.new_account_form.role = null;
            } catch (err) {
                base_vue.f_info(err.message, undefined, true);
            }
        },
        f_show_account_popup(account){
            this.edit_account.show_popup = true;
            this.edit_account.u_id = account.u_id;
            this.edit_account.u_name = account.u_name;
            this.edit_account.u_email = account.u_email;
            this.edit_account.u_role = account.u_role;
            this.edit_account.u_status = account.u_status;
            
            this.edit_account.u_code = account.u_code;
            this.edit_account.u_time = account.u_time;
        },
        async f_update_account(){
            const confirmed = confirm("Are you sure you want to update this account?");
            if (!confirmed) return;
            try {
                const res = await api_update_account(this.edit_account.u_id, this.edit_account.u_name, this.edit_account.u_email, this.edit_account.u_role, this.edit_account.u_status);
                base_vue.f_info(res.message);
                this.f_get_all_users();
                this.edit_account.show_popup = false;
            } catch (err) {
                base_vue.f_info(err.message, undefined, true);
            }
        },
        async f_delete_delete(){
            const confirmed = confirm("Are you sure you want to delete this account?");
            if (!confirmed) return;
            try {
                const res = await api_delete_account(this.edit_account.u_id);
                base_vue.f_info(res.message);
                this.f_get_all_users();
                this.edit_account.show_popup = false;
            } catch (err) {
                base_vue.f_info(err.message, undefined, true);
            }
        },
        async f_template() {
            const template = `
                <div class="p-4 rounded shadow">
                    <div class="mb-4 p-4 rounded shadow">
                        <h3 class="text-lg font-semibold mb-4">Create New Account</h3>
                        <label for="role" class="block mb-1 font-medium">Role:</label>
                        <select id="role" v-model="new_account_form.role" class="block w-full px-3 py-2 mb-4 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
                            <option v-for="role in role_enum" :key="role.enumlabel" :value="role.enumlabel">
                            {{ role.enumlabel }}
                            </option>
                        </select>

                        <button :disabled="!new_account_form.role" @click="f_create_account" class="w-full bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700 transition">
                            Create Account
                        </button>
                    </div>

                    <div class="overflow-auto">
                        <table v-if="account_list.length > 0" class="min-w-full border-collapse border border-gray-300">
                            <thead>
                                <tr>
                                    <th v-for="header in table_account_headers" :key="header" class="border border-gray-300 px-4 py-2">
                                        {{ header }}
                                    </th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="account in account_list" :key="account.u_id" class="hover:bg-gray-100 cursor-pointer" @click="f_show_account_popup(account)">
                                    <td class="border border-gray-300 px-4 py-2">{{ account.u_id }}</td>
                                    <td class="border border-gray-300 px-4 py-2">{{ account.u_name || '-' }}</td>
                                    <td class="border border-gray-300 px-4 py-2">{{ account.u_email || '-' }}</td>
                                    <td class="border border-gray-300 px-4 py-2">{{ account.u_code || '-' }}</td>
                                    <td class="border border-gray-300 px-4 py-2">{{ account.u_role }}</td>
                                    <td class="border border-gray-300 px-4 py-2">{{ account.u_status }}</td>
                                    <td class="border border-gray-300 px-4 py-2">{{ formatTime(account.u_time) }}</td>
                                </tr>
                            </tbody>
                        </table>
                        <div v-else class="select-none p-12 text-center">
                            <i class="fas fa-search text-4xl text-gray-400"></i>
                            <p class="text-gray-500 text-sm">No Results</p>
                        </div>
                    </div>

                    <!-- Popup Account -->
                    <div v-if="edit_account.show_popup" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full flex items-center justify-center">
                        <div class="relative mx-auto p-5 border w-[460px] shadow-lg rounded-md bg-white">
                            <button @click="edit_account.show_popup = false" class="absolute top-5 right-5 text-gray-500 hover:text-gray-800"><i class="fas fa-times"></i></button>
                            <div class="mt-3 text-center">
                                <h3 class="text-lg leading-6 font-medium text-gray-900">Edit Account</h3>
                                <div class="mt-2 px-3 py-3 space-y-3 text-left">
                                    <div class="space-y-1">
                                        <div class="flex">
                                            <div class="w-24 font-semibold">ID</div>
                                            <div class="overflow-auto">{{ edit_account.u_id || '-' }}</div>
                                        </div>
                                        <div class="flex">
                                            <div class="w-24 font-semibold">Code</div>
                                            <div class="overflow-auto">{{ edit_account.u_code || '-' }}</div>
                                        </div>
                                        <div class="flex">
                                            <div class="w-24 font-semibold">Created At</div>
                                            <div class="overflow-auto">{{ formatTime(edit_account.u_time) }}</div>
                                        </div>
                                    </div>
                                    <div>
                                        <label class="block text-sm font-medium text-gray-700">Name</label>
                                        <input v-model="edit_account.u_name" type="text" placeholder="Name" class="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-500" />
                                    </div>
                                    <div>
                                        <label class="block text-sm font-medium text-gray-700">Email</label>
                                        <input v-model="edit_account.u_email" type="email" placeholder="Email" class="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-500" />
                                    </div>
                                    <div>
                                        <label class="block text-sm font-medium text-gray-700">Role</label>
                                        <select v-model="edit_account.u_role" class="block w-full px-3 py-2 mb-4 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
                                            <option v-for="role in role_enum" :key="role.enumlabel" :value="role.enumlabel">
                                                {{ role.enumlabel }}
                                            </option>
                                        </select>
                                    </div>
                                    <div>
                                        <label class="block text-sm font-medium text-gray-700">Status</label>
                                        <select v-model="edit_account.u_status" class="block w-full px-3 py-2 mb-4 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
                                            <option v-for="status in status_enum" :key="status.enumlabel" :value="status.enumlabel">
                                                {{ status.enumlabel }}
                                            </option>
                                        </select>
                                    </div>
                                </div>
                                <div class="items-center px-4 py-3">
                                    <button @click="f_delete_delete" class="px-4 py-2 bg-red-500 text-white text-base font-medium rounded-md w-auto shadow-sm hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-300">Delete</button>
                                    <button @click="f_update_account" class="px-4 py-2 bg-green-500 text-white text-base font-medium rounded-md w-auto shadow-sm hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-300">Update</button>
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
                this.f_get_all_users();
            }else{
                dashboard_main.f_reset();
            }
        }
    }
});

account_manager.f_init();