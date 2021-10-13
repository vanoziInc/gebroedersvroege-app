<template>
  <v-container>
    <p>
      Current User: <br />
      {{ this.$store.state.auth.user }}
    </p>
    <v-data-table
      :headers="headers"
      :items="users"
      :items-per-page="5"
      class="elevation-1"
    ></v-data-table>

    <p>Add User:</p>
    <v-text-field v-model="payload.email"> </v-text-field><br />
    <v-text-field v-model="payload.password"> </v-text-field>
    <v-btn @click="addUser(payload)"> add user</v-btn>
    <p>Change User:</p>
  </v-container>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
export default {
  middleware: ['isAdmin'],
  data() {
    return {
      headers: [
        {
          text: "Email",
          value: "email",
        },
        {
          text: "Verified",
          value: "is_active",
        },
      ],
      payload: {
        email: "",
        password: "",
      },
    };
  },
  methods: {
    ...mapActions({
      getUsers: "users/getUsers",
      addUser: "users/addUser",
    }),
    async userLogin() {
      const form = new FormData();
      form.append("username", this.username);
      form.append("password", this.password);
      try {
        let response = await this.$auth.loginWith("local", { data: form });
      } catch (err) {
        console.log(err.response);
      }
    },
  },
  computed: {
    // mix the getters into computed with object spread operator
    ...mapGetters({
      users: "users/Users",
    }),
  },
  created() {
    this.getUsers();
  },
};
</script>

<style>
</style>