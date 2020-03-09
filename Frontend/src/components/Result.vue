<template>
    <div>
        <div>
            <v-app id="inspire">
                <v-data-table
                        :headers="headers"
                        :items="results"
                        :expanded.sync="expanded"
                        item-key="sequenceInformation.name"
                        class="elevation-1"
                        show-expand
                >
                    <template v-slot:header.selectedTwist="{header}">
                        <v-chip color="red" @click="selectAllTwist()">
                            {{header.text}}
                        </v-chip>
                    </template>

                    <template v-slot:header.vendors[0].offers[0].price="{header}">
                        <p class="mb-0" style="display: inline">Price</p>
                        <p class="mb-0" style="display: inline">(</p>
                        <p class="mb-0" style="display: inline">{{priceOverview[0]}}</p>
                        <p class="mb-0" style="display: inline">)</p>
                    </template>

                    <template v-slot:header.vendors[0].offers[0].turnoverTime="{header}">
                        <p class="mb-0" style="display: inline">Time</p>
                        <p class="mb-0" style="display: inline">(</p>
                        <p class="mb-0" style="display: inline">{{timeOverview[0]}}</p>
                        <p class="mb-0" style="display: inline">)</p>
                    </template>

                    <template v-slot:header.selectedIDT="{header}">
                        <v-chip color="green" @click="selectAllIDT()">
                            {{header.text}}
                        </v-chip>
                    </template>

                    <template v-slot:header.vendors[1].offers[0].price="{header}">
                        <p class="mb-0" style="display: inline">Price</p>
                        <p class="mb-0" style="display: inline">(</p>
                        <p class="mb-0" style="display: inline">{{priceOverview[1]}}</p>
                        <p class="mb-0" style="display: inline">)</p>
                    </template>

                    <template v-slot:header.vendors[1].offers[0].turnoverTime="{header}">
                        <p class="mb-0" style="display: inline">Time</p>
                        <p class="mb-0" style="display: inline">(</p>
                        <p class="mb-0" style="display: inline">{{timeOverview[1]}}</p>
                        <p class="mb-0" style="display: inline">)</p>
                    </template>

                    <template v-slot:header.selectedGeneArt="{header}">
                        <v-chip color="orange" @click="selectAllGeneArt()">
                            {{header.text}}
                        </v-chip>
                    </template>

                    <template v-slot:header.vendors[2].offers[0].price="{header}">
                        <p class="mb-0" style="display: inline">Price</p>
                        <p class="mb-0" style="display: inline">(</p>
                        <p class="mb-0" style="display: inline">{{priceOverview[2]}}</p>
                        <p class="mb-0" style="display: inline">)</p>
                    </template>

                    <template v-slot:header.vendors[2].offers[0].turnoverTime="{header}">
                        <p class="mb-0" style="display: inline">Time</p>
                        <p class="mb-0" style="display: inline">(</p>
                        <p class="mb-0" style="display: inline">{{timeOverview[2]}}</p>
                        <p class="mb-0" style="display: inline">)</p>
                    </template>

                    <template v-slot:item.selectedTwist="{item, value}">
                        <v-tooltip v-if="item.vendors[0].offers.length === 0" left>
                            <template v-slot:activator="{ on }">
                                <v-icon color="red" v-on="on">mdi-message</v-icon>
                            </template>
                            <span>No offer available</span>
                        </v-tooltip>
                        <v-tooltip v-else-if="item.vendors[0].offers[0].offerMessage.length !== 0" left>
                            <template v-slot:activator="{ on }">
                                <v-icon color="red" v-on="on">mdi-message</v-icon>
                            </template>
                            <span>{{item.vendors[0].offers[0].offerMessage[0].text}}</span>
                        </v-tooltip>
                        <v-checkbox v-else
                                    v-model="selectedTwist"
                                    :value="item.vendors[0].offers[0].id"
                                    @change="selectTwist(item.vendors[0].offers, 0)"
                                    color="red"></v-checkbox>
                    </template>

                    <template v-slot:item.vendors[0].offers[0].price="{item, value}">
                        <p v-if="item.vendors[0].offers.length === 0 || item.vendors[0].offers[0].offerMessage.length !== 0"
                           class="mb-0">0</p>
                        <v-chip v-else-if="item.vendors[0].offers[0].selected" color="red">{{value}}</v-chip>
                        <p v-else class="mb-0">{{value}}</p>
                    </template>

                    <template v-slot:item.vendors[0].offers[0].turnoverTime="{item, value}">
                        <p v-if="item.vendors[0].offers.length === 0 || item.vendors[0].offers[0].offerMessage.length !== 0"
                           class="mb-0">0</p>
                        <v-chip v-else-if="item.vendors[0].offers[0].selected" color="red">{{value}}</v-chip>
                        <p v-else class="mb-0">{{value}}</p>
                    </template>

                    <template v-slot:item.selectedIDT="{item}">
                        <v-tooltip v-if="item.vendors[1].offers.length === 0" left>
                            <template v-slot:activator="{ on }">
                                <v-icon color="green" v-on="on">mdi-message</v-icon>
                            </template>
                            <span>No offer available</span>
                        </v-tooltip>
                        <v-tooltip v-else-if="item.vendors[1].offers[0].offerMessage.length !== 0" left>
                            <template v-slot:activator="{ on }">
                                <v-icon color="green" v-on="on">mdi-message</v-icon>
                            </template>
                            <span>{{item.vendors[1].offers[0].offerMessage[0].text}}</span>
                        </v-tooltip>
                        <v-checkbox v-else
                                    v-model="selectedIDT"
                                    :value="item.vendors[1].offers[0].id"
                                    @change="selectIDT(item.vendors[1].offers, 0)"
                                    color="green"></v-checkbox>
                    </template>

                    <template v-slot:item.vendors[1].offers[0].price="{item, value}">
                        <p v-if="item.vendors[1].offers.length === 0 || item.vendors[1].offers[0].offerMessage.length !== 0"
                           class="mb-0">0</p>
                        <v-chip v-else-if="item.vendors[1].offers[0].selected" color="green">{{value}}</v-chip>
                        <p v-else class="mb-0">{{value}}</p>
                    </template>

                    <template v-slot:item.vendors[1].offers[0].turnoverTime="{item, value}">
                        <p v-if="item.vendors[1].offers.length === 0 || item.vendors[1].offers[0].offerMessage.length !== 0"
                           class="mb-0">0</p>
                        <v-chip v-else-if="item.vendors[1].offers[0].selected" color="green">{{value}}</v-chip>
                        <p v-else class="mb-0">{{value}}</p>
                    </template>

                    <template v-slot:item.selectedGeneArt="{item}">
                        <v-tooltip v-if="item.vendors[2].offers.length === 0" left>
                            <template v-slot:activator="{ on }">
                                <v-icon color="orange" v-on="on">mdi-message</v-icon>
                            </template>
                            <span>No offer available</span>
                        </v-tooltip>
                        <v-tooltip v-else-if="item.vendors[2].offers[0].offerMessage.length !== 0" left>
                            <template v-slot:activator="{ on }">
                                <v-icon color="orange" v-on="on">mdi-message</v-icon>
                            </template>
                            <span>{{item.vendors[2].offers[0].offerMessage[0].text}}</span>
                        </v-tooltip>
                        <v-checkbox v-else
                                    v-model="selectedGeneArt"
                                    :value="item.vendors[2].offers[0].id"
                                    @change="selectGeneArt(item.vendors[2].offers, 0)"
                                    color="orange"></v-checkbox>
                    </template>

                    <template v-slot:item.vendors[2].offers[0].price="{item, value}">
                        <p v-if="item.vendors[2].offers.length === 0 || item.vendors[2].offers[0].offerMessage.length !== 0"
                           class="mb-0">0</p>
                        <v-chip v-else-if="item.vendors[2].offers[0].selected" color="orange">{{value}}</v-chip>
                        <p v-else class="mb-0">{{value}}</p>
                    </template>

                    <template v-slot:item.vendors[2].offers[0].turnoverTime="{item, value}">
                        <p v-if="item.vendors[2].offers.length === 0 || item.vendors[2].offers[0].offerMessage.length !== 0"
                           class="mb-0">0</p>
                        <v-chip v-else-if="item.vendors[2].offers[0].selected" color="orange">{{value}}</v-chip>
                        <p v-else class="mb-0">{{value}}</p>
                    </template>

                    <template v-slot:expanded-item="{item, headers}">
                        <td :colspan="headers.length" class="pa-0">
                            <v-data-table
                                    :headers="headersSecond"
                                    :items="item.vendors[item.sequenceInformation.mostOffVendor].offers"
                                    item-key="sequenceInformation.name"
                                    class="elevation-1"
                                    hide-default-footer
                            >
                                <template v-slot:header.selectedTwist="{header}">
                                    <v-chip>
                                        {{header.text}}
                                    </v-chip>
                                </template>
                                <template v-slot:header.selectedIDT="{header}">
                                    <v-chip>
                                        {{header.text}}
                                    </v-chip>
                                </template>
                                <template v-slot:header.selectedGeneArt="{header}">
                                    <v-chip>
                                        {{header.text}}
                                    </v-chip>
                                </template>

                                <template v-slot:item="props">
                                    <tr>
                                        <td v-if="selectedVendors.includes(0)">
                                            <p class="mb-0"
                                               v-if="results[item.sequenceInformation.id].vendors[0].offers.length <= props.index"></p>
                                            <v-tooltip
                                                    v-else-if="results[item.sequenceInformation.id].vendors[0].offers[props.index].offerMessage.length !== 0"
                                                    right>
                                                <template v-slot:activator="{ on }">
                                                    <v-icon color="red" v-on="on">mdi-message</v-icon>
                                                </template>
                                                <span>{{results[item.sequenceInformation.id].vendors[0].offers[props.index].offerMessage[0].text}}</span>
                                            </v-tooltip>
                                            <v-checkbox v-else
                                                        v-model="selectedTwist"
                                                        :value="results[item.sequenceInformation.id].vendors[0].offers[props.index].id"
                                                        @change="selectTwist(results[item.sequenceInformation.id].vendors[0].offers, props.index)"
                                                        color="red"
                                                        :disabled="selectedTwist.includes(results[item.sequenceInformation.id].vendors[0].offers[0].id)">
                                            </v-checkbox>
                                        </td>
                                        <td v-if="selectedVendors.includes(0)">
                                            <p class="mb-0"
                                               v-if="results[item.sequenceInformation.id].vendors[0].offers.length <= props.index"></p>
                                            <p class="mb-0"
                                               v-else-if="results[item.sequenceInformation.id].vendors[0].offers[props.index].offerMessage.length !== 0">
                                                0</p>
                                            <p class="mb-0"
                                               v-else-if="results[item.sequenceInformation.id].vendors[0].offers[props.index].selected">
                                                <v-chip color="red">
                                                    {{results[item.sequenceInformation.id].vendors[0].offers[props.index].price}}
                                                </v-chip>
                                            </p>
                                            <p class="mb-0" v-else>
                                                {{results[item.sequenceInformation.id].vendors[0].offers[props.index].price}}
                                            </p>
                                        </td>
                                        <td v-if="selectedVendors.includes(0)">
                                            <p class="mb-0"
                                               v-if="results[item.sequenceInformation.id].vendors[0].offers.length <= props.index"></p>
                                            <p class="mb-0"
                                               v-else-if="results[item.sequenceInformation.id].vendors[0].offers[props.index].offerMessage.length !== 0">
                                                0</p>
                                            <p class="mb-0"
                                               v-else-if="results[item.sequenceInformation.id].vendors[0].offers[props.index].selected">
                                                <v-chip color="red">
                                                    {{results[item.sequenceInformation.id].vendors[0].offers[props.index].turnoverTime}}
                                                </v-chip>
                                            </p>
                                            <p class="mb-0" v-else>
                                                {{results[item.sequenceInformation.id].vendors[0].offers[props.index].turnoverTime}}
                                            </p>
                                        </td>

                                        <td v-if="selectedVendors.includes(1)">
                                            <p class="mb-0"
                                               v-if="results[item.sequenceInformation.id].vendors[1].offers.length <= props.index"></p>
                                            <v-tooltip
                                                    v-else-if="results[item.sequenceInformation.id].vendors[1].offers[props.index].offerMessage.length !== 0"
                                                    right>
                                                <template v-slot:activator="{ on }">
                                                    <v-icon color="green" v-on="on">mdi-message</v-icon>
                                                </template>
                                                <span>{{results[item.sequenceInformation.id].vendors[1].offers[props.index].offerMessage[0].text}}</span>
                                            </v-tooltip>
                                            <v-checkbox v-else
                                                        v-model="selectedIDT"
                                                        :value="results[item.sequenceInformation.id].vendors[1].offers[props.index].id"
                                                        @change="selectIDT(results[item.sequenceInformation.id].vendors[1].offers, props.index)"
                                                        color="green"
                                                        :disabled="selectedIDT.includes(results[item.sequenceInformation.id].vendors[1].offers[0].id)">
                                            </v-checkbox>
                                        </td>
                                        <td v-if="selectedVendors.includes(1)">
                                            <p class="mb-0"
                                               v-if="results[item.sequenceInformation.id].vendors[1].offers.length <= props.index"></p>
                                            <p class="mb-0"
                                               v-else-if="results[item.sequenceInformation.id].vendors[1].offers[props.index].offerMessage.length !== 0">
                                                0</p>
                                            <p class="mb-0"
                                               v-else-if="results[item.sequenceInformation.id].vendors[1].offers[props.index].selected">
                                                <v-chip color="green">
                                                    {{results[item.sequenceInformation.id].vendors[1].offers[props.index].price}}
                                                </v-chip>
                                            </p>
                                            <p class="mb-0" v-else>
                                                {{results[item.sequenceInformation.id].vendors[1].offers[props.index].price}}
                                            </p>
                                        </td>
                                        <td v-if="selectedVendors.includes(1)">
                                            <p class="mb-0"
                                               v-if="results[item.sequenceInformation.id].vendors[1].offers.length <= props.index"></p>
                                            <p class="mb-0"
                                               v-else-if="results[item.sequenceInformation.id].vendors[1].offers[props.index].offerMessage.length !== 0">
                                                0</p>
                                            <p class="mb-0"
                                               v-else-if="results[item.sequenceInformation.id].vendors[1].offers[props.index].selected">
                                                <v-chip color="green">
                                                    {{results[item.sequenceInformation.id].vendors[1].offers[props.index].turnoverTime}}
                                                </v-chip>
                                            </p>
                                            <p class="mb-0" v-else>
                                                {{results[item.sequenceInformation.id].vendors[1].offers[props.index].turnoverTime}}
                                            </p>
                                        </td>

                                        <td v-if="selectedVendors.includes(2)">
                                            <p class="mb-0"
                                               v-if="results[item.sequenceInformation.id].vendors[2].offers.length <= props.index"></p>
                                            <v-tooltip
                                                    v-else-if="results[item.sequenceInformation.id].vendors[2].offers[props.index].offerMessage.length !== 0"
                                                    right>
                                                <template v-slot:activator="{ on }">
                                                    <v-icon color="orange" v-on="on">mdi-message</v-icon>
                                                </template>
                                                <span>{{results[item.sequenceInformation.id].vendors[2].offers[props.index].offerMessage[0].text}}</span>
                                            </v-tooltip>
                                            <v-checkbox v-else
                                                        v-model="selectedGeneArt"
                                                        :value="results[item.sequenceInformation.id].vendors[2].offers[props.index].id"
                                                        @change="selectGeneArt(results[item.sequenceInformation.id].vendors[2].offers, props.index)"
                                                        color="orange"
                                                        :disabled="selectedGeneArt.includes(results[item.sequenceInformation.id].vendors[2].offers[0].id)">
                                            </v-checkbox>
                                        </td>
                                        <td v-if="selectedVendors.includes(2)">
                                            <p class="mb-0"
                                               v-if="results[item.sequenceInformation.id].vendors[2].offers.length <= props.index"></p>
                                            <p class="mb-0"
                                               v-else-if="results[item.sequenceInformation.id].vendors[2].offers[props.index].offerMessage.length !== 0">
                                                0</p>
                                            <p class="mb-0"
                                               v-else-if="results[item.sequenceInformation.id].vendors[2].offers[props.index].selected">
                                                <v-chip color="orange">
                                                    {{results[item.sequenceInformation.id].vendors[2].offers[props.index].price}}
                                                </v-chip>
                                            </p>
                                            <p class="mb-0" v-else>
                                                {{results[item.sequenceInformation.id].vendors[2].offers[props.index].price}}
                                            </p>
                                        </td>
                                        <td v-if="selectedVendors.includes(2)">
                                            <p class="mb-0"
                                               v-if="results[item.sequenceInformation.id].vendors[2].offers.length <= props.index"></p>
                                            <p class="mb-0"
                                               v-else-if="results[item.sequenceInformation.id].vendors[2].offers[props.index].offerMessage.length !== 0">
                                                0</p>
                                            <p class="mb-0"
                                               v-else-if="results[item.sequenceInformation.id].vendors[2].offers[props.index].selected">
                                                <v-chip color="orange">
                                                    {{results[item.sequenceInformation.id].vendors[2].offers[props.index].turnoverTime}}
                                                </v-chip>
                                            </p>
                                            <p class="mb-0" v-else>
                                                {{results[item.sequenceInformation.id].vendors[2].offers[props.index].turnoverTime}}
                                            </p>
                                        </td>
                                    </tr>
                                </template>
                            </v-data-table>
                        </td>
                    </template>
                </v-data-table>
                <p>{{selectedTwist}}</p>
                <p>{{checkTwist}}</p>
                <p>{{timeOverviewTwist}}</p>
                <!--                <p>{{selectedIDT}}</p>-->
                <!--                <p>{{selectedGeneArt}}</p>-->
                <!--                <p>{{computedHeaders}}</p>-->
                <!--                <p>{{computedHeadersSecond}}</p>-->
            </v-app>
        </div>
    </div>
