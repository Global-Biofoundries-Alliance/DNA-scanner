<template>
    <div>
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
                    <v-row v-for="(n,i) in resultBody.count" :key="i">
                        <v-card width="110px" tile outlined class="pa-2" style="border-right: 0">
                            {{result[i].sequenceInformation.id}}
                        </v-card>
                        <v-card width="150px" tile outlined class="pa-2" style="border-left: 0">
                            {{result[i].sequenceInformation.name}}
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
                    <v-row v-for="(n,i) in resultBody.count" :key="i">
                        <v-hover v-slot:default="{ hover }" v-for="(k,j) in vendors.length" :key="j">
                            <v-card width="200px" class="pt-2 pb-2" tile outlined
                                    :elevation="(hover || result[i].vendors[j].offers[0].selected) ? 16 : 0">
                                <v-card-actions style="padding-top: 2px; padding-bottom: 2px">
                                    <v-card-text class="ml-2 pa-0" style="font-size: 20px">
                                        {{result[i].vendors[j].offers[0].price}}
                                    </v-card-text>
                                    <v-spacer></v-spacer>
                                    <v-card-text class="mr-1 pa-0" style="text-align: right; font-size: 20px">
                                        {{result[i].vendors[j].offers[0].turnoverTime}}
                                    </v-card-text>
                                </v-card-actions>

                                <v-expand-transition v-if="result[i].vendors[j].offers[0].selected === true">
                                    <div
                                            v-if="hover"
                                            class="d-flex transition-fast-in-fast-out grey lighten-2 v-card--reveal display-3"
                                            style="height: 100%; width: 100%"
                                    >
                                        <v-icon class="ml-3" size="22px"
                                                @click="result[i].vendors[j].offers[0].selected = false">
                                            mdi-minus
                                        </v-icon>
                                    </div>
                                </v-expand-transition>

                                <v-expand-transition v-else-if="result[i].vendors[j].offers.length > 1">
                                    <div
                                            v-if="hover"
                                            class="d-flex transition-fast-in-fast-out grey lighten-2 v-card--reveal display-3"
                                            style="height: 100%; width: 100%"
                                    >

                                        <v-icon class="ml-3" size="22px"
                                                @click="dialogShow(i, j)">
                                            mdi-dots-horizontal
                                        </v-icon>

                                    </div>
                                </v-expand-transition>

                                <v-expand-transition v-else>
                                    <div
                                            v-if="hover"
                                            class="d-flex transition-fast-in-fast-out grey lighten-2 v-card--reveal display-3"
                                            style="height: 100%; width: 100%"
                                    >
                                        <v-icon class="ml-3" size="22px"
                                                @click="result[i].vendors[j].offers[0].selected = true">
                                            mdi-plus
                                        </v-icon>
                                    </div>
                                </v-expand-transition>
                            </v-card>
                        </v-hover>
                    </v-row>

                    <v-dialog v-model="dialog" scrollable max-width="300px">
                        <v-card>
                            <v-card-title>Select Offer</v-card-title>
                            <v-divider></v-divider>
                            <v-card-text style="height: 300px" class="pl-0 pr-0 pt-3">
                                <v-card-actions class="pl-12 pr-12">
                                    <v-icon class="mr-3" medium>{{icons.mdiCurrencyUsd}}</v-icon>
                                    <v-spacer></v-spacer>
                                    <v-icon class="ml-3" size="22px">mdi-watch</v-icon>
                                </v-card-actions>
                                <v-list rounded>
                                    <v-list-item-group v-model="dialogItem">
                                        <v-list-item v-for="(n, k) in dialogList" :key="k">
                                            <v-list-item-content>
                                                <v-card-actions class="pl-8 pr-8">
                                                    <span>{{n.price}}</span>
                                                    <v-spacer></v-spacer>
                                                    <span>{{n.turnoverTime}}</span>
                                                </v-card-actions>
                                            </v-list-item-content>
                                        </v-list-item>
                                    </v-list-item-group>
                                </v-list>
                            </v-card-text>
                            <v-divider></v-divider>
                            <v-card-actions>
                                <v-btn color="blue darken-1" text
                                       @click="dialogClose()">Close
                                </v-btn>
                                <v-btn color="blue darken-1" text
                                       @click="dialogSave()">Save
                                </v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-dialog>

                </v-col>
                <p>{{dialogItem}}</p>
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
                },
                dialogItem: null,
                dialog: false,
                dialogList: []
            }
        },
        computed: {
            result() {
                return this.$store.state.StoreSearchResult.result;
            },
            resultBody() {
                return this.$store.state.StoreSearchResult;
            },
            vendors() {
                return this.$store.state.StoreVendors;
            },
            permanentElevation() {
                return this.$store.state.StorePermanentElevation;
            }
        },
        methods: {
            dialogShow(i, j) {
                this.dialog = true;
                this.dialogList = this.$store.state.StoreSearchResult.result[i].vendors[j].offers
            },
            dialogSave() {
                this.dialog = false;
                this.dialogList[this.dialogItem].selected = true;
                this.dialogItem = null
            },
            dialogClose() {
                this.dialog = false;
                this.dialogItem = null
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
