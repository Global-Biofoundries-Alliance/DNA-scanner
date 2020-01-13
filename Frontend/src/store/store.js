import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

// the constant store stores data which should be available globally. To achieve that store is exported and added in main.js
export const store = new Vuex.Store({
    state: {
        StoreFile: [],
        StoreResult: []
    }
});
