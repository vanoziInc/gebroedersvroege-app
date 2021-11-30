// https://codepen.io/Jayesh_v/pen/wvgjMva

<template>
  <v-container>
    <ConfirmDlg ref="confirm" />
    <EditHoursDlg ref="edit" @save="save($event)" />

    <v-data-table
      :headers="headers"
      :items="workingHoursOfCurrentWeek"
      fixed-header
      hide-default-footer
      @click:row="openEditDialog"
      dense
      :item-class="itemRowBackground"
    >
      <!-- Datum pickers -->
      <template v-slot:top>
        <v-card class="d-flex justify-center" flat tile>
          <v-card class="pa-2" flat tile>
            <v-btn-toggle tile v-model="toggle_year">
              <v-icon @click="substractYear">mdi-chevron-triple-left</v-icon>

              <b class="mx-2">{{ computedSelectedYear }}</b>
              <v-icon @click="addYear" v-if="nextYearAllowed"
                >mdi-chevron-triple-right</v-icon
              >
            </v-btn-toggle>
          </v-card>
          <v-card class="pa-2" flat tile>
            <v-btn-toggle tile v-model="toggle_month">
              <v-icon @click="substractMonth">mdi-chevron-double-left</v-icon>

              <b class="mx-2">{{ computedSelectedMonth }}</b>

              <v-icon @click="addMonth" v-if="nextMonthAllowed"
                >mdi-chevron-double-right</v-icon
              >
            </v-btn-toggle>
          </v-card>
          <v-card class="pa-2" flat tile>
            <v-btn-toggle tile v-model="toggle_week">
              <v-icon @click="substractWeek">mdi-chevron-left</v-icon>
              <b class="mx-2">{{ computedSelectedWeek }}</b>

              <v-icon v-if="nextWeekAllowed" @click="addWeek"
                >mdi-chevron-right</v-icon
              >
            </v-btn-toggle>
          </v-card>
        </v-card>

        <v-toolbar flat>
          <!-- Indien functionality -->
          <div class="h6">Totaal uren: {{ totalHoursCurrentWeek }}</div>
          <v-spacer></v-spacer>
          <v-btn v-if="weekSubmitted" outlined color="grey" small>
            <v-icon class="mr-2" color="gre">mdi-content-save-outline</v-icon>
            Indienen
          </v-btn>
          <v-btn v-else outlined @click="submitWeek()" color="green" small>
            <v-icon class="mr-2" color="green">mdi-content-save-outline</v-icon>
            Indienen
          </v-btn>
        </v-toolbar>
      </template>
      <!-- This template looks for headers with formatters and executes them -->
      <template
        v-for="header in headers.filter((header) =>
          header.hasOwnProperty('formatter')
        )"
        v-slot:[`item.${header.value}`]="{ header, value }"
      >
        {{ header.formatter(value) }}
      </template>
    </v-data-table>
  </v-container>
</template>

