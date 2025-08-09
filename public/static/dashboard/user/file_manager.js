import { api_download_file, api_delete_file, api_get_all_file_name, api_upload_file, api_create_order_form } from '../api.js';

const file_manager = new Vue({
    data: {
        title: 'File Manager',
        media_file_list: [],
        selected_file: null
    },
    methods: {
        f_init() {
            dashboard_main.navigations.push({ name: this.title, callback: this.f_template });
        },
        async f_get_files() {
            try{
                const res = await api_get_all_file_name();
                //base_vue.f_info(res.message);
                this.media_file_list = res.data;
            } catch (err) {
                base_vue.f_info(err.message, undefined, true);
            }
        },
        async download_file(filename) {
            try{
                const res = await api_download_file(filename);
                base_vue.f_info(res.message);
                const url = window.URL.createObjectURL(res.data);
                const a = document.createElement("a");
                a.href = url;
                a.download = filename;
                document.body.appendChild(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(url);
            } catch (err) {
                base_vue.f_info(err.message, undefined, true);
            }
        },
        async delete_file(filename) {
            try{
                const res = await api_delete_file(filename);
                base_vue.f_info(res.message);
                this.f_get_files();
            } catch (err) {
                base_vue.f_info(err.message, undefined, true);
            }
        },
        handle_file_change(event) {
            this.selected_file = event.target.files[0];
        },
        async upload_file() {
            try{
                if (!this.selected_file) {
                    throw({message: "Pilih file dulu!"});
                }
                const res = await api_upload_file(this.selected_file);
                base_vue.f_info(res.message);
                this.selected_file = null;
                this.f_get_files();
            } catch (err) {
                base_vue.f_info(err.message, undefined, true);
            }
        },
        async create_order_form_file() {
            try{
                const res = await api_create_order_form();
                base_vue.f_info(res.message);
                this.f_get_files();
            } catch (err) {
                base_vue.f_info(err.message, undefined, true);
            }
        },
        f_template() {
            const template = `
                <div>
                    <button @click="create_order_form_file()" class="bg-blue-500 text-white px-3 py-1 ml-2">Create Order Form</button>
                    <div class="mb-4">
                        <input type="file" @change="handle_file_change" class="border p-2">
                        <button @click="upload_file" class="bg-blue-500 text-white px-3 py-1 ml-2">Upload</button>
                    </div>
                    <div class="border p-2 cursor-pointer hover:bg-gray-100 flex justify-between items-center" v-for="file in media_file_list" :key="file">
                        <span @click="download_file(file)" class="flex-1 hover:underline">{{ file }}</span>
                        <button @click="delete_file(file)" class="ml-4 bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600 focus:outline-none">Delete</button>
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
            this.f_get_files();
        }
    }
});

file_manager.f_init();