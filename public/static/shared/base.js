const base_vue = new Vue({
    el: '#base',
    data: {
        showAuthModal: false,
        authTab: 'login',
        v_info_list: [],
        v_login: {email: "test@exp.com", password: "Tadnxciw123_"},
        v_signup: {username: "Test User", email: "test@exp.com", password: "Tadnxciw123_"},
    },
    methods:{
        f_openAuth(tab = 'login') {
            this.authTab = tab;
            this.showAuthModal = true;
        },
        f_closeAuth() {
            this.showAuthModal = false;
        },
        f_info(message, duration=5000, error=false) {
            const wrapper = document.createElement('div');
            const bgClass = error ? 'bg-red-50 border-red-400' : 'bg-blue-50 border-blue-400';
            const textClass = error ? 'text-red-700' : 'text-blue-700';
            const iconClass = error ? 'fa-exclamation-circle text-red-400' : 'fa-info-circle text-blue-400';
            wrapper.innerHTML = `
                <div class="${bgClass} border-l-4 p-4 rounded-r-lg shadow-lg animate-fade-in">
                    <div class="flex">
                        <div class="flex-shrink-0">
                            <i class="fas ${iconClass}"></i>
                        </div>
                        <div class="ml-3">
                            <p class="text-sm ${textClass}">${message}</p>
                        </div>
                    </div>
                </div>
            `;

            const elem = wrapper.firstElementChild;
            this.$refs.info_container.appendChild(elem);

            setTimeout(() => {
                elem.remove();
            }, duration);
        },
        f_init(){
            console.log("Ready");
        },
        async f_login(){
            const body = new URLSearchParams();
            body.append("username", this.v_login.email);
            body.append("password", this.v_login.password);
            
            try {
                const response = await fetch('/api/auth/login', {
                    method: 'POST',
                    headers: {
                        //"Content-Type": "application/x-www-form-urlencoded",
                        'Accept': 'application/json'
                    },
                    body: body
                });

                if (!response.ok) {
                    const errorResult = await response.json();
                    const errorMsg = errorResult.detail || `HTTP error! status: ${response.status}`;
                    throw new Error(errorMsg);
                }

                const result = await response.json();
                //this.f_info(result.message);
                window.location.reload();
            } catch (error) {
                this.f_info(error, undefined, true);
            }
        },
        async f_signup(){
            const body = new URLSearchParams();
            body.append("username", this.v_signup.email);
            body.append("password", this.v_signup.password);
            body.append("name", this.v_signup.username);

            try {
                const response = await fetch('/api/auth/signup', {
                    method: 'POST',
                    headers: {
                        //"Content-Type": "application/x-www-form-urlencoded",
                        'Accept': 'application/json'
                    },
                    body: body
                });

                if (!response.ok) {
                    const errorResult = await response.json();
                    const errorMsg = errorResult.detail || `HTTP error! status: ${response.status}`;
                    throw new Error(errorMsg);
                }

                const result = await response.json();
                //this.f_info(result.message);
                window.location.reload();
            } catch (error) {
                this.f_info(error, undefined, true);
            }
        },
        async f_logout(){
            try {
                const response = await fetch('/api/auth/logout', {
                    method: 'POST',
                    headers: {
                        'Accept': 'application/json'
                    }
                });

                if (!response.ok) {
                    const errorResult = await response.json();
                    const errorMsg = errorResult.detail || `HTTP error! status: ${response.status}`;
                    throw new Error(errorMsg);
                }

                const result = await response.json();
                //this.f_info(result.message);
                window.location.reload();
            } catch (error) {
                this.f_info(error, undefined, true);
            }
        }
    },
    mounted() {
        this.f_init();
    }
});