</template>

<script>
    export default ({
        name: 'Result',
        data() {
            return {
                computedHeaders: [],
                computedHeadersSecond: [],
                expanded: [],
                selectedTwist: [],
                lengthTwist: 0,
                selectedIDT: [],
                lengthIDT: 0,
                selectedGeneArt: [],
                lengthGeneArt: 0,
                checkTwist: false,
                checkIDT: false,
                checkGeneArt: false,
                singleExpand: false,
                priceOverview: {
                    0: 0,
                    1: 0,
                    2: 0
                },
                timeOverview: {
                    0: 0,
                    1: 0,
                    2: 0
                },
                timeOverviewTwist: [0],
                timeOverviewIDT: [0],
                timeOverviewGeneArt: [0],

            }
        },
        methods: {
            selectTwist(offers, index) {
                if (!offers[index].selected) {
                    this.priceOverview[0] = Math.round((this.priceOverview[0] + offers[index].price) * 100) / 100;
                    this.timeOverviewTwist.push(offers[index].turnoverTime);
                    this.timeOverview[0] = Math.max(...this.timeOverviewTwist);
                    offers[index].selected = true;
                    var temp = offers[0];
                    offers[0] = offers[index];
                    offers[index] = temp;
                } else {
                    this.priceOverview[0] = Math.round((this.priceOverview[0] - offers[index].price) * 100) / 100;
                    this.timeOverviewTwist.splice(this.timeOverviewTwist.indexOf(offers[index].turnoverTime), 1);
                    this.timeOverview[0] = Math.max(...this.timeOverviewTwist);
                    offers[index].selected = false
                }
                this.checkTwist = this.selectedTwist.length >= this.results.length - this.lengthTwist;
            },
            selectAllTwist() {
                if (!this.checkTwist) {
                    this.results.forEach(i => {
                        if (i.vendors[0].offers.length !== 0) {
                            if (i.vendors[0].offers[0].offerMessage.length === 0 && !this.selectedTwist.includes(i.vendors[0].offers[0].id)) {
                                this.priceOverview[0] = Math.round((this.priceOverview[0] + i.vendors[0].offers[0].price) * 100) / 100;
                                this.timeOverviewTwist.push(i.vendors[0].offers[0].turnoverTime);
                                this.timeOverview[0] = Math.max(...this.timeOverviewTwist);
                                i.vendors[0].offers[0].selected = true;
                                this.selectedTwist.push(i.vendors[0].offers[0].id)
                            }
                        }
                    });
                    this.checkTwist = true;
                } else {
                    this.results.forEach(i => {
                        if (i.vendors[0].offers.length !== 0) {
                            if (i.vendors[0].offers[0].offerMessage.length === 0 && this.selectedTwist.includes(i.vendors[0].offers[0].id)) {
                                this.priceOverview[0] = Math.round((this.priceOverview[0] - i.vendors[0].offers[0].price) * 100) / 100;
                                this.timeOverviewTwist.splice(this.timeOverviewTwist.indexOf(i.vendors[0].offers[0].turnoverTime), 1);
                                this.timeOverview[0] = Math.max(...this.timeOverviewTwist);
                                i.vendors[0].offers[0].selected = false
                            }
                        }
                    });
                    this.selectedTwist = [];
                    this.checkTwist = false;
                }
            },
            selectIDT(offers, index) {
                if (!offers[index].selected) {
                    this.priceOverview[1] = Math.round((this.priceOverview[1] + offers[index].price) * 100) / 100;
                    this.timeOverviewIDT.push(offers[index].turnoverTime);
                    this.timeOverview[1] = Math.max(...this.timeOverviewIDT);
                    offers[index].selected = true;
                    var temp = offers[0];
                    offers[0] = offers[index];
                    offers[index] = temp;
                } else {
                    this.priceOverview[1] = Math.round((this.priceOverview[1] - offers[index].price) * 100) / 100;
                    this.timeOverviewIDT.splice(this.timeOverviewIDT.indexOf(offers[index].turnoverTime), 1);
                    this.timeOverview[1] = Math.max(...this.timeOverviewIDT);
                    offers[index].selected = false
                }
                this.checkIDT = this.selectedIDT.length >= this.results.length - this.lengthIDT;
            },
            selectAllIDT() {
                if (!this.checkIDT) {
                    this.results.forEach(i => {
                        if (i.vendors[1].offers.length !== 0) {
                            if (i.vendors[1].offers[0].offerMessage.length === 0 && !this.selectedIDT.includes(i.vendors[1].offers[0].id)) {
                                this.priceOverview[1] = Math.round((this.priceOverview[1] + i.vendors[1].offers[0].price) * 100) / 100;
                                this.timeOverviewIDT.push(i.vendors[1].offers[0].turnoverTime);
                                this.timeOverview[1] = Math.max(...this.timeOverviewIDT);
                                i.vendors[1].offers[0].selected = true;
                                this.selectedIDT.push(i.vendors[1].offers[0].id)
                            }
                        }
                    });
                    this.checkIDT = true;
                } else {
                    this.results.forEach(i => {
                        if (i.vendors[1].offers.length !== 0) {
                            if (i.vendors[1].offers[0].offerMessage.length === 0 && this.selectedIDT.includes(i.vendors[1].offers[0].id)) {
                                this.priceOverview[1] = Math.round((this.priceOverview[1] - i.vendors[1].offers[0].price) * 100) / 100;
                                this.timeOverviewIDT.splice(this.timeOverviewIDT.indexOf(i.vendors[1].offers[0].turnoverTime), 1);
                                this.timeOverview[1] = Math.max(...this.timeOverviewIDT);
                                i.vendors[1].offers[0].selected = false
                            }
                        }
                    });
                    this.selectedIDT = [];
                    this.checkIDT = false;
                }
            },
            selectGeneArt(offers, index) {
                if (!offers[index].selected) {
                    this.priceOverview[2] = Math.round((this.priceOverview[2] + offers[index].price) * 100) / 100;
                    this.timeOverviewGeneArt.push(offers[index].turnoverTime);
                    this.timeOverview[2] = Math.max(...this.timeOverviewGeneArt);
                    offers[index].selected = true;
                    var temp = offers[0];
                    offers[0] = offers[index];
                    offers[index] = temp;
                } else {
                    this.priceOverview[2] = Math.round((this.priceOverview[2] - offers[index].price) * 100) / 100;
                    this.timeOverviewGeneArt.splice(this.timeOverviewGeneArt.indexOf(offers[index].turnoverTime), 1);
                    this.timeOverview[2] = Math.max(...this.timeOverviewGeneArt);
                    offers[index].selected = false
                }
                this.checkGeneArt = this.selectedGeneArt.length >= this.results.length - this.lengthGeneArt;
            },
            selectAllGeneArt() {
                if (!this.checkGeneArt) {
                    this.results.forEach(i => {
                        if (i.vendors[2].offers.length !== 0) {
                            if (i.vendors[2].offers[0].offerMessage.length === 0 && !this.selectedGeneArt.includes(i.vendors[2].offers[0].id)) {
                                this.priceOverview[2] = Math.round((this.priceOverview[2] + i.vendors[2].offers[0].price) * 100) / 100;
                                this.timeOverviewGeneArt.push(i.vendors[2].offers[0].turnoverTime);
                                this.timeOverview[2] = Math.max(...this.timeOverviewGeneArt);
                                i.vendors[2].offers[0].selected = true;
                                this.selectedGeneArt.push(i.vendors[2].offers[0].id)
                            }
                        }
                    });
                    this.checkGeneArt = true;
                } else {
                    this.results.forEach(i => {
                        if (i.vendors[2].offers.length !== 0) {
                            if (i.vendors[2].offers[0].offerMessage.length === 0 && this.selectedGeneArt.includes(i.vendors[2].offers[0].id)) {
                                this.priceOverview[2] = Math.round((this.priceOverview[2] - i.vendors[2].offers[0].price) * 100) / 100;
                                this.timeOverviewGeneArt.splice(this.timeOverviewGeneArt.indexOf(i.vendors[2].offers[0].turnoverTime), 1);
                                this.timeOverview[2] = Math.max(...this.timeOverviewGeneArt);
                                i.vendors[2].offers[0].selected = false
                            }
                        }
                    });
                    this.selectedGeneArt = [];
                    this.checkGeneArt = false;
                }
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
            }

        },
        created() {
            let i, j, k;
            for (i = 0; i < this.$store.state.StoreSearchResult.length; i++) {
                for (j = 0; j < this.results[i].vendors.length; j++) {
                    if (this.results[i].vendors[j].offers.length === 0 || this.results[i].vendors[j].offers[0].offerMessage.length !== 0) {
                        if (j === 0) {
                            this.lengthTwist -= 1;
                        }
                        if (j === 1) {
                            this.lengthIDT -= 1;
                        }
                        if (j === 2) {
                            this.lengthGeneArt -= 1;
                        }
                    }
                    for (k = 0; k < this.results[i].vendors[j].offers.length; k++) {
                        if (this.results[i].vendors[j].offers[k].selected) {
                            if (j === 0) {
                                this.selectedTwist.push(this.results[i].vendors[j].offers[k].id);
                                this.priceOverview[j] = Math.round((this.priceOverview[j] + this.results[i].vendors[j].offers[k].price) * 100) / 100;
                                this.timeOverviewTwist.push(this.results[i].vendors[j].offers[k].turnoverTime);
                                this.timeOverview[0] = Math.max(...this.timeOverviewTwist);
                            }
                            if (j === 1) {
                                this.selectedIDT.push(this.results[i].vendors[j].offers[k].id);
                                this.priceOverview[j] = Math.round((this.priceOverview[j] + this.results[i].vendors[j].offers[k].price) * 100) / 100;
                                this.timeOverviewIDT.push(this.results[i].vendors[j].offers[k].turnoverTime);
                                this.timeOverview[1] = Math.max(...this.timeOverviewIDT);
                            }
                            if (j === 2) {
                                this.selectedGeneArt.push(this.results[i].vendors[j].offers[k].id);
                                this.priceOverview[j] = Math.round((this.priceOverview[j] + this.results[i].vendors[j].offers[k].price) * 100) / 100;
                                this.timeOverviewGeneArt.push(this.results[i].vendors[j].offers[k].turnoverTime);
                                this.timeOverview[2] = Math.max(...this.timeOverviewGeneArt);
                            }
                        }
                    }
                }
            }
            this.lengthTwist = Math.abs(this.lengthTwist);
            this.checkTwist = this.selectedTwist.length >= this.results.length - this.lengthTwist;

            this.lengthIDT = Math.abs(this.lengthIDT);
            this.checkIDT = this.selectedIDT.length >= this.results.length - this.lengthIDT;

            this.lengthGeneArt = Math.abs(this.lengthGeneArt);
            this.checkGeneArt = this.selectedGeneArt.length >= this.results.length - this.lengthGeneArt;

            this.computedHeaders.push({
                text: 'Sequence',
                align: 'left',
                sortable: false,
                value: 'sequenceInformation.name',
            });
            for (let i = 0; i < this.selectedVendors.length; i++) {
                this.computedHeaders.push(
                    {
                        text: this.vendors[this.selectedVendors[i]].name,
                        value: 'selected' + this.vendors[this.selectedVendors[i]].name,
                        sortable: false
                    },
                    {
                        text: '',
                        value: 'vendors[' + i + '].offers[0].price',
                        sortable: false
                    },
                    {
                        text: '',
                        value: 'vendors[' + i + '].offers[0].turnoverTime',
                        sortable: false
                    }
                );
                this.computedHeadersSecond.push(
                    {
                        text: this.vendors[this.selectedVendors[i]].name,
                        value: 'selected' + this.vendors[this.selectedVendors[i]].name,
                        sortable: false
                    },
                    {
                        text: 'Price',
                        value: 'price',
                        sortable: false
                    },
                    {
                        text: 'Time',
                        value: 'time',
                        sortable: false
                    }
                )
            }
            this.computedHeaders.push({
                text: '',
                value: 'data-table-expand'
            })
        }
    })
</script>

<style lang="sass">
    @import '../sass/variables.sass'

</style>
