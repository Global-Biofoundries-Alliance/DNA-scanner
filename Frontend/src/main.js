import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify';
import VueResource from 'vue-resource'
import VueRouter from "vue-router";
import { routes } from './routes';
import { store } from './store/store';

// here we gather all the extensions and libraries we use for vue js
// in our case we use VueResource for making http requests, VueRouter for routing, the store
// with its global variables, and vuetify for the nice google material design
Vue.use(VueResource);
Vue.use(VueRouter);

Vue.config.productionTip = false;

const router = new VueRouter({
  mode:'history',
  routes
});

new Vue({
  vuetify,
  router,
  store,
  render: h => h(App)
}).$mount('#app');
