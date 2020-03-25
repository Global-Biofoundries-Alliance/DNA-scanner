<template>
    <v-app>
        <v-app-bar
                app
                color="primary"
                dark
        >
            <v-app-bar-nav-icon v-if="this.$route.path !== '/'" @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
            <v-toolbar-title class="display-1 mx-auto font-weight-medium">DNA Scanner</v-toolbar-title>
        </v-app-bar>

        <v-content>
            <v-navigation-drawer
                    v-if="this.$route.path !== '/'"
                    v-model="drawer"
                    absolute
                    temporary
                    width="500px"
            >
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
            }
        },
        methods: {
            reloadPage() {
                this.drawer = false;
                this.filter = !this.filter
            }
        }
    };
</script>
