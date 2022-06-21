export default {
  async getAllMachines({ commit }) {
    try {
      let response = await this.$axios.get("/machines/");
      commit("GETMACHINES", response.data)
    } catch (err) {
      if (err.response) {
        this.$notifier.showMessage({
          content: err.response.data,
          color: "error",
        });
      }
    }
  },
  async addOrUpdateMachine({ commit }, payload) {
    try {
      let response = await this.$axios.put("/machines/", payload);
      commit("ADDORUPDATEMACHINE", response.data)
      this.$notifier.showMessage({
        content: "Machine succesvol toegevoegd/gewijzigd!",
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
  async deleteMachine({commit}, id) {
    try {
      let response = await this.$axios.delete("/machines/" + id);
      commit("DELETEMACHINE", id)
      this.$notifier.showMessage({
        content: response.data.detail,
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