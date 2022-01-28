<template>
  <v-container>
      <h5>Datum upload: 26 jan 2022</h5>
    <template>
          <v-card>
    <v-card-title>
      <v-text-field
        v-model="search"
        append-icon="mdi-magnify"
        label="Zoeken"
        single-line
        hide-details
      ></v-text-field>
    </v-card-title>
      <v-data-table
        :headers="headers"
        :items="items"
        :search="search"
        :items-per-page="100"
        mobile-breakpoint="0"
        class="elevation-1"
      >  <template v-slot:[`item.werknaam`]="{ item }">
    <a :href="item.link">{{item.werknaam}}</a>
  </template></v-data-table></v-card> </template
  ></v-container>
</template>

<script>
export default {
  data: () => ({
      search: '',
    headers: [
      {
        text: "Perceel",
        align: "start",
        sortable: true,
        value: "perceel nummer",
      },
      { text: "Werknaam", sortable: true, value: "werknaam" },
    //   { text: "Link", sortable: true, value: "boer en bunder link" },
      { text: "RVO ha", sortable: true, value: "RVO ha totaal" },
      { text: "Gewas", sortable: true, value: "gewas" },
      { text: "Opmerking", sortable: true, value: "opmerking" },
    ],

    items: [],
  }),
  methods: {
    async bouwplan() {
      // Login API call
      try {
        let response = await this.$axios.get("/bouwplan/");
        this.items = response.data;
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
    created() {
    this.bouwplan();
  },
};
</script>

<style>
</style>
