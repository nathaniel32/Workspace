const dashboard_user = new Vue({
    //el: '#dashboard_user',
    data: {
        name: ['client', 'client1'],
        sub: ''
    },
    methods:{
        f_init(){
            dashboard_main.navigations.push({name: "Input data", callback: this.f_input_data});
        },
        f_input_data(){
            dashboard_main.content.title = 'Input Data';
            dashboard_main.content.template = `
                <div>
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