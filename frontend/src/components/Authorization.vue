<template>
  <div class="authorization">
    <template v-if="type === 'login'">
      <h2>Login</h2>

      <label
        :class="{ error: 'email' in clientErrors || 'email' in serverErrors }"
      >
        <input
          type="email"
          placeholder="Email..."
          v-model="email"
          autocomplete="username"
          key="login-username"
        />
        <button tabindex="-1">
          <span class="icon-email"></span>
        </button>
      </label>

      <label
        :class="{
          error: 'password' in clientErrors || 'password' in serverErrors
        }"
      >
        <input
          type="password"
          placeholder="Password..."
          v-model="password"
          autocomplete="current-password"
          key="login-password"
        />
        <button tabindex="-1">
          <span class="icon-password"></span>
        </button>
      </label>

      <button @click="login">Submit</button>

      <ul>
        <li v-for="(value, name) in serverErrors" :key="name" class="error">
          {{ value }}
        </li>
        <li :class="{ error: 'email' in clientErrors }">
          The email must be a valid string e.g. happiness@gmail.com.
        </li>
        <li :class="{ error: 'password' in clientErrors }">
          The password should be at least 8 to 32 characters long and have one
          lowercase, one uppercase and one digit characters.
        </li>
      </ul>
    </template>

    <template v-if="type === 'register'">
      <h2>Register</h2>

      <label
        :class="{
          error: 'username' in clientErrors || 'username' in serverErrors
        }"
      >
        <input
          type="text"
          placeholder="Username..."
          v-model="username"
          autocomplete="false"
          key="register-name"
        />
        <button tabindex="-1">
          <span class="icon-account"></span>
        </button>
      </label>

      <label
        :class="{ error: 'email' in clientErrors || 'email' in serverErrors }"
      >
        <input
          type="email"
          placeholder="Email..."
          v-model="email"
          autocomplete="username"
          key="register-username"
        />
        <button tabindex="-1">
          <span class="icon-email"></span>
        </button>
      </label>

      <label
        :class="{
          error: 'password' in clientErrors || 'password' in serverErrors
        }"
      >
        <input
          type="password"
          placeholder="Password..."
          v-model="password"
          autocomplete="new-password"
          key="register-password"
        />
        <button tabindex="-1">
          <span class="icon-password"></span>
        </button>
      </label>

      <label
        :class="{
          error: 'confirm' in clientErrors || 'confirm' in serverErrors
        }"
      >
        <input
          type="password"
          placeholder="Confirm password..."
          v-model="confirm"
          autocomplete="new-password"
          key="register-confirm"
        />
        <button tabindex="-1">
          <span class="icon-password"></span>
        </button>
      </label>

      <button @click="register">Submit</button>

      <ul>
        <li v-for="(value, name) in serverErrors" :key="name" class="error">
          {{ value }}
        </li>
        <li :class="{ error: 'username' in clientErrors }">
          The username should be at least 4 to 32 characters long.
        </li>
        <li :class="{ error: 'email' in clientErrors }">
          The email must be a valid string e.g. happiness@gmail.com.
        </li>
        <li :class="{ error: 'password' in clientErrors }">
          The password should be at least 8 to 32 characters long and have one
          lowercase, one uppercase and one digit characters.
        </li>
        <li :class="{ error: 'confirm' in clientErrors }">
          Passwords should match.
        </li>
      </ul>
    </template>
  </div>
</template>

<script>
import Vue from "vue";

export default {
  name: "Authorization",

  props: {
    type: {
      type: String,
      default: "register"
    }
  },

  data() {
    return {
      username: "",
      email: "",
      password: "",
      confirm: "",
      clientErrors: {},
      serverErrors: {}
    };
  },

  methods: {
    login() {
      this.clientErrors = {};
      this.serverErrors = {};

      if (!this.validateEmail(this.email)) {
        this.clientErrors["email"] = true;
      }

      if (!this.validatePassword(this.password)) {
        this.clientErrors["password"] = true;
      }

      if (
        Object.keys(this.clientErrors).length === 0 &&
        this.clientErrors.constructor === Object
      ) {
        const t = this;

        this.$store
          .dispatch("login", {
            email: this.email,
            password: this.password
          })
          .catch(message => {
            Vue.set(t.serverErrors, message.type, message.message);
          });
      }
    },

    register() {
      this.clientErrors = {};
      this.serverErrors = {};

      if (!this.validateUsername(this.username)) {
        this.clientErrors["username"] = true;
      }

      if (!this.validateEmail(this.email)) {
        this.clientErrors["email"] = true;
      }

      if (!this.validatePassword(this.password)) {
        this.clientErrors["password"] = true;
      }

      if (
        !this.validatePassword(this.confirm) ||
        this.confirm !== this.password
      ) {
        this.clientErrors["confirm"] = true;
      }

      if (
        Object.keys(this.clientErrors).length === 0 &&
        this.clientErrors.constructor === Object
      ) {
        const t = this;

        this.$store
          .dispatch("register", {
            username: this.username,
            email: this.email,
            password: this.password
          })
          .catch(message => {
            Vue.set(t.serverErrors, message.type, message.message);
          });
      }
    },

    validateUsername(username) {
      return /^.{4,32}$/.test(username);
    },

    validateEmail(email) {
      return /^(([^<>()[\].,;:\s@"]+(\.[^<>()[\].,;:\s@"]+)*)|(".+"))@(([^<>()[\].,;:\s@"]+\.)+[^<>()[\].,;:\s@"]{2,})$/i.test(
        email
      );
    },

    validatePassword(password) {
      return /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,32}$/.test(password);
    }
  }
};
</script>

<style lang="sass" scoped>
.authorization
  &>h2
    margin: 4rem 0 2rem
    text-align: center

  &>label
    margin-top: 1rem
    border-radius: $step
    box-shadow: 0 0 0 1px $color-primary
    display: flex
    flex-flow: row
    align-items: stretch
    justify-content: stretch
    background-color: $color-white
    overflow: hidden

    input
      flex: 1 1 auto
      padding: $step $step*6 $step $step
      color: $color-dark

    button
      flex: 0 0 $step*3
      padding: 0 $step
      margin-left: -$step*5

      span
        font-size: 1.5rem
        vertical-align: middle

      @media (hover: hover), (-ms-high-contrast:none)
        &:hover
          background-color: $color-primary
          color: $color-white

    &.error
      &>*
        color: $color-error
        border-color: $color-error

      @media (hover: hover), (-ms-high-contrast:none)
        button:hover
          background-color: $color-error
          color: $color-white

  &>button
    height: $step*5
    width: 100%
    margin-top: 2rem
    border-radius: $step
    background-color: $color-primary
    color: $color-white

    @media (hover: hover), (-ms-high-contrast:none)
      &:hover, &:focus
        background-color: $color-dark

  &>ul
    width: 100%
    padding: $step*1.5
    margin-top: 1rem
    list-style: inside
    color: $color-dark

    &>li + li
      margin-top: $step

    &>li.error
      color: $color-error
</style>
