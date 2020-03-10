<template>
    <v-app>
        <v-app-bar
                app
                color="primary"
                dark
        >
            <!--            <v-icon v-if="this.$route.path !== '/'" class="ml-3" size="22px" @click="this.$router.push('')">mdi-arrow-left</v-icon>-->
            <v-app-bar-nav-icon v-if="this.$route.path !== '/'" @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
            <v-toolbar-title class="display-1 mx-auto font-weight-medium">DNA Scanner</v-toolbar-title>
        </v-app-bar>

        <v-content>
            <v-navigation-drawer
                    v-if="this.$route.path !== '/'"
                    v-model="drawer"
                    absolute
                    temporary
                    width="500px"
            >
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
                                        <v-checkbox v-for="vendor in vendors"
                                                    :key="vendor.id"
                                                    :label="`${vendor.name}`"
                                                    :value="vendor.id"
                                                    v-model="selectedVendors"></v-checkbox>
                                    </v-col>
                                </v-container>
                            </v-col>
                            <v-card-text>
                                <v-subheader>Select min and max price in Euros(€)</v-subheader>
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
                                <v-subheader>Select max delivery time in days(d)</v-subheader>
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
                    <v-btn color="blue darken-1" text @click="useFilter()">Use Filter</v-btn>
                </v-card-actions>
            </v-navigation-drawer>
            <router-view :key="filter"></router-view>
        </v-content>

    </v-app>
</template>

<script>

    export default {
        name: 'App',
        data() {
            return {
                filter: false,
                drawer: false,
            }
        },
        computed: {
            vendors() {
                return this.$store.state.StoreVendors;
            },
            selectedVendors: {
                get() {
                    return this.$store.state.StoreSelectedVendors;
                },
                set(value) {
                    this.$store.commit('updateSelectedVendors', value)
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
            }
        },
        methods: {
            reset() {
                this.$store.state.StoreSelectedVendors = [0, 1, 2];
                this.$store.state.StorePriceFilterRange = [0, 50];
                this.$store.state.StoreDeliveryDays = 30;
                this.$store.state.StorePreselectByPrice = false;
                this.$store.state.StorePreselectByTime = false;
            },
            useFilter() {

                var filter = {
                    "filter":
                        {
                            "vendors": this.$store.state.StoreSelectedVendors,
                            "price": this.$store.state.StorePriceFilterRange,
                            "deliveryDays": this.$store.state.StoreDeliveryDays,
                            "preselectByPrice": this.$store.state.StorePreselectByPrice,
                            "preselectByDeliveryDays": this.$store.state.StorePreselectByTime
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
                                this.$store.state.StoreCount = response.body.count;
                                this.$store.state.StoreSelectedVendors = this.selectedVendors;
                                // eslint-disable-next-line no-console
                                console.log(this.$store.state.StoreSearchResult);
                                // eslint-disable-next-line no-console
                                console.log(this.$store.state.StoreSelectedVendors);
                                this.drawer = false;
                                this.filter = !this.filter
                            })
                    });

            }
        }
    };
</script>
