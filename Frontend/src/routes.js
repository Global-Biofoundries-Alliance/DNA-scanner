import Landing from './components/Landing.vue'
import Result from './components/Result.vue'

//the constant routes holds the needed routes specifying the path and the component that should be shown when you visit the corresponding path
export const routes = [
    { path: '', component: Landing},
    { path: '/result', component: Result}
];
