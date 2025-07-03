const dashboard_admin = new Vue({
    data: {
        name: ['admin', 'joshua', 'yes'],
        sub: ''
    },
    methods:{
        f_init(){
            dashboard_main.navigations.push({name: "Admin Control Panel", callback: this.f_control_panel});
            dashboard_main.navigations.push({name: "Admin Statistics", callback: this.f_statistics});
        },
        f_control_panel(){
            dashboard_main.content.template = `
                <div>
                    <strong style="color:red">Ini teks tebal merah</strong>
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
            console.log(this.sub)
            dashboard_main.content.template = `
                <div>
                    <strong style="color:red">Ini teks tebal merah</strong>
                    {{ sub }}
                </div>
            `;
            dashboard_main.content.data = this;
        }
    }
});

dashboard_admin.f_init();