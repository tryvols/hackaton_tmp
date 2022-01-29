<template>
  <div class="home__wrapper">
    <v-app-bar
      class="home__header"
      color="#30ac7c"
      dense
      dark
    >
      <v-toolbar-title>Webcam Service</v-toolbar-title>

      <v-spacer></v-spacer>

      <v-btn @click="logout" plain>Log out</v-btn>
    </v-app-bar>

    <div
      class="home__new-conference-button"
      @click="createNewConference"
    >
      <span class="home__new-conference-button__text">
        New conference!
      </span>
    </div>

    <create-conference-dialog v-model="showCreateConferenceDialog"/>
  </div>
</template>

<script>
import { cleanAuthToken } from '../storage/auth-token';
import CreateConferenceDialog from './CreateConferenceDialog.vue';

export default {
  components: { CreateConferenceDialog },
  name: 'Home',
  data () {
    return {
      showCreateConferenceDialog: false
    };
  },
  methods: {
    logout () {
      cleanAuthToken();
      this.$store.dispatch('User/logout');
      this.$router.push('/auth/login');
    },
    createNewConference () {
      this.showCreateConferenceDialog = true;
      console.log('Works!');
    }
  }
};
</script>

<style lang="scss" scoped>
  .home {
    &__wrapper {
      display: flex;
      flex-direction: column;
      width: 100vw;
      height: 100vh;
    }

    &__header {
      max-height: 48px;
    }

    &__new-conference-button {
      display: flex;
      flex: 1;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      -webkit-box-shadow: 0px 0px 20px 25px rgba(48, 172, 124, 0.4) inset;
      -moz-box-shadow: 0px 0px 20px 25px rgba(48, 172, 124, 0.4) inset;
      box-shadow: 0px 0px 20px 25px rgba(48, 172, 124, 0.4) inset;

      &:hover {
        -webkit-box-shadow: 0px 0px 20px 35px rgba(48, 172, 124, 0.4) inset;
        -moz-box-shadow: 0px 0px 20px 35px rgba(48, 172, 124, 0.4) inset;
        box-shadow: 0px 0px 20px 35px rgba(48, 172, 124, 0.4) inset;
      }

      &__text {
        text-align: center;
        font-size: 32px;
        font-weight: bold;
        color: #30ac7c;
        text-shadow: 0px 0px 2px rgba(150, 150, 150, 0.4);
      }
    }
  }
</style>
