import Vue from 'vue';
import Vuetify from 'vuetify/lib';
import { Ripple } from 'vuetify/lib/directives/ripple'

// here we import Vuetify for the material design and use the ripple directive.
// this directive was added because of a bug in vuetify.
Vue.use(Vuetify, {
    directives: {
        Ripple: Ripple
    }
});

export default new Vuetify({
});
