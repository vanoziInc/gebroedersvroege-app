<template>
  <v-container>
    <v-card>
      <v-card-text>
        <!-- maand aanpassen -->
        <v-btn icon @click="substractMonth">
          <v-icon>mdi-chevron-double-left</v-icon>
        </v-btn>
        <b>{{ computedSelectedMonth }} - {{ computedSelectedYear }}</b>
        <v-btn icon @click="addMonth">
          <v-icon>mdi-chevron-double-right</v-icon>
        </v-btn>
        <v-data-table
          :headers="headers"
          :items="workingHoursInSelectedMonth"
          :items-per-page="31"
          :sort-by="['date']"
          :sort-desc="[true]"
          hide-default-footer
        ></v-data-table>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import moment from "moment";
export default {
  data: () => ({
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
    substractMonth() {
      this.today = moment(this.today)
        .subtract(1, "months")
        .format("YYYY-MM-DD");
    },
    addMonth() {
      this.today = moment(this.today).add(1, "months").format("YYYY-MM-DD");
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
      return this.today ? moment(this.date).isoWeekYear() : "";
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
  },
  created() {
    this.getAllWorkingHoursForUser(this.$auth.user.id);
  },
};
</script>

<style>
</style>