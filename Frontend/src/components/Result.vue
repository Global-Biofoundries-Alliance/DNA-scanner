<template>
    <div>
        <br><br>
        <p style="text-align: center">Your file: {{ file.name }}</p>
        <p style="text-align: center">Number of Sequences: XY</p>
        <br><br>
        <v-container fluid>
            <v-row>
                <v-col>
                    <v-row
                            :align="alignment"
                            class="grey lighten-5"
                    >
                        <v-card
                            outlined
                            style="margin-left: 40%"
                            width="21%"
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
                                style="margin-left: 1%"
                                width="21%"
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
        <v-row no-gutters
                v-for="n in 1"
                :key="n"
                style="margin-left: 15%">
            <v-col cols="4">
                <v-card
                        style="height: 5%; padding-top: 3% ;padding-bottom: 12.25%"
                        outlined
                        tile
                >
                    <v-row class="ml-3">
                        <p style="margin-left: 2.5%">
                            {{n}}
                        </p>
                        <p style="margin-left: 9%">
                            {{res.sequenceinformation.name}}
                        </p>
                        <v-spacer></v-spacer>
                        <v-col cols="2" sm="6" class="mt-n4">
                            <v-select
                                    v-model="value"
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
                            {{res.offers[0].turnovertime}}
                        </p>
                        <v-spacer></v-spacer>
                        <p class="mr-4">
                            {{res.offers[0].price}}
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
                            8
                        </p>
                        <v-spacer></v-spacer>
                        <p class="mr-4">
                            1.0
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
        props: ['file', 'res'],
        data() {
            return {
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
        }

    }
</script>

<style scoped>

</style>
