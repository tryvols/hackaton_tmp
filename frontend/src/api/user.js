import { backend } from '../plugins/axios';

const login = async ({ email, password }) => {
  return backend.post('/users/login/', {
    user: {
      email,
      password
    }
  });
};

const register = async ({ email, username, password }) => {
  return backend.post('/users/register/', {
    user: {
      email,
      username,
      password
    }
  });
};

export const userApi = {
  login,
  register
};
