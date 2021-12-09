<template>
  <v-container>
    <!-- tabs -->
    <!-- overzicht uren -->
    <!-- administratie indienen en vrijgeven -->
    <v-tabs centered>
      <v-tab href="#week_overview">Week overzicht</v-tab>
      <v-tab-item value="week_overview">
        <v-row class="mt-3">
          <v-col v-if="werknemer != null">
            {{ werknemer.first_name }} {{ werknemer.last_name }} 
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <!-- jaar aanpassen -->
            <v-btn icon @click="substractYear" v-if="werknemer !=null && previousYearAllowed">
              <v-icon>mdi-chevron-triple-left</v-icon>
            </v-btn>
            <b>{{ computedSelectedYear }}</b>
            <v-btn icon @click="addYear" v-if="nextYearAllowed">
              <v-icon>mdi-chevron-triple-right</v-icon>
            </v-btn>
          </v-col>
        </v-row>
        <v-simple-table dense class="mt-3">
          <template v-slot:default>
            <thead>
              <tr>
                <th class="text-left">Week</th>
                <th class="text-left">Van</th>
                <th class="text-left">Tot</th>
                <th class="text-left">Uren</th>
                <th class="text-left">Ingediend?</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, i) in week_overview" :key="i">
                <td>{{ item.week }}</td>
                <td>{{ formatDateforTemplate(item.week_start) }}</td>
                <td>{{ formatDateforTemplate(item.week_end) }}</td>
                <td>{{ item.sum_hours }}</td>
                <td>
                  <v-icon color="green" v-if="item.submitted">
                    mdi-hand-okay</v-icon
                  >
                  <v-icon color="red" v-else> mdi-close-octagon-outline</v-icon>
                </td>
              </tr>
            </tbody>
          </template>
        </v-simple-table>
      </v-tab-item>

      <v-tab href="#month_overview">Maand overzicht</v-tab>
      <v-tab-item value="month_overview">
        <v-container>
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
          <v-simple-table dense>
            <template v-slot:default>
              <thead>
                <tr>
                  <th class="text-left">Maand</th>
                  <th class="text-left">Totaal uren</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="item in workingHoursPerMonthInSelectedYear"
                  :key="item.month"
                >
                  <td>{{ item.month }}</td>
                  <td>{{ item.sum }}</td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
          <br />
          <v-row>
            <v-col class="justify-left"
              >Totaal uren: &nbsp {{ yearTotal }}</v-col
            >
          </v-row>
        </v-container>
      </v-tab-item>
    </v-tabs>
  </v-container>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import moment from "moment";
