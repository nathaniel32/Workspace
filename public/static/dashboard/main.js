const DynamicComponent = {
    props: ['template', 'dataObj'],
    data() {
        return { compiled: null };
    },
    watch: {
        template: {
            immediate: true,
            handler(newTemplate) {
                this.compiled = Vue.compile(newTemplate);
            }
        }
    },
    render(h) {
        if (!this.compiled) return h('div', 'Loading...');
        // context dataObj
        return this.compiled.render.call(this.dataObj, _c=h);
    },
    staticRenderFns() {
        return this.compiled ? this.compiled.staticRenderFns : [];
    }
};

const dashboard_main = new Vue({
    el: '#dashboard_main',
    data: {
        navigations: [],
        content: {
            title: "",
            template: "",
            data: ""
        },
        contentData: {}
    },
    components: {
        'dynamic-component': DynamicComponent
    },
    methods:{
        f_init(){
            base_vue.f_info("Welcome!", 5000);
        },
        f_reset(){
            this.content = {
                title: "",
                template: "",
                data: ""
            }
        }
    },
    mounted() {
        this.f_init();
    }
});