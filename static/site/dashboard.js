new Vue({
    el: '#role',
    data: {
    },
    methods:{
        async f_init(){
            base_vue.f_info("HELLO CLIENT", 5000);
            console.log(await getAllPriceList());
        },
    },
    mounted() {
        this.f_init();
    }
});