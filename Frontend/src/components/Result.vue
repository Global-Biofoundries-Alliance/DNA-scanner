<template>
    <div>
        <div>
            <p v-if="globalMessage !== ''" class="text-center font-weight-light headline">{{globalMessage}}</p>
            <v-app id="inspire">
                <v-data-table
                        :headers="headers"
                        :items="results"
                        :expanded.sync="expanded"
                        item-key="sequenceInformation.name"
                        class="elevation-1"
                        show-expand
                >

                    <template v-for="(n,i) in slots.length" v-slot:[slots[i].name]="{header}">
                        <v-chip :color=vendors[slots[i].key].color :key="slots[i].name"
                                @click="selectAll(slots[i].key)">
                            {{header.text}}
                        </v-chip>
                        <v-tooltip right :key="slots[i].key" v-if="vendorMessage[slots[i].key].messages.length !== 0 ">
                            <template v-slot:activator="{ on }">
                                <v-icon v-on="on">mdi-alert</v-icon>
                            </template>
                            <span>{{vendorMessage[slots[i].key].messages[0]}}</span>
                        </v-tooltip>
                    </template>

                    <template v-for="(n,i) in slots.length" v-slot:[slots[i].price]="{header}">
                        <div :key="i">
                            <p class="mb-0">Price</p>
                            <p class="mb-0" v-if="slots[i].key === 2">{{computedPriceTotal[slots[i].key]}}
                                ({{computedPriceOverview[slots[i].key]}})</p>
                        </div>
                    </template>

                    <template v-for="(n,i) in slots.length" v-slot:[slots[i].time]="{header}">
                        <div :key="i">
                            <p class="mb-0">Time</p>
                            <p class="mb-0" v-if="slots[i].key === 2">{{computedTimeTotal[slots[i].key]}}
                                ({{computedTimeOverview[slots[i].key]}})</p>
                        </div>
                    </template>

                    <template v-for="(n,i) in slots.length" v-slot:[slots[i].item]="{item, value}">
                        <div :key="i">
                            <v-tooltip v-if="item.vendors[slots[i].key].offers.length === 0" left>
                                <template v-slot:activator="{ on }">
                                    <v-icon :color=vendors[slots[i].key].color v-on="on">mdi-comment-alert</v-icon>
                                </template>
                                <span>No offer available</span>
                            </v-tooltip>
                            <v-tooltip v-else-if="item.vendors[slots[i].key].offers[0].offerMessage.length !== 0" left>
                                <template v-slot:activator="{ on }">
                                    <v-icon :color=vendors[slots[i].key].color v-on="on">mdi-comment-alert</v-icon>
                                </template>
                                <span>{{item.vendors[slots[i].key].offers[0].offerMessage[0].text}}</span>
                            </v-tooltip>
                            <v-checkbox v-else
                                        v-model="selectBox[item.sequenceInformation.id]"
                                        @change="select(item.sequenceInformation.id, item.vendors[slots[i].key].offers, item.vendors[slots[i].key].offers[0])"
                                        :value="item.vendors[slots[i].key].offers[0].key"
                                        :color=vendors[slots[i].key].color
                            >
                            </v-checkbox>
                        </div>
                    </template>

                    <template v-for="(n,i) in slots.length" v-slot:[slots[i].priceItem]="{item, value}">
                        <div :key="i">
                            <p v-if="slots[i].key === 0 || slots[i].key === 1" class="pb-0 mb-0">
                                <v-tooltip left>
                                    <template v-slot:activator="{ on }">
                                        <v-icon :color=vendors[slots[i].key].color v-on="on">mdi-comment-alert</v-icon>
                                    </template>
                                    <span>Price not available from vendor</span>
                                </v-tooltip>
                            </p>
                            <p v-else-if="item.vendors[slots[i].key].offers.length === 0 || item.vendors[slots[i].key].offers[0].offerMessage.length !== 0"
                               class="mb-0">
                                0
                            </p>
                            <v-chip v-else-if="selectBox[item.sequenceInformation.id] === item.vendors[slots[i].key].offers[0].key"
                                    :color=vendors[slots[i].key].color>
                                {{value}} {{item.vendors[slots[i].key].offers[0].currency}}
                            </v-chip>
                            <p v-else class="mb-0">{{value}} {{item.vendors[slots[i].key].offers[0].currency}}</p>
                        </div>
                    </template>

                    <template v-for="(n,i) in slots.length" v-slot:[slots[i].timeItem]="{item, value}">
                        <div :key="i">
                            <p v-if="slots[i].key === 0 || slots[i].key === 1" class="pb-0 mb-0">
                                <v-tooltip left>
                                    <template v-slot:activator="{ on }">
                                        <v-icon :color=vendors[slots[i].key].color v-on="on">mdi-comment-alert</v-icon>
                                    </template>
                                    <span>Time not available from vendor</span>
                                </v-tooltip>
                            </p>
                            <p v-else-if="item.vendors[slots[i].key].offers.length === 0 || item.vendors[slots[i].key].offers[0].offerMessage.length !== 0"
                               class="mb-0">0</p>
                            <v-chip v-else-if="selectBox[item.sequenceInformation.id] === item.vendors[slots[i].key].offers[0].key"
                                    :color=vendors[slots[i].key].color>{{value}} bd.
                            </v-chip>
                            <p v-else class="mb-0">{{value}} bd.</p>
                        </div>
                    </template>

                    <template v-slot:expanded-item="{item, headers}">
                        <td :colspan="headers.length" class="pa-0">
                            <v-row>
                                <v-col v-for="(n,i) in selectedVendors.length" :key="i">
                                    <v-data-table
                                            :headers="headersSecond[i]"
                                            :items="item.vendors[selectedVendors[i]].offers"
                                            item-key="sequenceInformation.name"
                                            class="elevation-1"
                                            hide-default-footer
                                    >
                                        <template v-slot:[slots[i].item]="props">
                                            <v-tooltip v-if="props.item.offerMessage.length !== 0" left>
                                                <template v-slot:activator="{ on }">
                                                    <v-icon :color=vendors[selectedVendors[i]].color v-on="on">
                                                        mdi-comment-alert
                                                    </v-icon>
                                                </template>
                                                <span>{{props.item.offerMessage[0].text}}</span>
                                            </v-tooltip>
                                            <v-checkbox v-else
                                                        v-model="selectBox[item.sequenceInformation.id]"
                                                        @change="select(item.sequenceInformation.id, item.vendors[selectedVendors[i]].offers, props.item)"
                                                        :value="props.item.key"
                                                        :color=vendors[selectedVendors[i]].color
                                            >
                                            </v-checkbox>
                                        </template>

                                        <template v-slot:item.price="props">
                                            <p v-if="selectedVendors[i] === 0 || selectedVendors[i] === 1" class="pb-0">
                                                <v-tooltip left>
                                                    <template v-slot:activator="{ on }">
                                                        <v-icon :color=vendors[selectedVendors[i]].color v-on="on">
                                                            mdi-comment-alert
                                                        </v-icon>
                                                    </template>
                                                    <span>Price not available from vendor</span>
                                                </v-tooltip>
                                            </p>
                                            <p v-else-if="props.item.offerMessage.length !== 0"
                                               class="mb-0">0</p>
                                            <v-chip v-else-if="selectBox[item.sequenceInformation.id] === props.item.key"
                                                    :color=vendors[selectedVendors[i]].color>
                                                {{props.value}} {{props.item.currency}}
                                            </v-chip>
                                            <p v-else class="mb-0">{{props.value}} {{props.item.currency}}</p>
                                        </template>

                                        <template v-slot:item.turnoverTime="props">
                                            <p v-if="selectedVendors[i] === 0 || selectedVendors[i] === 1" class="pb-0">
                                                <v-tooltip left>
                                                    <template v-slot:activator="{ on }">
                                                        <v-icon :color=vendors[selectedVendors[i]].color v-on="on">
                                                            mdi-comment-alert
                                                        </v-icon>
                                                    </template>
                                                    <span>Time not available from vendor</span>
                                                </v-tooltip>
                                            </p>
                                            <p v-else-if="props.item.offerMessage.length !== 0"
                                               class="mb-0">0</p>
                                            <v-chip v-else-if="selectBox[item.sequenceInformation.id] === props.item.key"
                                                    :color=vendors[selectedVendors[i]].color>
                                                {{props.value}} bd.
                                            </v-chip>
                                            <p v-else class="mb-0">{{props.value}} bd.</p>
                                        </template>
                                    </v-data-table>
                                </v-col>
                            </v-row>
                        </td>
                    </template>
                </v-data-table>
            </v-app>
        </div>
    </div>
