<template>
    <div>
        <p class="text-center display-1 font-weight-thin" style="margin-top: 13%">Upload your DNA sequences</p>
        <p class="text-center display-1 font-weight-thin">and get it synthesized with the best offers from different
            vendors</p>
        <v-container class="mt-4 pb-0">
            <v-file-input v-model="file" label="File input" outlined rounded prepend-icon="" hide-details
                          class="mb-4" accept=".fasta,.gb,.xml"></v-file-input>
        </v-container>
        <v-container>
            <v-row justify="center">
                <v-dialog v-model="dialog" persistent max-width="600px">
                    <template v-slot:activator="{ on }">
                        <v-btn @click="dialog = true">Set Filter</v-btn>
                    </template>
                    <v-card>
                        <v-card-title>
                            <span class="headline">Filter</span>
                        </v-card-title>
                        <v-card-text>
                            <v-container>
                                <v-row>
                                    <v-col cols="12" sm="6" md="4">
                                        <v-subheader>DNA Supplier</v-subheader>
                                        <v-container
                                                id="scroll-target"
                                                style="max-height: 210px"
                                                class="overflow-y-auto"
                                        >
                                            <v-col
                                                    style="height: auto"
                                            >
                                                <v-checkbox v-for="vendor in vendors" :key="vendor.name" :label="`${vendor.name}`" v-model="vendor.value"></v-checkbox>
                                            </v-col>
                                        </v-container>
                                    </v-col>
                                    <v-card-text>
                                        <v-subheader>Select min and max price in Euros(€)</v-subheader>
                                        <v-row>
                                            <v-col class="px-4">
                                                <v-range-slider
                                                        v-model="range"
                                                        :max="max"
                                                        :min="min"
                                                        hide-details
                                                        class="align-center"
                                                >
                                                    <template v-slot:prepend>
                                                        <v-text-field
                                                                v-model="range[0]"
                                                                class="mt-0 pt-0"
                                                                hide-details
                                                                single-line
                                                                type="number"
                                                                style="width: 60px"
                                                        ></v-text-field>
                                                    </template>
                                                    <template v-slot:append>
                                                        <v-text-field
                                                                v-model="range[1]"
                                                                class="mt-0 pt-0"
                                                                hide-details
                                                                single-line
                                                                type="number"
                                                                style="width: 60px"
                                                        ></v-text-field>
                                                    </template>
                                                </v-range-slider>
                                            </v-col>
                                        </v-row>
                                    </v-card-text>

                                    <v-card-text>
                                        <v-subheader>Select max delivery time in days(d)</v-subheader>
                                        <v-row>
                                            <v-col class="pr-4">
                                                <v-slider
                                                        v-model="deliveryDays"
                                                        class="align-center"
                                                        :max="max"
                                                        :min="min"
                                                        hide-details
                                                >
                                                    <template v-slot:append>
                                                        <v-text-field
                                                                v-model="deliveryDays"
                                                                class="mt-0 pt-0"
                                                                hide-details
                                                                single-line
                                                                type="number"
                                                                style="width: 60px"
                                                        ></v-text-field>
                                                    </template>
                                                </v-slider>
                                            </v-col>
                                        </v-row>
                                    </v-card-text>
                                </v-row>
                            </v-container>
                        </v-card-text>
                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn color="blue darken-1" text @click="reset()">Close</v-btn>
                            <v-btn color="blue darken-1" text @click="dialog = false">Save</v-btn>
                        </v-card-actions>
                    </v-card>
                </v-dialog>
                <v-btn color="primary" style="width: 25%;" class="ml-2" @click="searchNow()">Search</v-btn>
            </v-row>
        </v-container>
    </div>
</template>

<script>

    export default {
        name: 'HelloWorld',
        data() {
            return {
                file: [],
                min: 1,
                max: 1000,
                range: [1, 100],
                deliveryDays: 7,
                dialog: false,
                vendors: [],
                filter: []
            }
        },

        methods: {
            searchNow() {
                this.$http.post('/api/upload', {
                    headers: {
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, DELETE, PUT',
                        'Access-Control-Allow-Headers': 'append,delete,entries,foreach,get,has,keys,set,values,Authorization'
                    }
                })
                    .then(response => {
                        // eslint-disable-next-line no-console
                        console.log(response);
                        this.$store.state.StoreResult = response.body.result;
                        // eslint-disable-next-line no-console
                        console.log(this.$store.state.StoreResult);
                        this.$store.state.StoreFile = this.file;
                        this.$router.push('/result');
                    });
                // this.filter = [this.vendors, this.range, this.deliveryDays];
                // this.$http.post('/api/filter', this.filter);
            },
            reset() {
                this.dialog = false;
                for(let i = 0; i < this.vendors.length; i++) {
                    this.vendors[i].value = true;
                }
                this.range = [1, 100];
                this.deliveryDays = 7;
            }
        },
        created() {
            this.$http.get('/api/vendors', {
                headers: {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, DELETE, PUT',
                    'Access-Control-Allow-Headers': 'append,delete,entries,foreach,get,has,keys,set,values,Authorization'
                }
            })
                .then(response => {
                    for(let i = 0; i < response.body.vendors.length; i++) {
                        this.vendors[i] = {name: response.body.vendors[i], value: true};
                    }
                });
        }
    };
</script>

<style>
</style>

