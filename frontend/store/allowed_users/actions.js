export default {
    async getAllowedUsers({commit}) {
        try {
          let response = await this.$axios.get("/allowed_users/");
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
          let response = await this.$axios.post("/allowed_users/", payload);
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
      async deleteAllowedUser({commit}, id) {
        try {
          let response = await this.$axios.delete("/allowed_users/" + id);
          commit("DELETEALLOWEDUSER", response.data)
          this.$notifier.showMessage({
            content: "Uitnodiging ingetrokken!",
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