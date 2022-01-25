<template>
  <div class="registration">
    <h2 class="registration__header">Registration</h2>
    <validation-observer ref="observer">
      <v-form @submit.prevent="submit">
        <validation-provider v-slot="{ errors }" name="email" rules="required|email">
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

        <validation-provider v-slot="{ errors }" name="username" rules="required">
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

        <validation-provider v-slot="{ errors }" name="password" rules="required" ref="Password">
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

        <div
          class="registration__error"
          v-for="error in registrationValidationErrors"
          :key="error"
        >
          {{error}}
        </div>

        <div class="text-center">
          <v-btn class="registration__signin-btn" type="submit" rounded color="white" dark>
            Sign Up
          </v-btn>

          <v-btn class="registration__signup-btn" text rounded dark outlined @click="moveToLogin">
            Sign In
          </v-btn>
        </div>
      </v-form>
    </validation-observer>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex';
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
    ...mapState('User', [
      'registrationValidationErrors'
    ]),
    params () {
      return {
        email: this.email,
        password: this.password,
        username: this.username
      };
    }
  },
  methods: {
    ...mapActions('User', [
      'register'
    ]),
    async submit () {
      const valid = await this.$refs.observer.validate();
      if (valid) {
        await this.register(this.params);

        if (!this.registrationValidationErrors.length) {
          this.clear();
          this.$router.push('/');
        }
      }
    },
    clear () {
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

    &__error {
      font-size: 0.8em;

      &::first-letter {
        text-transform: capitalize;
      }
    }

    span + &__error {
      margin-top: -10px;
    }

    &__error + .text-center {
      margin-top: 15px;
    }
  }
</style>
