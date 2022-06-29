<template>
  <div>
    <!-- Machine maintenance issue dialog -->
    <EditMachineMaintenanceIssueDlg ref="editMachineMaintenanceIssue"
      @save="save($event)" />
    <!-- Normal user Homepage -->
    <v-container v-if="!userIsAdmin">
      <v-row class="justify-center">
        <v-col :cols="$vuetify.breakpoint.mdAndUp ? 8 : 12" class="justify-center">
          <v-card>
            <v-card-title class="justify-center">Uren registratie</v-card-title>
            <v-card-actions class="justify-center">
              <v-btn outlined color="primary" to="/working_hours/">Invoeren</v-btn>
              <v-btn outlined color="primary" to="/working_hours/overview">Overzicht</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>

      </v-row>
      <v-row class="justify-center">
        <v-col :cols="$vuetify.breakpoint.mdAndUp ? 8 : 12" class="justify-center">
          <v-card>
            <v-card-title class="justify-center">Storingen / Onderhoud</v-card-title>
            <v-card-actions class="justify-center">
              <v-btn outlined color="primary" xl-large @click="openEditMachineMaintenanceDlg">Nieuwe Melding</v-btn>
              <v-btn outlined color="primary" xl-large>Overzicht</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
    <!-- Admin homepage -->
    <v-container v-if="userIsAdmin">
      <v-row class="justify-center">
        <v-col :cols="$vuetify.breakpoint.mdAndUp ? 6 : 12">
          <v-card>
            <v-card-subtitle class="font-weight-bold">
              Ontbrekende uren afgelopen week
            </v-card-subtitle>
            <v-card-text>
              <p>
                Week {{ lastWeekNumber }}:
                <span class="font-weight-light font-italic">({{ formatDateforTemplate(beginningOfLastWeek) }} / {{
                    formatDateforTemplate(endOfLastWeek)
                }})</span>
              </p>
              <ul>
                <div v-for="(item, i) in usersNotSubmittedLastWeek" :key="i">


                  <li v-if="item.submitted == false">
                    <a v-bind:href="'/admin/working_hours/user/' + item.user_id">{{ item.name }}</a>
                  </li>
                </div>
              </ul>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import moment from "moment";
import { mapActions } from "vuex";
export default {

  data: () => ({
    dateformat: "YYYY-MM-DD",
    missingHoursLastWeek: null,
    usersNotSubmittedLastWeek: null,
    sevenDaysAgo: moment().subtract(7, "days"),
    title: "Home"
  }),
  head() {
    return {
      title: this.title,
    }
  },
  methods: {
    // Machine maintenace dialog
    async openEditMachineMaintenanceDlg() {
      if (await this.$refs.editMachineMaintenanceIssue.open("Storing / Onderhoud melden", {})) {
      }
    },
    save(maintenance_issue) {
      console.log("hoi");
      this.add_machine_maintenance_issue(maintenance_issue)
    },
    formatDateforTemplate(value) {
      return moment(value).locale("nl").format("DD MMM");
    },
    async notSubmittedLastWeek() {
      // Login API call
      if (this.userIsAdmin) {
        try {
          let response = await this.$axios.get(
            "/working_hours/admin/week_overview",
            {
              params: {
                from_date: this.beginningOfLastWeek,
                to_date: this.endOfLastWeek,
              },
            }
          );
          this.missingHoursLastWeek = response.data;
          this.usersNotSubmittedLastWeek = response.data[0].employee_info;
        } catch (err) {
          if (err.response) {
            this.$notifier.showMessage({
              content: err.response.data.detail,
              color: "error",
            });
          }
        }
      }
    },
    ...mapActions({
      add_machine_maintenance_issue: "machine_maintenance/addMachineMainetenanceIssue",
    }),
  },
  computed: {
    lastWeekNumber() {
      return this.sevenDaysAgo.isoWeek();
    },
    beginningOfLastWeek() {
      return this.sevenDaysAgo.startOf("isoweek").format(this.dateformat);
    },
    endOfLastWeek() {
      return this.sevenDaysAgo.endOf("isoweek").format(this.dateformat);
    },
    userIsAdmin() {
      if (this.$auth.user.roles.filter((e) => e.name === "admin").length > 0) {
        return true;
      } else {
        return false;
      }
    },
  },
  created() {
    this.notSubmittedLastWeek();
  },
};
</script>

<style scoped>
</style>
