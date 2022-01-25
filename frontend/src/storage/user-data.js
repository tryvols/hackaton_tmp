const USER_KEY = 'user_data';

let user = null;

const loadUserData = () => {
  user = JSON.parse(localStorage.getItem(USER_KEY));
};

export const getUserData = () => {
  if (!user) {
    loadUserData();
  }

  return user;
};

export const setUserData = ({ email, username }) => {
  user = { email, username };
  localStorage.setItem(USER_KEY, JSON.stringify(user));
};

export const cleanUserData = () => {
  user = null;
  localStorage.removeItem(USER_KEY);
};
