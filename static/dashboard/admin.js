const dashboard_admin = new Vue({
    data: {
        name: ['admin', 'admin2', 'admin3'],
        sub: ''
    },
    methods:{
        f_init(){
            dashboard_main.navigations.push({name: "Admin Control Panel", callback: this.f_control_panel});
            dashboard_main.navigations.push({name: "Admin Statistics", callback: this.f_statistics});
        },
        f_control_panel(){
            dashboard_main.content.title = 'Control Panel';
            dashboard_main.content.template = `
                <div>
                    <ul>
                        <li v-for="(item, index) in name" :key="index">{{ item }}</li>
                    </ul>
                    <input v-model="sub">
                    {{ sub }}
                </div>
            `;
            dashboard_main.content.data = this;
        },
        f_statistics(){
            dashboard_main.content.title = 'Statistik';
            dashboard_main.content.template = `
                <div>
                    {{ sub }}
                </div>
            `;
            dashboard_main.content.data = this;
        }
    }
});

dashboard_admin.f_init();