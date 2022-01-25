<template>
  <div class="login-form">
    <h2 class="login-form__header">LOGIN</h2>
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

        <validation-provider v-slot="{ errors }" name="password" rules="required">
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
          class="login-form__error"
          v-for="error in loginValidationErrors"
          :key="error"
        >
          {{error}}
        </div>

        <div class="text-center">
          <v-btn class="login-form__signin-btn" type="submit" color="white" rounded dark>
            Sign In
          </v-btn>

          <v-btn
            class="login-form__signup-btn"
            text
            rounded
            dark
            outlined
            @click="moveToRegistration"
          >
            Sign Up
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
  name: 'Login',
  components: {
    ValidationProvider,
    ValidationObserver
  },
  data: () => ({
    email: '',
    password: null,
    showPass: false
  }),
  computed: {
    ...mapState('User', [
      'loginValidationErrors'
    ]),
    params () {
      return {
        email: this.email,
        password: this.password
      };
    }
  },
  methods: {
    ...mapActions('User', [
      'login'
    ]),
    async submit () {
      const valid = await this.$refs.observer.validate();
      if (valid) {
        await this.login(this.params);

        if (!this.loginValidationErrors.length) {
          this.clear();
          this.$router.push('/');
        }
      }
    },
    clear () {
      this.email = '';
      this.password = null;
      this.$refs.observer.reset();
    },
    moveToRegistration () {
      this.$router.push('/auth/registration');
    }
  }
};
</script>

<style lang="scss" scoped>
  .login-form {
    color: #fff;

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
