<template>
  <v-container>
    <v-row class="justify-center">
      <v-col cols="lg-7 sm-6">
        <v-card>
          <v-card-text>
            <v-form id="login_form" ref="form" v-model="valid">
              <v-text-field
                id="login_email"
                v-model="email"
                :rules="emailRules"
                label="E-mail adres"
                required
              ></v-text-field>

              <v-text-field
                id="login_password"
                v-model="password"
                :rules="passwordRules"
                label="Wachtwoord"
                required
                :type="show ? 'text' : 'password'"
                :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append="show = !show"
              ></v-text-field>
            </v-form>
            <a href="/auth/forgot_password">Wachtwoord vergeten?</a>
          </v-card-text>
          <v-card-actions>

            <v-btn
              id="login_submit"
              color="primary"
              :disabled="!valid"
              @click="userLogin"
              >Login</v-btn
            >
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  middleware: ['isLoggedIn'],
  auth: false,
  data: () => ({
    title:"Login",
    show: false,
    valid: false,
    email: "",
    emailRules: [
      (v) => !!v || "E-mail adres is verplicht",
      (v) => /.+@.+\..+/.test(v) || "Dit is geen valide e-mail adres",
    ],
    password: "",
    passwordRules: [
      (v) => !!v || "Wachtwoord is verplicht",
      (v) => (v && v.length >= 5) || "Wachtwoord moet minstens 5 tekens lang zijn",
    ],
  }),
  head() {
      return {
        title: this.title,}
        },
  methods: {
    validate() {
      this.$refs.form.validate();
    },
    reset() {
      this.$refs.form.reset();
    },
    resetValidation() {
      this.$refs.form.resetValidation();
    },
    async userLogin() {
      // create login form
      const form = new FormData();
      form.append("username", this.email);
      form.append("password", this.password);
      // Login API call
      try {
        let response = await this.$auth.loginWith("local", { data: form });
        this.$notifier.showMessage({
          content: "Welcome " + this.$auth.user.email,
          color: "success",
        });
        this.$router.push("/");
      } catch (err) {
        if (err.response) {
          if (err.response.status == 401) {
            this.$notifier.showMessage({
              content: err.response.data.detail,
              color: "error",
            });
          }
        }
      }
    },
  },
};
</script>

<style>
</style>