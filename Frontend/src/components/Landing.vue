<template>
    <div>
        <v-container class="verticalSpace">
            <v-file-input v-model="file" label="File input" outlined rounded></v-file-input>
        </v-container>

        <v-row justify="center">
            <v-dialog v-model="dialog" persistent max-width="600px">
                <template v-slot:activator="{ on }">
                    <v-btn @click="dialog=true">Add Filter</v-btn>
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
                        <v-spacer></v-spacer>
                        <v-btn color="blue darken-1" text @click="dialog = false">Close</v-btn>
                        <v-btn color="blue darken-1" text @click="dialog = false">Save</v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
        </v-row>
        <br>
        <v-row justify="center">
            <v-btn color="primary" style="width: 20%;" class="align-center" @click="searchNow()"> Search</v-btn>
        </v-row>
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
                slider: 7,
                dialog: false,
                twist: true,
                idt: true,
                res: []
            }
        },

        methods: {
            searchNow() {
                this.$emit('gotFile', this.file);
                this.$http.post('upload', {headers:{'Access-Control-Allow-Origin': 'true'}})
                    .then(response => {
                        this.res = response.body.result[0];
                        this.$emit('gotRes', this.res);
                        this.$emit('switch');
                    });
            }
        }
    };
</script>

<style>
    .verticalSpace {
        margin-top: 10%;
    }
</style>

