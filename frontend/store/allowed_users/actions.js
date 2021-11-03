export default {
    async getAllowedUsers({commit}) {
        try {
          let response = await this.$axios.get("/allowed_users");
          commit("GETALLOWEDUSERS", response.data)
        } catch (err) {
          if (err.response) {
              this.$notifier.showMessage({
                content: err.response.data,
                color: "error",
              });
            }
        }
      },
      async addAllowedUser({commit}, payload) {
        try {
          let response = await this.$axios.post("/allowed_users", payload);
          commit("ADDALLOWEDUSER", response.data)
          this.$notifier.showMessage({
            content: "Uitnodiging om te registreren verstuurd!",
            color: "success",
          });
        } catch (err) {
          if (err.response) {
              this.$notifier.showMessage({
                content: err.response.data.detail,
                color: "error",
              });
          }
        }
      },
}