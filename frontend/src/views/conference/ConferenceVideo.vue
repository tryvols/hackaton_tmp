<template>
  <div
    class="conference-video__container"
    :style="styles"
    @mouseover="showVideoButtonsPanel"
    @mouseleave="hideVideoButtonsPanel"
  >
    <video class="conference-video" autoplay :srcObject.prop="stream"></video>
    <div class="conference-video__label">{{ name }}</div>
    <video-buttons-panel
      class="conference-video__buttons-panel"
      :show="videoButtonsPanelVisibility"
      @onClose="onClose"
    />
  </div>
</template>

<script>
import VideoButtonsPanel from './VideoButtonsPanel.vue';
export default {
  data () {
    return {
      videoButtonsPanelVisibility: false
    };
  },
  components: {
    VideoButtonsPanel
  },
  props: {
    styles: Object,
    uuid: {
      type: [String, Number],
      required: true
    },
    name: {
      type: String,
      required: true
    },
    stream: {
      type: MediaStream,
      required: true
    },
    buttonsPanel: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    onClose () {
      this.$emit('onClose', this.uuid);
    },
    showVideoButtonsPanel () {
      if (!this.buttonsPanel) {
        return;
      }
      this.videoButtonsPanelVisibility = true;
    },
    hideVideoButtonsPanel () {
      this.videoButtonsPanelVisibility = false;
    }
  }
};
</script>

<style lang="scss" scoped>
  .conference-video {
    position: absolute;
    left: 0;
    bottom: 0;
    height: auto;
    width: 100%;

    &__container {
      overflow: hidden;
      position: relative;
      border: 2px solid grey;
      box-sizing: border-box;
    }

    &__label {
      color: white;
      font: bold 18px Arial, Sans-Serif;
      line-height: 18px;
      height: 18px;

      background: rgba(0, 0, 0, 0.55);

      position: absolute;
      left: 0;
      bottom: 0;
      padding: 4px;
    }

    &__buttons-panel {
      position: absolute;
      bottom: 0;
      right: 0;
    }
  }
</style>
