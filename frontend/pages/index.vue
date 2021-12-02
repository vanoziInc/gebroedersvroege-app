<template>
  <v-container>
    <v-row class="justify-center">
      <v-col
        cols="lg-7 sm-6"
        class="justify-center"
      >
        <v-card>
          <v-card-title>Uren registratie</v-card-title>
          <v-card-text>
            Je kunt per week de gewerkte uren uren invoeren, als er bijzonderheden zijn kun je die kwijt bij de omschrijving.<br>
            Zodra je ze hebt ingedient zijn ze zichtbaar voor de administratie en in principe definitief <br>
            Mocht je toch een foutje hebben gemaakt kan de administratie de uren voor die week weer vrijgeven.
          </v-card-text>
          <v-card-actions class="justify-center">
            <v-btn
              x-large
              outlined
              color="primary"
              to="/working_hours/"
            >Invoeren</v-btn>
            <v-btn
              x-large
              outlined
              color="primary"
              to="/working_hours/overview"
            >Overzicht</v-btn>
          </v-card-actions>
        </v-card>

      </v-col>
    </v-row>

  </v-container>

</template>

<script>
export default {
  data: () => ({}),
};
</script>

<style scoped>
</style>