</template>

<script>
    export default ({
        name: 'Result',
        data() {
            return {
                computedSlots: [],
                computedHeaders: [],
                computedHeadersSecond: {
                    0: [],
                    1: [],
                    2: []
                },
                expanded: [],
                computedPriceOverview: [],
                computedPriceTotal: [],
                computedTimeOverview: [],
                computedTimeTotal: [],
                computedSelectedAll: [],

            }
        },
        methods: {
            selectAll(vendorKey) {
                if (this.computedSelectedAll[vendorKey]) {
                    this.results.forEach(i => {
                        if (i.vendors[vendorKey].offers.length !== 0 && i.vendors[vendorKey].offers[0].offerMessage.length === 0) {
                            this.selectBox[i.sequenceInformation.id] = false;
                        }
                    });
                    this.computedPriceOverview[vendorKey] = 0;
                    this.computedTimeOverview[vendorKey] = 0;
                    this.computedSelectedAll[vendorKey] = false;
                    this.$forceUpdate();
                } else {
                    this.computedPriceOverview[vendorKey] = 0;
                    this.computedTimeOverview[vendorKey] = 0;
                    this.results.forEach(i => {
                        if (i.vendors[vendorKey].offers.length !== 0 && i.vendors[vendorKey].offers[0].offerMessage.length === 0) {
                            this.selectBox[i.sequenceInformation.id] = i.vendors[vendorKey].offers[0].key;
                            if (i.vendors[vendorKey].offers[0].price > 0) {
                                this.computedPriceOverview[vendorKey] = Math.round((this.computedPriceOverview[vendorKey] + i.vendors[vendorKey].offers[0].price) * 100) / 100;
                            }
                            if (i.vendors[vendorKey].offers[0].turnoverTime > this.computedTimeOverview[vendorKey]) {
                                this.computedTimeOverview[vendorKey] = i.vendors[vendorKey].offers[0].turnoverTime
                            }
                            this.$forceUpdate();
                        }
                    });
                    this.computedSelectedAll[vendorKey] = true;
                    for (let j = 0; j < this.computedSelectedAll.length; j++) {
                        if (j !== vendorKey) {
                            this.computedPriceOverview[j] = 0;
                            this.computedTimeOverview[j] = 0;
                            this.results.forEach(i => {
                                if (i.vendors[j].offers.length !== 0 && i.vendors[j].offers[0].offerMessage.length === 0) {
                                    if (this.selectBox[i.sequenceInformation.id] === i.vendors[j].offers[0].key) {
                                        if (i.vendors[j].offers[0].price > 0) {
                                            this.computedPriceOverview[j] = Math.round((this.computedPriceOverview[j] + i.vendors[j].offers[0].price) * 100) / 100;
                                        }
                                        if (i.vendors[j].offers[0].turnoverTime > this.computedTimeOverview[j]) {
                                            this.computedTimeOverview[j] = i.vendors[j].offers[0].turnoverTime
                                        }
                                    }
                                }
                            });
                            this.$forceUpdate();
                            this.computedSelectedAll[j] = false
                        }
                    }
                }
            },
            select(sequenceId, offers, item) {
                let index = offers.indexOf(item);
                let temp = offers[0];
                offers[0] = item;
                offers[index] = temp;

                for (let j = 0; j < this.computedSelectedAll.length; j++) {
                    this.computedPriceOverview[j] = 0;
                    this.computedTimeOverview[j] = 0;
                    this.computedPriceTotal[j] = 0;
                    this.computedTimeTotal[j] = 0;
                    this.results.forEach(i => {
                        if (i.vendors[j].offers.length !== 0 && i.vendors[j].offers[0].offerMessage.length === 0) {
                            if (i.vendors[j].offers[0].price > 0) {
                                this.computedPriceTotal[j] = Math.round((this.computedPriceTotal[j] + i.vendors[j].offers[0].price) * 100) / 100;
                            }
                            if (i.vendors[j].offers[0].turnoverTime > this.computedTimeTotal[j]) {
                                this.computedTimeTotal[j] = i.vendors[j].offers[0].turnoverTime
                            }
                            if (this.selectBox[i.sequenceInformation.id] === i.vendors[j].offers[0].key) {
                                if (i.vendors[j].offers[0].price > 0) {
                                    this.computedPriceOverview[j] = Math.round((this.computedPriceOverview[j] + i.vendors[j].offers[0].price) * 100) / 100;
                                }
                                if (i.vendors[j].offers[0].turnoverTime > this.computedTimeOverview[j]) {
                                    this.computedTimeOverview[j] = i.vendors[j].offers[0].turnoverTime
                                }
                            }
                        }
                    });
                    this.$forceUpdate();
                }
                // eslint-disable-next-line no-console
                console.log(this.selectBox)

            },
        },
        computed: {
            vendors() {
                return this.$store.state.StoreVendors
            },
            selectedVendors() {
                return this.$store.state.StoreSelectedVendors
            },
            headers() {
                return this.computedHeaders
            },
            headersSecond() {
                return this.computedHeadersSecond
            },
            results() {
                return this.$store.state.StoreSearchResult
            },
            slots() {
                return this.computedSlots
            },
            vendorMessage() {
                return this.$store.state.StoreVendorMessage
            },
            globalMessage() {
                return this.$store.state.StoreGlobalMessage
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
        created() {
            for (let j = 0; j < this.vendors.length; j++) {
                this.computedPriceOverview[j] = 0;
                this.computedPriceTotal[j] = 0;
                this.computedTimeOverview[j] = 0;
                this.computedTimeTotal[j] = 0;
                this.computedSelectedAll[j] = false;
            }
            this.selectBox = [];
            this.results.forEach(i => {
                for (let j = 0; j < i.vendors.length; j++) {
                    for (let k = 0; k < i.vendors[j].offers.length; k++) {
                        if (i.vendors[j].offers[k].selected) {
                            this.selectBox[i.sequenceInformation.id] = i.vendors[j].offers[k].key;
                            if (i.vendors[j].offers[k].price > 0) {
                                this.computedPriceOverview[i.vendors[j].key] = Math.round((this.computedPriceOverview[i.vendors[j].key] + i.vendors[j].offers[k].price) * 100) / 100;
                            }
                            if (i.vendors[j].offers[k].turnoverTime > this.computedTimeOverview[i.vendors[j].key]) {
                                this.computedTimeOverview[i.vendors[j].key] = i.vendors[j].offers[k].turnoverTime
                            }
                        }
                        if (k === 0 && i.vendors[j].offers[0].offerMessage.length === 0 && i.vendors[j].offers.length !== 0) {
                            if (i.vendors[j].offers[k].price > 0) {
                                this.computedPriceTotal[i.vendors[j].key] = Math.round((this.computedPriceTotal[i.vendors[j].key] + i.vendors[j].offers[k].price) * 100) / 100;
                            }
                            if (i.vendors[j].offers[k].turnoverTime > this.computedTimeTotal[i.vendors[j].key]) {
                                this.computedTimeTotal[i.vendors[j].key] = i.vendors[j].offers[k].turnoverTime
                            }
                        }
                    }
                }
            });

            this.computedHeaders.push({
                text: 'Sequence',
                align: 'left',
                sortable: false,
                value: 'sequenceInformation.name',
            });
            this.selectedVendors.sort();
            for (let i = 0; i < this.selectedVendors.length; i++) {
                this.computedSlots.push({
                    key: this.selectedVendors[i],
                    name: "header.selected" + this.vendors[this.selectedVendors[i]].name,
                    price: "header.vendors[" + this.selectedVendors[i] + "].offers[0].price",
                    time: "header.vendors[" + this.selectedVendors[i] + "].offers[0].turnoverTime",
                    item: "item.selected" + this.vendors[this.selectedVendors[i]].name,
                    priceItem: "item.vendors[" + this.selectedVendors[i] + "].offers[0].price",
                    timeItem: "item.vendors[" + this.selectedVendors[i] + "].offers[0].turnoverTime",

                });
                this.computedHeaders.push(
                    {
                        text: this.vendors[this.selectedVendors[i]].name,
                        value: 'selected' + this.vendors[this.selectedVendors[i]].name,
                        sortable: false,
                    },
                    {
                        text: '',
                        value: 'vendors[' + this.selectedVendors[i] + '].offers[0].price',
                        sortable: false,
                    },
                    {
                        text: '',
                        value: 'vendors[' + this.selectedVendors[i] + '].offers[0].turnoverTime',
                        sortable: false,
                    }
                );
                this.computedHeadersSecond[i].push(
                    {
                        text: this.vendors[this.selectedVendors[i]].name,
                        value: 'selected' + this.vendors[this.selectedVendors[i]].name,
                        sortable: false,
                    },
                    {
                        text: 'Price',
                        value: 'price',
                        sortable: false,
                    },
                    {
                        text: 'Time',
                        value: 'turnoverTime',
                        sortable: false,
                    }
                )
            }
            this.computedHeaders.push({
                text: '',
                value: 'data-table-expand'
            });

            // // eslint-disable-next-line no-console
            // console.log(this.computedSlots);
            // // eslint-disable-next-line no-console
            // console.log(this.computedHeaders);
            // // eslint-disable-next-line no-console
            // console.log(this.computedHeadersSecond);
            // // eslint-disable-next-line no-console
            // console.log(this.selectedVendors)
        }
    })
</script>

<style lang="sass">
    @import '../sass/variables.sass'

</style>

<style>
    .v-data-table {
        border-radius: 10px;
    }
</style>
