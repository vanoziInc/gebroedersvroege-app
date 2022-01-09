<template>
  <div>
    <!-- Normal user Homepage -->
    <v-container v-if="!userIsAdmin">
      <v-row class="justify-center">
        <v-col
          :cols="$vuetify.breakpoint.mdAndUp ? 8: 12"
          class="justify-center"
        >
          <v-card>
            <v-card-title>Uren registratie</v-card-title>
            <v-card-text>
              Je kunt per week de gewerkte uren invoeren, als er
              bijzonderheden zijn kun je die kwijt bij de omschrijving. <br />
              Zodra je ze hebt ingedient zijn ze zichtbaar voor de administratie
              en in principe definitief. <br />
              Mocht je een foutje hebben gemaakt kan de administratie (Marijke
              of Marietje) de uren voor die week weer vrijgeven.
            </v-card-text>
            <v-card-actions class="justify-center">
              <v-btn
                outlined
                color="primary"
                to="/working_hours/"
              >Invoeren</v-btn>
              <v-btn
                outlined
                color="primary"
                to="/working_hours/overview"
              >Overzicht</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
    <!-- Admin homepage -->
    <v-container v-if="userIsAdmin">
      <v-row class="justify-center">
        <v-col :cols="$vuetify.breakpoint.mdAndUp ? 6: 12">
          <v-card>
            <v-card-subtitle class="font-weight-bold">
              Ontbrekende uren afgelopen week
            </v-card-subtitle>
            <v-card-text>
              <p>
                Week {{ lastWeekNumber }}:
                <span class="font-weight-light font-italic">({{ formatDateforTemplate(beginningOfLastWeek) }} / {{ formatDateforTemplate(endOfLastWeek) }})</span>
              </p>
              <ul>
                <div
                  v-for="(item, i) in usersNotSubmittedLastWeek"
                  :key="i"
                >

                
                <li v-if="item.submitted ==false">
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
export default {
  data: () => ({
    dateformat: "YYYY-MM-DD",
    missingHoursLastWeek: null,
    usersNotSubmittedLastWeek: null,
    sevenDaysAgo: moment().subtract(7, "days"),
  }),
  methods: {
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
