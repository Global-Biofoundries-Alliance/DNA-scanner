<template>
    <div>
        <div>
            <v-navigation-drawer permanent style="padding-top: 7%; padding-bottom: 12%" width="25%">
                <v-card>
                    <v-card-title>
                        <span class="headline mx-auto">Filter</span>
                    </v-card-title>
                    <v-card-text>
                        <v-container>
                            <v-row>
                                <v-col cols="12" sm="6" md="4">
                                    <v-subheader>DNA Supplier</v-subheader>
                                    <v-checkbox v-model="twist" label="TWIST" hide-details></v-checkbox>
                                    <v-checkbox v-model="idt" label="IDT" hide-details></v-checkbox>
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
                                                    v-model="slider"
                                                    class="align-center"
                                                    :max="max"
                                                    :min="min"
                                                    hide-details
                                            >
                                                <template v-slot:append>
                                                    <v-text-field
                                                            v-model="slider"
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
                        <v-btn class="mx-auto" color="blue darken-1" text @click="filter = true">Use Filter</v-btn>
                    </v-card-actions>
                </v-card>
            </v-navigation-drawer>
        </div>
        <div>
            <p style="margin-left: 26%;margin-bottom: 60%">Your file: {{ file.name }}</p>
        </div>
    </div>
</template>

<script>
    export default {
        name: "Search",
        data() {
            return {
                min: 1,
                max: 1000,
                range: [1, 100],
                slider: 7,
                twist: true,
                idt: true,
                filter: false
            }
        },
        props: ['file']
    }
</script>

<style scoped>

</style>
