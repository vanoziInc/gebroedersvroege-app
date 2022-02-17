<template>
  <v-container>
    {{ this.sumForWeeks}}
  </v-container>
</template>

<script>
import moment from "moment";
export default {
  data: () => ({
    working_hours: [],
    currentYear: "2022",
  }),
  methods: {
    async getWorkingHours() {
      try {
        let response = await this.$axios.get("/working_hours/between_dates/", {
          params: {
            // from_date: moment(this.today).startOf("year").format("YYYY-MM-DD"),
            from_date: moment(this.currentYear).startOf('year').startOf('week').format('YYYY-MM-DD'),
            // to_date:
            //   moment(this.today).year() < moment().year()
            //     ? moment(this.today).endOf("year").format("YYYY-MM-DD")
            //     : moment(this.today).endOf("isoweek").format("YYYY-MM-DD"),
            to_date: "2022-12-31",
          },
        });
        let working_hours = response.data;
        this.working_hours = working_hours;
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
    sumForWeeks() {
      if (this.working_hours != []) {
        let weekRange = []
        let totalWeeks = [];
        let weekOverview = {};
        let working_hours = this.working_hours;
        // Create the week range
        var a = moment(this.currentYear).startOf('year').format('YYYY-MM-DD');
        var b = moment().format('YYYY-MM-DD');

        // If you want an exclusive end date (half-open interval)
        for (var m = moment(a); m.isSameOrBefore(moment(b)); m.add(1, 'days')) {
        weekRange.push(m.isoWeek())
        }
        for (const item of working_hours) {
          item.week = moment(item.date).isoWeek();
        }
        console.log(weekRange)
      } else {
        return this.working_hours;
      }
    },
  },
  created() {
    this.getWorkingHours();
  },
};
</script>

<style>
</style>