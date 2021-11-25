<template>
  <v-container>
    <!-- tabs -->
    <!-- overzicht uren -->
    <!-- administratie indienen en vrijgeven -->
    <v-tabs centered>
      <v-tab href="#overview">Maand overzicht</v-tab>
      <v-tab-item value="overview">
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
        </v-container>
      </v-tab-item>
      <v-tab href="#openstaand">Openstaand</v-tab>
      <v-tab-item value="openstaand">
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
          <v-simple-table width="500px" dense>
            <template v-slot:default>
              <thead>
                <tr>
                  <th width="100px" class="text-left">Week</th>
                  <th width="200px" class="text-left">Van/Tot</th>
                  <th width="100px" class="text-left">Totaal uren</th>
                  <th width="100px" class="text-left">Ingediend</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="item in workingHoursPerWeekInSelectedYear"
                  :key="item.week_number"
                >
                  <td>{{ item.week_number }}</td>
                  <td>{{ item.start_of_week }} / {{ item.end_of_week }}</td>
                  <td>{{ item.total_hours }}</td>
                  <td v-if="item.submitted"><v-icon color="green">
                    mdi-hand-okay</v-icon></td>
                                      <td v-else><v-icon color="red">
                    mdi-skull-crossbones-outline</v-icon></td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
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
    dateformat: "YYYY-MM-DD",
    today: moment().format("YYYY-MM-DD"),
    headers: [
      {
        text: "Datum",
        value: "date",
        sortable: false,
        formatter: (x) =>
          x ? moment(x).locale("nl").format("dddd DD MMMM") : null,
      },
      {
        text: "Uren",
        value: "hours",
        sortable: false,
      },
      {
        text: "Omschrijving",
        value: "description",
        sortable: false,
      },
    ],
  }),
  methods: {
    ...mapActions({
      getAllWorkingHoursForUser: "working_hours/getAllWorkingHours",
    }),
    substractYear() {
      this.today = moment(this.today).subtract(1, "years").format("YYYY-MM-DD");
    },
    addYear() {
      this.today = moment(this.today).add(1, "years").format("YYYY-MM-DD");
    },

    getArraySum(a) {
      var total = 0;
      for (var i in a) {
        total += a[i].hours;
      }
      return total;
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
    workingHoursPerWeekInSelectedYear() {
      var hourSumsForYear = [];
      var date = moment(String(this.computedSelectedYear)).startOf("year");
      while (date <= moment(String(this.computedSelectedYear)).endOf("year")) {
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
        if (hoursWeek.length === 0) {
          var weekIsSubmitted = false;
        } else {
          var weekIsSubmitted = hoursWeek.every(function (e) {
            console.log(e.submitted);
            return e.submitted === true;
          });
        }

        console.log(hoursWeek);
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
    console.log(this.$route.params.slug);
    this.getAllWorkingHoursForUser(this.$route.params.slug);
  },
};
</script>

<style>
</style>