<template>
  <v-container>
    <v-data-table
      :headers="headers"
      :items="werknemers"
    >
      <template #item.name="{ item }">
                    <a v-bind:href="'/admin/working_hours/user/' + item.id">
                      {{ item.first_name }} {{ item.last_name }}
                    </a>
      </template>

    </v-data-table>
  </v-container>

</template>

<script>
import { mapGetters, mapActions } from "vuex";
export default {
  data: () => ({
    headers: [
      {
        text: "Naam",
        value: "name",
        sortable: false,
      },
    ],
  }),
  methods: {
    ...mapActions({
      getAllUsers: "users/getUsers",
    }),
  },
  computed: {
    ...mapGetters({
      werknemers: "users/Werknemers",
    }),
  },
  created() {
    this.getAllUsers();
  },
};
</script>

<style>
</style>