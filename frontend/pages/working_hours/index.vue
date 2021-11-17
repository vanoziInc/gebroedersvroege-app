// https://codepen.io/Jayesh_v/pen/wvgjMva

<template>
  <v-container>
    <ConfirmDlg ref="confirm" />
    <v-card>
      <v-card-title class="ml-4">
        <span>
          <h4 class="font-weight-light">Uren overzicht</h4>
        </span>
      </v-card-title>
      <v-card-subtitle class="ml-4">
        Week {{ computedSelectedWeek }}
        {{ computedSelectedYear }}
      </v-card-subtitle>
      <v-card-text class="mt-2">
        <v-data-table
          :headers="headers"
          :items="workingHoursOfCurrentWeek"
          fixed-header
          hide-default-footer
        >
          <template v-slot:top>
            <v-toolbar flat>
              <!-- TODO Week nummer maannummer-->
              <v-menu
                v-model="menu2"
                :close-on-content-click="false"
                :nudge-right="40"
                transition="scale-transition"
                offset-y
                min-width="auto"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                    v-model="computedDateFormattedMomentjs"
                    label="Ga naar week op basis van datum"
                    prepend-icon="mdi-calendar"
                    readonly
                    v-bind="attrs"
                    v-on="on"
                  ></v-text-field>
                </template>
                <v-date-picker
                  v-model="date"
                  @input="menu2 = false"
                  locale="nl"
                ></v-date-picker>
              </v-menu>
            </v-toolbar>
            <v-toolbar flat>
              <!-- maand aanpassen -->
              <v-btn
                icon
                @click="substractMonth"
              >
                <v-icon>mdi-chevron-double-left</v-icon>
              </v-btn>
              <b>{{ computedSelectedMonth }}</b>
              <v-btn
                icon
                @click="addMonth"
              >
                <v-icon>mdi-chevron-double-right</v-icon>
              </v-btn>
              <!-- week aanpassen -->
              <v-btn
                icon
                @click="substractWeek"
              >
                <v-icon>mdi-chevron-left</v-icon>
              </v-btn>
              <b>{{ computedSelectedWeek }}</b>
              <v-btn
                icon
                @click="addWeek"
              >
                <v-icon>mdi-chevron-right</v-icon>
              </v-btn>
              <v-btn icon>
                <v-icon>mdi-content-save-check-outline</v-icon>
              </v-btn>
              <span class="body-1">Indienen</span>
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
          <!-- Column Hours template -->
          <template v-slot:[`item.hours`]="{ item }">
            <v-form
              id="hours_form"
              ref="form"
              v-model="valid"
            >
              <v-text-field
                :rules="[rules.required, rules.integer]"
                v-model="editedItem.hours"
                :hide-details="true"
                dense
                single-line
                v-if="item.id === editedItem.id"
              ></v-text-field>

              <span v-else>{{ item.hours }}</span>
            </v-form>
          </template>
          <!-- Column description template -->
          <template v-slot:[`item.description`]="{ item }">
            <v-text-field
              v-model="editedItem.description"
              :hide-details="true"
              dense
              single-line
              v-if="item.id === editedItem.id"
            ></v-text-field>
            <span v-else>{{ item.description }}</span>
          </template>
          <!-- Actions Column -->
          <template v-slot:[`item.actions`]="{ item }">
            <div v-if="item.id === editedItem.id">
              <v-icon
                color="red"
                class="mr-3"
                @click="close"
              >
                mdi-window-close
              </v-icon>
              <v-icon
                color="green"
                @click="save"
                :disabled="!valid"
              > mdi-content-save </v-icon>
            </div>
            <div v-else>
              <v-icon
                v-if="computedEditDate(item.date)"
                color="green"
                class="mr-3"
                @click="editItem(item)"
              >
                mdi-pencil
              </v-icon>
              <v-icon
                v-if="item.hours !== ''"
                color="red"
                @click="delRecord(item)"
              >
                mdi-delete
              </v-icon>
            </div>
          </template>

          <template v-slot:no-data>
            <v-btn
              color="primary"
              @click="initialize"
            >Reset</v-btn>
          </template>
        </v-data-table>
      </v-card-text>
      <v-card-actions> </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>
import ConfirmDlg from "~/components/ConfirmDlg.vue";
import { mapGetters, mapActions } from "vuex";
import moment from "moment";
export default {
  data: () => ({
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
          x ? moment(x).locale("nl").format("ddd DD/MM") : null,
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
      {
        text: "Acties",
        value: "actions",
        sortable: false,
      },
    ],
    desserts: [],
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
    computedEditDate(date) {
      if (moment(date) < moment()) {
        return true;
      } else {
        return false;
      }
    },
    editItem(item) {
      this.editedIndex = this.workingHoursOfCurrentWeek.indexOf(item);
      this.editedItem = Object.assign({}, item);
    },
    deleteItem(item) {
      const index = this.workingHoursOfCurrentWeek.indexOf(item);
      confirm("Are you sure you want to delete this item?") &&
        this.deleteWorkingHoursForUser(item.id);
    },
    close() {
      setTimeout(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      }, 300);
    },
    addNew() {
      const addObj = Object.assign({}, this.defaultItem);
      addObj.id = this.desserts.length + 1;
      this.desserts.unshift(addObj);
    },
    save() {
      if (this.editedIndex > -1) {
        this.editedItem.user_id = this.$auth.user.id;
        console.log(this.editedItem);
        this.addOrUpdateWorkingHoursForUser(this.editedItem);
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
    // Confirmation dialog methods
    async delRecord(item) {
      if (
        await this.$refs.confirm.open(
          "Bevestig",
          "Weet je zeker dat je de uren wilt verwijderen?"
        )
      ) {
        this.deleteWorkingHoursForUser(item.id);
      }
    },
    deleteRecord() {
      console.log("Record deleted.");
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
              : Math.floor(Math.random() * 99999999) + 10000000,
          date: now.locale("nl").format("YYYY-MM-DD"),
          hours: working_hours_day !== undefined ? working_hours_day.hours : "",
          description:
            working_hours_day !== undefined
              ? working_hours_day.description
              : "",
        });
        now.add(1, "days");
      }
      return dates;
    },
  },
  created() {
    this.getAllWorkingHoursForUser(this.$auth.user.id);
  },
};
</script>