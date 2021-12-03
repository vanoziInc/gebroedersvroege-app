<template>
  <v-container>
    <v-tabs centered>
      <v-tab href="#not_submitted">Openstaade weken</v-tab>
      <v-tab-item value="hours_per_user">
        <v-simple-table dense>
          <template v-slot:default>
            <thead>
              <tr>
                <th class="text-left">Naam</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in werknemers" :key="item.name">
                <td>
                  <span
                    ><a v-bind:href="'/admin/working_hours/user/' + item.id">
                      {{ item.first_name }} {{ item.last_name }}
                    </a>
                  </span>
                </td>
              </tr>
            </tbody>
          </template>
        </v-simple-table>
      </v-tab-item>
      <v-tab href="#hours_per_user">Overzicht per medewerker</v-tab>
      <v-tab-item value="not_submitted">
        <!-- Overzicht alle werknemers -->
        <v-toolbar flat>
          <!-- jaar aanpassen -->
          <v-btn icon @click="substractYear">
            <v-icon>mdi-chevron-triple-left</v-icon>
          </v-btn>
          <b>{{ computedSelectedYear }}</b>
          <v-btn icon @click="addYear" v-if="nextYearAllowed">
            <v-icon>mdi-chevron-triple-right</v-icon>
          </v-btn>
        </v-toolbar>
        <div
          v-for="(item, index) in weeks_not_submitted"
          :key="item.week"
        >
          <v-card class="mb-2">
            <v-card-text>
              <p class="text-h6 text--primary">
                Weeknummer: {{ item.week }}
              </p>
              <div>Van: {{ item.week_start }}</div>
              <div>Tot: {{ item.week_end }}</div>
              <br />
              <div class="text--primary">
                Nog niet ingediend: {{ item.not_submitted }}
              </div>
            </v-card-text>
          </v-card>
        </div>

      </v-tab-item>
    </v-tabs>
  </v-container>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import moment from "moment";
export default {
  data: () => ({
    dateformat: "YYYY-MM-DD",
    today: moment().format("YYYY-MM-DD"),
    from_date: moment().subtract(4, "weeks").format("YYYY-MM-DD"),
    to_date: moment().subtract().format("YYYY-MM-DD"),
    weeks_not_submitted: null,
    headers_ingediend: [
      {
        text: "Week",
        value: "week_number",
        sortable: false,
      },
      {
        text: "Van",
        value: "start_of_week",
        sortable: false,
      },
      {
        text: "Tot",
        value: "end_of_week",
        sortable: false,
      },
      {
        text: "Niet ingediend",
        value: "not_submitted",
        sortable: false,
      },
    ],
    headers: [
      {
        text: "Naam",
        value: "full_name",
        sortable: false,
      },
    ],
  }),
  methods: {
    ...mapActions({
      getAllUsers: "users/getUsers",
      addWorkingHoursToAllUsersState:
        "working_hours/addWorkingHoursToAllUsersState",
      resetAll: "working_hours/resetStateAllUsersAllWorkingHours",
    }),
    async notSubmittedWeeks() {
      // Login API call
      try {
        let response = await await this.$axios.get(
          "/working_hours/admin/weeks_not_submitted",
          { params: { from_date: this.from_date, to_date: this.to_date } }
        );
        this.weeks_not_submitted = response.data.reverse();
      } catch (err) {
        if (err.response) {
          this.$notifier.showMessage({
            content: err.response.data.detail,
            color: "error",
          });
        }
      }
    },
  },
  computed: {
    workingHoursPerWeekInSelectedYear() {
      var usersNotSubmittedForWeeksInYear = [];
      var date = moment(String(this.computedSelectedYear)).startOf("year");
      if (this.computedSelectedYear == moment().year()) {
        var endDate = moment().endOf("isoweek");
      } else {
        var endDate = moment(String(this.computedSelectedYear)).endOf("year");
      }

      while (date <= endDate) {
        var beginningOfWeek = moment(date)
          .startOf("isoweek")
          .format(this.dateformat);
        var endOfWeek = moment(date).endOf("isoweek").format(this.dateformat);
        var weekNumber = moment(date).isoWeek();

        var users_not_submitted = [];

        for (const user of this.get_all_working_hours_all_users) {
          var working_hours = user.working_hours;
          var hoursWeek = working_hours.filter(
            (item) =>
              moment(item.date) >= moment(beginningOfWeek) &&
              moment(item.date) <= moment(endOfWeek)
          );
          if (hoursWeek.length === 0) {
            var weekIsSubmitted = false;
            users_not_submitted.push(
              user.user.first_name + " " + user.user.last_name
            );
          } else {
            var weekIsSubmitted = hoursWeek.every(function (e) {
              console.log(e.submitted);
              return e.submitted === true;
            });
          }
        }
        usersNotSubmittedForWeeksInYear.push({
          week_number: weekNumber,
          start_of_week: beginningOfWeek,
          end_of_week: endOfWeek,
          not_submitted: users_not_submitted,
        });
        date = date.add(7, "days");
      }
      return usersNotSubmittedForWeeksInYear.reverse();
    },
    // Getters from the store
    // mix the getters into computed with object spread operator
    ...mapGetters({
      users: "users/Users",
      // users met rol werknemer
      werknemers: "users/Werknemers",
      working_hours: "working_hours/get_all_working_hours",
      get_all_working_hours_all_users:
        "working_hours/get_all_working_hours_all_users",
    }),
    computedSelectedYear() {
      return this.today ? moment(this.today).isoWeekYear() : "";
    },
  },
  created() {
    this.notSubmittedWeeks()
  },
};
</script>

<style>
</style>