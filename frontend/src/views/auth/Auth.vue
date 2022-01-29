<template>
  <section class="section-container">
    <v-row class="signin">
      <v-col cols="8" class="left">
        <h1>Welcome to Webcam Service</h1>
      </v-col>
      <v-col cols="4" class="right">
        <router-view></router-view>
      </v-col>
    </v-row>
  </section>
</template>

<script>
export default {
  name: 'Auth'
};
</script>

<style lang="scss" scoped>
.section-container {
  background: #fff;
  height: 100%;
  width: 100%;
  box-shadow: 0 0 1px 1px rgba($color: #000000, $alpha: 0.1);
  box-sizing: border-box;

  .signin {
    display: flex;
    justify-content: space-between;
    padding: 0;
    height: 100%;
    margin: 0 auto;
    min-height: 600px;
    box-shadow: 0 0 1px 1px rgba($color: #000000, $alpha: 0.1);

    .left {
      padding: 30px;
      justify-content: center;
      align-items: center;
      box-sizing: border-box;
      display: flex;
      color: #30ac7c;
      background-color: #f9f9f9;
    }

    .right {
      padding: 30px;
      box-sizing: border-box;
      background: #30ac7c;
      color: #fff;
    }
  }
}
</style>
