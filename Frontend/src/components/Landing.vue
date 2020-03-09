<template>
    <div>
        <p class="text-center display-1 font-weight-thin" style="margin-top: 13%">Upload your DNA sequences</p>
        <p class="text-center display-1 font-weight-thin">and get it synthesized with the best offers from different
            vendors</p>
        <v-container class="mt-4 pb-0">
            <v-file-input v-model="file" label="File input" outlined rounded prepend-icon="" hide-details
                          class="mb-4"></v-file-input>
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
                                                <v-checkbox v-for="vendor in this.$store.state.StoreVendors"
                                                            :key="vendor.name"
                                                            :label="`${vendor.name}`"
                                                            :value="vendor.id"
                                                            v-model="vendors"></v-checkbox>
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

                                    <v-checkbox v-model="preselectByPrice" label="Preselect by price" class="ml-8 mr-4"
                                                :disabled="preselectByTime"></v-checkbox>

                                    <v-checkbox v-model="preselectByTime" label="Preselect by time"
                                                :disabled="preselectByPrice"></v-checkbox>
                                </v-row>
                            </v-container>
                        </v-card-text>
                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn color="blue darken-1" text @click="reset()">Reset</v-btn>
                            <v-btn color="blue darken-1" text @click="dialog = false">Save</v-btn>
                        </v-card-actions>
                    </v-card>
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
                    <v-text-field placeholder="Project Name" v-model="projectName" class="pa-0 centered-input" :error="projectName === '' && search"></v-text-field>
                </v-col>
            </v-row>
            <p class="text-center font-weight-light mt-4 mb-0">Does your file include Amino Acid Sequences?</p>
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
</template>

<script>
    export default {
        name: 'Landing',
        data() {
            return {
                projectName: "",
                strategies: ['Random', 'Balanced', 'Mostly Used', 'Least Different'],
                strategy: "",
                hosts: [],
                host: "",
                result: false,
                file: [],
                vendors: [0, 1, 2],
                preselectByPrice: false,
                preselectByTime: false,
                min: 1,
                max: 200,
                range: [0, 50],
                deliveryDays: 7,
                dialog: false,
                filter: [],
                noFile: false,
                colors: ["red", "green", "orange"],
                isAminoAcid: '0',
                wrongFile: false,
                search: false
            }
        },
        methods: {
            searchNow() {
                if(this.file === null) {
                    this.noFile = true;
                }
                else if (this.file.length === 0) {
                    this.noFile = true;
                }
                else if(this.projectName === "") {
                    this.search = true;
                }
                else {
                    this.$store.state.StoreSelectedVendors = this.vendors;
                    var data = new FormData();
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
                            if(response.body.length === 17) {
                                var filter = {
                                    "filter":
                                        {
                                            "vendors": this.vendors,
                                            "price": this.range,
                                            "deliveryDays": this.deliveryDays,
                                            "preselectByPrice": this.preselectByPrice,
                                            "preselectByDeliveryDays": this.preselectByTime
                                        }
                                };

                                this.$http.post('/api/filter', filter).then(response => {
                                    // eslint-disable-next-line no-console
                                    console.log(filter);
                                    // eslint-disable-next-line no-console
                                    console.log(response);
                                });

                                var selectedOptimization = {
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
                                        // eslint-disable-next-line no-console
                                        console.log(response);
                                        let i, j, k;
                                        var mostOffers = 0;
                                        var mostOffersVendor = 0;
                                        var offId = 0;
                                        for(i = 0; i < response.body.result.length; i++) {
                                            for(j = 0; j < response.body.result[i].vendors.length; j++) {
                                                if(response.body.result[i].vendors[j].offers.length > mostOffers) {
                                                    mostOffers = response.body.result[i].vendors[j].offers.length;
                                                    mostOffersVendor = j;
                                                }
                                                for(k = 0; k < response.body.result[i].vendors[j].offers.length; k++) {
                                                    offId = response.body.result[i].sequenceInformation.id.toString() + response.body.result[i].vendors[j].key.toString() + k.toString();
                                                    response.body.result[i].vendors[j].offers[k].id = offId;
                                                }
                                            }
                                            response.body.result[i].sequenceInformation.id = i;
                                            response.body.result[i].sequenceInformation.mostOffVendor = mostOffersVendor;
                                            mostOffers = 0;
                                            mostOffersVendor = 0
                                        }
                                        this.$store.state.StoreSearchResult = response.body.result;
                                        // eslint-disable-next-line no-console
                                        console.log(this.$store.state.StoreSearchResult);
                                        this.$store.state.StoreCount = response.body.count;
                                        this.$router.push('/result');
                                    });
                            }
                            else {
                                this.wrongFile = true
                            }

                        });
                }
            },
            reset() {
                this.dialog = false;
                this.vendors = [0, 1, 2];
                this.range = [0, 50];
                this.deliveryDays = 7;
                this.preselectByPrice = false;
                this.preselectByTime = false;
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

