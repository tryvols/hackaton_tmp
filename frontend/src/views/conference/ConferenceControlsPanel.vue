<template>
  <div class="conference-controls-panel">
    <v-btn
      class="conference-controls-panel__button"
      color="red darken-2"
      fab
      dark
      small
      @click="onClose"
    >
      <v-icon dark>mdi-close</v-icon>
    </v-btn>
    <v-btn
      class="conference-controls-panel__button"
      :color="isVideoMuted ? 'red darken-2' : 'grey darken-3'"
      fab
      dark
      small
      @click="changeMute"
    >
      <v-icon dark v-if="isVideoMuted">mdi-microphone-off</v-icon>
      <v-icon dark v-else>mdi-microphone</v-icon>
    </v-btn>
    <v-btn
      class="conference-controls-panel__button"
      :color="isVideoDisabled ? 'red darken-2' : 'grey darken-3'"
      fab
      dark
      small
      @click="changeVideoStreamState"
    >
      <v-icon dark v-if="isVideoDisabled">mdi-video-off</v-icon>
      <v-icon dark v-else>mdi-video</v-icon>
    </v-btn>
  </div>
</template>

<script>
export default {
  created () {
    this.isVideoDisabled = !this.enabledVideoByDefault;
    this.isVideoMuted = this.mutedByDefault;
  },
  data () {
    return {
      isVideoDisabled: false,
      isVideoMuted: true
    };
  },
  props: {
    enabledVideoByDefault: {
      type: Boolean,
      default: true
    },
    mutedByDefault: {
      type: Boolean,
      default: true
    }
  },
  methods: {
    changeMute () {
      this.isVideoMuted = !this.isVideoMuted;

      if (this.isVideoMuted) {
        this.mute();
      } else {
        this.unmute();
      }
    },

    changeVideoStreamState () {
      this.isVideoDisabled = !this.isVideoDisabled;

      if (this.isVideoDisabled) {
        this.disableVideo();
      } else {
        this.enableVideo();
      }
    },

    onClose () {
      this.$emit('finishCall');
    },
    mute () {
      this.$emit('mute');
    },
    unmute () {
      this.$emit('unmute');
    },
    enableVideo () {
      this.$emit('enableVideo');
    },
    disableVideo () {
      this.$emit('disableVideo');
    }
  }
};
</script>

<style lang="scss" scoped>
  .conference-controls-panel {
    display: flex;
    flex-direction: row;

    position: fixed;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);

    border-radius: 30px 30px 0px 0px / 30px 30px 0px 0px;
    padding: 15px;
    background: rgba(71, 66, 66, 0.55);

    &__button {
      & + & {
        margin-left: 10px;
      }
    }
  }
</style>
