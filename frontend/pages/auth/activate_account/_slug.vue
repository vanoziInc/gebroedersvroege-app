<template>
  <v-container>
    <v-row class="justify-center mt-6">
      <v-card>
        <v-card-title>Account activeren</v-card-title>
        <v-card-text>
          Door op onderstaande knop te klikken wordt het account actief!
        </v-card-text>
        <v-card-actions class="justify-center">
          <v-btn color="primary" @click="activateAccount()">Activeer</v-btn>
        </v-card-actions>
      </v-card>
    </v-row>
  </v-container>
</template>

    <script>
export default {
  auth: false,
  data: () => ({
    title: "Activeer account",
    token: "",
  }),
  head() {
    return {
      title: this.title,
    };
  },
  methods: {
    async activateAccount() {
      try {
        let response = await this.$axios.post("/auth/activate_account", {
          token: this.token,
        });
        this.$notifier.showMessage({
          content: "Je account is geactiveerd, je kunt nu inloggen",
          color: "success",
        });
        this.$router.push("/auth/login");
      } catch (err) {
        if (err.response) {
          if (
            err.response.status == 400 &&
            err.response.data.detail == "Deze link is verlopen"
          ) {
            this.$notifier.showMessage({
              content: err.response.data.detail,
              color: "error",
            });
            this.$router.push(
              "/auth/activate_account/request_new_activation_link"
            );
          } else {
            this.$notifier.showMessage({
              content: err.response.data.detail,
              color: "error",
            });
            this.$router.push("/auth/login");
          }
        }
      }
    },
  },
  mounted() {
    this.token = this.$route.params.slug;
  },
};
</script>
<style>
</style>