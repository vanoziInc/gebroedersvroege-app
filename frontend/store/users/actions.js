export default {
    async getUsers({commit}) {
        try {
          let response = await this.$axios.get("/users");
          commit("GETUSERS", response.data)
        } catch (err) {
          console.log(err.response);
        }
      },
      async addUser({commit}, payload) {
        try {
          let response = await this.$axios.post("/auth/register", payload);
          commit("ADDUSER", response.data)
          this.$notifier.showMessage({
            content: "Succesvol geregistreerd, er is een email onderweg met een activatie link!",
            color: "success",
          });
          this.$router.push('/auth/login')
        } catch (err) {
          if (err.response) {
            if (err.response.status == 400) {
              this.$notifier.showMessage({
                content: err.response.data.detail,
                color: "error",
              });
            }
          }
        }
      },
}