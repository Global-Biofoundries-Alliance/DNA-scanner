<!-- The Result component is the largest and most complex component. We have the following parts:
1. Template
    Here we have a paragraph over the data table which shows a general global message if one exists,
    a data table which you see when you get to the result page and a data table which is inside the first data table
    to be able to expand a row to show multiple offers by the vendors for one sequence.
2. Script
    It includes the methods selectAll() and select() which are responsible for selecting all available offers from
    one vendor by clicking on the vendor button from the header and for a single select by clicking on any checkbox
    Then we have a long computed list which gives us the possibility to use the global variables from the store.js file
    At the end we have a big created() part because it is responsible to show the preselected offers when opening the
    result page and accordingly computing the total price and maximum time for each vendor.
    It also creates the headers list for the first and second data table dynamically depending on your selection in the
    filter from the landing page.
-->
<template>
    <div>
        <div>
            <p v-if="globalMessage !== ''" class="text-center font-weight-light headline">{{globalMessage}}</p>
            <v-app id="inspire">
                <!--
                This v-data-table has the props headers, which are created in created() part at the bottom,
                items, which are in this case the results we get from the controller, expanded.sync, which
                saves which rows are expanded, and show-expand, which shows the arrows at the end
                to be able to expand a row.
                By giving the headers and items the values will be displayed automatically. That means if you
                just want to display simple data you don't need to do any further changes. But in our case we need to
                change the header and the columns to our needs. For that we use the template tag with the v-slot directive
                to know which column you want to change. To make the table dynamic and not hard coded a slots array is
                created at the created() part and its elements are used as the name says in the v-slot directive.
                -->
                <v-data-table
                        :headers="headers"
                        :items="results"
                        :expanded.sync="expanded"
                        item-key="sequenceInformation.name"
                        class="elevation-1"
                        show-expand
                >

                    <!-- This template tag changes the vendor name in the header by adding a v-chip around it
                         and adds an error sign if an error occurred
                    -->
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

<!--                    This changes price part in the header by adding a total and selected price overview.-->
<!--                    Right now it only shows the price overview for geneart (key === 2) because it is the only-->
<!--                    vendor which provides prices for a single sequence. If you remove the v-if from the second-->
<!--                    paragraph then you will see the overview for every vendor.-->
                    <template v-for="(n,i) in slots.length" v-slot:[slots[i].price]="{header}">
                        <div :key="i">
                            <p class="mb-0">Price</p>
                            <p class="mb-0" v-if="slots[i].key === 2">{{computedPriceTotal[slots[i].key]}}
                                ({{computedPriceOverview[slots[i].key]}})</p>
                        </div>
                    </template>

<!--                    This is the same as above, but with time and not price-->
                    <template v-for="(n,i) in slots.length" v-slot:[slots[i].time]="{header}">
                        <div :key="i">
                            <p class="mb-0">Time</p>
                            <p class="mb-0" v-if="slots[i].key === 2">{{computedTimeTotal[slots[i].key]}}
                                ({{computedTimeOverview[slots[i].key]}})</p>
                        </div>
                    </template>

<!--                    As you can see now in the v-slot, we change the items and not the header anymore.-->
<!--                    Here we change the column with the header vendor name. In this column an error icon is displayed-->
<!--                    when there is no offer or the offer has an error message. Then the price and time will be 0.-->
<!--                    If there is no error, then we have a v-checkbox, where the value of it is modeled by the selectBox-->
<!--                    array. If the user clicks on the checkbox, then the select method will be executed.-->
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

<!--                    This tag changes the column with the prices. Because there are no prices available from TWIST and IDT,-->
<!--                    there is always an error icon with the according message. The price is 0 if there is no offer or -->
<!--                    there is an error message for the offer. If the checkbox is selected then the price will be shown in -->
<!--                    a v-chip. Otherwise it will be shown without the v-chip.-->
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

<!--                    Here for the time column we have the same logic like for the price column-->
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

<!--                    Now we have the slot expanded-item, which is responsible for the data displayed when expanding a row.-->
<!--                    It has a td tag, which stands for table data, which includes again a row, which is again divided in-->
<!--                    columns. There is on column for each vendor. That means that each vendor has an own table where you -->
<!--                    can see all offers. How many columns are created depends on the users selection in filter.-->
<!--                    That is why we loop over the selectedVendors array-->
                    <template v-slot:expanded-item="{item, headers}">
                        <td :colspan="headers.length" class="pa-0">
                            <v-row>
                                <v-col v-for="(n,i) in selectedVendors.length" :key="i">
<!--                                    For this data table and its template tags we have the exact same logic like above -->
<!--                                    except that we don't have a show-expand prop and we don't change the header of the table.-->
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
            // This method is executed when the user clicked on the vendor name in the header.
            // It gets the key of the selected vendor and checks if it was already clicked. If yes then it deselects
            // every offer and sets all other variables to the initial values.
            // If it was not clicked before then it selects all offers by adding all offer keys to the selectBox array.
            // After that it computes the price and time values for the overview of the selected vendor and at the end
            // it does the same for the others.

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
            // This method is executed when the user clicked on a checkbox. Because the checkbox can also be
            // in the expanded row, it has to change the selected offer with the one at the top right now.
            // After that it sets the price and time values for all vendors to 0 and computes them according to the new
            // selection.

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
            // set the price, time, and selected variables to initial values.
            for (let j = 0; j < this.vendors.length; j++) {
                this.computedPriceOverview[j] = 0;
                this.computedPriceTotal[j] = 0;
                this.computedTimeOverview[j] = 0;
                this.computedTimeTotal[j] = 0;
                this.computedSelectedAll[j] = false;
            }
            this.selectBox = [];
            // now compute all the values for the preselected offers
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

            // here we create the headers for the tables above
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
        }
    })
</script>

<style lang="sass">

</style>

<style>
</style>