<script>
import ConfirmDlg from "~/components/ConfirmDlg.vue";
import EditHoursDlg from "~/components/EditHoursDlg.vue";
import { mapGetters, mapActions } from "vuex";
import moment from "moment";
export default {
  data: () => ({
    toggle_year: null,
    toggle_month: null,
    toggle_week: null,
    today: moment().format("YYYY-MM-DD"),
    date: moment().locale("nl").format("YYYY-MM-DD"),
    menu2: false,
    search: "",
    title: "Uren invoeren",
    valid: false,
    rules: {
      required: (value) => !!value || "Verplicht.",
      integer: (value) => isNaN(value) == false || "Moet cijfer zijn",
    },
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
    editedIndex: -1,
    defaultItem: {
      id: -1,
      date: null,
      hours: null,
      description: null,
    },
    editedItem: {
      id: -1,
    },
  }),
  head() {
    return {
      title: this.title,
    };
  },
  methods: {
    ...mapActions({
      getAllWorkingHoursForUser: "working_hours/getAllWorkingHours",
      addOrUpdateWorkingHoursForUser: "working_hours/addOrUpdateWorkingHours",
      deleteWorkingHoursForUser: "working_hours/deleteWorkingHours",
    }),
    close() {
      setTimeout(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      }, 300);
    },
    save(editedItem) {
      if (this.editedIndex > -1) {
        editedItem.user_id = this.$auth.user.id;
        this.addOrUpdateWorkingHoursForUser(editedItem);
        // Object.assign(this.desserts[this.editedIndex], this.editedItem);
      }
      this.close();
    },
    substractWeek() {
      this.date = moment(this.date).subtract(7, "days").format("YYYY-MM-DD");
    },
    addWeek() {
      this.date = moment(this.date).add(7, "days").format("YYYY-MM-DD");
    },
    substractMonth() {
      this.date = moment(this.date).subtract(1, "months").format("YYYY-MM-DD");
    },
    addMonth() {
      this.date = moment(this.date).add(1, "months").format("YYYY-MM-DD");
    },
    substractYear() {
      this.date = moment(this.date).subtract(1, "years").format("YYYY-MM-DD");
    },
    addYear() {
      this.date = moment(this.date).add(1, "years").format("YYYY-MM-DD");
    },
    // Method to submid all items in the week
    async submitWeek() {
      if (
        await this.$refs.confirm.open(
          "Bevestig",
          "Weet je zeker dat je de uren voor deze week wilt indienen?"
        )
      )
        for (let i = 0; i < this.workingHoursOfCurrentWeek.length; i++) {
          let item = this.workingHoursOfCurrentWeek[i];
          if (item.hours !== "") {
            item.user_id = this.$auth.user.id;
            item.submitted = true;
            this.addOrUpdateWorkingHoursForUser(item);
          }
        }
    },
    async openEditDialog(item) {
      for (let i = 0; i < this.workingHoursOfCurrentWeek.length; i++) {
        if (this.workingHoursOfCurrentWeek[i].submitted == true) {
          return false;
        }
        if (moment(item.date) > moment()) {
          return false;
        }
      }
      this.editedIndex = this.workingHoursOfCurrentWeek.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.editedItem.submitted = false;
      if (await this.$refs.edit.open("Uren aanpassen", this.editedItem)) {
      }
    },
    itemRowBackground(item) {
      if(item.submitted == true) {
        return "blue-grey lighten-5";
      }
      else if (moment(item.date) < moment()) {
        return "white";
      } else {
        return "blue-grey lighten-5";
      }
    },
  },

  computed: {
    // Getters from the store
    // mix the getters into computed with object spread operator
    ...mapGetters({
      working_hours: "working_hours/get_all_working_hours",
    }),

    computedDateFormattedMomentjs() {
      return this.date
        ? moment(this.date).locale("nl").format("dd, D MMMM YYYY")
        : "";
    },
    computedSelectedWeek() {
      return this.date ? moment(this.date).isoWeek() : "";
    },
    computedSelectedYear() {
      return this.date ? moment(this.date).isoWeekYear() : "";
    },
    computedSelectedMonth() {
      return this.date ? moment(this.date).locale("nl").format("MMM") : "";
    },
    computedFirstDayCurrentWeek() {
      return moment(this.date).startOf("isoweek");
    },
    computedLastDayCurrentWeek() {
      return moment(this.computedFirstDayCurrentWeek)
        .add(7, "days")
        .startOf("isoweek");
    },
    workingHoursOfCurrentWeek() {
      var now = this.computedFirstDayCurrentWeek.clone(),
        dates = [];

      while (now.isBefore(this.computedLastDayCurrentWeek)) {
        var working_hours_day = this.working_hours.find(
          (x) => x.date === now.locale("nl").format("YYYY-MM-DD")
        );

        dates.push({
          id:
            working_hours_day !== undefined
              ? working_hours_day.id
              : Math.floor(Math.random() * 99999999) + 1,
          date: now.locale("nl").format("YYYY-MM-DD"),
          hours: working_hours_day !== undefined ? working_hours_day.hours : 0,
          description:
            working_hours_day !== undefined
              ? working_hours_day.description
              : "",
          submitted:
            working_hours_day !== undefined
              ? working_hours_day.submitted
              : null,
        });
        now.add(1, "days");
      }
      return dates;
    },
    // all days submitted or not
    weekSubmitted() {
      var submittedItems = [];
      var unSubmittedItems = [];
      var undefinedItems = [];
      // there is an item not submitted yet
      for (let i = 0; i < this.workingHoursOfCurrentWeek.length; i++) {
        let item = this.workingHoursOfCurrentWeek[i];
        if (item.submitted == false) {
          unSubmittedItems.push(item);
        } else if (item.submitted == null) {
          undefinedItems.push(item);
        } else if (item.submitted == true) {
          submittedItems.push(item);
        }
      }
      if (unSubmittedItems.length > 0) {
        return false;
      } else if (undefinedItems.length == 7) {
        return false;
      } else {
        return true;
      }
    },
    nextWeekAllowed() {
      if (this.computedSelectedWeek + 1 < moment().isoWeek() + 1) {
        return true;
      } else {
        return false;
      }
    },

    nextMonthAllowed() {
      if (moment(this.date).month() + 1 < moment().month() + 1) {
        return true;
      } else {
        return false;
      }
    },
    nextYearAllowed() {
      if (moment(this.date).year() + 1 < moment().year() + 1) {
        return true;
      } else {
        return false;
      }
    },
    totalHoursCurrentWeek() {
      var total = 0;
      for (let i = 0; i < this.workingHoursOfCurrentWeek.length; i++) {
        var item = this.workingHoursOfCurrentWeek[i];
        total = total + item.hours;
      }
      return total;
    },
  },
  created() {
    this.getAllWorkingHoursForUser(this.$auth.user.id);
  },
};
</script>

<style scoped>
.white {
  background-color: white;
}
.grey {
  background-color: yellow;
}
</style>