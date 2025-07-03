const dashboard_admin = new Vue({
    data: {
        name: ['admin', 'joshua', 'yes'],
        sub: ''
    },
    methods:{
        f_init(){
            dashboard_main.navigations.push({name: "admin", callback: this.f_admin});
        },
        f_admin(){
            dashboard_main.content = `
                <div>
                    <strong style="color:red">Ini teks tebal merah</strong>
                    <ul>
                        <li v-for="(item, index) in name" :key="index">{{ item }}</li>
                    </ul>
                    <input v-model="sub">
                    {{ sub }}
                </div>
            `;
            dashboard_main.contentData = this;
            console.log("admin");
        }
    }
});

dashboard_admin.f_init();