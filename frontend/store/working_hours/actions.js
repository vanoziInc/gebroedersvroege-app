export default {
    async getAllWorkingHours({commit}, user_id) {
        try {
          let response = await this.$axios.get("/working_hours/all_for_user/" + user_id);
          commit("GETWORKINGHOURS", response.data)
        } catch (err) {
          if (err.response) {
              this.$notifier.showMessage({
                content: err.response.data,
                color: "error",
              });
            }
        }
      },
      async addWorkingHoursToAllUsersState({commit}, user) {
        try {
          let response = await this.$axios.get("/working_hours/all_for_user/" + user.id);
          const payload = response.data
          commit("GETWORKINGHOURSALLUSERS", { user, payload })
        } catch (err) {
          if (err.response) {
              this.$notifier.showMessage({
                content: err.response.data,
                color: "error",
              });
            }
        }
      },
      async addWorkingHours({commit}, payload) {
        try {
          let response = await this.$axios.post("/working_hours/", payload);
          commit("ADDWORKINGHOURS", response.data)
          this.$notifier.showMessage({
            content: "Uren succesvol toegevoegd!",
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
      async addOrUpdateWorkingHours({commit},payload) {
        try {
          let response = await this.$axios.put("/working_hours/", payload);
          commit("ADDORUPDATEWORKINGHOURS", response.data)
          if (response.data.submitted == true) {
            this.$notifier.showMessage({
              content: "Uren ingediend",
              color: "success",
            });
          }
          else {
            this.$notifier.showMessage({
              content: "Uren aangepast",
              color: "success",
            });
          }

        } catch (err) {
          if (err.response) {
              this.$notifier.showMessage({
                content: err.response.data.detail,
                color: "error",
              });
          }
        }
      },
      async deleteWorkingHours({commit}, id) {
        try {
          let response = await this.$axios.delete("/working_hours/" + id);
          commit("DELETEWORKINGHOURS", id)
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
      resetStateAllUsersAllWorkingHours({commit}) {
        commit("RESETALLWORKINGHOURSALLUSERS")
      }
}