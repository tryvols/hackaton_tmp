import { getAuthToken } from '../storage/auth-token';

const DEFAULT_AUTH_USER_ROUTE_NAME = 'Home';
const DEFAULT_GUEST_USER_REDIRECT_PATH = '/auth/login';
const AUTH_PAGES = ['Login', 'Registration'];

export const useAuthInterceptor = router => {
  router.beforeEach((to, from, next) => {
    const token = getAuthToken();
    const noPagesForRoute = to?.matched?.length === 0;
    const isAuthDirection = AUTH_PAGES.includes(to?.name);
    const directionAllowedForGuests = to?.matched?.some(record => !record?.meta?.guest);

    if (token && (isAuthDirection || noPagesForRoute)) {
      return next({
        name: from?.name ?? DEFAULT_AUTH_USER_ROUTE_NAME
      });
    }

    if (!token && (directionAllowedForGuests || noPagesForRoute)) {
      return next({
        path: DEFAULT_GUEST_USER_REDIRECT_PATH,
        params: { nextUrl: to.fullPath }
      });
    }

    return next();
  });
};
