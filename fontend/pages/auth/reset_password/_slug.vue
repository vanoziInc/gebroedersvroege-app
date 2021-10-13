<template>
  <v-container>
    <v-row class="justify-center mt-6">
      <v-col cols="lg-7 sm-6">
        <v-card>
          <v-card-text>
            <v-form ref="form" v-model="valid">
              <v-text-field
                v-model="password"
                :rules="passwordRules"
                label="Password"
                required
                :type="show ? 'text' : 'password'"
                :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append="show = !show"
              ></v-text-field>
              <v-text-field
                label="Confirm Password"
                v-model="confirmPassword"
                :rules="confirmPasswordRules.concat(passwordConfirmationRule)"
                required
                :type="show ? 'text' : 'password'"
                :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append="show = !show"
              ></v-text-field>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" :disabled="!valid" @click="resetPassword"
              >Reset Password</v-btn
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
    token: "",
    show: false,
    valid: false,
    password: "",
    passwordRules: [
      (v) => !!v || "Password is required",
      (v) => (v && v.length >= 5) || "Password must have 5+ characters",
    ],
    confirmPassword: "",
    confirmPasswordRules: [(v) => !!v || "Password is required"],
  }),
  methods: {
    async resetPassword() {
      try {
        let response = await this.$axios.post("/auth/reset_password", {
          token: this.token,
          password: this.password,
        });
        this.$notifier.showMessage({
          content: "Wachtwoord succesvol gerest, je kunt nu proberen in te loggen",
          color: "success",
        });
        this.$router.push("/auth/login");
        
      } catch (err) {
        console.log(err.response);
      }
    },
  },
  mounted() {
    this.token = this.$route.params.slug;
  },
  computed: {
    passwordConfirmationRule() {
      return () =>
        this.password === this.confirmPassword || "Password must match";
    },
  },
};
</script>
<style>
</style>