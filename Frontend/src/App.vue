<!-- This App component is the main component of this application. It is responsible for routing
between the Result and Landing component and also imports the Filter component.
The template part of this component is divided in two subparts: v-app-bar and v-content
Because we have a single page application the app-bar stays static but the content changes accordingly which is
handled by the router.
-->
<template>
    <v-app>
        <v-app-bar
                app
                color="primary"
                dark
        >
            <v-app-bar-nav-icon v-if="this.$route.path !== '/'" @click.stop="drawer = true"></v-app-bar-nav-icon>
            <v-toolbar-title v-if="this.$route.path !== '/'" class="display-1 mx-auto font-weight-medium pl-0" style="padding-left: 270px !important">DNA Scanner</v-toolbar-title>
            <v-toolbar-title v-else class="display-1 mx-auto font-weight-medium pl-0">DNA Scanner</v-toolbar-title>
            <v-btn v-if="this.$route.path !== '/'" @click="reload()">UPLOAD NEW FILE</v-btn>
            <v-tooltip v-if="this.$route.path !== '/'" :disabled="disableErrorMsg" bottom open-on-click>
                <template v-slot:activator="{ on }">
                    <v-btn class="ml-5" @click="order()" v-on="on">FINISH ORDER</v-btn>
                </template>
                <span>{{errorMessage}}</span>
            </v-tooltip>

        </v-app-bar>

        <v-content>
            <!-- The navigation drawer is also only displayed after the user clicked on search and on the app-bar-nav-icon
            from above. If the user clicked on the icon is modeled by the v-model directive and the drawer variable.
            -->
            <v-navigation-drawer
                    v-if="this.$route.path !== '/'"
                    v-model="drawer"
                    absolute
                    temporary
                    stateless
                    width="500px"
            >
                <!-- Here we use the Filter component which is importet as FilterDNA. It passes the value true for isApp
                to tell the Filter that we are calling it from the App component. When the event @usedFilter is emitted from
                the Filter we run the reloadPage() method.-->
                <FilterDNA isApp="true" @usedFilter="reloadPage()"></FilterDNA>
            </v-navigation-drawer>
            <router-view :key="filter"></router-view>
        </v-content>

    </v-app>
</template>

<script>
    import FilterDNA from './components/Filter.vue'

    export default {
        name: 'App',
        components: {
            FilterDNA
        },
        data() {
            return {
                filter: false,
                drawer: false,
                errorMessage: "",
                disableErrorMsg: true,
            }
        },
        computed: {
            selectBox: {
                get() {
                    return this.$store.state.StoreSelectedOffers;
                },
                set(value) {
                    this.$store.commit('updateSelectedOffers', value)
                }
            }
        },
        methods: {
            reloadPage() {
                this.drawer = false;
                this.filter = !this.filter
            },
            order() {
                let selected = [];

                for (let i = 0; i < this.$store.state.StoreSearchResult.length; i++) {
                    if (this.selectBox[this.$store.state.StoreSearchResult[i].sequenceInformation.id]) {
                        selected.push(this.selectBox[this.$store.state.StoreSearchResult[i].sequenceInformation.id])
                    }
                }

                // eslint-disable-next-line no-console
                console.log("selectedOrder:" + selected);

                let selection = {
                    "offers": selected
                };

                this.$http.post('/api/order', selection)
                    .then(response => {
                        //eslint-disable-next-line no-console
                        console.log(response);
                        let vendorErrors = [];
                        response.body.forEach(i => {
                           if(i.type !== "NOT_SUPPORTED") {
                               window.open(i.url, '_blank');
                           }
                           else {
                               vendorErrors.push(i.vendor)
                           }
                        });
                        this.disableErrorMsg = true;
                        if(vendorErrors.length !== 0) {
                            let msg = "";
                            for(let i = 0; i < vendorErrors.length; i++) {
                                if(i === 0) {
                                    msg = msg + this.$store.state.StoreVendors[vendorErrors[i]].name
                                } else {
                                    msg = msg + ", " + this.$store.state.StoreVendors[vendorErrors[i]].name
                                }
                            }
                            this.errorMessage = "An error occurred while ordering from the vendor(s):" + msg;
                            this.disableErrorMsg = false;
                        }
                    })
            },
            reload() {
                this.$router.back()
            }
        }
    };
</script>
