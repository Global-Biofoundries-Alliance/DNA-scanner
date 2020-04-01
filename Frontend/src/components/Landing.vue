<!-- This Landing component is displayed on the front page.
The template is divided in two parts. One part is displayed when before the user clicked on search (loading = false)
and the other part is displayed when the user clicked on search and the loading circle appears (loading = true).
-->
<template>
    <div>
        <!-- The first div just includes the elements first displayed when you open the webpage. These are the paragraphs
        which include the text, the file input, the buttons, the alerts if an error occurred, the selection for the strategy and codon usage table, and the logo.
        The second div just includes the loading circle and the text underneath it.
        -->
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
                              class="mb-4">
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
                <v-alert v-if="noSelection" type="error" class="mt-4 mx-auto" width="350px">
                    Please select your strategy and codon usage table
                </v-alert>
                <v-alert v-if="resultError" type="error" class="mt-4 mx-auto" width="350px">
                    An error occurred while getting the results from the vendors
                </v-alert>
                <p class="text-center font-weight-light mt-4 mb-0">Please give your project a name:</p>
                <v-row justify="center">
                    <v-col cols="5" class="pa-0">
                        <v-text-field placeholder="Project Name"
                                      v-model="projectName"
                                      class="pa-0 centered-input"
                                      :error="projectName === '' && noProjectName">
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
                <p v-if="isAminoAcid === '1'" class="text-center font-weight-light mt-4">After selecting your strategy and codon usage table your request will be processed by boost</p>
                <v-img v-if="isAminoAcid === '1'" :src="require('../assets/BoostLogo.png')"></v-img>
                <v-row v-if="isAminoAcid === '1'">
                    <v-col cols="6">
                        <p class="text-center">Select your Strategy</p>
                        <v-overflow-btn
                                class="my-2"
                                :items="strategies"
                                label="Strategies"
                                target="#dropdown-example"
                                v-model="strategy"
                        ></v-overflow-btn>
                    </v-col>
                    <v-spacer></v-spacer>
                    <v-col cols="6">
                        <p class="text-center">Select your Codon Usage Table</p>
                        <v-overflow-btn
                                class="my-2 font-italic"
                                :items="hosts"
                                label="Codon Usage Table"
                                target="#dropdown-example"
                                v-model="host"
                        ></v-overflow-btn>
                    </v-col>
                </v-row>
            </v-container>
        </div>
        <div v-if="loading" style="height: 100vh; display: flex; justify-content: center; align-items: center; flex-direction: column;">
            <v-progress-circular
                    :size="100"
                    :width="7"
                    color="blue"
                    indeterminate
                    class="mb-4"
                    style="margin-top: -15%"
            ></v-progress-circular>
            <p class="font-weight-light">Please Wait.</p>
            <p class="font-weight-light">Contacting the Vendor APIs...</p>
            <p v-if="isAminoAcid === '1'" class="font-weight-light">Contacting Boost...</p>
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
                strategies: ['Random', 'Balanced', 'MostlyUsed'],
                strategy: "",
                hosts: [],
                host: "",
                result: false,
                file: [],
                dialog: false,
                noFile: false,
                colors: ["#B8DE29FF", "#2D708EFF", "#3CBB75FF"],
                isAminoAcid: '0',
                wrongFile: false,
                noProjectName: false,
                loading: false,
                noSelection: false,
                resultError: false
            }
        },
        methods: {
            // This method is executed when the user clicked on search. It checks at first, if a file was chosen, then
            // if the user clicked on yes at the selection but didn't choose any strategy or codon usage table. After that
            // it checks if the project name is empty. If any error occurred it changes the according variable and an error
            // alert will be displayed. If there is no error we come to the last else part where we make the following requests:
            // 1. /filter with the chosen filter from the user
            // 2. /codon_optimization with the chosen strategy and the codon usage table
            // 3. /upload with the chosen file
            // 4. /results without any data
            // If there is an error by uploading a wrong file or the results throw an error it will be displayed.
            // If there is no error '/result' is added to the url so that the router changes to the Result component.

            searchNow() {
                if (this.file === null) {
                    this.noFile = true;
                } else if (this.file.length === 0) {
                    this.noFile = true;
                } else if (this.isAminoAcid === '1' && (this.strategy === "" || this.host === "")) {
                    this.noFile = false;
                    this.noSelection = true
                } else if (this.projectName === "") {
                    this.noFile = false;
                    this.noSelection = false;
                    this.noProjectName = true;
                } else {
                    this.noFile = false;
                    this.noSelection = false;
                    this.noProjectName = false;

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
                        let selectedOptimization = {
                            "strategy": this.strategy,
                            "host": this.host
                        };
                        this.$http.post('/api/codon_optimization', selectedOptimization)
                            .then(response => {
                                // eslint-disable-next-line no-console
                                console.log(response);

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
                                        // eslint-disable-next-line no-console
                                        console.log(response);
                                        if(response.body.length === 17) {
                                            this.loading = true;
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
                                                    this.$store.state.StoreSearchResult = response.body.result;
                                                    // eslint-disable-next-line no-console
                                                    console.log(this.$store.state.StoreSearchResult);
                                                    this.$store.state.StoreVendorMessage = response.body.vendorMessage;
                                                    if(response.body.globalMessage.length !== 0) {
                                                        let msg = "";
                                                        response.body.globalMessage.forEach(i => {
                                                            msg = msg + i
                                                        });
                                                        this.$store.state.StoreGlobalMessage = msg;
                                                    }
                                                    this.loading = false;
                                                    this.$router.push('/result');
                                                },response => {
                                                    // eslint-disable-next-line no-console
                                                    console.log(response);
                                                    this.loading = false;
                                                    this.resultError = true;
                                                });

                                        }
                                        else {
                                            this.wrongFile = true;
                                        }
                                    })
                            })
                    });
                }
            },
        },
        // This part is executed when the user loads the website. Here we make two requests. One to get the available
        // vendors and one to get the codon usage tables.

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
    /*This class is used for the project name field to show the entered text in the center of the field */
    .centered-input input {
        text-align: center;
    }
</style>

