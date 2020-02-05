<template>
    <v-app>
        <v-app-bar
                app
                color="primary"
                dark
        >
            <v-app-bar-nav-icon v-if="this.$route.path === '/result'" @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
            <v-toolbar-title class="display-1 mx-auto font-weight-medium">DNA Scanner</v-toolbar-title>
        </v-app-bar>

        <v-content>
            <v-navigation-drawer
                    v-if="this.$route.path === '/result'"
                    v-model="drawer"
                    absolute
                    temporary
                    width="500px"
            >
                <v-card-title>
                    <span class="headline" >Filter</span>
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
                    <v-btn color="blue darken-1" text @click="reset()">Reset</v-btn>
                    <v-btn color="blue darken-1" text @click="drawer = false">Use Filter</v-btn>
                </v-card-actions>
            </v-navigation-drawer>
            <router-view></router-view>
        </v-content>

    </v-app>
</template>

<script>

    export default {
        name: 'App',
        data() {
            return {
                drawer: false,
                min: 1,
                max: 1000,
                range: [1, 100],
                deliveryDays: 7,
            }
        },
        computed: {
            vendors() {
                return this.$store.state.StoreVendors;
            }
        },
        methods: {
            reset() {
                for(let i = 0; i < this.$store.state.StoreVendors.length; i++) {
                    this.$store.state.StoreVendors[i].value = true;
                }
                this.range = [1, 100];
                this.deliveryDays = 7;
            }
        }
    };
</script>
