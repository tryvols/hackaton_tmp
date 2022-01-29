import { userApi } from '../api/user';
import { setAuthToken } from '../storage/auth-token';
import { cleanUserData, getUserData, setUserData } from '../storage/user-data';

export const User = {
  namespaced: true,

  state: {
    email: '',
    username: '',
    loginValidationErrors: [],
    registrationValidationErrors: []
  },

  mutations: {
    setUserCredentials: (state, { email = '', username = '' } = {}) => {
      state.email = email;
      state.username = username;
    },

    setLoginValidationErrors: (state, errors) => {
      state.loginValidationErrors = errors ? Object.values(errors).map(([error]) => error) : [];
    },

    setRegistrationValidationErrors: (state, errors) => {
      state.registrationValidationErrors = errors ? Object.values(errors).map(([error]) => error) : [];
    }
  },

  actions: {
    initDataOnLoad: ({ commit }) => {
      const { email = '', username = '' } = getUserData() ?? {};
      commit('setUserCredentials', { email, username });
    },

    logout: ({ commit }) => {
      commit('setUserCredentials');
      cleanUserData();
    },

    login: async ({ commit }, credentials) => {
      try {
        const response = await userApi.login(credentials);
        const data = response?.data?.user;

        setAuthToken(data?.token);

        const userData = {
          email: data?.email,
          username: data?.username
        };

        commit('setUserCredentials', userData);
        setUserData(userData);

        commit('setLoginValidationErrors', null);
      } catch (error) {
        if (error?.response?.status) {
          commit('setLoginValidationErrors', error?.response?.data?.user);
        }
      }
    },

    register: async ({ commit }, payload) => {
      try {
        const response = await userApi.register(payload);
        const data = response?.data?.user;

        setAuthToken(data?.token);

        const userData = {
          email: data?.email,
          username: data?.username
        };

        commit('setUserCredentials', userData);
        setUserData(userData);

        commit('setRegistrationValidationErrors', null);
      } catch (error) {
        if (error?.response?.status) {
          commit('setRegistrationValidationErrors', error?.response?.data?.user);
        }
      }
    }
  }
};
