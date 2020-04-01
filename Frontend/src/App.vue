<!-- This App component is the main component of this application. It is responsible for routing
between the Result and Landing component and also imports the Filter component.
The template part of this component is divided in two subparts: v-app-bar and v-content
Because we have a single page application the app-bar stays static but the content changes accordingly, which is
handled by the router.
-->
<template>
    <v-app>
        <!-- The app bar includes the filter icon, the title DNA Scanner, and the buttons upload new file and finish order.
        In the Landing page only the title is displayed.
        -->
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
            from above. If the user clicked on the icon it is modeled by the v-model directive and the drawer variable.
            -->
            <v-navigation-drawer
                    v-if="this.$route.path !== '/'"
                    v-model="drawer"
                    absolute
                    temporary
                    stateless
                    width="500px"
            >
                <!-- Here we use the Filter component which is imported as FilterDNA. It passes the value true for isApp
                to tell the Filter that we are calling it from the App component. When the event @usedFilter is emitted from
                the Filter we run the reloadPage() method.-->
                <FilterDNA isApp="true" @usedFilter="reloadPage()"></FilterDNA>
            </v-navigation-drawer>
            <!-- This router-view tag is responsible for routing between the routes defined in the routes.js file which
            are in this case the Landing and Result component. The key of this tag is the filter variable which means
            that whenever the filter variable is changed it reloads the component which changed it. In our case it is the
            Result component because there when we change the filter and click on save we need to make new requests and
            reload the page with the new results.
            -->
            <router-view :key="filter"></router-view>
        </v-content>

    </v-app>
</template>

<script>
    import FilterDNA from './components/Filter.vue'

    export default {
        name: 'App',
        // components that we want to import
        components: {
            FilterDNA
        },
        // here we define all the variables and give them a initial value
        data() {
            return {
                filter: false,
                drawer: false,
                errorMessage: "",
                disableErrorMsg: true,
            }
        },
        // here we define the data which we want to use in this component from the store.js file
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
        // here are all the methods that should be executed in this component
        methods: {
            // Closes the filter drawer and changes the filter variable so that the page reloads
            reloadPage() {
                this.drawer = false;
                this.filter = !this.filter
            },
            // Is executed when the button finish order is clicked. It sends the selected offers to the order
            // endpoint and opens the URLs from the response. If there is an error it will be displayed in under the
            // button finish order

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
            // is executed when the button upload new file is clicked. It just tells the router to go one route back.
            reload() {
                this.$router.back()
            }
        }
    };
</script>
