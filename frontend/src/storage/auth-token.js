import { setBackendToken } from '../plugins/axios';

const TOKEN_KEY = 'jwt';

let token = null;

const loadAuthToken = () => {
  token = localStorage.getItem(TOKEN_KEY);
  setBackendToken(token);
};

export const getAuthToken = () => {
  if (!token) {
    loadAuthToken();
  }

  return token;
};

export const setAuthToken = _token => {
  token = _token;
  localStorage.setItem(TOKEN_KEY, _token);
  setBackendToken(_token);
};

export const cleanAuthToken = () => {
  token = null;
  localStorage.removeItem(TOKEN_KEY);
};
