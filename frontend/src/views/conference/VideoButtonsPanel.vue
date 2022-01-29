<template>
  <div class="video-buttons-panel" v-if="show">
    <v-btn color="red" fab dark small @click="onClose">
      <v-icon dark>mdi-close</v-icon>
    </v-btn>
  </div>
</template>

<script>
export default {
  props: {
    show: {
      type: Boolean,
      default: true
    }
  },
  methods: {
    onClose () {
      this.$emit('onClose');
    }
  }
};
</script>

<style lang="scss" scoped>
  .video-buttons-panel {
    display: flex;
    flex-direction: column;
    padding: 12px;
  }
</style>
