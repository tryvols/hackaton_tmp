import { backend } from '../plugins/axios';

const createConference = async () => {
  return backend.post('/conference/create/');
};

export const conferenceApi = {
  createConference
};
