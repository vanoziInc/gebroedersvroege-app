<template>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
export default {
  data() {
    return {
      title: "Home",
      login: {
        username: "test@test.com",
        password: "test123$%",
      },
    };
  },
  head() {
    return {
      title: this.title,
    };
  },
  methods: {
    ...mapActions({
      getUsers: "users/getUsers",
    }),
    async userLogin() {
      const form = new FormData();
      form.append("username", this.login.username);
      form.append("password", this.login.password);
      try {
        let response = await this.$auth.loginWith("local", { data: form });
      } catch (err) {
        console.log(err.response);
      }
    },

    addOne() {
      this.$store.commit("todos/increment");
    },

    refresh() {
      this.$auth.refreshTokens();
    },
  },
  computed: {
    // mix the getters into computed with object spread operator
    ...mapGetters({
      users: "users/Users",
    }),
  },
};
</script>
