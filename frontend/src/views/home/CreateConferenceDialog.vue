<template>
  <v-dialog
    class="create-conference-dialog"
    :value="isShown"
    @change="updateModal"
    width="500"
    persistent
  >
    <v-card>
      <v-card-title class="create-conference-dialog__header">
        Take your conference link!
      </v-card-title>

      <v-card-text class="create-conference-dialog__code">
        {{ conferenceCode | confCodeToLink }}
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          color="green darken-1"
          text
          @click="closeModal"
        >
          Close
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { conferenceApi } from '../../api/conference';

export default {
  name: 'CreateConferenceDialog',
  data () {
    return {
      conferenceCode: null
    };
  },
  model: {
    prop: 'isShown',
    event: 'change'
  },
  props: {
    isShown: Boolean
  },
  watch: {
    isShown (next, prev) {
      if (prev !== next && next === true) {
        this.createNewConference();
      }
    }
  },
  filters: {
    confCodeToLink (conferenceCode) {
      if (!conferenceCode) {
        return '';
      }

      return `${window.location.href}conference/${conferenceCode}`;
    }
  },
  methods: {
    async createNewConference () {
      const conference = await conferenceApi.createConference();
      this.conferenceCode = conference?.data?.conference?.url;
    },
    updateModal (value) {
      this.$emit('change', value);
    },
    closeModal () {
      this.updateModal(false);
    }
  }
};
</script>

<style lang="scss" scoped>
  .create-conference-dialog {
    &__header {
      background-color: #30ac7c;
      color: white;
    }

    &__code {
      font-size: 16px;
      margin-top: 20px;
    }
  }
</style>
