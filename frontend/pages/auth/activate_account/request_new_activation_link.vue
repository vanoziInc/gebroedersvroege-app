<template>
    <v-container>
    <v-row class="justify-center">
      <v-col cols="lg-7 sm-6">
        <v-card>
            <v-card-title>Nieuwe activatie link aanvragen</v-card-title>
          <v-card-text>
            <v-form id="request_new_activation_link" ref="form" v-model="valid">
              <v-text-field
                v-model="email"
                :rules="emailRules"
                label="E-mail adres"
                hint="Je ontvangt een email met een link om je account te activeren"
                required
              ></v-text-field>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-btn
              color="primary"
              :disabled="!valid"
              @click="requestLink"
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
         valid: false,
             email: "",
    emailRules: [
      (v) => !!v || "E-mail adres is verplicht",
      (v) => /.+@.+\..+/.test(v) || "Dit is geen valide e-mail adres",
    ],
 }),
 methods:{
    async requestLink() {

      // Login API call
      try {
        let response = await this.$axios.get("/auth/resent_activation_token/" + this.email);
        this.$notifier.showMessage({
          content: "Er is een email onderweg met een link om je account te activeren",
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
 }

}
</script>

<style>

</style>