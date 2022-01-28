export const routes = [
  {
    path: '/auth',
    name: 'Auth',
    meta: {
      guest: true
    },
    component: () => import('../views/Auth.vue'),
    children: [
      {
        path: 'login',
        name: 'Login',
        // route level code-splitting
        // this generates a separate chunk (login.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import('../views/Login.vue'), /* webpackChunkName: "login" */
        meta: {
          guest: true
        }
      },
      {
        path: 'registration',
        name: 'Registration',
        component: () => import('../views/Registration.vue'),
        meta: {
          guest: true
        }
      }
    ]
  },
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/conference/:code',
    name: 'Conference',
    component: () => import('../views/Conference.vue')
  }
];
