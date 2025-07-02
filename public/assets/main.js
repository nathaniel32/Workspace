//import { prompt_bot } from './bot.js';
//import { api_get_all_categories, api_get_all_models, api_create_input, api_create_output } from './api.js';
//import { html_to_text } from './utils.js';

new Vue({
    el: '#app',
    data: {
        v_info: "",
    },
    methods:{
        f_clear_info(duration, message){
            this.v_info = message;
            setTimeout(()=>{
                this.v_info = "";
            }, duration);
        },
        f_init(){
            console.log("ok");
        }
    },
    mounted() {
        this.f_init();
    }
});