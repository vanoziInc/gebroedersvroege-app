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
              <tr
                v-for="item in werknemers"
                :key="item.name"
              >
                <td>
                  <span><a v-bind:href="'/admin/working_hours/user/' + item.id">
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
        <v-container>
          <v-row>
            <v-col
              cols="4"
              class="justify-left"
            >
              <v-dialog
                ref="dialog"
                v-model="modal"
                :return-value.sync="date"
                persistent
                width="290px"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                    label="Selecteer data"
                    prepend-icon="mdi-calendar"
                    readonly
                    v-bind="attrs"
                    v-on="on"
                    v-model="dateRangeText"
                  ></v-text-field>
                </template>
                <v-date-picker
                  locale="nl-nl"
                  v-model="dates"
                  range
                >
                  <v-spacer></v-spacer>
                  <v-btn
                    text
                    color="primary"
                    @click="modal = false"
                  >
                    Annuleer
                  </v-btn>
                  <v-btn
                    text
                    color="primary"
                    @click="modal=false; notSubmittedWeeks()"
                  >
                    OK
                  </v-btn>
                </v-date-picker>
              </v-dialog>

            </v-col>
          </v-row>

          <v-expansion-panels focusable>
            <v-expansion-panel
              v-for="(item,i) in weeks_not_submitted"
              :key="i"
            >
              <v-expansion-panel-header class="subtitle-1">Week {{item.week}}:&nbsp;<span class="subtitle-2 font-weight-light font-italic"> ({{item.week_start}} - {{item.week_end}})</span></v-expansion-panel-header>
              <v-expansion-panel-content>
                <ul class="mt-2">
                  <li
                    v-for="(item, i) in item.not_submitted"
                    :key="i"
                  >{{item.email}}</li>
                </ul>
                </v-data-table>
              </v-expansion-panel-content>
            </v-expansion-panel>
          </v-expansion-panels>
        </v-container>
        <!-- Overzicht alle werknemers -->
        <!-- <div
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
        </div> -->

      </v-tab-item>
    </v-tabs>
  </v-container>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import moment from "moment";
export default {
  data: () => ({
    modal: false,
    dateformat: "YYYY-MM-DD",
    today: moment().format("YYYY-MM-DD"),
    from_date: moment().subtract(4, "weeks").format("YYYY-MM-DD"),
    to_date: moment().subtract().format("YYYY-MM-DD"),
    dates: [
      moment().subtract(4, "weeks").format("YYYY-MM-DD"),
      moment().subtract().format("YYYY-MM-DD"),
    ],
    weeks_not_submitted: null,
    headers_ingediend: [
      {
        text: "Email",
        value: "email",
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
          { params: { from_date: this.dates[0], to_date: this.dates[1] } }
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
    
    dateRangeText() {
      const sortedDates = this.dates.sort((a,b) => moment(a).diff(b));
      console.log(sortedDates)
      return sortedDates.join(" ~ ");
    },
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
    this.notSubmittedWeeks();
  },
};
</script>

<style>
</style>