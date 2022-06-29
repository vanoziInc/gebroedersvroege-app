export default {
  async getAllMachineMaintenanceIssues({ commit }) {
    try {
      let response = await this.$axios.get("/machine_maintenance_issues/");
      commit("GETMACHINEMAINTENANCEISSUES", response.data)
    } catch (err) {
      if (err.response) {
        this.$notifier.showMessage({
          content: err.response.data,
          color: "error",
        });
      }
    }
  },
  async addMachineMainetenanceIssue({ commit }, payload) {
    try {
      let response = await this.$axios.post("/machine_maintenance_issues/", payload);
      commit("ADDORUPDATEMACHINEMAINTENANCEISSUES", response.data)
      this.$notifier.showMessage({
        content: "Storing / Onderhoud succesvol toegevoegd",
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
  async updateMachineMainetenanceIssue({ commit }, payload) {
    try {
      let response = await this.$axios.put("/machine_maintenance_issues/", payload);
      commit("ADDORUPDATEMACHINEMAINTENANCEISSUES", response.data)
      this.$notifier.showMessage({
        content: "Storing / Onderhoud  succesvol gewijzigd",
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
  async deleteMachineMaintenanceIssue({commit}, id) {
    try {
      let response = await this.$axios.delete("/machine_maintenance_issues/" + id);
      commit("DELETEMACHINEMAINTENANCEISSUE", id)
      this.$notifier.showMessage({
        content: "Storing / Onderhoud  succesvol gewijzigd",
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