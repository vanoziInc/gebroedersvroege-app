<template>
  <v-container>
    <v-simple-table dense>
    <template v-slot:default>
      <thead>
        <tr>
          <th class="text-left">
            Naam
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="item in werknemers"
          :key="item.name"
        >
          <td><span><a v-bind:href="'/admin/working_hours/user/'+ item.id">
          {{ item.first_name }} {{ item.last_name }}
          </a>
            
            </span></td>
        </tr>
      </tbody>
    </template>
  </v-simple-table>
    </v-container
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
      // users met rol werknemer
      werknemers: 'users/Werknemers'
    }),
    
  },
  created() {
    this.getAllUsers();
  },
};
</script>

<style>
</style>