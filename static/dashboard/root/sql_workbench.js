import { api_workbench_query } from '../api.js';

const dashboard_root_workbench = new Vue({
    data: {
        title: 'SQL Workbench',
        sqlQuery: '',
        queryResult: null,
        displayedResults: [],
        queryError: null,
        executing: false,
        rowsPerPage: 50,
        schema: null,
        loadingSchema: false,
        showSchema: false,
        queryExamples: [
            { label: 'List Tables', query: "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';" },
            { label: 'Database Size', query: "SELECT pg_size_pretty(pg_database_size(current_database())) AS \"Database Size\";" },
            { label: 'Active Connections', query: "SELECT COUNT(*) FROM pg_stat_activity WHERE state = 'active';" },
            { label: 'Enums', query: `SELECT n.nspname AS schema,
       t.typname AS enum_name,
       e.enumlabel AS value
FROM pg_type t
   JOIN pg_enum e ON t.oid = e.enumtypid
   JOIN pg_catalog.pg_namespace n ON n.oid = t.typnamespace
ORDER BY enum_name, e.enumsortorder;` }
        ]
    },
    computed: {
        hasMoreData() {
            return this.queryResult && this.displayedResults.length < this.queryResult.length;
        },
        remainingRows() {
            return this.queryResult.length - this.displayedResults.length;
        }
    },
    methods: {
        f_init() {
            dashboard_main.navigations.push({ name: this.title, callback: this.f_template });
        },

        async f_template() {
            const template = `
                <div class="p-4 space-y-4">
                    <div class="flex justify-between items-center">
                        <button @click="toggleSchema" class="text-sm bg-blue-200 px-3 py-1 rounded hover:bg-blue-300">
                            {{ showSchema ? 'Hide Schema' : 'Show Schema' }}
                        </button>
                        <button @click="loadSchema" :disabled="loadingSchema" class="text-sm bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600">
                            {{ loadingSchema ? 'Loading...' : 'Reload Schema' }}
                        </button>
                    </div>

                    <div v-if="showSchema" class="bg-gray-100 p-3 rounded text-xs overflow-auto max-h-60 border">
                        <pre v-if="schema">{{ schema }}</pre>
                        <p v-else class="text-gray-500">No schema loaded.</p>
                    </div>

                    <textarea 
                        v-model="sqlQuery"
                        class="w-full p-2 border border-gray-300 rounded"
                        rows="5"
                        placeholder="Enter SQL query..."
                    ></textarea>

                    <div class="space-x-2">
                        <button @click="executeQuery" :disabled="executing || !sqlQuery.trim()" class="bg-green-500 text-white px-4 py-1 rounded hover:bg-green-600">
                            {{ executing ? 'Executing...' : 'Execute' }}
                        </button>
                        <button @click="clearQuery" class="bg-gray-400 text-white px-4 py-1 rounded hover:bg-gray-500">
                            Clear
                        </button>
                    </div>

                    <div class="space-x-1">
                        <button 
                            v-for="example in queryExamples" 
                            :key="example.label"
                            @click="sqlQuery = example.query"
                            class="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded hover:bg-blue-200"
                        >
                            {{ example.label }}
                        </button>
                    </div>

                    <div v-if="queryError" class="text-red-600 mt-4">
                        Error: {{ queryError }}
                    </div>

                    <div v-if="displayedResults.length" class="overflow-auto border mt-4">
                        <table class="min-w-full text-sm">
                            <thead class="bg-gray-100">
                                <tr>
                                    <th v-for="col in Object.keys(displayedResults[0])" class="px-2 py-1 border">{{ col }}</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(row, idx) in displayedResults" :key="idx" class="hover:bg-gray-50">
                                    <td v-for="col in Object.keys(row)" class="px-2 py-1 border">
                                        {{ formatValue(row[col]) }}
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div v-if="hasMoreData" class="mt-3">
                        <button @click="loadMoreData" class="bg-blue-500 text-white px-4 py-1 rounded hover:bg-blue-600">
                            Load More ({{ remainingRows }})
                        </button>
                    </div>
                </div>
            `;

            if (dashboard_main.content.template != template){
                dashboard_main.content.template = template;
                dashboard_main.content.title = this.title;
                dashboard_main.content.data = this;
                this.loadSchema();
            }else{
                dashboard_main.f_reset();
            }
        },

        toggleSchema() {
            this.showSchema = !this.showSchema;
        },

        async loadSchema() {
            this.loadingSchema = true;
            try {
                const response = await fetch('/api/workbench/schema');
                const data = await response.json();
                this.schema = data.data;
            } catch (err) {
                this.schema = 'Failed to load schema: ' + err.message;
            } finally {
                this.loadingSchema = false;
            }
        },

        async executeQuery() {
            this.executing = true;
            this.queryError = null;
            this.queryResult = null;
            this.displayedResults = [];

            try {
                const res = await api_workbench_query(this.sqlQuery);
                this.queryResult = res.data.data || [];
                this.displayedResults = this.queryResult.slice(0, this.rowsPerPage);
            } catch (err) {
                this.queryError = err.message;
                base_vue.f_info(err.message);
            } finally {
                this.executing = false;
            }
        },

        loadMoreData() {
            const next = this.displayedResults.length + this.rowsPerPage;
            this.displayedResults = this.queryResult.slice(0, next);
        },

        clearQuery() {
            this.sqlQuery = '';
            this.queryResult = null;
            this.displayedResults = [];
            this.queryError = null;
        },

        formatValue(val) {
            if (val === null || val === undefined) return 'NULL';
            const str = String(val);
            return str.length > 100 ? str.slice(0, 100) + '...' : str;
        }
    }
});

dashboard_root_workbench.f_init();
