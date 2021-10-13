<template>
  <v-container>
    <v-row class="justify-center">
      <v-col cols="lg-7 sm-6">
        <v-card>
          <v-card-text>
            <v-form ref="form" v-model="valid">
              <v-text-field
                v-model="email"
                :rules="emailRules"
                label="E-mail"
                required
              ></v-text-field>

              <v-text-field
                v-model="password"
                :rules="passwordRules"
                label="Password"
                required
                :type="show ?'text': 'password'"
                :append-icon="show ?'mdi-eye':'mdi-eye-off'"   
                @click:append="show=!show"
              ></v-text-field>
              <v-text-field
                label="Confirm Password"
                v-model="confirmPassword"
                :rules="confirmPasswordRules.concat(passwordConfirmationRule)"
                required
                :type="show ?'text': 'password'"
                :append-icon="show ?'mdi-eye':'mdi-eye-off'"   
                @click:append="show=!show"
              ></v-text-field>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" :disabled="!valid" @click="registerUser"
              >Register</v-btn
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
    show:false,
    valid: false,
    email: "",
    emailRules: [
      (v) => !!v || "E-mail is required",
      (v) => /.+@.+\..+/.test(v) || "E-mail must be valid",
    ],
    password: "",
    passwordRules: [
      (v) => !!v || "Password is required",
      (v) => (v && v.length >= 5) || "Password must have 5+ characters",
    ],
    confirmPassword: "",
    confirmPasswordRules: [(v) => !!v || "Password is required"],
  }),

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
    registerUser() {
      this.$store.dispatch("users/addUser", {
        email: this.email,
        password: this.password,
      });
      console.log("henk")
    },
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