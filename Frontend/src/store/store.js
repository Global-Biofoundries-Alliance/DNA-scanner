import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export const store = new Vuex.Store({
    state: {
        StoreSelectedVendors: [0, 1, 2],
        StoreFilterMin: 1,
        StoreFilterMax: 1000,
        StorePriceFilterRange: [1, 1000],
        StoreDeliveryDays: 100,
        StorePreselectByTime: false,
        StorePreselectByPrice: false,
        StoreFile: [],
        StoreSearchResult: [],
        StoreVendors: [],
        StoreSelectedOffers: {},
        StoreVendorMessage: [],
        StoreGlobalMessage: ''

    },
    mutations: {
        updateSelectedVendors(state, arr) {
            state.StoreSelectedVendors = arr
        },
        updateRange(state, r) {
            state.StorePriceFilterRange = r
        },
        updateFilterMax(state, max) {
            state.StoreFilterMax = max
        },
        updateFilterMin(state, min) {
            state.StoreFilterMin = min
        },
        updateDeliveryDays(state, days) {
            state.StoreDeliveryDays = days
        },
        updatePreselectByPrice(state, price) {
            state.StorePreselectByPrice = price
        },
        updatePreselectByTime(state, time) {
            state.StorePreselectByTime = time
        },
        updateSelectedOffers(state, offers) {
            state.StoreSelectedOffers = offers
        }
    }
});
