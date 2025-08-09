const media_management = new Vue({
    data: {
        title: 'Media Management',
        media_file_list: [],
        selected_file: null
    },
    methods: {
        f_init() { //1x panggil
            dashboard_main.navigations.push({ name: this.title, callback: this.f_template });
            this.f_get_files();
        },
        async f_get_files() {
            try {
                const res = await fetch('/api/media');
                this.media_file_list = await res.json();
            } catch (err) {
                console.error('Gagal memuat file:', err);
            }
        },
        downloadFile(filename) {
            fetch(`/api/media/${encodeURIComponent(filename)}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error("File tidak ditemukan atau server error");
                    }
                    return response.blob();
                })
                .then(blob => {
                    // Buat URL sementara untuk blob
                    const url = window.URL.createObjectURL(blob);

                    // Buat elemen <a> untuk trigger download
                    const a = document.createElement("a");
                    a.href = url;
                    a.download = filename; // nama file saat disimpan
                    document.body.appendChild(a);
                    a.click();

                    // Bersihkan
                    a.remove();
                    window.URL.revokeObjectURL(url);
                })
                .catch(err => {
                    console.error("Gagal mendownload:", err);
                });
        },
        async deleteFile(filename) {
            try {
                const response = await fetch(`/api/media/${encodeURIComponent(filename)}`, { method: "DELETE" });
                if (!response.ok) {
                    throw new Error("File tidak ditemukan atau server error");
                }
                const result = await response.json();
                alert(result.message);
                this.f_get_files(); // refresh list
            } catch (err) {
                console.error(err);
                alert("Gagal menghapus file");
            }
        },
        handleFileChange(event) {
            this.selected_file = event.target.files[0];
        },
        async uploadFile() {
            if (!this.selected_file) {
                alert("Pilih file dulu!");
                return;
            }
            const formData = new FormData();
            formData.append("file", this.selected_file);

            try {
                const res = await fetch("/api/media", {
                    method: "POST",
                    body: formData
                });
                const result = await res.json();
                alert(result.message);
                this.selected_file = null;
                this.f_get_files(); // refresh list
            } catch (err) {
                console.error("Gagal upload:", err);
            }
        },
        f_template() {
            const template = `
                <div>
                    <div class="mb-4">
                        <input type="file" @change="handleFileChange" class="border p-2">
                        <button @click="uploadFile" class="bg-blue-500 text-white px-3 py-1 ml-2">Upload</button>
                    </div>
                    <div class="border p-2 cursor-pointer hover:bg-gray-100 flex justify-between items-center" v-for="file in media_file_list" :key="file">
                        <span @click="downloadFile(file)" class="flex-1 hover:underline">{{ file }}</span>
                        <button @click="deleteFile(file)" class="ml-4 bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600 focus:outline-none">Delete</button>
                    </div>
                </div>
            `;
            if (dashboard_main.content.template != template){
                dashboard_main.content.template = template;
                dashboard_main.content.title = this.title;
                dashboard_main.content.data = this;
            }else{
                dashboard_main.f_reset();
            }
        }
    }
});

media_management.f_init();