export default {
  data: () => ({
    werknemer: null,
    dateformat: "YYYY-MM-DD",
    today: moment().format("YYYY-MM-DD"),
    week_overview: null,
    headers: [
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
        text: "Totaal uren",
        value: "total_hours",
        sortable: false,
      },
      {
        text: "Ingediend?",
        value: "submitted",
        sortable: false,
      },
    ],
  }),
  methods: {
    formatDateforTemplate(value) {
      return moment(value).locale("nl").format("DD MMM");
    },
    ...mapActions({
      getAllWorkingHoursForUser: "working_hours/getAllWorkingHours",
    }),
    substractYear() {
      this.today = moment(this.today).subtract(1, "years").format("YYYY-MM-DD");
      this.weekOverview();
    },
    addYear() {
      this.today = moment(this.today).add(1, "years").format("YYYY-MM-DD");
      this.weekOverview();
    },

    getArraySum(a) {
      var total = 0;
      for (var i in a) {
        total += a[i].hours;
      }
      return total;
    },
    async weekOverview() {
      // Login API call
      try {
        let response = await this.$axios.get("/working_hours/week_overview/", {
          params: {
            from_date: moment(this.today).startOf("year").format("YYYY-MM-DD"),
            to_date: moment(this.today).endOf("year").format("YYYY-MM-DD"),
            user_id: this.$route.params.slug,
          },
        });
        this.week_overview = response.data.week_data.reverse();
        this.werknemer = response.data.werknemer;
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
    // Getters from the store
    // mix the getters into computed with object spread operator
    ...mapGetters({
      working_hours: "working_hours/get_all_working_hours",
    }),
    firstOfMonth() {
      return moment(this.today).startOf("month").format("YYYY-MM-DD");
    },
    lastOfMonth() {
      return moment(this.today).endOf("month").format("YYYY-MM-DD");
    },
    computedSelectedYear() {
      return this.today ? moment(this.today).isoWeekYear() : "";
    },
    computedSelectedMonth() {
      return this.today ? moment(this.today).locale("nl").format("MMM") : "";
    },
    daysInSelectedMonth() {
      var count = moment(this.today).month(this.today).daysInMonth();
      var days = [];
      for (var i = 1; i < count + 1; i++) {
        days.push(
          moment(this.today).month(this.today).date(i).format("YYYY-MM-DD")
        );
      }
      return days;
    },
    workingHoursInSelectedMonth() {
      const filteredHours = this.working_hours.filter((item) =>
        this.daysInSelectedMonth.includes(item.date)
      );
      return filteredHours;
    },
    yearTotal() {
      var total = 0;

      for (
        var i = 0, n = this.workingHoursPerMonthInSelectedYear.length;
        i < n;
        ++i
      ) {
        total += this.workingHoursPerMonthInSelectedYear[i].sum;
      }
      return total;
    },
    workingHoursPerMonthInSelectedYear() {
      var hourSumsForYear = [];
      for (let i = 0; i < 12; i++) {
        var beginningOfMonth = moment(
          String(this.computedSelectedYear) + "-" + String(i + 1) + "-01"
        ).startOf("month");
        var endOfMonth = moment(
          String(this.computedSelectedYear) + "-" + String(i + 1) + "-01"
        ).endOf("month");
        var hoursMonth = this.working_hours.filter(
          (item) =>
            moment(item.date) >= beginningOfMonth &&
            moment(item.date) <= endOfMonth
        );
        var total = this.getArraySum(hoursMonth);
        hourSumsForYear.push({
          month: moment().month(i).locale("nl").format("MMMM"),
          sum: total,
        });
      }
      return hourSumsForYear;
    },
    nextYearAllowed() {
      if (moment(this.today).year() + 1 < moment().year() + 1) {
        return true;
      } else {
        return false;
      }
    },
    previousYearAllowed() {
      if (moment(this.werknemer.created_at).year() < moment(this.today).year()
      ) {
        return true;
      } else {
        return false;
      }
    },
    workingHoursPerWeekInSelectedYear() {
      var hourSumsForYear = [];
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
        var hoursWeek = this.working_hours.filter(
          (item) =>
            moment(item.date) >= moment(beginningOfWeek) &&
            moment(item.date) <= moment(endOfWeek)
        );
        // checker fucntion
        let checker = (arr) => arr.every(Boolean);
        let result = hoursWeek.map((a) => a.submitted);
        console.log(result);
        if (moment(this.$auth.user.created_at) > moment(endOfWeek)) {
          console.log(endOfWeek);
          console.log(this.$auth.user.created_at);
          var weekIsSubmitted = null;
        } else if (hoursWeek.length === 0) {
          var weekIsSubmitted = false;
        } else if (checker(result) === true) {
          var weekIsSubmitted = true;
        }

        console.log(endOfWeek);
        console.log(hoursWeek.length);
        // var weekIsSubmitted = hoursWeek.every(function (e) {
        //   return e.submitted === true;
        // });
        // if (weekIsSubmitted == true) {
        //   console.log(hoursWeek);
        //   var weekIsSubmitted = false;
        // }
        // } else if (moment(this.$auth.user.created_at) > endOfWeek) {
        //   var weekIsSubmitted = null;
        //   // var weekIsSubmitted = hoursWeek.every(function (e) {
        //   //   console.log(e.submitted);
        //   //   return e.submitted === true;
        //   // });
        // }
        var total = this.getArraySum(hoursWeek);
        hourSumsForYear.push({
          week_number: weekNumber,
          start_of_week: beginningOfWeek,
          total_hours: total,
          end_of_week: endOfWeek,
          submitted: weekIsSubmitted,
        });
        date = date.add(7, "days");
      }
      return hourSumsForYear;
    },
  },
  created() {
    this.weekOverview();
    console.log(this.$route.params.slug);
    this.getAllWorkingHoursForUser(this.$route.params.slug);

  },
};
</script>

<style>
</style>