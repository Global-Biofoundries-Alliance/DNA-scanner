<!-- This Filter is component is used twice, once in the Landing Page and once in the Result page.
     Because it is used twice, this component avoids code duplication and uses global variables from this.$store.state.variableName,
     wherefore we have a computed list, where each local variable has a getter and setter method to read and write on the according
     global variable. This computed list is needed because the local variables are used in v-model directive, where you can't use global variables directly.
     To differentiate if the filter is used from the App component or Landing component, we have a props field, which includes the variable isApp.
     When the Filter is used in the App component it will pass the value true for isApp, wherefore the action for the save button is also different.-->
<template>
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
                                            v-model="selectedVendors"></v-checkbox>
                            </v-col>
                        </v-container>
                    </v-col>

                    <v-card-text>
                        <v-subheader>Select min and max price</v-subheader>
                        <v-row>
                            <v-col class="px-4">
                                <v-range-slider
                                        v-model="priceRange"
                                        :max="maxVal"
                                        :min="minVal"
                                        hide-details
                                        class="align-center"
                                >
                                    <template v-slot:prepend>
                                        <v-text-field
                                                v-model="priceRange[0]"
                                                class="mt-0 pt-0"
                                                hide-details
                                                single-line
                                                type="number"
                                                style="width: 60px"
                                        ></v-text-field>
                                    </template>
                                    <template v-slot:append>
                                        <v-text-field
                                                v-model="priceRange[1]"
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
                        <v-subheader>Select max delivery time in business days(bd)</v-subheader>
                        <v-row>
                            <v-col class="pr-4">
                                <v-slider
                                        v-model="deliveryDays"
                                        class="align-center"
                                        :max="maxVal"
                                        :min="minVal"
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
            <v-btn color="blue darken-1" text @click="save()">Save</v-btn>
        </v-card-actions>
    </v-card>
</template>

<script>
    export default {
        name: "FilterDNA",
        props:['isApp'],
        computed: {
            selectedVendors: {
                get() {
                    return this.$store.state.StoreSelectedVendors;
                },
                set(value) {
                    this.$store.commit('updateSelectedVendors', value);
                }
            },
            priceRange: {
                get() {
                    return this.$store.state.StorePriceFilterRange;
                },
                set(value) {
                    this.$store.commit('updateRange', value)
                }
            },
            maxVal: {
                get() {
                    return this.$store.state.StoreFilterMax;
                },
                set(value) {
                    this.$store.commit('updateFilterMax', value)
                }
            },
            minVal: {
                get() {
                    return this.$store.state.StoreFilterMin;
                },
                set(value) {
                    this.$store.commit('updateFilterMin', value)
                }
            },
            deliveryDays: {
                get() {
                    return this.$store.state.StoreDeliveryDays;
                },
                set(value) {
                    this.$store.commit('updateDeliveryDays', value)
                }
            },
            preselectByPrice: {
                get() {
                    return this.$store.state.StorePreselectByPrice;
                },
                set(value) {
                    this.$store.commit('updatePreselectByPrice', value)
                }
            },
            preselectByTime: {
                get() {
                    return this.$store.state.StorePreselectByTime;
                },
                set(value) {
                    this.$store.commit('updatePreselectByTime', value)
                }
            },
            selectBox: {
                get() {
                    return this.$store.state.StoreSelectedOffers;
                },
                set(value) {
                    this.$store.commit('updateSelectedOffers', value)
                }
            }
        },
        methods: {
            reset() {
                this.selectedVendors = [0, 1, 2];
                this.priceRange = [0, 1000];
                this.deliveryDays = 100;
                this.preselectByPrice = false;
                this.preselectByTime = false;
            },
            save() {
                // If this.isApp is true, then the current selected offer ids, filter and a new results request is sent to the controller.
                // At the end a usedFilter event is emitted to tell the App component to close the sidebar and reload the page.
                // If this.isApp is false, then a saved event is emitted to tell the Landing component to close the filter dialog.
                if(this.isApp) {
                    let selected = [];

                    for(let i = 0; i < this.$store.state.StoreSearchResult.length; i++) {
                        if(this.selectBox[this.$store.state.StoreSearchResult[i].sequenceInformation.id]) {
                            selected.push(this.selectBox[this.$store.state.StoreSearchResult[i].sequenceInformation.id])
                        }
                    }

                    // eslint-disable-next-line no-console
                    console.log("selected:" + selected);

                    let selection = {
                        "selected": selected
                    };

                    this.$http.post('/api/select', selection)
                        .then(response => {
                            // eslint-disable-next-line no-console
                            console.log(response);
                        });

                    let filter = {
                        "filter":
                            {
                                "vendors": this.selectedVendors,
                                "price": this.priceRange,
                                "deliveryDays": this.deliveryDays,
                                "preselectByPrice": this.preselectByPrice,
                                "preselectByDeliveryDays": this.preselectByTime
                            }
                    };


                    this.$http.post('/api/filter', filter)
                        .then(response => {
                            // eslint-disable-next-line no-console
                            console.log(filter);
                            // eslint-disable-next-line no-console
                            console.log(response);

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
                                    // eslint-disable-next-line no-console
                                    console.log(this.selectedVendors);
                                    this.$emit('usedFilter');
                                })
                        });

                }
                else {
                    this.$emit('saved')
                }
            }
        }
    }
</script>

<style scoped>

</style>
