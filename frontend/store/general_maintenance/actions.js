export default {
    async getAllGeneralMaintenance({commit}) {
        try {
          let response = await this.$axios.get("/general_maintenance/");
          commit("GETGENERALMAINTENANCE", response.data)
        } catch (err) {
          if (err.response) {
              this.$notifier.showMessage({
                content: err.response.data,
                color: "error",
              });
            }
        }
      },
      async addGeneralMaintenance({commit}, payload) {
        try {
          let response = await this.$axios.post("/general_maintenance/", payload);
          commit("ADDGENERALMAINTENANCE", response.data)
          this.$notifier.showMessage({
            content: "Onderhoudsitem succesvol toegevoegd",
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
      async updateGeneralMaintenance({commit}, id, payload) {
        try {
          let response = await this.$axios.put("/general_maintenance/" + id, payload);
          commit("UPDATEGENERALMAINTENANCE", response.data)
          this.$notifier.showMessage({
            content: "Onderhoudsitem toegevoegd",
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
      async deleteGeneralMaintenance({commit}, id) {
        try {
          let response = await this.$axios.delete("/general_maintenance/" + id);
          commit("DELETEGENERALMAINTENANCE", response.data)
          this.$notifier.showMessage({
            content: "Onderhoudsitem verwijdert!",
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