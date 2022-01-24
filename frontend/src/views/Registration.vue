<template>
  <div class="registration">
    <h2 class="registration__header">Registration</h2>
    <validation-observer ref="observer">
      <v-form @submit.prevent="submit">
        <validation-provider v-slot="{ errors }" name="Email" rules="required|email">
          <v-text-field
            v-model="email"
            :error-messages="errors"
            label="Email"
            required
            outlined
            dark
            filled
            dense
          ></v-text-field>
        </validation-provider>

        <validation-provider v-slot="{ errors }" name="Username" rules="required">
          <v-text-field
            v-model="username"
            :error-messages="errors"
            label="Username"
            required
            outlined
            dark
            filled
            dense
          ></v-text-field>
        </validation-provider>

        <validation-provider v-slot="{ errors }" name="Password" rules="required" ref="Password">
          <v-text-field
            v-model="password"
            :error-messages="errors"
            label="Password"
            :append-icon="showPass ? 'mdi-eye' : 'mdi-eye-off'"
            @click:append="showPass = !showPass"
            required
            outlined
            dense
            dark
            filled
            :type="showPass ? 'text' : 'password'"
          ></v-text-field>
        </validation-provider>

        <div class="text-center">
          <v-btn class="registration__signin-btn" type="submit" rounded color="white" dark>
            Sign In
          </v-btn>

          <v-btn class="registration__signup-btn" text rounded dark outlined @click="moveToLogin">
            Sign Up
          </v-btn>
        </div>
      </v-form>
    </validation-observer>
  </div>
</template>

<script>
import { required, email } from 'vee-validate/dist/rules';
import { extend, ValidationProvider, setInteractionMode, ValidationObserver } from 'vee-validate';

setInteractionMode('eager');

extend('required', {
  ...required,
  message: '{_field_} can not be empty'
});

extend('email', {
  ...email,
  message: 'Email must be valid'
});

export default {
  name: 'Registration',
  components: {
    ValidationProvider,
    ValidationObserver
  },
  data: () => ({
    username: '',
    email: '',
    password: null,
    showPass: false
  }),
  computed: {
    params () {
      return {
        email: this.email,
        password: this.password
      };
    }
  },
  methods: {
    async submit () {
      const valid = await this.$refs.observer.validate();
      if (valid) {
        this.login(this.params); // action to login
      }
    },
    clear () {
      // you can use this method to clear login form
      this.username = '';
      this.email = '';
      this.password = null;
      this.$refs.observer.reset();
    },
    moveToLogin () {
      this.$router.push('/auth/login');
    }
  }
};
</script>

<style lang="scss" scoped>
  .registration {
    &__header {
      text-align: center;
      margin: 30px 0;
    }

    &__signin-btn {
      width: 100%;
      color: #30ac7c !important;
    }

    &__signup-btn {
      margin-top: 20px;
      width: 100%;
    }
  }
</style>
