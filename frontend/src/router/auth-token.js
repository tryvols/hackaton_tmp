const TOKEN_KEY = 'jwt';

let token = null;

const saveAuthToken = _token => {
  localStorage.setItem(TOKEN_KEY, _token);
};

const loadAuthToken = () => {
  token = localStorage.getItem(TOKEN_KEY);
};

export const getAuthToken = () => {
  if (!token) {
    loadAuthToken();
  }

  return token;
};

export const setAuthToken = _token => {
  token = _token;
  saveAuthToken(_token);
};

export const cleanAuthToken = () => {
  token = null;
  localStorage.removeItem(TOKEN_KEY);
};
