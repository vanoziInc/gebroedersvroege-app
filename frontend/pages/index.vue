<template>
  <div>
    <v-container v-if="!userIsAdmin">
      <v-row class="justify-center">
        <v-col cols="lg-7 sm-6" class="justify-center">
          <v-card>
            <v-card-title>Uren registratie</v-card-title>
            <v-card-text>
              Je kunt per week de gewerkte uren uren invoeren, als er
              bijzonderheden zijn kun je die kwijt bij de omschrijving. <br />
              Zodra je ze hebt ingedient zijn ze zichtbaar voor de administratie
              en in principe definitief <br />
              Mocht je een foutje hebben gemaakt kan de administratie (Marijke
              of Marietje) de uren voor die week weer vrijgeven.
            </v-card-text>
            <v-card-actions class="justify-center">
              <v-btn x-large outlined color="primary" to="/working_hours/"
                >Invoeren</v-btn
              >
              <v-btn
                x-large
                outlined
                color="primary"
                to="/working_hours/overview"
                >Overzicht</v-btn
              >
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
    <!-- Admin homepage -->
    <v-container v-if="userIsAdmin">
      <v-row class="justify-center">
        <v-col cols="lg-7 sm-6" class="justify-center">
          <v-card>
            <v-card-title>Openstaand afgelopen week</v-card-title>
            <v-card-text> </v-card-text>
            <v-card-actions class="justify-center">
              <v-btn x-large outlined color="primary" to="/working_hours/"
                >Week overzicht</v-btn
              >
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
export default {
  data: () => ({}),
  methods: {
    async notSubmittedWeeks() {
      // Login API call
      try {
        let response = await this.$axios.get(
          "/working_hours/admin/week_overview",
          { params: { from_date: this.dates[0], to_date: this.dates[1] } }
        );
        this.weeks_not_submitted = response.data.reverse();
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
  computed: {
    userIsAdmin() {
      if (this.$auth.user.roles.filter((e) => e.name === "admin").length > 0) {
        return true;
      } else {
        return false;
      }
    },
  },
};
</script>

<style scoped>
</style>