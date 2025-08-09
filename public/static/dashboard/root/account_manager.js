import { api_workbench_query, api_get_workbench_schema } from '../api.js';

const account_manager = new Vue({
    data: {
        title: 'Account Manager'
    },
    methods: {
        f_init() {
            dashboard_main.navigations.push({ name: this.title, callback: this.f_template });
        },

        async f_template() {
            const template = `
                <div class="p-4">
                    ok
                </div>
            `;

            if (dashboard_main.content.template != template){
                dashboard_main.content.template = template;
                dashboard_main.content.title = this.title;
                dashboard_main.content.data = this;
            }else{
                dashboard_main.f_reset();
            }
        }
    }
});

account_manager.f_init();