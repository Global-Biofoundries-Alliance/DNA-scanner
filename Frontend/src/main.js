import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify';
import VueResource from 'vue-resource'
import VueRouter from "vue-router";
import { routes } from './routes';
import { store } from './store/store';

Vue.use(VueResource);
Vue.use(VueRouter);

Vue.config.productionTip = false;

const router = new VueRouter({
  routes
});

new Vue({
  vuetify,
  router,
  store,
  render: h => h(App)
}).$mount('#app');
