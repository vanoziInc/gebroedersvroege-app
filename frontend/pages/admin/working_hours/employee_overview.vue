<template>
  <v-container>

    <v-simple-table
      dense
      class="mt-3"
    >
      <template v-slot:default>
        <thead>
          <tr>
            <th class="text-left">Naam</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(item, i) in werknemers"
            :key="i"
          >
            <td> <a v-bind:href="'/admin/working_hours/user/' + item.id">
                {{ item.first_name }} {{ item.last_name }}
              </a></td>
          </tr>
        </tbody>
      </template>
    </v-simple-table>
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