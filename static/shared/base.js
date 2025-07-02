const base_vue = new Vue({
    el: '#base',
    data: {
        v_info: "",
        v_login: {email: "test@exp.com", password: "Tadnxciw123_"},
        v_signup: {username: "Test User", email: "test@exp.com", password: "Tadnxciw123_"},
    },
    methods:{
        f_info(message, duration){
            this.v_info = message;
            setTimeout(()=>{
                this.v_info = "";
            }, duration);
        },
        f_init(){
            console.log("ok");
        },
        async f_login(){
            try {
                const body = new URLSearchParams();
                body.append("username", this.v_login.email);
                body.append("password", this.v_login.password);

                const response = await fetch("/api/auth/login", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded"
                    },
                    body: body
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.detail);
                }

                const data = await response.json();
                alert(data.message);
                window.location.reload();
            } catch (error) {
                alert("Error: " + error.message);
            }
        },
        async f_signup(){
            try {
                const body = new URLSearchParams();
                body.append("username", this.v_signup.email);
                body.append("password", this.v_signup.password);
                body.append("name", this.v_signup.username);

                const response = await fetch("/api/auth/signup", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded"
                    },
                    body: body
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.detail);
                }

                const data = await response.json();
                alert(data.message);
                window.location.reload();
            } catch (error) {
                alert("Error: " + error.message);
            }
        },
        async f_logout(){
            try {
                const response = await fetch("/api/auth/logout", {
                    method: "POST"
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.detail);
                }

                const data = await response.json();
                alert(data.message);
                window.location.reload();
            } catch (error) {
                alert("Error: " + error.message);
            }
        }
    },
    mounted() {
        this.f_init();
    }
});