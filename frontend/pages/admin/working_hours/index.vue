<template>
  <v-container>
      {{nonAdminUsers}}
    <v-data-table
      :headers="headers"
      :items="users"
      hide-default-footer
    >
    <template v-slot:[`item.full_name`]="{ item }">{{ item.first_name }} {{ item.last_name }}</template>
    </v-data-table></v-container
  >
</template>

<script>
import { mapGetters, mapActions } from "vuex";
export default {
  data: () => ({
    headers: [
      {
        text: "Naam",
        value: "full_name",
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
    // Getters from the store
    // mix the getters into computed with object spread operator
    ...mapGetters({
      users: "users/Users",
      nonAdminUsers: 'users/nonAdminUsers'
    }),
  },
  created() {
    this.getAllUsers();
  },
};
</script>

<style>
</style>