<template>
    <div>
        <!--        <v-container style="margin-right: 0; margin-left: 600px; margin-top: 30px">-->
        <!--            <v-row>-->
        <!--                <v-card width="200px" style="text-align: center" tile outlined class="pa-6" v-for="vendor in vendors" :key="vendor.name">-->
        <!--                    {{vendor.name}}-->
        <!--                </v-card>-->
        <!--            </v-row>-->
        <!--            <v-row>-->
        <!--                <v-card width="200px" tile outlined class="pa-2 mt-12" v-for="i in vendors.length" :key="i">-->
        <!--                    {{i}}-->
        <!--                </v-card>-->
        <!--            </v-row>-->
        <!--        </v-container>-->
        <!--        <v-container style="margin-top: 50px">-->
        <!--            <v-row class="mb-4">-->
        <!--                    <v-card width="110px" tile outlined class="pa-2" style="border-right: 0">-->
        <!--                        ID-->
        <!--                    </v-card>-->
        <!--                    <v-card width="150px" tile outlined class="pa-2" style="border-left: 0">-->
        <!--                        Name-->
        <!--                    </v-card>-->
        <!--            </v-row>-->
        <!--            <v-row v-for="(n,i) in 10" :key="i">-->
        <!--                    <v-card width="110px" tile outlined class="pa-2" style="border-right: 0">-->
        <!--                        {{result[i].sequenceinformation.id}}-->
        <!--                    </v-card>-->
        <!--                    <v-card width="150px" tile outlined class="pa-2" style="border-left: 0">-->
        <!--                        {{result[i].sequenceinformation.name}}-->
        <!--                    </v-card>-->
        <!--            </v-row>-->
        <!--        </v-container>-->
        <v-container>
            <v-row>
                <v-col cols="4" style="margin-top: 100px">
                    <v-row class="mb-4">
                        <v-card width="110px" tile outlined class="pa-2" style="border-right: 0">
                            ID
                        </v-card>
                        <v-card width="150px" tile outlined class="pa-2" style="border-left: 0">
                            Name
                        </v-card>
                    </v-row>
                    <v-row v-for="(n,i) in 1" :key="i">
                        <v-card width="110px" tile outlined class="pa-2" style="border-right: 0">
                            {{result[i].sequenceinformation.id}}
                        </v-card>
                        <v-card width="150px" tile outlined class="pa-2" style="border-left: 0">
                            {{result[i].sequenceinformation.name}}
                        </v-card>
                    </v-row>
                </v-col>
                <v-col cols="8">
                    <v-row>
                        <v-card width="200px" style="text-align: center" tile outlined class="pa-6"
                                v-for="vendor in vendors" :key="vendor.name">
                            {{vendor.name}}
                        </v-card>
                    </v-row>
                    <v-row class="mb-4">
                        <v-card width="200px" tile outlined class="mt-6" v-for="i in vendors.length" :key="i">
                            <v-card-actions>
                                <v-icon class="mr-3" medium>{{icons.mdiCurrencyUsd}}</v-icon>
                                <v-spacer></v-spacer>
                                <v-icon class="ml-3" size="22px">mdi-watch</v-icon>
                            </v-card-actions>
                        </v-card>
                    </v-row>
                    <v-row v-for="(n,i) in 1" :key="i">
                        <v-hover v-slot:default="{ hover }" v-for="(k,j) in vendors.length" :key="j">
                            <v-card width="200px" class="pt-2 pb-2" tile outlined
                                    :elevation="(hover || permanentElevation[i][j]) ? 16 : 0">
                                <v-card-actions style="padding-top: 2px; padding-bottom: 2px">
                                    <v-card-text class="ml-2 pa-0" style="font-size: 20px">
                                        {{j}}
                                    </v-card-text>
                                    <v-spacer></v-spacer>
                                    <v-card-text class="mr-1 pa-0" style="text-align: right; font-size: 20px">
                                        {{j + 1}}
                                    </v-card-text>
                                </v-card-actions>

                                <v-expand-transition v-if="permanentElevation[i][j] === true">
                                    <div
                                            v-if="hover"
                                            class="d-flex transition-fast-in-fast-out grey lighten-2 v-card--reveal display-3"
                                            style="height: 100%; width: 100%"
                                    >
                                        <v-icon class="ml-3" size="22px" @click="permanentElevation[i][j] = false">
                                            mdi-minus
                                        </v-icon>
                                    </div>
                                </v-expand-transition>

                                <v-expand-transition v-else>
                                    <div
                                            v-if="hover"
                                            class="d-flex transition-fast-in-fast-out grey lighten-2 v-card--reveal display-3"
                                            style="height: 100%; width: 100%"
                                    >
                                        <v-icon class="ml-3" size="22px" @click="permanentElevation[i][j] = true">
                                            mdi-plus
                                        </v-icon>
                                    </div>
                                </v-expand-transition>
                            </v-card>
                        </v-hover>
                    </v-row>
                </v-col>
                <p>{{permanentElevation}} e</p>
            </v-row>
        </v-container>
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
                }
            }
        },
        computed: {
            result() {
                return this.$store.state.StoreSearchResult;
            },
            vendors() {
                return this.$store.state.StoreVendors;
            },
            permanentElevation() {
                return this.$store.state.StorePermanentElevation;
            }
        }

    }
</script>

<style scoped>
    .v-card--reveal {
        align-items: center;
        bottom: 0;
        justify-content: center;
        opacity: .5;
        position: absolute;
        width: 100%;
    }
</style>
