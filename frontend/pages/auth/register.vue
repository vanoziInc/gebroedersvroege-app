<template>
  <v-container>
    <v-row class="justify-center">
      <v-col cols="lg-7 sm-6">
        <v-card>
          <v-card-text>
            <v-form ref="form" v-model="valid">
                            <v-text-field
                v-model="firstName"
                :rules="nameRules"
                label="Voornaam"
                required
              ></v-text-field>
                            <v-text-field
                v-model="lastName"
                :rules="nameRules"
                label="Achternaam"
                required
              ></v-text-field>

              <v-text-field
                v-model="email"
                :rules="emailRules"
                label="E-mail adres"
                required
              ></v-text-field>

              <v-text-field
                v-model="password"
                :rules="passwordRules"
                label="Wachtwoord"
                required
                :type="show ?'text': 'password'"
                :append-icon="show ?'mdi-eye':'mdi-eye-off'"   
                @click:append="show=!show"
              ></v-text-field>
              <v-text-field
                label="Herhaal wachtwoord"
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
              >Registreer</v-btn
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
  middleware: ['isLoggedIn'],
  data: () => ({
    show:false,
    valid: false,
    firstName:"",
    lastName:"",
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
        nameRules: [
      (v) => !!v || "Dit veld is verplicht",
      (v) => (v && v.length <= 20) || "Maximaal 20 tekens",
    ],
    confirmPassword: "",
    confirmPasswordRules: [(v) => !!v || "Dit veld is verplicht"],
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
        first_name: this.firstName,
        last_name:this.lastName,
        email: this.email,
        password: this.password,
      });
    },
  },
  computed: {
    passwordConfirmationRule() {
      return () =>
        this.password === this.confirmPassword || "Wachtwoorden moeten overeen komen";
    },
  },
};
</script>

<style>
</style>