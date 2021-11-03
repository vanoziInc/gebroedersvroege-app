<template>
  <v-container>
    <v-row class="justify-center">
      <v-col cols="lg-7 sm-6">
        <v-card>
          <v-card-title>Wachtwoord vergeten</v-card-title>
          <v-card-text>
            <v-form id="forgot_password_form" ref="form" v-model="valid">
              <v-text-field
                v-model="email"
                :rules="emailRules"
                label="E-mail adres"
                hint="Je ontvangt een email met een link om je wachtwoord te resetten"
                required
              ></v-text-field>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-btn
              id="login_submit"
              color="primary"
              :disabled="!valid"
              @click="forgotPassword"
              >VERSTUUR</v-btn
            >
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  auth: false,
  data: () => ({
    title:"Wachtwoord vergeten",
    valid: false,
    email: "",
    emailRules: [
      (v) => !!v || "E-mail is required",
      (v) => /.+@.+\..+/.test(v) || "E-mail must be valid",
    ],
  }),
    head() {
      return {
        title: this.title,}
        },
  methods: {
    async forgotPassword() {
      // Login API call
      try {
        let response = await await this.$axios.get(
          "/auth/forgot_password/" + this.email
        );
        this.$notifier.showMessage({
          content:
            "Er is een email onderweg met een link om je password te resetten",
          color: "success",
        });
        this.$router.push("/auth/login");
      } catch (err) {
        if (err.response) {
            this.$notifier.showMessage({
              content: err.response.data.detail,
              color: "error",
            });
        }
      }
    },
  },
};
</script>

<style>
</style>