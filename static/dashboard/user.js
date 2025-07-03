const dashboard_user = new Vue({
    //el: '#dashboard_user',
    data: {
        name: ['client', 'joshua', 'yes'],
        sub: ''
    },
    methods:{
        f_init(){
            dashboard_main.navigations.push({name: "client", callback: this.f_client});
        },
        f_client(){
            dashboard_main.content.template = `
                <div>
                    <strong style="color:red">Ini teks tebal merah</strong>
                    <ul>
                        <li v-for="(item, index) in name" :key="index">{{ item }}</li>
                    </ul>
                    <input v-model="sub">
                    client {{ sub }}
                </div>
            `;
            dashboard_main.content.data = this;
            console.log("client");
        }
    }
});

dashboard_user.f_init();