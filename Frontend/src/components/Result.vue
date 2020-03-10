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

                    <template v-slot:header.selectedIDT="{header}">
                        <v-chip color="green" @click="selectAllIDT()">
                            {{header.text}}
                        </v-chip>
                    </template>

                    <template v-slot:header.selectedGeneArt="{header}">
                        <v-chip color="orange" @click="selectAllGeneArt()">
                            {{header.text}}
                        </v-chip>
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
                                    v-model="selected[0]"
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
                                    v-model="selected[1]"
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
                                    v-model="selected[2]"
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

                                        <!--                                        <td v-for="(n,i) in 3" :key="i">-->
                                        <!--                                            <p class="mb-0"-->
                                        <!--                                               v-if="results[item.sequenceInformation.id].vendors[i].offers.length <= props.index"></p>-->
                                        <!--                                            <v-tooltip-->
                                        <!--                                                    v-else-if="results[item.sequenceInformation.id].vendors[i].offers[props.index].offerMessage.length !== 0"-->
                                        <!--                                                    right>-->
                                        <!--                                                <template v-slot:activator="{ on }">-->
                                        <!--                                                    <v-icon color="red" v-on="on">mdi-message</v-icon>-->
                                        <!--                                                </template>-->
                                        <!--                                                <span>{{results[item.sequenceInformation.id].vendors[i].offers[props.index].offerMessage[0].text}}</span>-->
                                        <!--                                            </v-tooltip>-->
                                        <!--                                            <v-checkbox v-else-->
                                        <!--                                                        v-model="selected[i]"-->
                                        <!--                                                        :value="results[item.sequenceInformation.id].vendors[i].offers[props.index].id"-->
                                        <!--                                                        @change="selectTwist(results[item.sequenceInformation.id].vendors[i].offers, props.index)"-->
                                        <!--                                                        color="red">-->
                                        <!--                                            </v-checkbox>-->
                                        <!--                                        </td>-->

                                        <!--                                        <td v-for="(n,i) in 3" :key="i">-->
                                        <!--                                            <p class="mb-0"-->
                                        <!--                                               v-if="results[item.sequenceInformation.id].vendors[i].offers.length <= props.index"></p>-->
                                        <!--                                            <p class="mb-0"-->
                                        <!--                                               v-else-if="results[item.sequenceInformation.id].vendors[i].offers[props.index].offerMessage.length !== 0">-->
                                        <!--                                                0-->
                                        <!--                                            </p>-->
                                        <!--                                            <p class="mb-0"-->
                                        <!--                                               v-else-if="results[item.sequenceInformation.id].vendors[i].offers[props.index].selected">-->
                                        <!--                                                <v-chip color="red">-->
                                        <!--                                                    {{results[item.sequenceInformation.id].vendors[i].offers[props.index].price}}-->
                                        <!--                                                </v-chip>-->
                                        <!--                                            </p>-->
                                        <!--                                            <p class="mb-0" v-else>-->
                                        <!--                                                {{results[item.sequenceInformation.id].vendors[i].offers[props.index].price}}-->
                                        <!--                                            </p>-->
                                        <!--                                        </td>-->

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
                                                        v-model="selected[0]"
                                                        :value="results[item.sequenceInformation.id].vendors[0].offers[props.index].id"
                                                        @change="selectTwist(results[item.sequenceInformation.id].vendors[0].offers, props.index)"
                                                        color="red"></v-checkbox>
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
                                                        v-model="selected[1]"
                                                        :value="results[item.sequenceInformation.id].vendors[1].offers[props.index].id"
                                                        @change="selectIDT(results[item.sequenceInformation.id].vendors[1].offers, props.index)"
                                                        color="green"></v-checkbox>
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
                                                        v-model="selected[2]"
                                                        :value="results[item.sequenceInformation.id].vendors[2].offers[props.index].id"
                                                        @change="selectGeneArt(results[item.sequenceInformation.id].vendors[2].offers, props.index)"
                                                        color="orange">
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
                lengthTwist: 0,
                lengthIDT: 0,
                lengthGeneArt: 0,
                checkTwist: false,
                checkIDT: false,
                checkGeneArt: false,
                singleExpand: false,
                selected: {
                    0: [],
                    1: [],
                    2: []
                }
                // results: [
                //     {
                //         sequenceInformation: {
                //             id: 0,
                //             name: 'Frozen Yogurt',
                //             mostOff: 2,
                //             mostOffVendor: 2
                //         },
                //         vendors: [
                //             {
                //                 key: 0,
                //                 offers: []
                //             },
                //             {
                //                 key: 1,
                //                 offers: [
                //                     {
                //                         id: "010",
                //                         offerMessage: [],
                //                         price: 0.8,
                //                         selected: false,
                //                         turnoverTime: 4
                //                     }
                //                 ]
                //             },
                //             {
                //                 key: 2,
                //                 offers: [
                //                     {
                //                         id: "020",
                //                         offerMessage: [
                //                             {
                //                                 messageType: 1006,
                //                                 text: "This vendor cannot synthesize this sequence"
                //                             }
                //                         ],
                //                         price: 0.8,
                //                         selected: false,
                //                         turnoverTime: 9
                //                     },
                //                     {
                //                         id: "021",
                //                         offerMessage: [],
                //                         price: 0.8,
                //                         selected: false,
                //                         turnoverTime: 30
                //                     }
                //                 ]
                //             }
                //         ]
                //     },
                //     {
                //         sequenceInformation: {
                //             id: 1,
                //             name: 'Ice cream Sandwich',
                //             mostOff: 3,
                //             mostOffVendor: 2
                //         },
                //         vendors: [
                //             {
                //                 key: 0,
                //                 offers: []
                //             },
                //             {
                //                 key: 1,
                //                 offers: [
                //                     {
                //                         id: "110",
                //                         offerMessage: [],
                //                         price: 0.9,
                //                         selected: false,
                //                         turnoverTime: 60
                //                     },
                //                     {
                //                         id: "111",
                //                         offerMessage: [],
                //                         price: 0.2,
                //                         selected: false,
                //                         turnoverTime: 5
                //                     }
                //                 ]
                //             },
                //             {
                //                 key: 2,
                //                 offers: [
                //                     {
                //                         id: "120",
                //                         offerMessage: [
                //                             {
                //                                 messageType: 1006,
                //                                 text: "This vendor cannot synthesize this sequence"
                //                             }
                //                         ],
                //                         price: 0.7,
                //                         selected: false,
                //                         turnoverTime: 90
                //                     },
                //                     {
                //                         id: "121",
                //                         offerMessage: [
                //                             {
                //                                 messageType: 1006,
                //                                 text: "This vendor cannot synthesize this sequence"
                //                             }
                //                         ],
                //                         price: 0.95,
                //                         selected: false,
                //                         turnoverTime: 33
                //                     },
                //                     {
                //                         id: "122",
                //                         offerMessage: [],
                //                         price: 0.4,
                //                         selected: false,
                //                         turnoverTime: 8
                //                     }
                //                 ]
                //             }
                //         ]
                //     },
                // ],
            }
        },
        methods: {
            selectTwist(offers, index) {
                if (!offers[index].selected) {
                    offers[index].selected = true;
                    var temp = offers[0];
                    offers[0] = offers[index];
                    offers[index] = temp;
                } else {
                    offers[index].selected = false
                }
                this.checkTwist = this.selected[0].length >= this.results.length - this.lengthTwist;
            },
            selectAllTwist() {
                if (!this.checkTwist) {
                    this.results.forEach(i => {
                        if (i.vendors[0].offers.length !== 0) {
                            if (i.vendors[0].offers[0].offerMessage.length === 0 && !this.selected[0].includes(i.vendors[0].offers[0].id)) {
                                i.vendors[0].offers[0].selected = true;
                                this.selected[0].push(i.vendors[0].offers[0].id)
                            }
                        }
                    });
                    this.checkTwist = true;
                } else {
                    this.results.forEach(i => {
                        let j;
                        for (j = 0; j < i.vendors[0].offers.length; j++) {
                            i.vendors[0].offers[j].selected = false
                        }

                    });
                    this.selected[0] = [];
                    this.checkTwist = false;
                }
            },
            selectIDT(offers, index) {
                if (!offers[index].selected) {
                    offers[index].selected = true;
                    var temp = offers[0];
                    offers[0] = offers[index];
                    offers[index] = temp;
                } else {
                    offers[index].selected = false
                }
                this.checkIDT = this.selected[1].length >= this.results.length - this.lengthIDT;
            },
            selectAllIDT() {
                if (!this.checkIDT) {
                    this.results.forEach(i => {
                        if (i.vendors[1].offers.length !== 0) {
                            if (i.vendors[1].offers[0].offerMessage.length === 0 && !this.selected[1].includes(i.vendors[1].offers[0].id)) {
                                i.vendors[1].offers[0].selected = true;
                                this.selected[1].push(i.vendors[1].offers[0].id)
                            }
                        }
                    });
                    this.checkIDT = true;
                } else {
                    this.results.forEach(i => {
                        let j;
                        for (j = 0; j < i.vendors[1].offers.length; j++) {
                            i.vendors[1].offers[j].selected = false
                        }
                    });
                    this.selected[1] = [];
                    this.checkIDT = false;
                }
            },
            selectGeneArt(offers, index) {
                if (!offers[index].selected) {
                    offers[index].selected = true;
                    var temp = offers[0];
                    offers[0] = offers[index];
                    offers[index] = temp;
                } else {
                    offers[index].selected = false
                }
                this.checkGeneArt = this.selected[2].length >= this.results.length - this.lengthGeneArt;
            },
            selectAllGeneArt() {
                if (!this.checkGeneArt) {
                    this.results.forEach(i => {
                        if (i.vendors[2].offers.length !== 0) {
                            if (i.vendors[2].offers[0].offerMessage.length === 0 && !this.selected[2].includes(i.vendors[2].offers[0].id)) {
                                i.vendors[2].offers[0].selected = true;
                                this.selected[2].push(i.vendors[2].offers[0].id)
                            }
                        }
                    });
                    this.checkGeneArt = true;
                } else {
                    this.results.forEach(i => {
                        let j;
                        for (j = 0; j < i.vendors[2].offers.length; j++) {
                            i.vendors[2].offers[j].selected = false
                        }
                    });
                    this.selected[2] = [];
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
            },

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
                                this.selected[0].push(this.results[i].vendors[j].offers[k].id);
                            }
                            if (j === 1) {
                                this.selected[1].push(this.results[i].vendors[j].offers[k].id);
                            }
                            if (j === 2) {
                                this.selected[2].push(this.results[i].vendors[j].offers[k].id);
                            }
                        }
                    }
                }
            }
            this.lengthTwist = Math.abs(this.lengthTwist);
            this.checkTwist = this.selected[0].length >= this.results.length - this.lengthTwist;

            this.lengthIDT = Math.abs(this.lengthIDT);
            this.checkIDT = this.selected[1].length >= this.results.length - this.lengthIDT;

            this.lengthGeneArt = Math.abs(this.lengthGeneArt);
            this.checkGeneArt = this.selected[2].length >= this.results.length - this.lengthGeneArt;

            this.computedHeaders.push({
                text: 'Sequence',
                align: 'left',
                sortable: false,
                value: 'sequenceInformation.name',
            });
            this.selectedVendors.sort();
            for (let i = 0; i < this.selectedVendors.length; i++) {
                this.computedHeaders.push(
                    {
                        text: this.vendors[this.selectedVendors[i]].name,
                        value: 'selected' + this.vendors[this.selectedVendors[i]].name,
                        sortable: false
                    },
                    {
                        text: 'Price',
                        value: 'vendors[' + this.vendors[this.selectedVendors[i]].id + '].offers[0].price',
                        sortable: false
                    },
                    {
                        text: 'Time',
                        value: 'vendors[' + this.vendors[this.selectedVendors[i]].id + '].offers[0].turnoverTime',
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
