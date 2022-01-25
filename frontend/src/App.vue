<template>
  <v-app id="app">
    <keep-alive :include="['Login', 'Registration']">
      <router-view></router-view>
    </keep-alive>
  </v-app>
</template>

<script>
export default {
  name: 'App',
  created () {
    this.$store.dispatch('User/initDataOnLoad');
  }
};
</script>

<style lang="scss" scoped>
#app {
  width: 100vw;
  padding: 0;
  margin: 0;
}

::v-deep .v-application--wrap {
  padding: 0;
  margin: 0;
  // min-height: fit-content;
}
</style>
