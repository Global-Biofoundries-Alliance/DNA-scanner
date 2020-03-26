<!-- This Landing component is displayed on the front page. It
-->
<template>
    <div>
        <div v-if="!loading">
            <p class="text-center display-1 font-weight-thin" style="margin-top: 13%">Upload your DNA sequences</p>
            <p class="text-center display-1 font-weight-thin">and get it synthesized with the best offers from different
                vendors</p>
            <v-container class="mt-4 pb-0">
                <v-file-input v-model="file"
                              label="File input: Pure DNA or Amino Acid Sequences"
                              outlined
                              rounded
                              prepend-icon=""
                              hide-details
                              class="mb-4"
                              accept=".fasta,.gb,.xml">
                </v-file-input>
            </v-container>
            <v-container>
                <v-row justify="center">
                    <v-dialog v-model="dialog" persistent max-width="600px">
                        <template v-slot:activator="{ on }">
                            <v-btn @click="dialog = true">Set Filter</v-btn>
                        </template>
                        <!-- The Filter component is called and if the saved button is clicked in the Filter then it emits a saved event, after which the dialog is closed-->
                        <FilterDNA @saved="dialog = false"></FilterDNA>
                    </v-dialog>
                    <v-btn color="primary" style="width: 25%;" class="ml-2" @click="searchNow()">Search</v-btn>
                </v-row>
                <v-alert v-if="noFile" type="error" class="mt-4 mx-auto" width="350px">
                    Please upload a file
                </v-alert>
                <v-alert v-if="wrongFile" type="error" class="mt-4 mx-auto" width="350px">
                    Wrong File Format
                </v-alert>
                <p class="text-center font-weight-light mt-4 mb-0">Please give your project a name:</p>
                <v-row justify="center">
                    <v-col cols="5" class="pa-0">
                        <v-text-field placeholder="Project Name"
                                      v-model="projectName"
                                      class="pa-0 centered-input"
                                      :error="projectName === '' && search">
                        </v-text-field>
                    </v-col>
                </v-row>
                <p class="text-center font-weight-light mt-4 mb-0">Does your file consists of only Amino Acid
                    Sequences?</p>
                <v-row justify="center" class="mt-n4">
                    <v-radio-group v-model="isAminoAcid" hide-details row>
                        <v-radio value="1" label="Yes"></v-radio>
                        <v-radio value="0" label="No"></v-radio>
                    </v-radio-group>
                </v-row>
                <v-row v-if="isAminoAcid === '1'">
                    <v-col cols="6">
                        <p class="text-center">Select your Strategy</p>
                        <v-overflow-btn
                                class="my-2"
                                :items="strategies"
                                label="Strategies"
                                target="#dropdown-example"
                        ></v-overflow-btn>
                    </v-col>
                    <v-spacer></v-spacer>
                    <v-col cols="6">
                        <p class="text-center">Select your Codon Usage Table</p>
                        <v-overflow-btn
                                class="my-2"
                                :items="hosts"
                                label="Codon Usage Table"
                                target="#dropdown-example"
                        ></v-overflow-btn>
                    </v-col>
                </v-row>
            </v-container>
        </div>
        <div v-if="loading">
            <v-progress-circular
                    :size="100"
                    :width="7"
                    color="blue"
                    indeterminate
                    style="margin-left: 47%; margin-top: 15%"
            ></v-progress-circular>
            <p style="text-align: center">Please Wait</p>
        </div>
    </div>
</template>

<script>
    import FilterDNA from './Filter.vue'

    export default {
        name: 'Landing',
        components: {
            FilterDNA
        },
        data() {
            return {
                projectName: "",
                strategies: ['Random', 'Balanced', 'Mostly Used', 'Least Different'],
                strategy: "",
                hosts: [],
                host: "",
                result: false,
                file: [],
                dialog: false,
                noFile: false,
                colors: ["red", "green", "orange"],
                isAminoAcid: '0',
                wrongFile: false,
                search: false,
                loading: false
            }
        },
        methods: {
            searchNow() {
                if (this.file === null) {
                    this.noFile = true;
                } else if (this.file.length === 0) {
                    this.noFile = true;
                } else if (this.projectName === "") {
                    this.search = true;
                } else {
                    this.loading = true;
                    let data = new FormData();
                    data.append('seqfile', this.file);
                    data.append('prefix', this.projectName);

                    this.$http.post('/api/upload', data, {
                        headers: {
                            'Access-Control-Allow-Origin': '*',
                            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, DELETE, PUT',
                            'Access-Control-Allow-Headers': 'append,delete,entries,foreach,get,has,keys,set,values,Authorization',
                        }
                    })
                        .then(response => {
                            if (response.body.length === 17) {
                                let filter = {
                                    "filter":
                                        {
                                            "vendors": this.$store.state.StoreSelectedVendors,
                                            "price": this.$store.state.StorePriceFilterRange,
                                            "deliveryDays": this.$store.state.StoreDeliveryDays,
                                            "preselectByPrice": this.$store.state.StorePreselectByPrice,
                                            "preselectByDeliveryDays": this.$store.state.StorePreselectByTime
                                        }
                                };

                                this.$http.post('/api/filter', filter).then(response => {
                                    // eslint-disable-next-line no-console
                                    console.log(filter);
                                    // eslint-disable-next-line no-console
                                    console.log(response);
                                });

                                let selectedOptimization = {
                                    "strategy": this.strategy,
                                    "host": this.host
                                };
                                this.$http.post('/api/codon_optimization', selectedOptimization)
                                    .then(response => {
                                        // eslint-disable-next-line no-console
                                        console.log(response);
                                    });

                                this.$http.post('/api/results', {
                                    headers: {
                                        'Access-Control-Allow-Origin': '*',
                                        'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, DELETE, PUT',
                                        'Access-Control-Allow-Headers': 'append,delete,entries,foreach,get,has,keys,set,values,Authorization',
                                    }
                                })
                                    .then(response => {
                                        this.$store.state.StoreSearchResult = response.body.result;
                                        // eslint-disable-next-line no-console
                                        console.log(this.$store.state.StoreSearchResult);
                                        this.$store.state.StoreCount = response.body.count;
                                        this.loading = false;
                                        this.$router.push('/result');
                                    });
                            } else {
                                this.wrongFile = true
                            }

                        });
                }
            },
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
                    for (let i = 0; i < response.body.length; i++) {
                        this.$store.state.StoreVendors[i] = {
                            id: i,
                            name: response.body[i].shortName,
                            color: this.colors[i]
                        };
                    }
                    // eslint-disable-next-line no-console
                    console.log(this.$store.state.StoreVendors);
                });
            this.$http.get('/api/available_hosts', {
                headers: {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, DELETE, PUT',
                    'Access-Control-Allow-Headers': 'append,delete,entries,foreach,get,has,keys,set,values,Authorization'
                }
            })
                .then(response => {
                    this.hosts = response.body
                })
        }
    };
</script>

<style>
    .centered-input input {
        text-align: center;
    }
</style>

