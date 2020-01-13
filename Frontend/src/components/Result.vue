<template>
    <div>
        <br><br>
        <p style="text-align: center">Your file: {{ fileName }}</p>
        <br><br>
        <v-container fluid>
            <v-row>
                <v-col>
                    <v-row
                            class="grey lighten-5"
                    >
                        <v-card
                            outlined
                            style="margin-left: 43.2%"
                            width="240px"
                            >
                            <v-list-item three-line>
                                <v-list-item-content>
                                    <v-list-item-title class="headline mb-1" style="text-align: center">TWIST
                                    </v-list-item-title>
                                </v-list-item-content>
                            </v-list-item>

                            <v-card-actions>
                                <v-icon class="ml-3">mdi-watch</v-icon>
                                <v-spacer></v-spacer>
                                <v-icon class="mr-3">{{icons.mdiCurrencyUsd}}</v-icon>
                            </v-card-actions>
                        </v-card>
                        <v-card
                                outlined
                                style="margin-left: 0.7%"
                                width="238px"
                        >
                            <v-list-item three-line>
                                <v-list-item-content>
                                    <v-list-item-title class="headline mb-1" style="text-align: center">IDT
                                    </v-list-item-title>
                                </v-list-item-content>
                            </v-list-item>

                            <v-card-actions>
                                <v-icon class="ml-3">mdi-watch</v-icon>
                                <v-spacer></v-spacer>
                                <v-icon class="mr-3">{{icons.mdiCurrencyUsd}}</v-icon>
                            </v-card-actions>
                        </v-card>
                    </v-row>
                </v-col>
            </v-row>
        </v-container>
        <v-row style="margin-left: 15.5%">
            <p>Seq.Nr.</p>
            <p style="margin-left: 2%">Sequence</p>
        </v-row>
<!--        this is the part where the rows for the results are created -->
        <v-row no-gutters
                v-for="(n,i) in 10"
                :key="i"
                style="margin-left: 15%">
            <v-col cols="4" style="height: 100px;">
                <v-card
                        style="height: 5%; padding-top: 3% ;padding-bottom: 12.25%"
                        outlined
                        tile
                >
                    <v-row class="ml-3">
                        <p style="margin-left: 2.5%" class="mb-0">
                            {{n}}
                        </p>
                        <p style="margin-left: 9%" class="mb-0">
                            {{result[i].sequenceinformation.name}}
                        </p>
                        <v-spacer></v-spacer>
                        <v-col cols="2" sm="6" class="mt-n4">
                            <v-select
                                    v-model="value[i]"
                                    :items="items"
                                    chips
                                    label="Select Merchant"
                                    multiple
                                    solo
                            ></v-select>
                        </v-col>
                    </v-row>
                </v-card>
            </v-col>
            <v-col :cols="2">
                <v-card
                        class="pa-4"
                        outlined
                        tile
                >
                    <v-row class="ml-2">
                        <p>
                            {{result[i].offers[0].turnovertime}}
                        </p>
                        <v-spacer></v-spacer>
                        <p class="mr-4">
                            {{result[i].offers[0].price}}
                        </p>
                    </v-row>
                </v-card>
            </v-col>
            <v-col :cols="2" class="ml-3">
                <v-card
                        class="pa-4"
                        outlined
                        tile
                >
                    <v-row class="ml-2">
                        <p>
                            {{result[i].offers[1].turnovertime}}
                        </p>
                        <v-spacer></v-spacer>
                        <p class="mr-4">
                            {{result[i].offers[1].price}}
                        </p>
                    </v-row>
                </v-card>
            </v-col>
        </v-row>
    </div>
</template>

<script>
    import {mdiCurrencyUsd} from '@mdi/js';

    export default {
        name: "Result",
        data() {
            return {
                fileName: this.$store.state.StoreFile.name,
                icons: {
                    mdiCurrencyUsd
                },
                alignmentsAvailable: [
                    'start',
                    'center',
                    'end',
                    'baseline',
                    'stretch',
                ],
                alignment: 'right',
                dense: false,
                justifyAvailable: [
                    'start',
                    'center',
                    'end',
                    'space-around',
                    'space-between',
                ],
                items: ['TWIST', 'IDT'],
                value: [],
            }
        },
        computed: {
            result() {
                return this.$store.state.StoreResult;
            }
        }

    }
</script>

<style scoped>

</style>
