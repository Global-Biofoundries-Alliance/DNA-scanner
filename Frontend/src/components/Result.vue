<template>
    <div>
        <p style="text-align: center">Your file: {{ file.name }}</p>
        <p style="text-align: center">Number of Sequences: XY</p>
        <v-container fluid>
            <v-row>
                <v-col>
                    <v-row
                            :align="alignment"
                            class="grey lighten-5"
                    >
                        <v-card
                            outlined
                            style="margin-left: 50%"
                            width="24.5%"
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
                        <v-spacer></v-spacer>
                        <v-card
                                outlined
                                width="24.5%"
                                class="ml-n2"
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
        <v-row class="ml-3">
            <p>Seq.Nr.</p>
            <p style="margin-left: 3%">Sequence</p>
        </v-row>
        <v-row no-gutters
                v-for="n in 5"
                :key="n">
            <v-col cols="6">
                <v-card
                        class="pa-4"
                        outlined
                        tile
                >
                    <v-row class="ml-3">
                        <p>
                            {{n}}
                        </p>
                        <p style="margin-left: 9%">
                            atggtgccagtgagcgggaaatcaggcagttcaaacacggctgtatcagcgagtgacaac
                        </p>
                        <v-chip class="ml-8">TWIST</v-chip>
                        <v-chip class="ml-8">IDT</v-chip>
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
                            10
                        </p>
                        <v-spacer></v-spacer>
                        <p class="mr-4">
                            99.9
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
                            99.9
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
        props: ['file'],
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
            }
        }

    }
</script>

<style scoped>

</style>
