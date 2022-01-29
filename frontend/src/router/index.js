import Vue from 'vue';
import VueRouter from 'vue-router';
import { useAuthInterceptor } from './auth-interceptor';
import { routes } from './routes';

Vue.use(VueRouter);

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
});

useAuthInterceptor(router);

export default router;
