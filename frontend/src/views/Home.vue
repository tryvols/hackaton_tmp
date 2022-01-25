<template>
  <button @click="logout">Hello world!</button>
</template>

<script>
import { cleanAuthToken } from '../storage/auth-token';

export default {
  name: 'Home',
  methods: {
    logout () {
      cleanAuthToken();
      this.$store.dispatch('User/logout');
      this.$router.push('/auth/login');
    }
  }
};
</script>
