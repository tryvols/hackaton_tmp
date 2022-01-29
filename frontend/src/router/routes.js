export const routes = [
  {
    path: '/auth',
    name: 'Auth',
    meta: {
      guest: true
    },
    redirect: '/auth/login',
    component: () => import('../views/auth/Auth.vue'),
    children: [
      {
        path: 'login',
        name: 'Login',
        // route level code-splitting
        // this generates a separate chunk (login.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import('../views/auth/Login.vue'), /* webpackChunkName: "login" */
        meta: {
          guest: true
        }
      },
      {
        path: 'registration',
        name: 'Registration',
        component: () => import('../views/auth/Registration.vue'),
        meta: {
          guest: true
        }
      }
    ]
  },
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/home/Home.vue')
  },
  {
    path: '/conference/:code',
    name: 'Conference',
    component: () => import('../views/conference/Conference.vue')
  }
];
