import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export const store = new Vuex.Store({
    state: {
        StoreFile: [],
        StoreSearchResult: [],
        PriceFilterMin: 1,
        PriceFilterMax: 1000,
        PriceFilterCurrentRange: [1, 100],
        DeliveryFilterMin: 1,
        DeliveryFilterMax: 1000,
        DeliveryFilterCurrent: 7,
        StoreVendors: [],
        StoreDialogItem: null,
        StoreSize: 2,
        StoreOffset: 0,
        StoreLength: 0
    }
});
