<template>
    <v-app>
        <v-app-bar
                app
                color="primary"
                dark
        >

        </v-app-bar>

        <!-- At first only the landing component is displayed. After clicking on search the result component is shown.
        For that the landing comp. passes two events: (1) switch and (2) gotFile which says that result comp. can be
        shown and the file is passed to the result comp.-->
        <v-content>
            <Landing @switch="mySearch = true" @gotFile="fileName = $event" v-if="!mySearch"></Landing>
            <Result v-if="mySearch" :file="fileName"></Result>
        </v-content>

    </v-app>
</template>

<script>
    import Landing from './components/Landing'
    import Result from "@/components/Result";

    export default {
        name: 'App',

        components: {
            Landing,
            Result
        },

        data() {
            return {
                mySearch: false,
                fileName: null
            }
        }
    };
</script>
