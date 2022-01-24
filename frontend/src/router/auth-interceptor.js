import { getAuthToken } from './auth-token';

const DEFAULT_AUTH_USER_ROUTE_NAME = 'Home';
const DEFAULT_GUEST_USER_REDIRECT_PATH = '/auth/login';

export const useAuthInterceptor = router => {
  router.beforeEach((to, from, next) => {
    if (to?.matched?.length === 0) {
      if (from?.name) {
        next({ name: from.name });
      } else {
        next({ path: DEFAULT_GUEST_USER_REDIRECT_PATH });
      }
    }

    if (to?.matched?.some(record => !record?.meta?.guest)) {
      next({
        path: DEFAULT_GUEST_USER_REDIRECT_PATH,
        params: { nextUrl: to.fullPath }
      });
    } else {
      if (!getAuthToken()) {
        next();
      } else {
        next({ name: DEFAULT_AUTH_USER_ROUTE_NAME });
      }
    }
  });
};
